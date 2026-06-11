# MovieSongDownloader/ui/search.py

import reflex as rx
from MovieSongDownloader.ui.state import AppState
from MovieSongDownloader.ui import style


def movie_search_card(movie: rx.Var[dict]) -> rx.Component:
    """Renders a movie card result in search grid."""
    poster_src = rx.cond(
        movie["poster_url"],
        movie["poster_url"],
        "https://via.placeholder.com/150x220?text=No+Poster",
    )

    return rx.vstack(
        rx.image(
            src=poster_src,
            width="100%",
            height="260px",
            object_fit="cover",
            border_radius="8px",
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
                font_size="12px",
                color=style.COLOR_TEXT_MUTED,
            ),
            rx.cond(
                movie["rating"],
                rx.badge(
                    f"★ {movie['rating']}",
                    background_color="#F59E0B",
                    color=style.COLOR_BG_SECONDARY,
                    font_weight="bold",
                ),
            ),
            justify="between",
            width="100%",
        ),
        width="100%",
        padding="12px",
        background_color=style.COLOR_BG_SECONDARY,
        border=f"1px solid {style.COLOR_BORDER}",
        border_radius="10px",
        align_items="start",
        spacing="2",
        cursor="pointer",
        on_click=AppState.on_browse_clicked(movie),
        transition="all 0.2s ease-in-out",
        _hover={"transform": "scale(1.02)", "border_color": style.COLOR_ACCENT},
    )


def search_view() -> rx.Component:
    """Renders the Soundtracks Search tab view."""
    return rx.vstack(
        rx.heading("Soundtracks Search", size="8", color=style.COLOR_TEXT_PRIMARY),
        rx.text(
            "Search Wikipedia for movies, or paste a JioSaavn or Spotify Album link directly.",
            color=style.COLOR_TEXT_MUTED,
            font_size="14px",
        ),
        # Inputs Form
        rx.form(
            rx.hstack(
                rx.input(
                    name="search_query",
                    placeholder="Search movie titles or JioSaavn/Spotify album link...",
                    value=AppState.search_query,
                    on_change=AppState.set_search_query,
                    background_color="transparent",
                    border=f"1px solid {style.COLOR_BORDER}",
                    color=style.COLOR_TEXT_PRIMARY,
                    width="100%",
                    size="3",
                ),
                rx.input(
                    name="search_year",
                    placeholder="Year (Optional)",
                    value=AppState.search_year,
                    on_change=AppState.set_search_year,
                    background_color="transparent",
                    border=f"1px solid {style.COLOR_BORDER}",
                    color=style.COLOR_TEXT_PRIMARY,
                    width="150px",
                    size="3",
                ),
                rx.button(
                    "Search",
                    background_color=style.COLOR_ACCENT,
                    color=style.COLOR_TEXT_PRIMARY,
                    cursor="pointer",
                    size="3",
                    padding="0 24px",
                    type="submit",
                ),
                width="100%",
                spacing="3",
                align_items="center",
            ),
            on_submit=AppState.run_search,
            width="100%",
            margin_top="24px",
        ),
        rx.divider(color=style.COLOR_BORDER, margin_top="16px"),
        # Results section
        rx.cond(
            AppState.search_loading,
            rx.center(
                rx.vstack(
                    rx.spinner(color=style.COLOR_ACCENT, size="3"),
                    rx.text(
                        "Searching movies / resolving Jiosaavn link...",
                        font_size="13px",
                        color=style.COLOR_TEXT_MUTED,
                    ),
                    spacing="3",
                ),
                width="100%",
                height="300px",
            ),
            rx.vstack(
                rx.cond(
                    AppState.search_error,
                    rx.center(
                        rx.text(
                            AppState.search_error,
                            color=style.COLOR_ACCENT,
                            font_size="14px",
                        ),
                        width="100%",
                        height="100px",
                    ),
                ),
                rx.cond(
                    AppState.search_results.length() == 0,
                    rx.center(
                        rx.text(
                            "No results found. Type a query and search.",
                            color=style.COLOR_TEXT_MUTED,
                            font_size="14px",
                        ),
                        width="100%",
                        height="200px",
                    ),
                    rx.grid(
                        rx.foreach(AppState.search_results, movie_search_card),
                        columns="5",
                        spacing="4",
                        width="100%",
                        padding="16px 0",
                    ),
                ),
                width="100%",
            ),
        ),
        width="100%",
        spacing="4",
        align_items="start",
    )
