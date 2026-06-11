# MovieSongDownloader/main.py

import argparse
import importlib
import os
import signal
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path

from importlib.abc import MetaPathFinder

sub_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.dirname(os.path.dirname(sub_dir))
services_dir = os.path.join(workspace_root, "services")

# Remove subdirectory from path to avoid package naming collision
if sub_dir in sys.path:
    sys.path.remove(sub_dir)

# Add workspace root and services directory to path
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)
if services_dir not in sys.path:
    sys.path.insert(0, services_dir)

# Register Redirector so MovieSongDownloader -> movie_song_downloader works seamlessly
class MovieSongDownloaderRedirector(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname.startswith("MovieSongDownloader"):
            real_name = fullname.replace("MovieSongDownloader", "movie_song_downloader", 1)
            mod = importlib.import_module(real_name)
            sys.modules[fullname] = mod
            return mod.__spec__
        return None

sys.meta_path.insert(0, MovieSongDownloaderRedirector())

# Import shared config loader from root
from config.loader import load_config, load_env  # noqa: E402

# Import MovieSongDownloader package first to trigger early DNS override bootstrap inside __init__.py
import MovieSongDownloader  # noqa: F401, E402


class DevConfigWatcher:
    def __init__(self, root_dir: Path, callback):
        self.root_dir = root_dir
        self.callback = callback
        self.files = [self.root_dir.parent / ".env", self.root_dir / "rxconfig.py"]
        self.mod_times = {path: path.stat().st_mtime for path in self.files if path.exists()}
        self.running = True

    def watch(self):
        while self.running:
            for path in self.files:
                if path.exists():
                    mtime = path.stat().st_mtime
                    if self.mod_times.get(path) != mtime:
                        self.mod_times[path] = mtime
                        self.callback(path)
            time.sleep(2)

    def stop(self):
        self.running = False


def apply_env_from_config(root_dir: Path):
    runtime = load_config()
    env_settings = runtime.get("app", {})
    os.environ.setdefault("FLET_WEB_PORT", str(env_settings.get("flet_port", 8555)))
    os.environ.setdefault("ENV", env_settings.get("env", "dev"))
    env_file = root_dir.parent / ".env"
    for key, value in load_env(env_file).items():
        if key not in os.environ:
            os.environ[key] = value


def reload_rxconfig(root_dir: Path):
    try:
        import rxconfig

        importlib.reload(rxconfig)
        print("Reloaded rxconfig.py", flush=True)
    except Exception as exc:
        print(f"Failed to reload rxconfig: {exc}", file=sys.stderr, flush=True)


def is_port_free(port: int) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("0.0.0.0", port))
        return True
    except OSError:
        return False


def find_free_port(start_port: int = 8555, max_port: int = 8600) -> int:
    for port in range(start_port, max_port + 1):
        if is_port_free(port):
            return port
    raise RuntimeError(f"No free ports found between {start_port} and {max_port}")


def get_processes_on_port(port: int) -> list[int]:
    try:
        import psutil
    except ImportError:
        return []

    pids = set()
    for conn in psutil.net_connections(kind="inet"):
        if conn.laddr and conn.laddr.port == port and conn.pid and conn.pid != os.getpid():
            pids.add(conn.pid)
    return sorted(pids)


def kill_process(pid: int) -> bool:
    try:
        import psutil
        proc = psutil.Process(pid)
        proc.terminate()
        proc.wait(timeout=3)
        return True
    except Exception:
        pass

    if sys.platform.startswith("win"):
        try:
            subprocess.run(
                ["taskkill", "/PID", str(pid), "/F", "/T"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except Exception:
            return False

    try:
        os.kill(pid, signal.SIGTERM)
        return True
    except Exception:
        return False


def release_port(port: int) -> bool:
    if is_port_free(port):
        return True

    pids = get_processes_on_port(port)
    if not pids:
        return False

    killed = []
    for pid in pids:
        if kill_process(pid):
            killed.append(pid)

    if killed:
        print(
            f"Stopped existing process(es) {', '.join(str(pid) for pid in killed)} "
            f"using port {port}",
            flush=True,
        )
        time.sleep(1)

    return is_port_free(port)


def main():
    root_dir = Path(__file__).resolve().parent
    repo_root = root_dir.parent
    print(f"Launching Reflex App from workspace root: {repo_root}", flush=True)

    apply_env_from_config(root_dir)
    parser = argparse.ArgumentParser(description="Movie Song Downloader launcher")
    parser.add_argument("--env", choices=["dev", "prod"], default="dev")
    parser.add_argument("--frontend-port", dest="frontend_port", default=os.environ.get("FLET_WEB_PORT"))
    args, extra_args = parser.parse_known_args(sys.argv[1:])

    requested_port = int(args.frontend_port) if args.frontend_port else None
    frontend_port = requested_port
    if requested_port is None:
        configured_port = int(os.environ.get("FLET_WEB_PORT", 8555))
        if is_port_free(configured_port):
            frontend_port = configured_port
        elif release_port(configured_port):
            frontend_port = configured_port
        else:
            fallback_port = find_free_port(configured_port + 1)
            print(
                f"Configured port {configured_port} is unavailable, using fallback port {fallback_port}",
                flush=True,
            )
            frontend_port = fallback_port
    else:
        if not is_port_free(requested_port):
            if release_port(requested_port):
                frontend_port = requested_port
            else:
                fallback_port = find_free_port(requested_port + 1)
                print(
                    f"Requested port {requested_port} is unavailable and could not be released, using fallback port {fallback_port}",
                    flush=True,
                )
                frontend_port = fallback_port

    cmd = ["reflex", "run"]
    if frontend_port:
        cmd.extend(["--frontend-port", str(frontend_port)])
    if args.env == "prod":
        cmd.append("--env")
        cmd.append("prod")
    cmd.extend(extra_args)

    if args.env == "dev":
        def on_config_change(path: Path):
            if path.name == ".env":
                apply_env_from_config(root_dir)
                print("Reloaded .env settings", flush=True)
            elif path.name == "rxconfig.py":
                reload_rxconfig(root_dir)

        watcher = DevConfigWatcher(root_dir, on_config_change)
        watcher_thread = threading.Thread(target=watcher.watch, daemon=True)
        watcher_thread.start()

    print(f"Running command: {' '.join(cmd)}", flush=True)
    try:
        env = os.environ.copy()
        env["PYTHONPATH"] = f"{workspace_root}{os.pathsep}{services_dir}{os.pathsep}{env.get('PYTHONPATH', '')}"
        subprocess.run(cmd, cwd=repo_root, env=env, check=True)
    except KeyboardInterrupt:
        print("\nExiting Reflex Application...", flush=True)
    except subprocess.CalledProcessError as exc:
        print(f"Reflex exited with {exc.returncode}", file=sys.stderr, flush=True)
        sys.exit(exc.returncode)
    finally:
        if args.env == "dev":
            watcher.stop()


if __name__ == "__main__":
    main()
