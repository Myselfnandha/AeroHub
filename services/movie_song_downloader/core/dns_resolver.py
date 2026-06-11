import socket
import logging
import ssl
import json
import urllib.request
import httpx
from typing import Dict, Optional

logger = logging.getLogger("MovieSongDownloader.DnsResolver")

_original_getaddrinfo = socket.getaddrinfo
_dns_overrides: Dict[str, str] = {}
_active_doh_url: str = "https://cloudflare-dns.com/dns-query"

DOH_PROVIDERS = {
    "cloudflare": "https://cloudflare-dns.com/dns-query",
    "google": "https://dns.google/dns-query",
    "quad9": "https://dns.quad9.net:5053/dns-query",
}

DOMAINS_TO_RESOLVE = [
    "www.jiosaavn.com",
    "www.omdbapi.com",
]


def _patched_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    """Intercepts DNS lookups for blocked domains, returns DoH-resolved IPs.
    TLS SNI still uses the original hostname so HTTPS works correctly."""
    if host is None:
        return _original_getaddrinfo(host, port, family, type, proto, flags)

    if isinstance(host, bytes):
        host_str = host.decode("utf-8", errors="ignore")
    elif isinstance(host, str):
        host_str = host
    else:
        host_str = str(host)

    clean_host = host_str.rstrip(".")

    # Fast bypass for numeric IPs, localhost, and local network domains
    is_numeric = False
    try:
        # Check if valid IPv4
        socket.inet_aton(clean_host)
        is_numeric = True
    except Exception:
        pass
    if not is_numeric:
        try:
            # Check if valid IPv6
            socket.inet_pton(socket.AF_INET6, clean_host)
            is_numeric = True
        except Exception:
            pass

    is_local = (
        not clean_host
        or clean_host.lower() in ("localhost", "none", "127.0.0.1", "::1", "0.0.0.0")
        or clean_host.endswith(".local")
        or is_numeric
        or "." not in clean_host
    )

    if is_local:
        return _original_getaddrinfo(clean_host, port, family, type, proto, flags)

    resolved = _dns_overrides.get(clean_host)
    if resolved:
        logger.debug(f"DNS override: {clean_host} -> {resolved}")
        try:
            return _original_getaddrinfo(resolved, port, family, type, proto, flags)
        except Exception as e:
            logger.warning(
                f"DNS override original getaddrinfo failed for {resolved}: {e}. Retrying with AI_NUMERICHOST."
            )
            try:
                f = socket.AF_INET if family in (0, socket.AF_INET) else family
                t = type or socket.SOCK_STREAM
                p = proto or socket.IPPROTO_TCP
                return _original_getaddrinfo(
                    resolved, port, f, t, p, socket.AI_NUMERICHOST
                )
            except Exception as e2:
                logger.error(
                    f"DNS override backup getaddrinfo failed for {resolved}: {e2}. Using manual fallback."
                )
                f = socket.AF_INET if family in (0, socket.AF_INET) else family
                t = type or socket.SOCK_STREAM
                p = proto or socket.IPPROTO_TCP
                return [(f, t, p, "", (resolved, port))]

    # For non-overridden hosts, strip trailing dots and attempt system resolution.
    # If the system resolver fails (e.g. Jio/ISP blocks or DNS poisoning), fall back
    # dynamically to DNS-over-HTTPS in real-time.
    try:
        return _original_getaddrinfo(clean_host, port, family, type, proto, flags)
    except Exception as e:
        # Avoid recursive calls if it's the DoH provider domain itself failing
        if (
            clean_host in _dns_overrides
            or "dns-query" in clean_host
            or "cloudflare-dns.com" in clean_host
            or "dns.google" in clean_host
        ):
            raise e

        logger.warning(
            f"System DNS lookup failed for {clean_host}: {e}. Attempting real-time DoH fallback..."
        )
        resolved = _resolve_via_doh_sync(clean_host, _active_doh_url)
        if resolved:
            _dns_overrides[clean_host] = resolved
            logger.info(
                f"Dynamically resolved {clean_host} -> {resolved} via DoH fallback."
            )
            try:
                return _original_getaddrinfo(resolved, port, family, type, proto, flags)
            except Exception as e2:
                logger.warning(
                    "Dynamic DNS override original getaddrinfo failed for %s: %s. "
                    "Retrying with AI_NUMERICHOST.",
                    resolved,
                    e2,
                )
                try:
                    f = socket.AF_INET if family in (0, socket.AF_INET) else family
                    t = type or socket.SOCK_STREAM
                    p = proto or socket.IPPROTO_TCP
                    return _original_getaddrinfo(
                        resolved, port, f, t, p, socket.AI_NUMERICHOST
                    )
                except Exception as e3:
                    logger.error(
                        f"Dynamic DNS override backup getaddrinfo failed for {resolved}: {e3}. Using manual fallback."
                    )
                    f = socket.AF_INET if family in (0, socket.AF_INET) else family
                    t = type or socket.SOCK_STREAM
                    p = proto or socket.IPPROTO_TCP
                    return [(f, t, p, "", (resolved, port))]

        # If DoH resolution fails too, raise the original getaddrinfo exception
        if clean_host != host:
            try:
                return _original_getaddrinfo(host, port, family, type, proto, flags)
            except Exception:
                raise e
        raise e


