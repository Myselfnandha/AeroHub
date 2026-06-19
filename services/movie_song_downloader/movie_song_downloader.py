# movie_song_downloader/movie_song_downloader.py

import reflex as rx
import time

from movie_song_downloader.ui.state import AppState
from movie_song_downloader.ui import style
from movie_song_downloader.ui.home import home_view, watchlist_view
from movie_song_downloader.ui.search import search_view
from movie_song_downloader.ui.songs import songs_view
from movie_song_downloader.ui.downloads import downloads_view
from movie_song_downloader.ui.settings import settings_view


def sidebar_nav_button(label: str, icon_name: str, tab_name: str) -> rx.Component:
    """Renders a single button in the sidebar rail."""
    is_active = AppState.active_tab == tab_name
    btn_color = rx.cond(is_active, style.COLOR_ACCENT, style.COLOR_TEXT_MUTED)
    btn_bg = rx.cond(is_active, style.COLOR_BORDER, "transparent")

    return rx.button(
        rx.hstack(
            rx.icon(icon_name, color=btn_color, size=18),
            rx.text(
                label,
                color=rx.cond(
                    is_active, style.COLOR_TEXT_PRIMARY, style.COLOR_TEXT_MUTED
                ),
                font_weight="semibold",
            ),
            align_items="center",
            spacing="3",
        ),
        on_click=AppState.set_tab(tab_name),
        background_color=btn_bg,
        variant="ghost",
        cursor="pointer",
        width="100%",
        justify_content="start",
        padding="12px 16px",
        height="auto",
        _hover={"background_color": style.COLOR_BORDER, "opacity": 0.9},
    )


def sidebar() -> rx.Component:
    """Renders the fixed sidebar navigation."""
    return rx.vstack(
        # App Title/Logo Area
        rx.vstack(
            rx.hstack(
                rx.icon("music-4", color=style.COLOR_ACCENT, size=26),
                rx.heading(
                    "AeroHub Sync",
                    size="5",
                    color=style.COLOR_TEXT_PRIMARY,
                    font_weight="bold",
                ),
                align_items="center",
                spacing="2",
            ),
            rx.text(
                "Song Downloader v2.0", font_size="11px", color=style.COLOR_TEXT_MUTED
            ),
            align_items="start",
            spacing="1",
            margin_bottom="32px",
        ),
        # Navigation Rail Items
        sidebar_nav_button("Home", "home", "home"),
        sidebar_nav_button("Search", "search", "search"),
        sidebar_nav_button("Watchlist", "bookmark", "watchlist"),
        sidebar_nav_button("Downloads", "download", "downloads"),
        sidebar_nav_button("Settings", "settings", "settings"),
        style=style.SIDEBAR_STYLE,
    )


