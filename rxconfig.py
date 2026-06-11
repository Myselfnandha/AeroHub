import reflex as rx

config = rx.Config(
    app_name="MovieSongDownloader",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.RadixThemesPlugin(),
    ],
)
