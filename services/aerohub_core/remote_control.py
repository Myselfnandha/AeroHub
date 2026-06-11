import json
import logging
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

logger = logging.getLogger("AeroHub.RemoteControl")


class LocalControlHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload, status=200):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _unauthorized(self):
        self._send_json({"error": "Unauthorized"}, status=401)

    def _parse_request(self):
        parsed = urlparse(self.path)
        return parsed.path, parse_qs(parsed.query)

    def _allowed(self):
        token = self.server.control_token
        if not token:
            return True
        header = self.headers.get("X-Local-Token") or self.headers.get("Authorization")
        if header and header.strip() == token:
            return True
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        if params.get("token", [""])[0] == token:
            return True
        return False

    def do_GET(self):
        if not self._allowed():
            return self._unauthorized()

        path, params = self._parse_request()
        core = self.server.core
        if path == "/health":
            return self._send_json(core.get_health())
        if path == "/status":
            return self._send_json(core.get_status())
        if path == "/metrics":
            return self._send_json(core.get_metrics())
        if path == "/control":
            action = params.get("action", [""])[0]
            service_id = params.get("service", [""])[0]
            if action and service_id:
                result = core.control_service(service_id, action)
                return self._send_json(result)
            return self._send_json({"error": "action and service are required"}, status=400)
        if path == "/self-update":
            result = core.perform_self_update()
            status_code = 200 if result.get("status") == "updated" else 500
            return self._send_json(result, status=status_code)
        return self._send_json({"error": "not found"}, status=404)

    def log_message(self, format, *args):
        logger.debug(format % args)


class LocalControlServer(ThreadingHTTPServer):
    def __init__(self, server_address, RequestHandlerClass, core, token=None):
        super().__init__(server_address, RequestHandlerClass)
        self.core = core
        self.control_token = token
