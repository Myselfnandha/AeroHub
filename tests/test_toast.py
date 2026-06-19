import os
import sys

if "TCL_LIBRARY" not in os.environ or "TK_LIBRARY" not in os.environ:
    base_tcl_dir = os.path.join(
        os.environ.get("LOCALAPPDATA", ""),
        "Programs",
        "Python",
        "Python312",
        "tcl"
    )
    if os.path.isdir(base_tcl_dir):
        os.environ["TCL_LIBRARY"] = os.path.join(base_tcl_dir, "tcl8.6")
        os.environ["TK_LIBRARY"] = os.path.join(base_tcl_dir, "tk8.6")

import tkinter as tk

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from services.aerohub_core.toast_utils import BaseToast  # noqa: E402


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