async def _resolve_via_doh(hostname: str, doh_url: str) -> Optional[str]:
    """Resolves a hostname to an IPv4 address using DNS-over-HTTPS (RFC 8484 JSON)."""
    params = {"name": hostname, "type": "A"}
    headers = {"Accept": "application/dns-json"}
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(doh_url, params=params, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                for answer in data.get("Answer", []):
                    if answer.get("type") == 1:
                        ip = answer["data"]
                        logger.info(f"DoH resolved {hostname} -> {ip}")
                        return ip
    except Exception as e:
        logger.warning(f"DoH resolution failed for {hostname}: {e}")
    return None


async def bootstrap_dns(provider: str = "cloudflare") -> None:
    """Pre-resolves blocked domains via DoH and patches socket.getaddrinfo.
    Call once at app startup before any API requests."""
    global _active_doh_url
    doh_url = DOH_PROVIDERS.get(provider, DOH_PROVIDERS["cloudflare"])
    _active_doh_url = doh_url
    logger.info(f"Bootstrapping DNS via DoH provider: {provider} ({doh_url})")

    for domain in DOMAINS_TO_RESOLVE:
        ip = await _resolve_via_doh(domain, doh_url)
        if ip:
            _dns_overrides[domain] = ip

    if _dns_overrides:
        socket.getaddrinfo = _patched_getaddrinfo
        logger.info(
            f"DNS overrides active for {len(_dns_overrides)} domain(s): {list(_dns_overrides.keys())}"
        )
    else:
        logger.warning(
            "No DNS overrides resolved. Some providers may be unreachable if ISP blocks DNS."
        )


def _resolve_via_doh_sync(hostname: str, doh_url: str) -> Optional[str]:
    """Resolves a hostname to an IPv4 address synchronously using DNS-over-HTTPS."""
    url = f"{doh_url}?name={hostname}&type=A"
    req = urllib.request.Request(url, headers={"Accept": "application/dns-json"})
    try:
        ctx = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=ctx, timeout=5.0) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                for answer in data.get("Answer", []):
                    if answer.get("type") == 1:
                        ip = answer["data"]
                        logger.info(f"DoH resolved {hostname} -> {ip} (sync)")
                        return ip
    except Exception as e:
        logger.warning(f"DoH resolution failed synchronously for {hostname}: {e}")
    return None


def bootstrap_dns_sync(provider: str = "cloudflare") -> None:
    """Pre-resolves blocked domains synchronously via DoH and patches socket.getaddrinfo.
    Call at early startup before any libraries perform DNS lookups."""
    global _active_doh_url
    doh_url = DOH_PROVIDERS.get(provider, DOH_PROVIDERS["cloudflare"])
    _active_doh_url = doh_url
    logger.info(
        f"Synchronously bootstrapping DNS via DoH provider: {provider} ({doh_url})"
    )

    for domain in DOMAINS_TO_RESOLVE:
        ip = _resolve_via_doh_sync(domain, doh_url)
        if ip:
            _dns_overrides[domain] = ip

    if _dns_overrides:
        socket.getaddrinfo = _patched_getaddrinfo
        logger.info(
            f"DNS overrides active for {len(_dns_overrides)} domain(s): {list(_dns_overrides.keys())}"
        )
    else:
        logger.warning(
            "No DNS overrides resolved. Some providers may be unreachable if ISP blocks DNS."
        )


def clear_dns_overrides() -> None:
    """Restores original DNS resolution."""
    _dns_overrides.clear()
    socket.getaddrinfo = _original_getaddrinfo
    logger.info("DNS overrides cleared, restored system resolver.")
