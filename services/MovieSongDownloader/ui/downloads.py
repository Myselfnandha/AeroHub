# MovieSongDownloader/ui/downloads.py

import reflex as rx
from MovieSongDownloader.ui.state import AppState
from MovieSongDownloader.ui import style


def status_badge_color(status: rx.Var[str]) -> rx.Var[str]:
    return rx.match(
        status,
        ("queued", style.COLOR_WARN),
        ("downloading", style.COLOR_INFO),
        ("fetching_lyrics", style.COLOR_INFO),
        ("embedding_cover", style.COLOR_INFO),
        ("embedding_metadata", style.COLOR_INFO),
        ("copying_to_destination", style.COLOR_WARN),
        ("completed", style.COLOR_SUCCESS),
        ("failed", style.COLOR_ERROR),
        ("paused", style.COLOR_DIM),
        ("cancelled", style.COLOR_DIM),
        style.COLOR_TEXT_PRIMARY,
    )


def download_job_card(job: rx.Var[dict]) -> rx.Component:
    """Renders a single download job progress card."""
    is_active = rx.cond(
        (job["status"] == "completed")
        | (job["status"] == "failed")
        | (job["status"] == "cancelled")
        | (job["status"] == "paused"),
        False,
        True,
    )

    progress_percent = rx.cond(
        is_active,
        job["progress"].to(int),
        rx.cond(job["status"] == "completed", 100, 0),
    )

    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.text(
                    job["track_title"],
                    font_weight="bold",
                    font_size="16px",
                    color=style.COLOR_TEXT_PRIMARY,
                ),
                rx.text(
                    f"{job['track_artist']} • {job['album_title']}",
                    font_size="13px",
                    color=style.COLOR_TEXT_MUTED,
                    overflow="hidden",
                    text_overflow="ellipsis",
                    white_space="nowrap",
                    width="100%",
                ),
                align_items="start",
                spacing="1",
                width="100%",
            ),
            rx.badge(
                job["status"],
                background_color=status_badge_color(job["status"]),
                color=style.COLOR_BG_SECONDARY,
                font_weight="bold",
                padding_x="10px",
                padding_y="6px",
                border_radius="999px",
                text_transform="capitalize",
            ),
            justify="between",
            width="100%",
            align_items="center",
            spacing="4",
        ),
        rx.hstack(
            rx.progress(value=progress_percent, color_scheme="cyan", width="100%"),
            rx.text(
                f"{progress_percent}%",
                font_size="12px",
                color=style.COLOR_TEXT_MUTED,
                width="48px",
                text_align="right",
            ),
            width="100%",
            align_items="center",
            spacing="3",
        ),
        rx.hstack(
            rx.text(
                rx.cond(
                    job["format"],
                    f"Format: {job['format']}",
                    "Format: mp3",
                ),
                font_size="12px",
                color=style.COLOR_TEXT_MUTED,
            ),
            rx.text(
                rx.cond(
                    job["output_path"],
                    job["output_path"],
                    "Output path pending",
                ),
                font_size="12px",
                color=style.COLOR_TEXT_MUTED,
                overflow="hidden",
                white_space="nowrap",
                text_overflow="ellipsis",
                width="100%",
            ),
            width="100%",
            spacing="4",
        ),
        rx.cond(
            job["error_message"],
            rx.box(
                rx.text(
                    job["error_message"],
                    color=style.COLOR_ERROR,
                    font_size="12px",
                    max_width="100%",
                    overflow="hidden",
                    white_space="nowrap",
                    text_overflow="ellipsis",
                ),
                width="100%",
                background_color="#111827",
                padding="10px",
                border_radius="10px",
            ),
        ),
        rx.hstack(
            rx.cond(
                is_active,
                rx.icon_button(
                    rx.icon("square"),
                    on_click=AppState.cancel_download_job(job["id"].to(int)),
                    color_scheme="red",
                    variant="ghost",
                    size="2",
                    cursor="pointer",
                    tooltip="Cancel Download",
                ),
                rx.cond(
                    job["status"] == "paused",
                    rx.icon_button(
                        rx.icon("play"),
                        on_click=AppState.resume_download_job(job["id"].to(int)),
                        color_scheme="green",
                        variant="ghost",
                        size="2",
                        cursor="pointer",
                        tooltip="Resume Download",
                    ),
                    rx.cond(
                        (job["status"] == "failed") | (job["status"] == "cancelled"),
                        rx.icon_button(
                            rx.icon("rotate-ccw"),
                            on_click=AppState.retry_download_job(job["id"].to(int)),
                            color_scheme="blue",
                            variant="ghost",
                            size="2",
                            cursor="pointer",
                            tooltip="Retry Download",
                        ),
                    ),
                ),
            ),
            width="100%",
            justify="end",
            align_items="center",
        ),
        width="100%",
        padding="18px",
        background_color=style.COLOR_BG_SECONDARY,
        border=f"1px solid {style.COLOR_BORDER}",
        border_radius="16px",
        spacing="3",
        box_shadow="0 18px 36px rgba(0,0,0,0.08)",
    )


def downloads_view() -> rx.Component:
    """Renders the Downloads Manager view."""
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.heading(
                    "Downloads Manager",
                    size="8",
                    color=style.COLOR_TEXT_PRIMARY,
                ),
                rx.text(
                    "Track active downloads, monitor queue progress, and recover failed jobs.",
                    color=style.COLOR_TEXT_MUTED,
                    font_size="14px",
                ),
                align_items="start",
                spacing="1",
            ),
            rx.button(
                "Refresh Queue",
                on_click=AppState.load_download_jobs,
                background_color=style.COLOR_ACCENT,
                color=style.COLOR_TEXT_PRIMARY,
                cursor="pointer",
                size="2",
            ),
            width="100%",
            justify="between",
            align_items="center",
            flex_wrap="wrap",
            gap="12px",
        ),
        rx.divider(color=style.COLOR_BORDER, margin_top="16px"),
        rx.cond(
            AppState.downloads_loading,
            rx.center(
                rx.vstack(
                    rx.spinner(color=style.COLOR_ACCENT, size="3"),
                    rx.text(
                        "Loading download queue...",
                        font_size="13px",
                        color=style.COLOR_TEXT_MUTED,
                    ),
                    spacing="3",
                ),
                width="100%",
                height="260px",
            ),
            rx.cond(
                AppState.download_jobs.length() == 0,
                rx.center(
                    rx.vstack(
                        rx.icon("cloud-download", size=48, color=style.COLOR_DIM),
                        rx.heading("No downloads yet", size="5", color=style.COLOR_TEXT_MUTED),
                        rx.text(
                            "Select songs and queue downloads to see progress here.",
                            color=style.COLOR_TEXT_MUTED,
                            font_size="13px",
                        ),
                        spacing="3",
                    ),
                    width="100%",
                    height="260px",
                    padding="24px",
                    border=f"1px dashed {style.COLOR_BORDER}",
                    border_radius="16px",
                ),
                rx.vstack(
                    rx.foreach(AppState.download_jobs, download_job_card),
                    spacing="3",
                    width="100%",
                    padding_bottom="30px",
                ),
            ),
        ),
        width="100%",
        spacing="4",
        align_items="start",
    )
