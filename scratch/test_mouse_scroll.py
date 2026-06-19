import time
from pynput import mouse

def on_scroll(x, y, dx, dy):
    print(f"[{time.time():.3f}] Scroll event: x={x}, y={y}, dx={dx}, dy={dy}")

print("Starting mouse listener... Scroll around the screen and over the taskbar.")
with mouse.Listener(on_scroll=on_scroll) as listener:
    try:
        listener.join()
    except KeyboardInterrupt:
        print("Listener stopped.")
