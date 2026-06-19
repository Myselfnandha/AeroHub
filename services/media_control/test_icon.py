import win32api
import win32gui
import win32ui
import win32con
from PIL import Image


def get_icon(path):
    ico_x = 32
    ico_y = 32

    large, small = win32gui.ExtractIconEx(path, 0)
    if not large:
        return None

    hicon = large[0]
    win32gui.DestroyIcon(small[0]) if small else None

    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
    hbmp = win32ui.CreateBitmap()
    hbmp.CreateCompatibleBitmap(hdc, ico_x, ico_y)
    hdc_mem = hdc.CreateCompatibleDC()

    hdc_mem.SelectObject(hbmp)

    # Fill background with #1a1a3e
    brush = win32gui.CreateSolidBrush(win32api.RGB(0x1A, 0x1A, 0x3E))
    win32gui.FillRect(hdc_mem.GetSafeHdc(), (0, 0, ico_x, ico_y), brush)
    win32gui.DeleteObject(brush)

    # Draw icon
    win32gui.DrawIconEx(
        hdc_mem.GetSafeHdc(), 0, 0, hicon, ico_x, ico_y, 0, None, win32con.DI_NORMAL
    )

    bmpinfo = hbmp.GetInfo()
    bmpstr = hbmp.GetBitmapBits(True)

    im = Image.frombuffer(
        "RGBA", (bmpinfo["bmWidth"], bmpinfo["bmHeight"]), bmpstr, "raw", "BGRA", 0, 1
    )

    win32gui.DestroyIcon(hicon)
    return im


im = get_icon(r"C:\Program Files\Mozilla Firefox\firefox.exe")
if im:
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    im.save(os.path.join(script_dir, "firefox_icon_bg.png"))
    print("Icon saved")
