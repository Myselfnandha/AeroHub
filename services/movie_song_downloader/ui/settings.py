# MovieSongDownloader/ui/settings.py

import reflex as rx
from MovieSongDownloader.ui.state import AppState
from MovieSongDownloader.ui import style
from MovieSongDownloader.ui.songs import dir_explorer_modal


def settings_view() -> rx.Component:
    """Renders the settings configurations panel."""
    # Presets options
    folder_options = [
        "{Year}/{Movie}/Songs",
        "{Movie}",
        "{Artist}/{Album}",
        "{Movie}/{Songs}",
        "Custom...",
    ]
    filename_options = [
        "{TrackNum} - {Title}",
        "{Title}",
        "{Artist} - {Title}",
        "{TrackNum}. {Title}",
        "Custom...",
    ]
    audio_formats = ["mp3", "flac"]
    bitrates = ["320", "192", "128"]

    # Custom field visibility checks
    show_custom_folder = AppState.folder_format_dropdown == "Custom..."
    show_custom_filename = AppState.filename_format_dropdown == "Custom..."

    return rx.vstack(
        rx.heading("Settings Dashboard", size="8", color=style.COLOR_TEXT_PRIMARY),
        rx.text(
            "Configure OMDb API keys, download formats, path templates, and automation.",
            color=style.COLOR_TEXT_MUTED,
            font_size="14px",
        ),
        # --- DATA SOURCES CARD ---
        rx.vstack(
            rx.text(
                "DATA SOURCES",
                font_size="16px",
                font_weight="bold",
                color=style.COLOR_ACCENT,
            ),
            rx.text(
                "Wikipedia + JioSaavn (automatic, no keys needed) • OMDb for ratings/cast",
                font_size="12px",
                color=style.COLOR_TEXT_MUTED,
            ),
            rx.divider(color=style.COLOR_BORDER),
            # OMDb Key
            rx.vstack(
                rx.text(
                    "OMDb API Key (Required for ratings/cast)",
                    font_size="13px",
                    font_weight="semibold",
                    color=style.COLOR_TEXT_PRIMARY,
                ),
                rx.input(
                    value=AppState.omdb_api_key,
                    on_change=AppState.set_omdb_api_key,
                    type="password",
                    width="100%",
                    background_color="transparent",
                    border=f"1px solid {style.COLOR_BORDER}",
                    color=style.COLOR_TEXT_PRIMARY,
                ),
                align_items="start",
                width="100%",
            ),
            # Deezer ARL
            rx.vstack(
                rx.text(
                    "Deezer ARL Cookie Token (Optional for higher quality Deezer sources)",
                    font_size="13px",
                    font_weight="semibold",
                    color=style.COLOR_TEXT_PRIMARY,
                ),
                rx.input(
                    value=AppState.deezer_arl,
                    on_change=AppState.set_deezer_arl,
                    type="password",
                    width="100%",
                    background_color="transparent",
                    border=f"1px solid {style.COLOR_BORDER}",
                    color=style.COLOR_TEXT_PRIMARY,
                ),
                align_items="start",
                width="100%",
            ),
            width="100%",
            spacing="4",
            padding="24px",
            background_color=style.COLOR_BG_SECONDARY,
            border=f"1px solid {style.COLOR_BORDER}",
            border_radius="10px",
            align_items="start",
            margin_top="24px",
        ),
        # --- DOWNLOADS & CUSTOM PATHS CARD ---
        rx.vstack(
            rx.text(
                "DOWNLOADS & CUSTOM PATHS",
                font_size="16px",
                font_weight="bold",
                color=style.COLOR_ACCENT,
            ),
            rx.divider(color=style.COLOR_BORDER),
            # Output Dir Selector
            rx.vstack(
                rx.text(
                    "Music Output Directory",
                    font_size="13px",
                    font_weight="semibold",
                    color=style.COLOR_TEXT_PRIMARY,
                ),
                rx.hstack(
                    rx.input(
                        value=AppState.output_dir,
                        read_only=True,
                        width="100%",
                        background_color="transparent",
                        border=f"1px solid {style.COLOR_BORDER}",
                        color=style.COLOR_TEXT_PRIMARY,
                    ),
                    rx.button(
                        rx.hstack(rx.icon("folder-open"), rx.text("Browse")),
                        on_click=AppState.open_dir_explorer("output_dir"),
                        background_color=style.COLOR_ACCENT,
                        color=style.COLOR_TEXT_PRIMARY,
                        cursor="pointer",
                    ),
                    width="100%",
                    spacing="3",
                ),
                align_items="start",
                width="100%",
            ),
            # Folder and Filename dropdowns
            rx.flex(
                # Folder dropdown
                rx.vstack(
                    rx.text(
                        "Folder Path Template",
                        font_size="13px",
                        font_weight="semibold",
                        color=style.COLOR_TEXT_PRIMARY,
                    ),
                    rx.select(
                        folder_options,
                        value=AppState.folder_format_dropdown,
                        on_change=AppState.set_folder_format_dropdown,
                        width="100%",
                    ),
                    rx.cond(
                        show_custom_folder,
                        rx.input(
                            placeholder="Custom Folder Path (e.g. {Artist}/{Album})",
                            value=AppState.folder_format_custom,
                            on_change=AppState.set_folder_format_custom,
                            width="100%",
                            margin_top="8px",
                            background_color="transparent",
                            border=f"1px solid {style.COLOR_BORDER}",
                            color=style.COLOR_TEXT_PRIMARY,
                        ),
                    ),
                    align_items="start",
                    flex="1",
                ),
                # Filename dropdown
                rx.vstack(
                    rx.text(
                        "Filename Format Template",
                        font_size="13px",
                        font_weight="semibold",
                        color=style.COLOR_TEXT_PRIMARY,
                    ),
                    rx.select(
                        filename_options,
                        value=AppState.filename_format_dropdown,
                        on_change=AppState.set_filename_format_dropdown,
                        width="100%",
                    ),
                    rx.cond(
                        show_custom_filename,
                        rx.input(
                            placeholder="Custom Filename Format (e.g. {TrackNum} - {Title})",
                            value=AppState.filename_format_custom,
                            on_change=AppState.set_filename_format_custom,
                            width="100%",
                            margin_top="8px",
                            background_color="transparent",
                            border=f"1px solid {style.COLOR_BORDER}",
                            color=style.COLOR_TEXT_PRIMARY,
                        ),
                    ),
                    align_items="start",
                    flex="1",
                ),
                width="100%",
                spacing="4",
            ),
            # Format and Bitrate
            rx.flex(
                rx.vstack(
                    rx.text(
                        "Audio Format",
                        font_size="13px",
                        font_weight="semibold",
                        color=style.COLOR_TEXT_PRIMARY,
                    ),
                    rx.select(
                        audio_formats,
                        value=AppState.audio_format,
                        on_change=AppState.set_audio_format,
                        width="100%",
                    ),
                    align_items="start",
                    flex="1",
                ),
                rx.vstack(
                    rx.text(
                        "MP3 Bitrate (kbps)",
                        font_size="13px",
                        font_weight="semibold",
                        color=style.COLOR_TEXT_PRIMARY,
                    ),
                    rx.select(
                        bitrates,
                        value=AppState.bitrate,
                        on_change=AppState.set_bitrate,
                        width="100%",
                    ),
                    align_items="start",
                    flex="1",
                ),
                width="100%",
                spacing="4",
            ),
            # Download Provider Selection
            rx.vstack(
                rx.text(
                    "Download Provider Backend",
                    font_size="13px",
                    font_weight="semibold",
                    color=style.COLOR_TEXT_PRIMARY,
                ),
                rx.select(
                    ["spotiflac", "deezspot"],
                    value=AppState.download_provider,
                    on_change=AppState.set_download_provider,
                    width="100%",
                ),
                rx.text(
                    (
                        "Priority Details: \n• spotiflac: true lossless downloads utilizing Tidal, Qobuz, "
                        "Deezer, and Amazon. Requires globally installed spotiflac. \n• deezspot: fetches "
                        "and matches JioSaavn direct audio or Deezer links, utilizing yt-dlp/deezload "
                        "as a backup."
                    ),
                    font_size="12px",
                    color=style.COLOR_TEXT_MUTED,
                    white_space="pre-line",
                    margin_top="4px",
                ),
                align_items="start",
                width="100%",
            ),
            # Switch controls
            rx.vstack(
                rx.hstack(
                    rx.switch(
                        checked=AppState.save_lrc_file,
                        on_change=AppState.set_save_lrc_file,
                        color_scheme="cyan",
                        cursor="pointer",
                    ),
                    rx.text(
                        "Save sidecar .lrc/.txt lyrics file",
                        color=style.COLOR_TEXT_PRIMARY,
                    ),
                    spacing="2",
                ),
                rx.hstack(
                    rx.switch(
                        checked=AppState.embed_lyrics,
                        on_change=AppState.set_embed_lyrics,
                        color_scheme="cyan",
                        cursor="pointer",
                    ),
                    rx.text(
                        "Embed lyrics metadata inside audio file",
                        color=style.COLOR_TEXT_PRIMARY,
                    ),
                    spacing="2",
                ),
                rx.hstack(
                    rx.switch(
                        checked=AppState.auto_download,
                        on_change=AppState.set_auto_download,
                        color_scheme="cyan",
                        cursor="pointer",
                    ),
                    rx.text(
                        "Auto-download matched soundtracks for watchlist items",
                        color=style.COLOR_TEXT_PRIMARY,
                    ),
                    spacing="2",
                ),
                align_items="start",
                spacing="3",
                margin_top="12px",
            ),
            width="100%",
            spacing="4",
            padding="24px",
            background_color=style.COLOR_BG_SECONDARY,
            border=f"1px solid {style.COLOR_BORDER}",
            border_radius="10px",
            align_items="start",
            margin_top="24px",
        ),
        # Save Trigger Button & Feedback status
        rx.hstack(
            rx.button(
                "Save Settings",
                on_click=AppState.save_settings,
                background_color=style.COLOR_ACCENT,
                color=style.COLOR_TEXT_PRIMARY,
                cursor="pointer",
                size="3",
                padding="0 32px",
            ),
            rx.cond(
                AppState.settings_status_msg,
                rx.text(
                    AppState.settings_status_msg,
                    color=AppState.settings_status_color,
                    font_weight="bold",
                    font_size="14px",
                ),
            ),
            width="100%",
            spacing="4",
            align_items="center",
            margin_top="24px",
            padding_bottom="40px",
        ),
        # Overlay Folder Picker dialog
        dir_explorer_modal(),
        width="100%",
        spacing="4",
        align_items="start",
    )
