# MovieSongDownloader/ui/home.py

import reflex as rx
from MovieSongDownloader.ui.state import AppState
from MovieSongDownloader.ui import style


def movie_card(movie: rx.Var[dict]) -> rx.Component:
    """Renders a single movie card with poster and controls."""
    poster_src = rx.cond(
        movie["poster_url"],
        movie["poster_url"],
        "https://via.placeholder.com/150x220?text=No+Poster",
    )

    return rx.vstack(
        rx.image(
            src=poster_src,
            width="100%",
            height="240px",
            object_fit="cover",
            border_radius="6px",
        ),
        rx.text(
            movie["title"],
            font_weight="bold",
            font_size="14px",
            color=style.COLOR_TEXT_PRIMARY,
            overflow="ellipsis",
            white_space="nowrap",
            width="100%",
        ),
        rx.hstack(
            rx.text(
                rx.cond(movie["year"], movie["year"].to(str), "N/A"),
                font_size="11px",
                color=style.COLOR_TEXT_MUTED,
            ),
            rx.cond(
                movie["rating"],
                rx.text(
                    f"★ {movie['rating']}",
                    font_size="11px",
                    color="#F59E0B",
                    font_weight="bold",
                ),
            ),
            justify="between",
            width="100%",
        ),
        rx.hstack(
            rx.button(
                "Browse",
                on_click=AppState.on_browse_clicked(movie),
                color=style.COLOR_ACCENT,
                variant="ghost",
                size="2",
                cursor="pointer",
                padding="0",
            ),
            rx.icon_button(
                rx.icon("plus"),
                on_click=AppState.add_to_watchlist_from_card(movie),
                color_scheme="green",
                variant="ghost",
                size="1",
                cursor="pointer",
            ),
            justify="between",
            width="100%",
        ),
        width="180px",
        padding="12px",
        background_color=style.COLOR_BG_SECONDARY,
        border=f"1px solid {style.COLOR_BORDER}",
        border_radius="8px",
        align_items="start",
        spacing="2",
        transition="all 0.2s ease-in-out",
        _hover={"transform": "scale(1.03)", "border_color": style.COLOR_ACCENT},
    )


def watchlist_row(item: rx.Var[dict]) -> rx.Component:
    """Renders a single row in the watchlist table."""
    status_bg = rx.match(
        item["status"],
        ("watching", "#F59E0B"),
        ("found", "#3B82F6"),
        ("downloaded", "#22C55E"),
        ("expired", style.COLOR_ACCENT),
        style.COLOR_TEXT_PRIMARY,
    )

    return rx.hstack(
        rx.icon("tv", color=style.COLOR_ACCENT, size=20),
        rx.vstack(
            rx.text(
                item["title"],
                font_weight="bold",
                font_size="15px",
                color=style.COLOR_TEXT_PRIMARY,
            ),
            rx.text(
                rx.cond(
                    item["last_checked"],
                    f"Last checked: {item['last_checked']}",
                    "Last checked: N/A",
                ),
                font_size="11px",
                color=style.COLOR_TEXT_MUTED,
            ),
            align_items="start",
            spacing="1",
        ),
        rx.spacer(),
        rx.text(
            rx.cond(item["auto_download"], "Auto-DL", "Manual"),
            font_size="12px",
            color=style.COLOR_TEXT_MUTED,
        ),
        rx.badge(
            item["status"],
            background_color=status_bg,
            color=style.COLOR_BG_SECONDARY,
            font_weight="bold",
            padding_x="8px",
            padding_y="4px",
            border_radius="4px",
        ),
        rx.icon_button(
            rx.icon("trash-2"),
            on_click=AppState.remove_watchlist_item(item["id"].to(int)),
            color_scheme="red",
            variant="ghost",
            size="2",
            cursor="pointer",
        ),
        width="100%",
        padding="12px 16px",
        background_color=style.COLOR_BG_SECONDARY,
        border=f"1px solid {style.COLOR_BORDER}",
        border_radius="8px",
        align_items="center",
    )


def home_view() -> rx.Component:
    """Builds the primary dashboard containing recent releases in grid mode."""
    return rx.vstack(
        # Page Title
        rx.heading("Dashboard Home", size="8", color=style.COLOR_TEXT_PRIMARY),
        rx.text(
            "Recent movie releases from Wikipedia. Click browse to explore soundtracks.",
            color=style.COLOR_TEXT_MUTED,
            font_size="14px",
        ),
        # Recent Releases Header
        rx.vstack(
            rx.text(
                "Recent Tamil Releases",
                font_size="18px",
                font_weight="bold",
                color=style.COLOR_ACCENT,
            ),
            rx.text(
                "Tamil cinema releases from Wikipedia. Details via OMDb.",
                color=style.COLOR_TEXT_MUTED,
                font_size="12px",
            ),
            align_items="start",
            spacing="1",
            margin_top="24px",
        ),
        # Releases Grid Body (Always Grid Mode)
        rx.cond(
            AppState.releases_loading,
            rx.center(
                rx.vstack(
                    rx.spinner(color=style.COLOR_ACCENT, size="3"),
                    rx.text(
                        "Loading...",
                        font_size="13px",
                        color=style.COLOR_TEXT_MUTED,
                    ),
                    spacing="3",
                ),
                width="100%",
                height="200px",
            ),
            rx.cond(
                AppState.recent_releases.length() == 0,
                rx.center(
                    rx.text(
                        "No recent releases found in local database cache.",
                        color=style.COLOR_TEXT_MUTED,
                    ),
                    width="100%",
                    height="150px",
                ),
                # Grid wrap (always)
                rx.flex(
                    rx.foreach(AppState.recent_releases, movie_card),
                    spacing="4",
                    wrap="wrap",
                    width="100%",
                    padding="12px 4px",
                ),
            ),
        ),
        width="100%",
        spacing="4",
        align_items="start",
    )


def watchlist_view() -> rx.Component:
    """Builds the dedicated Watchlist tab."""
    return rx.vstack(
        # Page Title
        rx.heading("My Watchlist", size="8", color=style.COLOR_TEXT_PRIMARY),
        rx.text(
            "Track movies and automatically download their soundtracks.",
            color=style.COLOR_TEXT_MUTED,
            font_size="14px",
        ),
        # Watchlist Header with Check Button
        rx.hstack(
            rx.text(
                "Tracked Movies",
                font_size="18px",
                font_weight="bold",
                color=style.COLOR_ACCENT,
            ),
            rx.button(
                AppState.watchlist_btn_text,
                on_click=AppState.trigger_watchlist_check,
                disabled=AppState.watchlist_btn_disabled,
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
        # Watchlist Items
        rx.cond(
            AppState.watchlist_loading,
            rx.center(
                rx.spinner(color=style.COLOR_ACCENT), width="100%", height="100px"
            ),
            rx.cond(
                AppState.watchlist_items.length() == 0,
                rx.center(
                    rx.text(
                        "Watchlist empty. Search or browse movies to add them here.",
                        color=style.COLOR_TEXT_MUTED,
                        font_size="14px",
                    ),
                    width="100%",
                    height="100px",
                    border=f"1px dashed {style.COLOR_BORDER}",
                    border_radius="8px",
                ),
                rx.vstack(
                    rx.foreach(AppState.watchlist_items, watchlist_row),
                    spacing="3",
                    width="100%",
                ),
            ),
        ),
        width="100%",
        spacing="4",
        align_items="start",
    )

