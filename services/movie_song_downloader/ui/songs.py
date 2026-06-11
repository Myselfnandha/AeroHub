# MovieSongDownloader/ui/songs.py

import reflex as rx
from MovieSongDownloader.ui.state import AppState
from MovieSongDownloader.ui import style


def track_row(track: rx.Var[dict]) -> rx.Component:
    """Renders a single track row with details, select checkbox, and preview clip."""
    # Track duration formatting MM:SS
    duration_sec = track["duration_ms"].to(int) / 1000
    minutes = (duration_sec / 60).to(int)
    seconds = (duration_sec % 60).to(int)
    # Pad single digit seconds
    duration_str = rx.cond(
        seconds < 10, f"{minutes}:0{seconds}", f"{minutes}:{seconds}"
    )

    is_checked = AppState.selected_track_ids.contains(track["db_id"])
    is_playing = AppState.audio_preview_url == track["preview_url"]

    return rx.hstack(
        rx.checkbox(
            checked=is_checked,
            on_change=lambda _: AppState.toggle_track_selection(track["db_id"]),
            color_scheme="cyan",
            cursor="pointer",
        ),
        rx.text(
            track["track_number"].to(str),
            width="30px",
            font_size="13px",
            color=style.COLOR_TEXT_MUTED,
        ),
        rx.vstack(
            rx.text(
                track["title"],
                font_weight="bold",
                font_size="14px",
                color=style.COLOR_TEXT_PRIMARY,
            ),
            rx.text(track["artist"], font_size="12px", color=style.COLOR_TEXT_MUTED),
            align_items="start",
            spacing="1",
            width="100%",
        ),
        rx.spacer(),
        rx.text(duration_str, font_size="13px", color=style.COLOR_TEXT_MUTED),
        rx.cond(
            track["preview_url"],
            rx.cond(
                is_playing,
                rx.icon_button(
                    rx.icon("square"),
                    on_click=AppState.play_preview_clip(track["preview_url"]),
                    color=style.COLOR_ACCENT,
                    variant="ghost",
                    size="2",
                    cursor="pointer",
                ),
                rx.icon_button(
                    rx.icon("play"),
                    on_click=AppState.play_preview_clip(track["preview_url"]),
                    color=style.COLOR_ACCENT,
                    variant="ghost",
                    size="2",
                    cursor="pointer",
                ),
            ),
        ),
        width="100%",
        padding="8px 12px",
        background_color=style.COLOR_BG_SECONDARY,
        border_radius="6px",
        align_items="center",
    )


def dir_explorer_modal() -> rx.Component:
    """A beautiful, browser-compatible local folder explorer built inside a Reflex dialog."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "Local Directory Explorer", color=style.COLOR_ACCENT, font_weight="bold"
            ),
            rx.dialog.description(
                "Browse and select an absolute path on your host machine to store downloads.",
                color=style.COLOR_TEXT_MUTED,
                font_size="13px",
            ),
            rx.vstack(
                # Current Path indicator
                rx.hstack(
                    rx.text(
                        "Current Path:",
                        font_weight="bold",
                        font_size="13px",
                        color=style.COLOR_TEXT_MUTED,
                    ),
                    rx.text(
                        AppState.dir_explorer_path,
                        font_size="13px",
                        color=style.COLOR_TEXT_PRIMARY,
                    ),
                    spacing="2",
                    width="100%",
                    padding_y="8px",
                ),
                # Explorer Area
                rx.vstack(
                    # Up directory button
                    rx.button(
                        rx.hstack(rx.icon("folder-up"), rx.text(".. Parent Directory")),
                        on_click=AppState.navigate_up_dir,
                        width="100%",
                        variant="ghost",
                        color_scheme="gray",
                        cursor="pointer",
                        justify_content="start",
                    ),
                    # Directories listing
                    rx.cond(
                        AppState.dir_explorer_error,
                        rx.text(
                            AppState.dir_explorer_error,
                            color="#EF4444",
                            font_size="13px",
                        ),
                        rx.cond(
                            AppState.dir_explorer_items.length() == 0,
                            rx.text(
                                "No subdirectories found.",
                                color=style.COLOR_TEXT_MUTED,
                                font_size="13px",
                                padding_y="12px",
                            ),
                            rx.vstack(
                                rx.foreach(
                                    AppState.dir_explorer_items,
                                    lambda folder: rx.button(
                                        rx.hstack(
                                            rx.icon("folder", color=style.COLOR_ACCENT),
                                            rx.text(folder),
                                        ),
                                        on_click=AppState.navigate_dir(folder),
                                        width="100%",
                                        variant="ghost",
                                        color_scheme="cyan",
                                        cursor="pointer",
                                        justify_content="start",
                                    ),
                                ),
                                spacing="1",
                                width="100%",
                            ),
                        ),
                    ),
                    width="100%",
                    height="300px",
                    overflow_y="scroll",
                    border=f"1px solid {style.COLOR_BORDER}",
                    border_radius="6px",
                    padding="12px",
                    background_color=style.COLOR_BG_PRIMARY,
                ),
                # Modal Actions Footer
                rx.hstack(
                    rx.button(
                        "Cancel",
                        on_click=AppState.cancel_dir_explorer,
                        variant="soft",
                        color_scheme="gray",
                        cursor="pointer",
                    ),
                    rx.button(
                        "Select Folder",
                        on_click=AppState.select_current_dir,
                        background_color=style.COLOR_ACCENT,
                        color=style.COLOR_TEXT_PRIMARY,
                        cursor="pointer",
                    ),
                    width="100%",
                    justify="end",
                    spacing="3",
                    margin_top="16px",
                ),
                width="100%",
            ),
            background_color=style.COLOR_BG_SECONDARY,
            border=f"1px solid {style.COLOR_BORDER}",
            max_width="500px",
        ),
        open=AppState.dir_explorer_open,
    )


def missing_dir_dialog() -> rx.Component:
    """Warning dialog shown if the output directory is not set when enqueuing tracks."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "Output Directory Not Set", color=style.COLOR_ACCENT, font_weight="bold"
            ),
            rx.dialog.description(
                "No output directory has been configured. Click below to browse and select a path.",
                color=style.COLOR_TEXT_PRIMARY,
                font_size="14px",
            ),
            rx.hstack(
                rx.button(
                    "Default to Downloads",
                    on_click=AppState.cancel_dir_explorer,
                    variant="soft",
                    color_scheme="gray",
                    cursor="pointer",
                ),
                rx.button(
                    "Select Folder",
                    on_click=AppState.trigger_dialog_folder_picker,
                    background_color=style.COLOR_ACCENT,
                    color=style.COLOR_TEXT_PRIMARY,
                    cursor="pointer",
                ),
                width="100%",
                justify="end",
                spacing="3",
                margin_top="20px",
            ),
            background_color=style.COLOR_BG_SECONDARY,
            border=f"1px solid {style.COLOR_BORDER}",
        ),
        open=AppState.missing_dir_dialog_open,
    )


