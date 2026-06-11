import tkinter as tk
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from toast_utils import BaseToast  # noqa: E402


def test():
    root = tk.Tk()
    root.withdraw()
    settings = {"toast_pos": "Center"}
    toast = BaseToast(root, "Test", "This is a test", settings)
    toast.show()
    root.after(3000, root.destroy)
    root.mainloop()


if __name__ == "__main__":
    test()
