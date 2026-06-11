import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "services", "health_app"))
from health_app import HealthApp  # noqa: E402


def main():
    import time

    app = HealthApp()
    app._on_settings(None, None)

    # We don't have a main Tk loop because HealthApp relies on the tray icon
    # for its main loop. But for this test, we can just start a simple blocking loop.
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