def songs_view() -> rx.Component:
    """Detailed album sheet listing songs and supporting playback previews & queuing."""
    cover_src = rx.cond(
        AppState.selected_album["cover_url"],
        AppState.selected_album["cover_url"],
        "https://via.placeholder.com/120?text=No+Cover",
    )

    return rx.vstack(
        # Back Header
        rx.button(
            rx.hstack(rx.icon("arrow-left"), rx.text("Back to Search")),
            on_click=AppState.close_songs_view,
            color=style.COLOR_ACCENT,
            variant="ghost",
            cursor="pointer",
            size="2",
            padding="0",
        ),
        # Album Detail Card
        rx.hstack(
            rx.image(
                src=cover_src,
                width="120px",
                height="120px",
                object_fit="cover",
                border_radius="8px",
            ),
            rx.vstack(
                rx.text(
                    "SOUNDTRACK ALBUM",
                    size="1",
                    color=style.COLOR_ACCENT,
                    font_weight="bold",
                ),
                rx.heading(
                    AppState.selected_album["title"],
                    size="6",
                    color=style.COLOR_TEXT_PRIMARY,
                ),
                rx.text(
                    f"Movie: {AppState.selected_movie['title']} ({AppState.selected_movie['year']})",
                    font_size="14px",
                    color=style.COLOR_TEXT_MUTED,
                ),
                rx.text(
                    f"Artists: {AppState.selected_album['artist']}",
                    font_size="13px",
                    color=style.COLOR_TEXT_MUTED,
                ),
                align_items="start",
                spacing="1",
            ),
            spacing="4",
            margin_top="16px",
            align_items="center",
        ),
        # Sub-controls
        rx.hstack(
            rx.checkbox(
                label="Select All Tracks",
                checked=AppState.select_all,
                on_change=lambda _: AppState.toggle_select_all(),
                color_scheme="cyan",
                cursor="pointer",
                font_weight="bold",
            ),
            rx.button(
                AppState.download_btn_text,
                on_click=AppState.download_selected_tracks,
                disabled=AppState.download_btn_disabled,
                background_color=style.COLOR_ACCENT,
                color=style.COLOR_TEXT_PRIMARY,
                cursor="pointer",
                size="2",
            ),
            width="100%",
            justify="between",
            margin_top="24px",
            align_items="center",
        ),
        rx.divider(color=style.COLOR_BORDER),
        # Tracks Listing area
        rx.cond(
            AppState.tracks_loading,
            rx.center(
                rx.vstack(
                    rx.spinner(color=style.COLOR_ACCENT, size="3"),
                    rx.text(
                        "Loading album tracks and syncing database records...",
                        font_size="13px",
                        color=style.COLOR_TEXT_MUTED,
                    ),
                    spacing="3",
                ),
                width="100%",
                height="200px",
            ),
            rx.cond(
                AppState.album_tracks.length() == 0,
                rx.center(
                    rx.text(
                        "No tracks found for this soundtrack album.",
                        color=style.COLOR_TEXT_MUTED,
                    ),
                    width="100%",
                    height="100px",
                ),
                rx.vstack(
                    rx.foreach(AppState.album_tracks, track_row),
                    spacing="2",
                    width="100%",
                    padding_bottom="30px",
                ),
            ),
        ),
        # Declarative Audio Node for Preview Playbacks
        rx.cond(
            AppState.audio_preview_url != "",
            rx.audio(
                src=AppState.audio_preview_url,
                playing=True,
                controls=False,
                width="0px",
                height="0px",
            ),
        ),
        # Warning Dialog and Directory Explorer Modals
        missing_dir_dialog(),
        dir_explorer_modal(),
        width="100%",
        spacing="4",
        align_items="start",
    )
