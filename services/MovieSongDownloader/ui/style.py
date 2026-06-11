# MovieSongDownloader/ui/style.py

# Colors
COLOR_ACCENT = "#06B6D4"  # Cyan accent
COLOR_ACCENT_LIGHT = "#22D3EE"  # Light cyan for hover/focus
COLOR_TEXT_PRIMARY = "#FFFFFF"  # Crisp white
COLOR_TEXT_MUTED = "#94A3B8"  # Muted cool gray
COLOR_BG_PRIMARY = "#0B0F19"  # Deep dark blue/gray
COLOR_BG_SECONDARY = "#111827"  # Dark gray
COLOR_BORDER = "#1F2937"  # Dark gray border
COLOR_SUCCESS = "#22C55E"
COLOR_WARN = "#FBBF24"
COLOR_ERROR = "#EF4444"
COLOR_INFO = "#60A5FA"
COLOR_DIM = "#64748B"

# Base container styling
BASE_STYLE = {
    "background_color": COLOR_BG_PRIMARY,
    "color": COLOR_TEXT_PRIMARY,
    "font_family": "system-ui, sans-serif",
    "min_height": "100vh",
}

# Sidebar/Navbar styles
SIDEBAR_STYLE = {
    "width": "240px",
    "height": "100vh",
    "position": "fixed",
    "left": "0",
    "top": "0",
    "background_color": COLOR_BG_SECONDARY,
    "border_right": f"1px solid {COLOR_BORDER}",
    "padding": "24px",
    "z_index": "100",
}

# Main content layout
CONTENT_STYLE = {
    "margin_left": "240px",
    "padding": "32px",
    "background_color": COLOR_BG_PRIMARY,
    "min_height": "100vh",
}

# Card layout
CARD_STYLE = {
    "background_color": COLOR_BG_SECONDARY,
    "border": f"1px solid {COLOR_BORDER}",
    "border_radius": "10px",
    "padding": "20px",
}

# Input fields
INPUT_STYLE = {
    "border": f"1px solid {COLOR_BORDER}",
    "focus_border_color": COLOR_ACCENT,
    "color": COLOR_TEXT_PRIMARY,
    "background_color": "transparent",
}

# Buttons
BUTTON_STYLE = {
    "background_color": COLOR_ACCENT,
    "color": COLOR_TEXT_PRIMARY,
    "_hover": {
        "background_color": COLOR_ACCENT_LIGHT,
    },
}
