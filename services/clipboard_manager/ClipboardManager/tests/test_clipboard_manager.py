import sys
import os

# Insert the parent directory so we can import clipboard_manager
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest  # noqa: E402
from unittest.mock import patch, MagicMock  # noqa: E402

from clipboard_manager import ClipboardManagerApp  # noqa: E402


@pytest.fixture
def manager():
    # Use in-memory SQLite database for safe testing
    with (
        patch("clipboard_manager.ClipboardDB.__init__", return_value=None),
        patch("clipboard_manager.pystray.Icon"),
    ):
        m = ClipboardManagerApp()
        # Mock the DB
        m.db = MagicMock()
        return m


def test_emergency_save_hook_text(manager):
    # Simulate an emergency hook with TEXT clipboard data
    with patch("clipboard_manager.win32clipboard") as mock_clipboard:
        # It should say TEXT format is available
        mock_clipboard.IsClipboardFormatAvailable.side_effect = lambda fmt: (
            fmt == 13
        )  # win32con.CF_UNICODETEXT
        mock_clipboard.GetClipboardData.return_value = "Emergency Text!"

        manager._emergency_save_hook()

        # Verify db.add_entry was called
        manager.db.add_entry.assert_called_once_with("text", "Emergency Text!")


def test_emergency_save_hook_filepath(manager):
    # Simulate an emergency hook with CF_HDROP clipboard data
    with patch("clipboard_manager.win32clipboard") as mock_clipboard:
        # 13 = CF_UNICODETEXT, 15 = CF_HDROP
        def _mock_format(fmt):
            if fmt == 13:
                return False
            if fmt == 15:
                return True
            return False

        mock_clipboard.IsClipboardFormatAvailable.side_effect = _mock_format
        mock_clipboard.GetClipboardData.return_value = (
            "C:\\test1.txt",
            "C:\\test2.txt",
        )

        manager._emergency_save_hook()

        # Verify db.add_entry was called
        manager.db.add_entry.assert_called_once_with(
            "filepath", "C:\\test1.txt\nC:\\test2.txt"
        )


def test_emergency_save_hook_empty(manager):
    with patch("clipboard_manager.win32clipboard") as mock_clipboard:
        mock_clipboard.IsClipboardFormatAvailable.return_value = False
        manager._emergency_save_hook()
        # Ensure it doesn't add anything if no format is available
        manager.db.add_entry.assert_not_called()
