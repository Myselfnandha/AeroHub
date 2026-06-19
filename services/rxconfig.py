import reflex as rx

config = rx.Config(
    app_name="movie_song_downloader",
    ignored_paths=[
        "movie_song_downloader/.logs", 
        "movie_song_downloader/.db",
        "movie_song_downloader/.cache",
        "AeroHub.db",
        "**/*.db",
        "**/*.log",
        "**/*.db-journal",
    ],
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.RadixThemesPlugin(),
    ],
)