def setup_wizard() -> rx.Component:
    """Renders the welcoming setup wizard modal when OMDb Key is missing."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "Welcome! Quick Setup", color=style.COLOR_ACCENT, font_weight="bold"
            ),
            rx.dialog.description(
                (
                    "Movie details come from Wikipedia & JioSaavn automatically. "
                    "For ratings, cast info, and high-quality Deezer files, "
                    "configure key credentials below."
                ),
                color=style.COLOR_TEXT_MUTED,
                font_size="13px",
            ),
            rx.vstack(
                # OMDb Key input
                rx.vstack(
                    rx.text(
                        "OMDb API Key (Required for ratings & cast)",
                        font_size="12px",
                        font_weight="semibold",
                    ),
                    rx.input(
                        placeholder="Get a free key from omdbapi.com",
                        value=AppState.setup_omdb_key,
                        on_change=AppState.set_setup_omdb_key,
                        type="password",
                        width="100%",
                        background_color="transparent",
                        border=f"1px solid {style.COLOR_BORDER}",
                        color=style.COLOR_TEXT_PRIMARY,
                    ),
                    align_items="start",
                    width="100%",
                    margin_top="12px",
                ),
                # Deezer ARL input
                rx.vstack(
                    rx.text(
                        "Deezer ARL Token (Optional for 320kbps MP3s)",
                        font_size="12px",
                        font_weight="semibold",
                    ),
                    rx.input(
                        placeholder="Paste your Deezer ARL cookie",
                        value=AppState.setup_deezer_arl,
                        on_change=AppState.set_setup_deezer_arl,
                        type="password",
                        width="100%",
                        background_color="transparent",
                        border=f"1px solid {style.COLOR_BORDER}",
                        color=style.COLOR_TEXT_PRIMARY,
                    ),
                    align_items="start",
                    width="100%",
                    margin_top="12px",
                ),
                rx.cond(
                    AppState.setup_status_msg,
                    rx.text(
                        AppState.setup_status_msg,
                        color="#EF4444",
                        font_size="12px",
                        margin_top="8px",
                    ),
                ),
                rx.hstack(
                    rx.button(
                        "Save and Continue",
                        on_click=AppState.save_setup_wizard,
                        background_color=style.COLOR_ACCENT,
                        color=style.COLOR_TEXT_PRIMARY,
                        cursor="pointer",
                        width="100%",
                        margin_top="20px",
                    ),
                    width="100%",
                ),
                width="100%",
            ),
            background_color=style.COLOR_BG_SECONDARY,
            border=f"1px solid {style.COLOR_BORDER}",
        ),
        open=AppState.setup_wizard_open,
    )


def index() -> rx.Component:
    """The root page layout wrapping sidebar and active content views."""
    active_view = rx.cond(
        AppState.show_songs_view,
        songs_view(),
        rx.match(
            AppState.active_tab,
            ("home", home_view()),
            ("search", search_view()),
            ("watchlist", watchlist_view()),
            ("downloads", downloads_view()),
            ("settings", settings_view()),
            home_view(),
        ),
    )

    return rx.hstack(
        sidebar(),
        rx.box(active_view, style=style.CONTENT_STYLE, width="100%"),
        setup_wizard(),
        style=style.BASE_STYLE,
        on_mount=[AppState.on_load, AppState.load_home_data, AppState.start_polling],
    )


# Instantiate Reflex app
app = rx.App(
    style={
        "background_color": style.COLOR_BG_PRIMARY,
        "color": style.COLOR_TEXT_PRIMARY,
    }
)

# Register base route
app.add_page(index, route="/", title="Movie Song Downloader & Sync")

# Compatibility shim: some Starlette versions do not expose decorator helpers
# like `.get()` on the app object. Reflex exposes the underlying Starlette
# app as `app._api`. Provide lightweight `.get/.post` decorators that wrap
# no-arg or async functions and return a JSONResponse for Starlette routes.
try:
    api = app._api
    if not hasattr(api, "get"):
        import inspect
        from starlette.responses import JSONResponse

        def _make_decorator(method):
            def decorator(path):
                def register(fn):
                    async def endpoint(request):
                        if inspect.iscoroutinefunction(fn):
                            result = await fn()
                        else:
                            result = fn()
                        return JSONResponse(result)

                    api.add_route(path, endpoint, methods=[method])
                    return fn

                return register

            return decorator

        api.get = _make_decorator("GET")
        api.post = _make_decorator("POST")
        api.put = _make_decorator("PUT")
        api.delete = _make_decorator("DELETE")
except Exception:
    # If anything goes wrong, skip compatibility shim and let Reflex handle it.
    pass


migration_status = {
    "ok": False,
    "message": "pending",
    "timestamp": None,
}


@app._api.get("/health")
async def health_check():
    return {
        "status": "ok" if migration_status["ok"] else "degraded",
        "migration": migration_status,
    }


@app._api.get("/metrics")
async def metrics():
    active_jobs = 0
    try:
        from movie_song_downloader.core.job_queue import job_queue

        active_jobs = len(await job_queue.get_all_jobs())
    except Exception:
        active_jobs = -1

    return {
        "movie_song_downloader_active_jobs": active_jobs,
        "migration_ok": migration_status["ok"],
    }


@app._api.get("/migration-status")
async def migration_status_endpoint():
    return migration_status


@app._api.get("/run-migrations")
async def run_migrations_endpoint():
    """Trigger database migrations on-demand and return the resulting status."""
    import logging
    logger = logging.getLogger("movie_song_downloader.FastAPI")
    try:
        from movie_song_downloader.core.database import db

        logger.info("Manual migration trigger requested via /run-migrations")
        await db.run_migrations()
        migration_status["ok"] = True
        migration_status["message"] = "migrations applied successfully"
        migration_status["timestamp"] = time.time()
        return {"status": "ok", "migration": migration_status}
    except Exception as e:
        migration_status["ok"] = False
        migration_status["message"] = str(e)
        migration_status["timestamp"] = time.time()
        logger.critical(f"Manual migration failed: {e}", exc_info=True)
        return {"status": "error", "error": str(e)}, 500


@app._api.on_event("startup")
async def startup_event():
    import logging

    logger = logging.getLogger("movie_song_downloader.FastAPI")
    logger.info("Initializing database migrations via FastAPI startup hook...")
    try:
        from movie_song_downloader.core.database import db

        await db.run_migrations()
        migration_status["ok"] = True
        migration_status["message"] = "migrations applied successfully"
        migration_status["timestamp"] = time.time()
        logger.info("Database migrations applied successfully.")
    except Exception as e:
        migration_status["ok"] = False
        migration_status["message"] = str(e)
        migration_status["timestamp"] = time.time()
        logger.critical(
            f"Critical error applying DB migrations: {e}", exc_info=True
        )
        raise

    try:
        from movie_song_downloader.services.download_service import download_service

        logger.info("Starting background download service worker...")
        await download_service.start()
    except Exception as e:
        logger.error(f"Failed to start download service worker: {e}")


@app._api.on_event("shutdown")
async def shutdown_event():
    import logging

    logger = logging.getLogger("movie_song_downloader.FastAPI")
    logger.info(
        "Stopping background download service worker via FastAPI shutdown hook..."
    )
    try:
        from movie_song_downloader.services.download_service import download_service

        await download_service.stop()
    except Exception as e:
        logger.error(f"Error stopping download service worker: {e}")
