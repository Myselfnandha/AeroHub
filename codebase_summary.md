# Codebase Summary: UTILITIES

## Overview
- **Scan Date:** 2026-06-11 15:22:38
- **Source Folder:** `c:\Users\NANDHA A\Desktop\FOLDERS\UTILITIES`
- **Total Text Files:** 403
- **Estimated Token Count:** 214,513

## Directory Tree
```text
UTILITIES/
├── .GEMINI.md
├── .continue/
│   └── agents/
├── .env.example
├── .flake8
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── release.yml
├── .gitignore
├── .pre-commit-config.yaml
├── .ruff.toml
├── Dockerfile
├── Launchers/
│   ├── check_logs.ps1
│   ├── fix_startup.bat
│   ├── install.bat
│   ├── install_aerohub_service.ps1
│   ├── install_elevated_startup.bat
│   ├── reregister_startup.bat
│   ├── run_aerohub.bat
│   ├── run_aerohub.vbs
│   └── uninstall_aerohub_service.ps1
├── Logs/
├── Makefile
├── MusicREADME.md
├── README.md
├── README.scripts.md
├── TgFdmProxy/
├── aerohub_service.ps1
├── analyze.py
├── config/
│   ├── __init__.py
│   ├── app.yaml
│   ├── loader.py
│   └── logging.py
├── dev_run.ps1
├── docker-compose.yml
├── firefox_icon_bg.png
├── prod_run.ps1
├── pytest.ini
├── reflex.lock/
│   ├── bun.lock
│   └── package.json
├── requirements.txt
├── run.ps1
├── run.sh
├── run_app.bat
├── run_app.ps1
├── run_docker.ps1
├── run_utility.ps1
├── rxconfig.py
├── scratch/
│   ├── check_console.py
│   ├── extract_transcript.py
│   ├── extracted/
│   │   ├── step_101_tc_0.json
│   │   ├── step_103_tc_0.json
│   │   ├── step_105_replacement.py
│   │   ├── step_105_tc_0.json
│   │   ├── step_107_tc_0.json
│   │   ├── step_109_tc_0.json
│   │   ├── step_10_tc_0.json
│   │   ├── step_111_tc_0.json
│   │   ├── step_113_tc_0.json
│   │   ├── step_115_tc_0.json
│   │   ├── step_117_tc_0.json
│   │   ├── step_119_tc_0.json
│   │   ├── step_121_replacement.py
│   │   ├── step_121_tc_0.json
│   │   ├── step_123_tc_0.json
│   │   ├── step_125_replacement.py
│   │   ├── step_125_tc_0.json
│   │   ├── step_127_tc_0.json
│   │   ├── step_129_tc_0.json
│   │   ├── step_12_tc_0.json
│   │   ├── step_131_replacement.py
│   │   ├── step_131_tc_0.json
│   │   ├── step_133_tc_0.json
│   │   ├── step_135_replacement.py
│   │   ├── step_135_tc_0.json
│   │   ├── step_137_tc_0.json
│   │   ├── step_139_replacement.py
│   │   ├── step_139_tc_0.json
│   │   ├── step_141_tc_0.json
│   │   ├── step_143_replacement.py
│   │   ├── step_143_tc_0.json
│   │   ├── step_145_tc_0.json
│   │   ├── step_147_tc_0.json
│   │   ├── step_149_replacement.py
│   │   ├── step_149_tc_0.json
│   │   ├── step_14_tc_0.json
│   │   ├── step_164_tc_0.json
│   │   ├── step_166_tc_0.json
│   │   ├── step_168_tc_0.json
│   │   ├── step_170_tc_0.json
│   │   ├── step_184_tc_0.json
│   │   ├── step_186_tc_0.json
│   │   ├── step_188_tc_0.json
│   │   ├── step_18_tc_0.json
│   │   ├── step_190_tc_0.json
│   │   ├── step_192_tc_0.json
│   │   ├── step_194_tc_0.json
│   │   ├── step_196_tc_0.json
│   │   ├── step_198_tc_0.json
│   │   ├── step_202_tc_0.json
│   │   ├── step_204_tc_0.json
│   │   ├── step_20_tc_0.json
│   │   ├── step_212_tc_0.json
│   │   ├── step_214_tc_0.json
│   │   ├── step_216_tc_0.json
│   │   ├── step_22_tc_0.json
│   │   ├── step_230_tc_0.json
│   │   ├── step_232_tc_0.json
│   │   ├── step_234_tc_0.json
│   │   ├── step_238_tc_0.json
│   │   ├── step_240_tc_0.json
│   │   ├── step_242_tc_0.json
│   │   ├── step_244_tc_0.json
│   │   ├── step_246_tc_0.json
│   │   ├── step_248_tc_0.json
│   │   ├── step_250_replacement.py
│   │   ├── step_250_tc_0.json
│   │   ├── step_252_tc_0.json
│   │   ├── step_254_tc_0.json
│   │   ├── step_256_tc_0.json
│   │   ├── step_262_tc_0.json
│   │   ├── step_264_tc_0.json
│   │   ├── step_266_tc_0.json
│   │   ├── step_268_tc_0.json
│   │   ├── step_270_tc_0.json
│   │   ├── step_272_tc_0.json
│   │   ├── step_274_tc_0.json
│   │   ├── step_278_tc_0.json
│   │   ├── step_282_tc_0.json
│   │   ├── step_284_tc_0.json
│   │   ├── step_286_replacement.py
│   │   ├── step_286_tc_0.json
│   │   ├── step_288_tc_0.json
│   │   ├── step_290_replacement.py
│   │   ├── step_290_tc_0.json
│   │   ├── step_292_tc_0.json
│   │   ├── step_294_tc_0.json
│   │   ├── step_296_tc_0.json
│   │   ├── step_298_tc_0.json
│   │   ├── step_300_tc_0.json
│   │   ├── step_302_replacement.py
│   │   ├── step_302_tc_0.json
│   │   ├── step_304_tc_0.json
│   │   ├── step_306_tc_0.json
│   │   ├── step_308_tc_0.json
│   │   ├── step_314_tc_0.json
│   │   ├── step_318_tc_0.json
│   │   ├── step_320_tc_0.json
│   │   ├── step_322_tc_0.json
│   │   ├── step_324_tc_0.json
│   │   ├── step_326_tc_0.json
│   │   ├── step_328_tc_0.json
│   │   ├── step_330_tc_0.json
│   │   ├── step_332_tc_0.json
│   │   ├── step_334_tc_0.json
│   │   ├── step_336_tc_0.json
│   │   ├── step_338_tc_0.json
│   │   ├── step_340_tc_0.json
│   │   ├── step_34_tc_0.json
│   │   ├── step_381_tc_0.json
│   │   ├── step_397_tc_0.json
│   │   ├── step_413_tc_0.json
│   │   ├── step_419_tc_0.json
│   │   ├── step_421_tc_0.json
│   │   ├── step_423_tc_0.json
│   │   ├── step_433_tc_0.json
│   │   ├── step_435_tc_0.json
│   │   ├── step_437_tc_0.json
│   │   ├── step_439_tc_0.json
│   │   ├── step_441_tc_0.json
│   │   ├── step_445_tc_0.json
│   │   ├── step_447_tc_0.json
│   │   ├── step_449_tc_0.json
│   │   ├── step_451_tc_0.json
│   │   ├── step_459_tc_0.json
│   │   ├── step_461_tc_0.json
│   │   ├── step_52_tc_0.json
│   │   ├── step_62_tc_0.json
│   │   ├── step_65_tc_0.json
│   │   ├── step_67_replacement.py
│   │   ├── step_67_tc_0.json
│   │   ├── step_69_tc_0.json
│   │   ├── step_71_tc_0.json
│   │   ├── step_73_replacement.py
│   │   ├── step_73_tc_0.json
│   │   ├── step_75_tc_0.json
│   │   ├── step_77_tc_0.json
│   │   ├── step_79_tc_0.json
│   │   ├── step_81_tc_0.json
│   │   ├── step_83_replacement.py
│   │   ├── step_83_tc_0.json
│   │   ├── step_85_tc_0.json
│   │   ├── step_87_replacement.py
│   │   ├── step_87_tc_0.json
│   │   ├── step_89_tc_0.json
│   │   ├── step_91_tc_0.json
│   │   ├── step_93_replacement.py
│   │   ├── step_93_tc_0.json
│   │   ├── step_95_tc_0.json
│   │   ├── step_97_tc_0.json
│   │   ├── step_99_replacement.py
│   │   └── step_99_tc_0.json
│   ├── find_port_8555.py
│   ├── inspect_filepicker.py
│   ├── inspect_reflex_api.py
│   ├── spotiflac_result_5GeBgck1MU2tlIkMpsn8uT.mp3
│   ├── step74.txt
│   ├── test_aiosqlite.py
│   ├── test_picker.py
│   └── test_startup.py
├── services/
│   ├── .gitignore
│   ├── Logs/
│   ├── MovieSongDownloader/
│   │   ├── .cache/
│   │   │   ├── covers/
│   │   │   │   ├── 2bff74c3b656e868cad90add051f3849.jpg
│   │   │   │   ├── 6aaa0ebe44ba6da5636d7668922f30a3.jpg
│   │   │   │   ├── 751837a9471480ccdd193d4d7c52579d.jpg
│   │   │   │   ├── 87514016310e4d973d3459017483ea84.jpg
│   │   │   │   ├── 89434b36241d6d4e0bb622bc97a14e30.jpg
│   │   │   │   ├── 9fa42e078d9f046b88a73b939d969c01.jpg
│   │   │   │   ├── a0a2ced3a7b581b1750b5aace48761dd.jpg
│   │   │   │   ├── a1f4571e39d2c45fcc5286a85d0a5bdb.jpg
│   │   │   │   ├── a2fab01d124fc8200d1da4c9e1b93322.jpg
│   │   │   │   ├── b8b3a19cbb59dd8b50ed2db145678966.jpg
│   │   │   │   ├── d129f47aca99361800348e80f3f43081.jpg
│   │   │   │   ├── de02becef0e573215643a78a8a43c4e5.jpg
│   │   │   │   └── fbe41fac45fa2bc741c7bdf7c96867a5.jpg
│   │   │   └── posters/
│   │   │       ├── 18366dbb9828d767d53deecca9dbf2fc.jpg
│   │   │       ├── 1b88c20481333dc41e54ce8bcb84d942.jpg
│   │   │       ├── 27f017b6cb308af6a02f2945fb6100b2.jpg
│   │   │       ├── 2b118c951f28dd55353a42a3643480db.jpg
│   │   │       ├── 2e3bead2b8e83f3b5e31f3bbe524c2f2.jpg
│   │   │       ├── 2ea7ab53df30e485e97be0309b1df468.jpg
│   │   │       ├── 444172ad8a2ff48d2bcd6d4600ae60b2.png
│   │   │       ├── 5d9dc28c0cbfc982f3b5e9015b8a288e.jpg
│   │   │       ├── 7268fa1f34b15ba1ee31fe42f98924f7.jpg
│   │   │       ├── 7eed315173d5f0d4c8b1a1907a057cd4.jpg
│   │   │       ├── 818e62caa9ef00b8b9e91370fbbf7516.jpg
│   │   │       ├── 9cb8c883c3342e3c757042172a1acc3f.jpg
│   │   │       └── cc306c9941af5aa9075b792442004803.png
│   │   ├── .logs/
│   │   ├── MovieSongDownloader.py
│   │   ├── Unknown.lrc
│   │   ├── Unknown.mp3
│   │   ├── Unknown.txt
│   │   ├── __init__.py
│   │   ├── bin/
│   │   ├── build_prod.ps1
│   │   ├── build_prod.sh
│   │   ├── cache/
│   │   │   └── temp/
│   │   ├── config.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── cache_manager.py
│   │   │   ├── database.py
│   │   │   ├── dns_resolver.py
│   │   │   ├── event_bus.py
│   │   │   ├── job_queue.py
│   │   │   ├── migrations/
│   │   │   │   ├── 001_initial.sql
│   │   │   │   ├── 002_provider_health.sql
│   │   │   │   ├── 003_cache.sql
│   │   │   │   ├── 004_scraper_sources.sql
│   │   │   │   └── 005_release_date_enrichment.sql
│   │   │   ├── models.py
│   │   │   ├── rate_limiter.py
│   │   │   └── settings_manager.py
│   │   ├── dev_run.ps1
│   │   ├── main.py
│   │   ├── movie.json
│   │   ├── playlist.m3u
│   │   ├── providers/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── deezspot_provider.py
│   │   │   ├── jiosaavn_provider.py
│   │   │   ├── lyrics_provider.py
│   │   │   ├── metadata_normalizer.py
│   │   │   ├── musicbrainz_provider.py
│   │   │   ├── omdb_provider.py
│   │   │   ├── spotiflac_provider.py
│   │   │   ├── spotify_provider.py
│   │   │   ├── tagging_provider.py
│   │   │   ├── wikidata_provider.py
│   │   │   └── wikipedia_provider.py
│   │   ├── requirements.txt
│   │   ├── scripts/
│   │   │   └── run_migrations.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── download_service.py
│   │   │   ├── folder_service.py
│   │   │   ├── movie_service.py
│   │   │   ├── soundtrack_service.py
│   │   │   └── watchlist_service.py
│   │   ├── settings_backup.json
│   │   ├── test_output/
│   │   │   ├── spotiflac_result_1nHTOlxSEyyrLH6wzzMJTd.mp3
│   │   │   └── spotiflac_temp_1nHTOlxSEyyrLH6wzzMJTd/
│   │   │       ├── track1.flac
│   │   │       └── transcoded.mp3
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── conftest.py
│   │   │   ├── test_cache.py
│   │   │   ├── test_cache_verification.py
│   │   │   ├── test_event_bus.py
│   │   │   ├── test_folder_service.py
│   │   │   ├── test_jiosaavn_provider.py
│   │   │   ├── test_job_queue.py
│   │   │   ├── test_lyrics_waterfall.py
│   │   │   ├── test_movie_service.py
│   │   │   ├── test_musicbrainz_provider.py
│   │   │   ├── test_normalizer.py
│   │   │   ├── test_omdb_provider.py
│   │   │   ├── test_spotiflac_provider.py
│   │   │   ├── test_spotify_provider.py
│   │   │   ├── test_wikidata_provider.py
│   │   │   └── test_wikipedia_provider.py
│   │   └── ui/
│   │       ├── __init__.py
│   │       ├── components/
│   │       │   └── __init__.py
│   │       ├── downloads.py
│   │       ├── home.py
│   │       ├── search.py
│   │       ├── settings.py
│   │       ├── songs.py
│   │       ├── state.py
│   │       └── style.py
│   ├── aerohub_core/
│   │   ├── Logs/
│   │   ├── aerohub.py
│   │   ├── aerohub_config.json
│   │   └── remote_control.py
│   ├── clipboard_manager/
│   │   └── ClipboardManager/
│   │       ├── clipboard_manager.py
│   │       ├── config.json
│   │       ├── exports/
│   │       │   ├── clipboard_export_20260526_224114.md
│   │       │   ├── clipboard_export_20260526_224116.md
│   │       │   └── clipboard_export_20260526_224120.md
│   │       └── tests/
│   │           └── test_clipboard_manager.py
│   ├── health_app/
│   │   ├── codebase_summary.md
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── audio.py
│   │   │   ├── constants.py
│   │   │   ├── gamma.py
│   │   │   ├── logger.py
│   │   │   ├── media.py
│   │   │   ├── settings.py
│   │   │   └── utils.py
│   │   ├── health_app.py
│   │   ├── resources/
│   │   │   ├── ambient/
│   │   │   │   ├── campfire.mp3
│   │   │   │   ├── forest.mp3
│   │   │   │   ├── night.mp3
│   │   │   │   ├── ocean.mp3
│   │   │   │   ├── rain.mp3
│   │   │   │   └── waterfall.mp3
│   │   │   ├── breathing_8d.wav
│   │   │   ├── on_pre_break.wav
│   │   │   ├── on_stop_break.wav
│   │   │   └── sounds/
│   │   │       ├── bubble_pop.wav
│   │   │       ├── crystal_bell.wav
│   │   │       ├── cyber_alert.wav
│   │   │       ├── digital_chime.wav
│   │   │       ├── echo_ping.wav
│   │   │       ├── retro_beep.wav
│   │   │       ├── sci_fi_sweep.wav
│   │   │       ├── soft_click.wav
│   │   │       ├── tech_chirp.wav
│   │   │       └── zen_bowl.wav
│   │   ├── settings.json
│   │   ├── test_preview.py
│   │   ├── tests/
│   │   │   └── test_health_app.py
│   │   └── ui/
│   │       ├── __init__.py
│   │       ├── overlay.py
│   │       ├── settings_ui.py
│   │       ├── theme.py
│   │       └── toast.py
│   ├── media_control/
│   │   ├── MediaControl.vbs
│   │   ├── Volume_Control_Taskbar.vbs
│   │   ├── assets/
│   │   │   ├── Screenshot 2026-04-21 220014.png
│   │   │   ├── Screenshot 2026-04-21 222831.png
│   │   │   ├── image.png
│   │   │   └── play-button-icon-flat-style-music-player-vector-illustration-isolated-background-playback-interface-sign-business-concept_157943-45709.avif
│   │   ├── debug_sessions.py
│   │   ├── media_control.py
│   │   ├── patch.py
│   │   ├── reference.png
│   │   ├── requirements.txt
│   │   ├── run_media_control.bat
│   │   ├── test_icon.py
│   │   └── test_pause.py
│   ├── movie_song_downloader/
│   │   ├── .cache/
│   │   │   ├── covers/
│   │   │   │   ├── 2bff74c3b656e868cad90add051f3849.jpg
│   │   │   │   ├── 6aaa0ebe44ba6da5636d7668922f30a3.jpg
│   │   │   │   ├── 751837a9471480ccdd193d4d7c52579d.jpg
│   │   │   │   ├── 87514016310e4d973d3459017483ea84.jpg
│   │   │   │   ├── 89434b36241d6d4e0bb622bc97a14e30.jpg
│   │   │   │   ├── 9fa42e078d9f046b88a73b939d969c01.jpg
│   │   │   │   ├── a0a2ced3a7b581b1750b5aace48761dd.jpg
│   │   │   │   ├── a1f4571e39d2c45fcc5286a85d0a5bdb.jpg
│   │   │   │   ├── a2fab01d124fc8200d1da4c9e1b93322.jpg
│   │   │   │   ├── b8b3a19cbb59dd8b50ed2db145678966.jpg
│   │   │   │   ├── d129f47aca99361800348e80f3f43081.jpg
│   │   │   │   ├── de02becef0e573215643a78a8a43c4e5.jpg
│   │   │   │   └── fbe41fac45fa2bc741c7bdf7c96867a5.jpg
│   │   │   └── posters/
│   │   │       ├── 18366dbb9828d767d53deecca9dbf2fc.jpg
│   │   │       ├── 1b88c20481333dc41e54ce8bcb84d942.jpg
│   │   │       ├── 27f017b6cb308af6a02f2945fb6100b2.jpg
│   │   │       ├── 2b118c951f28dd55353a42a3643480db.jpg
│   │   │       ├── 2e3bead2b8e83f3b5e31f3bbe524c2f2.jpg
│   │   │       ├── 2ea7ab53df30e485e97be0309b1df468.jpg
│   │   │       ├── 444172ad8a2ff48d2bcd6d4600ae60b2.png
│   │   │       ├── 5d9dc28c0cbfc982f3b5e9015b8a288e.jpg
│   │   │       ├── 7268fa1f34b15ba1ee31fe42f98924f7.jpg
│   │   │       ├── 7eed315173d5f0d4c8b1a1907a057cd4.jpg
│   │   │       ├── 818e62caa9ef00b8b9e91370fbbf7516.jpg
│   │   │       ├── 9cb8c883c3342e3c757042172a1acc3f.jpg
│   │   │       └── cc306c9941af5aa9075b792442004803.png
│   │   ├── .logs/
│   │   ├── MovieSongDownloader.py
│   │   ├── Unknown.lrc
│   │   ├── Unknown.mp3
│   │   ├── Unknown.txt
│   │   ├── __init__.py
│   │   ├── bin/
│   │   ├── build_prod.ps1
│   │   ├── build_prod.sh
│   │   ├── cache/
│   │   │   └── temp/
│   │   ├── config.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── cache_manager.py
│   │   │   ├── database.py
│   │   │   ├── dns_resolver.py
│   │   │   ├── event_bus.py
│   │   │   ├── job_queue.py
│   │   │   ├── migrations/
│   │   │   │   ├── 001_initial.sql
│   │   │   │   ├── 002_provider_health.sql
│   │   │   │   ├── 003_cache.sql
│   │   │   │   ├── 004_scraper_sources.sql
│   │   │   │   └── 005_release_date_enrichment.sql
│   │   │   ├── models.py
│   │   │   ├── rate_limiter.py
│   │   │   └── settings_manager.py
│   │   ├── dev_run.ps1
│   │   ├── main.py
│   │   ├── movie.json
│   │   ├── playlist.m3u
│   │   ├── providers/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── deezspot_provider.py
│   │   │   ├── jiosaavn_provider.py
│   │   │   ├── lyrics_provider.py
│   │   │   ├── metadata_normalizer.py
│   │   │   ├── musicbrainz_provider.py
│   │   │   ├── omdb_provider.py
│   │   │   ├── spotiflac_provider.py
│   │   │   ├── spotify_provider.py
│   │   │   ├── tagging_provider.py
│   │   │   ├── wikidata_provider.py
│   │   │   └── wikipedia_provider.py
│   │   ├── requirements.txt
│   │   ├── scripts/
│   │   │   └── run_migrations.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── download_service.py
│   │   │   ├── folder_service.py
│   │   │   ├── movie_service.py
│   │   │   ├── soundtrack_service.py
│   │   │   └── watchlist_service.py
│   │   ├── settings_backup.json
│   │   ├── test_output/
│   │   │   ├── spotiflac_result_1nHTOlxSEyyrLH6wzzMJTd.mp3
│   │   │   └── spotiflac_temp_1nHTOlxSEyyrLH6wzzMJTd/
│   │   │       ├── track1.flac
│   │   │       └── transcoded.mp3
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── conftest.py
│   │   │   ├── test_cache.py
│   │   │   ├── test_cache_verification.py
│   │   │   ├── test_event_bus.py
│   │   │   ├── test_folder_service.py
│   │   │   ├── test_jiosaavn_provider.py
│   │   │   ├── test_job_queue.py
│   │   │   ├── test_lyrics_waterfall.py
│   │   │   ├── test_movie_service.py
│   │   │   ├── test_musicbrainz_provider.py
│   │   │   ├── test_normalizer.py
│   │   │   ├── test_omdb_provider.py
│   │   │   ├── test_spotiflac_provider.py
│   │   │   ├── test_spotify_provider.py
│   │   │   ├── test_wikidata_provider.py
│   │   │   └── test_wikipedia_provider.py
│   │   └── ui/
│   │       ├── __init__.py
│   │       ├── components/
│   │       │   └── __init__.py
│   │       ├── downloads.py
│   │       ├── home.py
│   │       ├── search.py
│   │       ├── settings.py
│   │       ├── songs.py
│   │       ├── state.py
│   │       └── style.py
│   ├── reflex.lock/
│   │   ├── bun.lock
│   │   └── package.json
│   ├── requirements.txt
│   ├── rxconfig.py
│   └── tg_fdm_proxy/
│       └── TgFdmProxy/
│           ├── .env.example
│           ├── Dockerfile
│           ├── docker-compose.yml
│           ├── download_analytics.json
│           ├── install_startup.py
│           ├── tg_fdm_proxy.py
│           └── watchdog.bat
├── system_utils.py
├── task.md
├── test_output/
│   ├── spotiflac_result_1nHTOlxSEyyrLH6wzzMJTd.mp3
│   └── spotiflac_temp_1nHTOlxSEyyrLH6wzzMJTd/
│       ├── track1.flac
│       └── transcoded.mp3
├── tests/
│   ├── test_health_toast.py
│   ├── test_toast.py
│   ├── test_toast_queue.py
│   └── test_ui.py
├── toast_status.json
├── toast_utils.py
├── toggles/
│   ├── battery_monitor/
│   │   ├── battery_monitor.py
│   │   ├── battery_settings_ui.py
│   │   ├── settings.json
│   │   ├── sounds/
│   │   │   ├── mac_connect.wav
│   │   │   └── mac_disconnect.wav
│   │   └── test_battery_monitor.py
│   ├── temp_monitor/
│   │   ├── settings.json
│   │   ├── temp_monitor.py
│   │   └── temp_settings_ui.py
│   └── touch_toggle/
│       ├── TouchToggle.ps1
│       ├── install_touch_toggle_service.ps1
│       ├── run_hidden.vbs
│       ├── touch_settings.json
│       ├── touch_toggle.py
│       └── uninstall_touch_toggle_service.ps1
└── tools/
    └── taskbar_scroll/
        ├── settings.json
        └── taskbar_scroll.py
```

## File Contents

### File: `.GEMINI.md`
- **Path:** `.GEMINI.md`
- **Estimated Tokens:** 3,983
- **mtime:** 1781169078.497

````markdown
---
trigger: always_on
---

# GEMINI.md - Antigravity Kit

> This file defines how the AI behaves in this workspace.

---

## 🛑 STOP: CODEBASE SUMMARY GATE (READ BEFORE ANY MULTI-FILE WORK)

> ⛔ **HARD RULE — ZERO EXCEPTIONS:** You are **FORBIDDEN** from using `view_file` on multiple files to understand a folder. You **MUST** use the codebase summary instead.

**This rule OVERRIDES your default behavior.** Do NOT open files one-by-one. Do NOT use `list_dir` + `view_file` loops. This wastes tokens.

### Trigger Conditions (When This Gate Activates)

This gate activates when the user request involves ANY of these:
- "analyze", "understand", "overview", "explain the codebase"
- "refactor", "restructure", "reorganize"
- Multi-file edits, feature implementation, debugging across files
- Any task where you need to read **2 or more files** in a folder

### Protocol (Execute These Steps IN ORDER)

```
STEP 1: python .agent/scripts/analyze.py <folder> -o <folder>/codebase_summary.md --check
        → Exit 0 = FRESH → Go to Step 3
        → Exit 1 = STALE → Go to Step 2

STEP 2: python .agent/scripts/analyze.py <folder> -o <folder>/codebase_summary.md -y
        (This regenerates the summary)

STEP 3: view_file on <folder>/codebase_summary.md
        (Read ONE file instead of N files. Done.)
```

### Agent Flags

| Flag | Purpose |
|------|---------|
| `-y` | Non-interactive (skip prompts) |
| `--check` | Staleness check (exit 0=fresh, 1=stale) |
| `--summary-only` | Tree + file list only, no code (ultra-compact) |
| `--max-file-tokens N` | Skip files above N tokens (use 5000) |

### Violation Check

❌ **VIOLATION:** Using `view_file` on 3+ files in the same folder without first reading `codebase_summary.md`
❌ **VIOLATION:** Saying "let me check each file" or opening files in a loop
✅ **CORRECT:** Run analyze.py → read summary → then open ONLY specific files you need to edit

> 🔴 **Self-Check:** Before EVERY `view_file` call, ask: "Am I about to open multiple files in the same folder? If YES → use the summary first."

---

## CRITICAL: AGENT & SKILL PROTOCOL (START HERE)

> **MANDATORY:** You MUST read the appropriate agent file and its skills BEFORE performing any implementation. This is the highest priority rule.

### 1. Modular Skill Loading Protocol

Agent activated → Check frontmatter "skills:" → Read SKILL.md (INDEX) → Read specific sections.

- **Selective Reading:** DO NOT read ALL files in a skill folder. Read `SKILL.md` first, then only read sections matching the user's request.
- **Rule Priority:** P0 (GEMINI.md) > P1 (Agent .md) > P2 (SKILL.md). All rules are binding.

### 2. Enforcement Protocol

1. **When agent is activated:**
    - ✅ Activate: Read Rules → Check Frontmatter → Load SKILL.md → Apply All.
2. **Forbidden:** Never skip reading agent rules or skill instructions. "Read → Understand → Apply" is mandatory.

---

## 🧠 THINKING PROTOCOL (INTERNAL REASONING)

> **This governs how you think — not just what you output.**

### The Problem to Eliminate

❌ **Gemini default (FORBIDDEN):**
```
I'm now diving into the specifics of each background loop...
I've just confirmed the toast mapping logic. The simplicity is a relief.
I'm now investigating how to style comboboxes...
I've just had a major breakthrough!
I'm now refining the UI controls...
```
This is **robot diary writing** — narrating every micro-action as if performing for an audience. It is verbose, mechanical, and adds zero value. **Never do this.**

---

### The Standard to Follow

✅ **Claude-style thinking (REQUIRED):**

Think in **conclusions**, not **processes**. Your internal reasoning must be:

| Principle | Rule |
|-----------|------|
| **Short** | Max 3–5 lines of reasoning before acting. If you need more, you're overthinking. |
| **Goal-first** | Start with: *What does this need to accomplish?* |
| **Constraint-aware** | Note the key constraint or tradeoff in one line. |
| **Decisive** | Land on ONE approach. Don't narrate the search. |
| **Silent** | Never announce you are thinking. Just think, then do. |

---

### Thinking Template (Use This)

```
Goal: [one sentence — what must the output achieve]
Constraint: [the key limit — time, API, type, edge case]
Approach: [chosen method + brief reason why]
→ Execute.
```

**Example — implementing a background loop:**
```
Goal: health tip loop that fires every N minutes, skippable when paused
Constraint: needs thread-safe queue for GUI updates, interval from settings
Approach: threading.Timer recursion + gui_queue.put() for toast trigger
→ Execute.
```

---

### Hard Rules

- 🚫 Never write `I'm now...` / `I've just...` / `I'm focusing on...`
- 🚫 Never dramatize discoveries — no `"Major breakthrough!"` or `"This is a relief."`
- 🚫 Never narrate tool reads — just read and apply
- 🚫 Never think out loud for more than 5 lines before producing output
- ✅ Think in code terms, not English diary entries
- ✅ If stuck, state the blocker in ONE line then ask
- ✅ Reasoning should be invisible to the user — only the output matters

---

## 📥 REQUEST CLASSIFIER (STEP 1)

**Before ANY action, classify the request:**

| Request Type     | Trigger Keywords                           | Active Tiers                   | Result                      |
| ---------------- | ------------------------------------------ | ------------------------------ | --------------------------- |
| **QUESTION**     | "what is", "how does", "explain"           | TIER 0 only                    | Text Response               |
| **SURVEY/INTEL** | "analyze", "list files", "overview"        | TIER 0 + Explorer              | Session Intel (No File)     |
| **SIMPLE CODE**  | "fix", "add", "change" (single file)       | TIER 0 + TIER 1 (lite)         | Inline Edit                 |
| **COMPLEX CODE** | "build", "create", "implement", "refactor" | TIER 0 + TIER 1 (full) + Agent | **{task-slug}.md Required** |
| **DESIGN/UI**    | "design", "UI", "page", "dashboard"        | TIER 0 + TIER 1 + Agent        | **{task-slug}.md Required** |
| **SLASH CMD**    | /create, /orchestrate, /debug              | Command-specific flow          | Variable                    |

---

## 🤖 INTELLIGENT AGENT ROUTING (STEP 2 - AUTO)

**ALWAYS ACTIVE: Before responding to ANY request, automatically analyze and select the best agent(s).**

> 🔴 **MANDATORY:** You MUST follow the protocol defined in `@[skills/intelligent-routing]`.

### Auto-Selection Protocol

1. **Analyze (Silent)**: Detect domains (Frontend, Backend, Security, etc.) from user request.
2. **Select Agent(s)**: Choose the most appropriate specialist(s).
3. **Inform User**: Concisely state which expertise is being applied.
4. **Apply**: Generate response using the selected agent's persona and rules.

### Response Format (MANDATORY)

When auto-applying an agent, inform the user:

```markdown
🤖 **Applying knowledge of `@[agent-name]`...**

[Continue with specialized response]
```

**Rules:**

1. **Silent Analysis**: No verbose meta-commentary ("I am analyzing...").
2. **Respect Overrides**: If user mentions `@agent`, use it.
3. **Complex Tasks**: For multi-domain requests, use `orchestrator` and ask Socratic questions first.

### ⚠️ AGENT ROUTING CHECKLIST (MANDATORY BEFORE EVERY CODE/DESIGN RESPONSE)

**Before ANY code or design work, you MUST complete this mental checklist:**

| Step | Check | If Unchecked |
|------|-------|--------------|
| 1 | Did I identify the correct agent for this domain? | → STOP. Analyze request domain first. |
| 2 | Did I READ the agent's `.md` file (or recall its rules)? | → STOP. Open `.agent/agents/{agent}.md` |
| 3 | Did I announce `🤖 Applying knowledge of @[agent]...`? | → STOP. Add announcement before response. |
| 4 | Did I load required skills from agent's frontmatter? | → STOP. Check `skills:` field and read them. |

**Failure Conditions:**

- ❌ Writing code without identifying an agent = **PROTOCOL VIOLATION**
- ❌ Skipping the announcement = **USER CANNOT VERIFY AGENT WAS USED**
- ❌ Ignoring agent-specific rules (e.g., Purple Ban) = **QUALITY FAILURE**

> 🔴 **Self-Check Trigger:** Every time you are about to write code or create UI, ask yourself:
> "Have I completed the Agent Routing Checklist?" If NO → Complete it first.

---

## TIER 0: UNIVERSAL RULES (Always Active)

### 🌐 Language Handling

When user's prompt is NOT in English:

1. **Internally translate** for better comprehension
2. **Respond in user's language** - match their communication
3. **Code comments/variables** remain in English

### 🧹 Clean Code (Global Mandatory)

**ALL code MUST follow `@[skills/clean-code]` rules. No exceptions.**

- **Code**: Concise, direct, no over-engineering. Self-documenting.
- **Testing**: Mandatory. Pyramid (Unit > Int > E2E) + AAA Pattern.
- **Performance**: Measure first. Adhere to 2025 standards (Core Web Vitals).
- **Infra/Safety**: 5-Phase Deployment. Verify secrets security.

### 📁 File Dependency Awareness

**Before modifying ANY file:**

1. Check `CODEBASE.md` → File Dependencies
2. Identify dependent files
3. Update ALL affected files together



### 🗺️ System Map Read

> 🔴 **MANDATORY:** Read `ARCHITECTURE.md` at session start to understand Agents, Skills, and Scripts.

**Path Awareness:**

- Agents: `.agent/` (Project)
- Skills: `.agent/skills/` (Project)
- Runtime Scripts: `.agent/skills/<skill>/scripts/`

### 🧠 Read → Understand → Apply

```
❌ WRONG: Read agent file → Start coding
✅ CORRECT: Read → Understand WHY → Apply PRINCIPLES → Code
```

**Before coding, answer:**

1. What is the GOAL of this agent/skill?
2. What PRINCIPLES must I apply?
3. How does this DIFFER from generic output?

---

## TIER 1: CODE RULES (When Writing Code)

### 📱 Project Type Routing

| Project Type                           | Primary Agent         | Skills                        |
| -------------------------------------- | --------------------- | ----------------------------- |
| **MOBILE** (iOS, Android, RN, Flutter) | `mobile-developer`    | mobile-design                 |
| **WEB** (Next.js, React web)           | `frontend-specialist` | frontend-design               |
| **BACKEND** (API, server, DB)          | `backend-specialist`  | api-patterns, database-design |

> 🔴 **Mobile + frontend-specialist = WRONG.** Mobile = mobile-developer ONLY.

### 🛑 Socratic Gate

**For complex requests, STOP and ASK first:**

### 🛑 GLOBAL SOCRATIC GATE (TIER 0)

**MANDATORY: Every user request must pass through the Socratic Gate before ANY tool use or implementation.**

| Request Type            | Strategy       | Required Action                                                   |
| ----------------------- | -------------- | ----------------------------------------------------------------- |
| **New Feature / Build** | Deep Discovery | ASK minimum 3 strategic questions                                 |
| **Code Edit / Bug Fix** | Context Check  | Confirm understanding + ask impact questions                      |
| **Vague / Simple**      | Clarification  | Ask Purpose, Users, and Scope                                     |
| **Full Orchestration**  | Gatekeeper     | **STOP** subagents until user confirms plan details               |
| **Direct "Proceed"**    | Validation     | **STOP** → Even if answers are given, ask 2 "Edge Case" questions |

**Protocol:**

1. **Never Assume:** If even 1% is unclear, ASK.
2. **Handle Spec-heavy Requests:** When user gives a list (Answers 1, 2, 3...), do NOT skip the gate. Instead, ask about **Trade-offs** or **Edge Cases** (e.g., "LocalStorage confirmed, but should we handle data clearing or versioning?") before starting.
3. **Wait:** Do NOT invoke subagents or write code until the user clears the Gate.
4. **Reference:** Full protocol in `@[skills/brainstorming]`.

### 🏁 Final Checklist Protocol

**Trigger:** When the user says "son kontrolleri yap", "final checks", "çalıştır tüm testleri", or similar phrases.

| Task Stage       | Command                                            | Purpose                        |
| ---------------- | -------------------------------------------------- | ------------------------------ |
| **Manual Audit** | `python .agent/scripts/checklist.py .`             | Priority-based project audit   |
| **Pre-Deploy**   | `python .agent/scripts/checklist.py . --url <URL>` | Full Suite + Performance + E2E |

**Priority Execution Order:**

1. **Security** → 2. **Lint** → 3. **Schema** → 4. **Tests** → 5. **UX** → 6. **Seo** → 7. **Lighthouse/E2E**

**Rules:**

- **Completion:** A task is NOT finished until `checklist.py` returns success.
- **Reporting:** If it fails, fix the **Critical** blockers first (Security/Lint).

**Available Scripts (12 total):**

| Script                     | Skill                 | When to Use         |
| -------------------------- | --------------------- | ------------------- |
| `security_scan.py`         | vulnerability-scanner | Always on deploy    |
| `dependency_analyzer.py`   | vulnerability-scanner | Weekly / Deploy     |
| `lint_runner.py`           | lint-and-validate     | Every code change   |
| `test_runner.py`           | testing-patterns      | After logic change  |
| `schema_validator.py`      | database-design       | After DB change     |
| `ux_audit.py`              | frontend-design       | After UI change     |
| `accessibility_checker.py` | frontend-design       | After UI change     |
| `seo_checker.py`           | seo-fundamentals      | After page change   |
| `bundle_analyzer.py`       | performance-profiling | Before deploy       |
| `mobile_audit.py`          | mobile-design         | After mobile change |
| `lighthouse_audit.py`      | performance-profiling | Before deploy       |
| `playwright_runner.py`     | webapp-testing        | Before deploy       |

> 🔴 **Agents & Skills can invoke ANY script** via `python .agent/skills/<skill>/scripts/<script>.py`

### 🎭 Gemini Mode Mapping

| Mode     | Agent             | Behavior                                     |
| -------- | ----------------- | -------------------------------------------- |
| **plan** | `project-planner` | 4-phase methodology. NO CODE before Phase 4. |
| **ask**  | -                 | Focus on understanding. Ask questions.       |
| **edit** | `orchestrator`    | Execute. Check `{task-slug}.md` first.       |

**Plan Mode (4-Phase):**

1. ANALYSIS → Research, questions
2. PLANNING → `{task-slug}.md`, task breakdown
3. SOLUTIONING → Architecture, design (NO CODE!)
4. IMPLEMENTATION → Code + tests

> 🔴 **Edit mode:** If multi-file or structural change → Offer to create `{task-slug}.md`. For single-file fixes → Proceed directly.

---

## TIER 2: DESIGN RULES (Reference)

> **Design rules are in the specialist agents, NOT here.**

| Task         | Read                            |
| ------------ | ------------------------------- |
| Web UI/UX    | `.agent/frontend-specialist.md` |
| Mobile UI/UX | `.agent/mobile-developer.md`    |

**These agents contain:**

- Purple Ban (no violet/purple colors)
- Template Ban (no standard layouts)
- Anti-cliché rules
- Deep Design Thinking protocol

> 🔴 **For design work:** Open and READ the agent file. Rules are there.

---

## 📁 QUICK REFERENCE

### Agents & Skills

- **Masters**: `orchestrator`, `project-planner`, `security-auditor` (Cyber/Audit), `backend-specialist` (API/DB), `frontend-specialist` (UI/UX), `mobile-developer`, `debugger`, `game-developer`
- **Key Skills**: `clean-code`, `brainstorming`, `app-builder`, `frontend-design`, `mobile-design`, `plan-writing`, `behavioral-modes`

### Key Scripts

- **Verify**: `.agent/scripts/verify_all.py`, `.agent/scripts/checklist.py`
- **Analyze**: `.agent/scripts/analyze.py` (codebase summary generator for token-efficient folder analysis)
- **Scanners**: `security_scan.py`, `dependency_analyzer.py`
- **Audits**: `ux_audit.py`, `mobile_audit.py`, `lighthouse_audit.py`, `seo_checker.py`
- **Test**: `playwright_runner.py`, `test_runner.py`

---
````

---

### File: `.env.example`
- **Path:** `.env.example`
- **Estimated Tokens:** 94
- **mtime:** 1780923522.094

```
# Example environment variables
# Use environment variables or OS secret stores instead of committing secrets.
FLET_WEB_PORT=8555
REFLEX_FRONTEND_PORT=3000
AEROHUB_CONTROL_TOKEN=change-me
SENTRY_DSN=

# MovieSongDownloader provider keys
# OMDB_API_KEY=
# DEEZER_ARL=

# TgFdmProxy secrets should be injected from CI/Docker/OS secret stores.
# API_ID=
# API_HASH=
# BOT_TOKEN=
```

---

### File: `.flake8`
- **Path:** `.flake8`
- **Estimated Tokens:** 24
- **mtime:** 1780861886.648

```
[flake8]
max-line-length = 120
exclude = .agent, scratch, scratch/extracted
extend-ignore = E203
```

---

### File: `.github/workflows/ci.yml`
- **Path:** `.github/workflows/ci.yml`
- **Estimated Tokens:** 434
- **mtime:** 1780923522.093

```yaml
name: CI
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  lint:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.11, 3.12]
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run pre-commit
        run: |
          python -m pip install pre-commit
          pre-commit run --all-files
      - name: Lint
        run: flake8 --max-line-length=120 --exclude=.agent,scratch

  test:
    runs-on: windows-latest
    strategy:
      matrix:
        python-version: [3.12]
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Compile Python
        run: |
          python -m py_compile $(Get-ChildItem -Recurse -Filter *.py | ForEach-Object { $_.FullName })
      - name: Run tests
        run: pytest -q

  docker-build:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker image
        run: docker build -t moviesongdownloader:latest .
      - name: Save build files
        uses: actions/upload-artifact@v4
        with:
          name: docker-build-files
          path: |
            Dockerfile
            docker-compose.yml
```

---

### File: `.github/workflows/release.yml`
- **Path:** `.github/workflows/release.yml`
- **Estimated Tokens:** 324
- **mtime:** 1780923522.093

```yaml
name: Release
on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.12
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: pytest -q
      - name: Build Docker image
        run: docker build -t moviesongdownloader:${{ github.ref_name }} .
      - name: Upload release artifact
        uses: actions/upload-artifact@v4
        with:
          name: moviesongdownloader-archive
          path: |
            ./Dockerfile
            ./docker-compose.yml
            ./requirements.txt
            ./MovieSongDownloader/**
      - name: Push Docker image (optional)
        if: github.event_name == 'push' && github.ref_type == 'tag' && secrets.DOCKERHUB_USERNAME && secrets.DOCKERHUB_TOKEN
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: ${{ secrets.DOCKERHUB_USERNAME }}/moviesongdownloader:${{ github.ref_name }}
          registry: docker.io
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
```

---

### File: `.gitignore`
- **Path:** `.gitignore`
- **Estimated Tokens:** 72
- **mtime:** 1780574296.842

```
.states
assets/external/
.web
# Agent / IDE
.agent/
.agentignore
.understand-anything/

# Python
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
dist/
build/

# Runtime artifacts
*.log
*.session
*.session.backup
*.db

# Secrets
.env

# Build artifacts
*.exe
*.spec

# OS
Thumbs.db
desktop.ini
```

---

### File: `.pre-commit-config.yaml`
- **Path:** `.pre-commit-config.yaml`
- **Estimated Tokens:** 133
- **mtime:** 1780923522.093

```yaml
repos:
-   repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
    - id: black
      language_version: python3.12
-   repo: https://github.com/PyCQA/isort
    rev: 5.13.0
    hooks:
    - id: isort
      name: isort (python)
-   repo: https://gitlab.com/pycqa/flake8
    rev: 6.0.0
    hooks:
    - id: flake8
      name: flake8
      additional_dependencies: [flake8==6.0.0]
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
    - id: check-added-large-files
      args: ["--maxkb=500"]
```

---

### File: `.ruff.toml`
- **Path:** `.ruff.toml`
- **Estimated Tokens:** 7
- **mtime:** 1780754192.842

```toml
extend-exclude = ["scratch"]
```

---

### File: `Dockerfile`
- **Path:** `Dockerfile`
- **Estimated Tokens:** 173
- **mtime:** 1780923522.103

```dockerfile
# Multi-stage Dockerfile for MovieSongDownloader
FROM python:3.12-slim AS builder
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential ffmpeg curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt
COPY . .
RUN python -m compileall MovieSongDownloader

FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY --from=builder /install /usr/local
COPY --from=builder /app /app
EXPOSE 8555
ENTRYPOINT ["python", "MovieSongDownloader/main.py", "--env", "prod"]
```

---

### File: `Launchers/check_logs.ps1`
- **Path:** `Launchers/check_logs.ps1`
- **Estimated Tokens:** 82
- **mtime:** 1780135489.634

```powershell
$events = Get-WinEvent -FilterHashtable @{LogName='Application'; ProviderName='Application Error'} -MaxEvents 5 -ErrorAction SilentlyContinue
if ($events) {
    $events | Where-Object { $_.Message -match 'explorer.exe' } | Select-Object TimeCreated, Message | Format-List
} else {
    Write-Output "No application errors found."
}
```

---

### File: `Launchers/fix_startup.bat`
- **Path:** `Launchers/fix_startup.bat`
- **Estimated Tokens:** 474
- **mtime:** 1781085421.897

```
@echo off
title AeroHub - Fix Startup Task
echo.
echo  [36m╔══════════════════════════════════════════════╗[0m
echo  [36m║      AeroHub Startup Fix                    ║[0m
echo  [36m╚══════════════════════════════════════════════╝[0m
echo.

:: Check for admin
NET SESSION >nul 2>&1
if %errorLevel% == 0 (
    echo  [32m✓[0m Administrative permissions confirmed.
) else (
    echo  [31m✗[0m Please right-click this file and select "Run as administrator".
    pause
    exit /b
)

:: Derive VBS path from this script's location
set "VBS_PATH=%~dp0run_aerohub.vbs"

echo.
echo  [33m[1/3][0m Removing broken scheduled task...
schtasks /delete /tn "AeroHub_ElevatedStartup" /f >nul 2>&1
echo  [32m✓[0m Old task removed.

echo.
echo  [33m[2/3][0m Creating fixed scheduled task...
echo        Using: %VBS_PATH%
powershell -NoProfile -Command "$arg = [char]34 + '%VBS_PATH%' + [char]34; $action = New-ScheduledTaskAction -Execute 'wscript.exe' -Argument $arg; $trigger = New-ScheduledTaskTrigger -AtLogOn; $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit 0; $principal = New-ScheduledTaskPrincipal -UserId '%USERNAME%' -LogonType Interactive -RunLevel Highest; $task = New-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -Principal $principal; Register-ScheduledTask -TaskName 'AeroHub_ElevatedStartup' -InputObject $task -Force"

if %errorLevel% == 0 (
    echo.
    echo  [32m✓[0m Task created successfully!
) else (
    echo.
    echo  [31m✗[0m Failed to create task.
    pause
    exit /b
)

echo.
echo  [33m[3/3][0m Verifying...
schtasks /query /tn "AeroHub_ElevatedStartup" /fo LIST | findstr "Task To Run"
echo.
echo  [32m════════════════════════════════════════════════[0m
echo  [32m  ✓ FIXED! AeroHub will start on next login.  [0m
echo  [32m════════════════════════════════════════════════[0m
echo.
pause
exit
```

---

### File: `Launchers/install.bat`
- **Path:** `Launchers/install.bat`
- **Estimated Tokens:** 366
- **mtime:** 1781116280.34

```
@echo off
title AeroHub - Install Dependencies
echo.
echo  [36m╔══════════════════════════════════════════════╗[0m
echo  [36m║        AeroHub Utilities Suite Setup         ║[0m
echo  [36m╚══════════════════════════════════════════════╝[0m
echo.

echo  [33m[1/2][0m Installing Python dependencies...
echo.
pip install -r requirements.txt
echo.

echo  [33m[2/2][0m Creating directory structure...
if not exist "Logs" mkdir "Logs"
if not exist "services\clipboard_manager\exports" mkdir "services\clipboard_manager\exports"
if not exist "services\health_app\resources\ambient" mkdir "services\health_app\resources\ambient"
if not exist "toggles\battery_monitor\sounds" mkdir "toggles\battery_monitor\sounds"
if not exist "services\media_control\assets" mkdir "services\media_control\assets"

echo.
echo  [32m✓ Installation complete![0m
echo.
echo  To start AeroHub, run:
echo    [36mLaunchers\run_aerohub.bat[0m
echo.
echo  Or run individual utilities directly:
echo    python services\aerohub_core\aerohub.py
echo    python services\clipboard_manager\clipboard_manager.py
echo    python services\health_app\health_app.py
echo    python services\media_control\media_control.py
echo    python toggles\battery_monitor\battery_monitor.py
echo    python toggles\temp_monitor\temp_monitor.py
echo    python toggles\touch_toggle\touch_toggle.py
echo    python services\tg_fdm_proxy\TgFdmProxy\tg_fdm_proxy.py
echo    python tools\taskbar_scroll\taskbar_scroll.py
echo.
pause
```

---

### File: `Launchers/install_aerohub_service.ps1`
- **Path:** `Launchers/install_aerohub_service.ps1`
- **Estimated Tokens:** 206
- **mtime:** 1781116253.136

```powershell
param(
    [string]$TaskName = "AeroHub Core",
    [string]$PythonExecutable = "python"
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$scriptPath = Join-Path $root "..\services\aerohub_core\aerohub.py"
$action = New-ScheduledTaskAction -Execute $PythonExecutable -Argument "`"$scriptPath`" --service"
$trigger = New-ScheduledTaskTrigger -AtLogOn
$principal = New-ScheduledTaskPrincipal -UserId "NT AUTHORITY\SYSTEM" -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

try {
    Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force
    Write-Host "Installed scheduled task: $TaskName"
} catch {
    Write-Error "Failed to install service task: $_"
    exit 1
}
```

---

### File: `Launchers/install_elevated_startup.bat`
- **Path:** `Launchers/install_elevated_startup.bat`
- **Estimated Tokens:** 396
- **mtime:** 1781085434.546

```
@echo off
title AeroHub Silent Elevated Startup Setup
NET SESSION >nul 2>&1
if %errorLevel% == 0 (
    echo Administrative permissions confirmed.
) else (
    echo Please right-click this file and select "Run as administrator".
    pause
    exit /b
)

set TASKNAME=AeroHub_ElevatedStartup
set "VBS_PATH=%~dp0run_aerohub.vbs"

echo Removing old scheduled task if exists...
schtasks /delete /tn "%TASKNAME%" /f >nul 2>&1

echo Creating new elevated logon scheduled task...
echo Using: %VBS_PATH%
:: Create the task in powershell to ensure battery restrictions are disabled
powershell -NoProfile -Command "$arg = [char]34 + '%VBS_PATH%' + [char]34; $action = New-ScheduledTaskAction -Execute 'wscript.exe' -Argument $arg; $trigger = New-ScheduledTaskTrigger -AtLogOn; $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit 0; $principal = New-ScheduledTaskPrincipal -UserId '%USERNAME%' -LogonType Interactive -RunLevel Highest; $task = New-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -Principal $principal; Register-ScheduledTask -TaskName '%TASKNAME%' -InputObject $task -Force"

if %errorLevel% == 0 (
    echo.
    echo ========================================================
    echo SUCCESS: AeroHub is now set to start silently as Admin!
    echo ========================================================
    echo Starting AeroHub now...
    schtasks /run /tn "%TASKNAME%"
    echo.
    echo You can close this window now.
) else (
    echo.
    echo FAILED to create scheduled task.
)
pause
exit
```

---

### File: `Launchers/reregister_startup.bat`
- **Path:** `Launchers/reregister_startup.bat`
- **Estimated Tokens:** 389
- **mtime:** 1781085451.901

```
@echo off
title AeroHub - Re-register Startup Task
echo.
echo  [36m  AeroHub Startup Task Fix[0m
echo.

:: Check for admin
NET SESSION >nul 2>&1
if %errorLevel% == 0 (
    echo  [32m✓[0m Admin confirmed.
) else (
    echo  [31m✗[0m Need admin. Re-launching elevated...
    powershell -Command "Start-Process cmd -ArgumentList '/c \"%~f0\"' -Verb RunAs"
    exit /b
)

:: Derive VBS path from this script's location
set "VBS_PATH=%~dp0run_aerohub.vbs"

echo.
echo  [33m[1/2][0m Removing old task...
schtasks /delete /tn "AeroHub_ElevatedStartup" /f >nul 2>&1
echo  [32m✓[0m Done.

echo.
echo  [33m[2/2][0m Creating task with path: %VBS_PATH%
powershell -NoProfile -Command "$arg = [char]34 + '%VBS_PATH%' + [char]34; $action = New-ScheduledTaskAction -Execute 'wscript.exe' -Argument $arg; $trigger = New-ScheduledTaskTrigger -AtLogOn; $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit 0; $principal = New-ScheduledTaskPrincipal -UserId '%USERNAME%' -LogonType Interactive -RunLevel Highest; $task = New-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -Principal $principal; Register-ScheduledTask -TaskName 'AeroHub_ElevatedStartup' -InputObject $task -Force"

if %errorLevel% == 0 (
    echo.
    echo  [32m✓ Task registered! AeroHub will auto-start on next login.[0m
    echo.
    echo  Starting AeroHub now...
    schtasks /run /tn "AeroHub_ElevatedStartup"
    echo  [32m✓ AeroHub launched.[0m
) else (
    echo.
    echo  [31m✗ Failed to register task.[0m
)
echo.
pause
```

---

### File: `Launchers/run_aerohub.bat`
- **Path:** `Launchers/run_aerohub.bat`
- **Estimated Tokens:** 21
- **mtime:** 1781116262.899

```
@echo off
cd /d "%~dp0\.."
start "" /B pythonw services\aerohub_core\aerohub.py
exit
```

---

### File: `Launchers/run_aerohub.vbs`
- **Path:** `Launchers/run_aerohub.vbs`
- **Estimated Tokens:** 272
- **mtime:** 1781116270.706

```
Set FSO = CreateObject("Scripting.FileSystemObject")
Set WshShell = CreateObject("WScript.Shell")

' Derive paths from this script's location
LaunchersDir = FSO.GetParentFolderName(WScript.ScriptFullName)
UtilitiesDir = FSO.GetParentFolderName(LaunchersDir)

' Find pythonw.exe — prefer the one next to current python
PythonwExe = ""
' Try common locations
Dim candidates
candidates = Array( _
    WshShell.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Programs\Python\Python312\pythonw.exe", _
    WshShell.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Programs\Python\Python313\pythonw.exe", _
    WshShell.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Programs\Python\Python311\pythonw.exe" _
)

For Each p In candidates
    If FSO.FileExists(p) Then
        PythonwExe = p
        Exit For
    End If
Next

' Fallback: just use pythonw from PATH
If PythonwExe = "" Then PythonwExe = "pythonw.exe"

AeroHubScript = UtilitiesDir & "\services\aerohub_core\aerohub.py"

WshShell.CurrentDirectory = UtilitiesDir
WshShell.Run """" & PythonwExe & """ """ & AeroHubScript & """", 0, False
```

---

### File: `Launchers/uninstall_aerohub_service.ps1`
- **Path:** `Launchers/uninstall_aerohub_service.ps1`
- **Estimated Tokens:** 61
- **mtime:** 1780923522.093

```powershell
param(
    [string]$TaskName = "AeroHub Core"
)

try {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "Removed scheduled task: $TaskName"
} catch {
    Write-Warning "Could not remove task. It may not exist: $_"
}
```

---

### File: `Makefile`
- **Path:** `Makefile`
- **Estimated Tokens:** 226
- **mtime:** 1781116243.402

```
# Makefile — common developer tasks
.PHONY: lint test precommit run-dev run-prod build docker-build service-install service-uninstall

lint:
	flake8 --max-line-length=120 --exclude=.agent,scratch

precommit:
	python -m pip install pre-commit
	pre-commit run --all-files

test:
	python -m py_compile $(shell git ls-files '*.py') && pytest -q

run-dev:
	powershell -File dev_run.ps1

run-prod:
	powershell -File prod_run.ps1

build:
	powershell -File services\movie_song_downloader\build_prod.ps1

docker-build:
	docker build -t moviesongdownloader:latest .

service-install:
	powershell -File Launchers\install_aerohub_service.ps1

service-uninstall:
	powershell -File Launchers\uninstall_aerohub_service.ps1

service-install-touch:
	powershell -File toggles\touch_toggle\install_touch_toggle_service.ps1

service-uninstall-touch:
	powershell -File toggles\touch_toggle\uninstall_touch_toggle_service.ps1
```

---

### File: `README.md`
- **Path:** `README.md`
- **Estimated Tokens:** 4,431
- **mtime:** 1780923522.099

````markdown
<div align="center">

# AeroHub

**The Ultimate Windows Automation & Wellness Suite**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Windows 10/11](https://img.shields.io/badge/Windows-10%20%7C%2011-0078d4?style=for-the-badge&logo=windows&logoColor=white)](https://microsoft.com)
[![License](https://img.shields.io/badge/License-Private-444?style=for-the-badge)](.)
[![Status](https://img.shields.io/badge/Status-Active-00ff88?style=for-the-badge)](.)

A highly modular suite of **8 background daemons, system tray utilities, and productivity toggles** — all orchestrated through a central headless System Tray Hub with a floating dashboard widget.

</div>

---

## Architecture

AeroHub follows a **hub-and-spoke** architecture. The central orchestrator (`AeroHub_Core`) manages the lifecycle of every child utility — starting, stopping, health-monitoring, and auto-restarting crashed processes.

```
AeroHub_Core (Orchestrator)
│
├── ClipboardManager ─── Background clipboard history with SQLite + GUI
├── HealthApp ────────── Eye break reminders, 8D audio, weather-based display warmth
├── MediaControl ─────── System-wide tray media controls (Prev │ Play/Pause │ Next)
├── BatteryMonitor ───── macOS-style charge/discharge toast notifications
├── TempMonitor ──────── CPU/GPU thermal monitoring with color-coded tray icon
├── TouchToggle ──────── One-click touchscreen enable/disable via tray
├── TgFdmProxy ──────── Telegram → Download Manager bridge (FDM / IDM / Neat)
└── TaskbarScroll ────── Scroll-wheel volume control on the Windows taskbar
```

### Developer Quickstart

- Install Python 3.12+ and add it to `PATH`
- Create a local `.env` from `.env.example`
- Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

- Run in development mode:

```powershell
./run.ps1 --env dev --port 8555
```

- Run in production mode:

```powershell
./run.ps1 --env prod --port 8555
```

- Run a utility with a consistent wrapper:

```powershell
./run_utility.ps1 --name BatteryMonitor
```

- Install AeroHub as a Windows service wrapper:

```powershell
./Launchers/install_aerohub_service.ps1
```

- Run AeroHub headless/service mode:

```powershell
python AeroHub_Core/aerohub.py --service
```

- Perform a self-update from git and restart AeroHub:

```powershell
python AeroHub_Core/aerohub.py --self-update
```

- Install TouchToggle startup service:

```powershell
./TouchToggle/install_touch_toggle_service.ps1
```

- Or install/uninstall from the Makefile:

```powershell
make service-install-touch
make service-uninstall-touch
```

- Local control API:

  - `GET http://127.0.0.1:8200/health`
  - `GET http://127.0.0.1:8200/status`
  - `GET http://127.0.0.1:8200/metrics`
  - `GET http://127.0.0.1:8200/control?action=start&service=<id>`
  - `GET http://127.0.0.1:8200/self-update`

  Use `X-Local-Token: <token>` or `?token=<token>` when `control_token` is configured.

- Validate formatting and linting:

```powershell
make precommit
make lint
```

- Run tests:

```powershell
make test
```

### Key Design Decisions

| Decision | Rationale |
|---|---|
| **Per-utility `pythonw.exe` hardlinks** | Each tray icon gets its own unique process name so Windows groups them correctly in the system tray |
| **Native Win32 `DwmSetWindowAttribute`** | All GUI windows use DWM rounded corners on Windows 11 (DWMWA_WINDOW_CORNER_PREFERENCE = 33) |
| **UDP IPC for game mode** | AeroHub Core sends lightweight UDP packets to child services to pause/resume during fullscreen gaming |
| **Rotated log files** | Every module writes to `Logs/` with `RotatingFileHandler` (2–5 MB cap, 2–3 backups) — no log bloat |
| **Unique AppUserModelIDs** | Each process calls `SetCurrentProcessExplicitAppUserModelID` so Windows identifies each tray icon separately |

---

## Modules

### 1. AeroHub Core — The Orchestrator

> `AeroHub_Core/aerohub.py` · ~1120 lines

The nerve center. Runs in the background with a **system tray icon** and a **draggable floating dashboard widget** in the desktop corner.

- **Lifecycle Manager** — Auto-starts configured processes, monitors health every 3 seconds, auto-restarts crashes after a configurable delay
- **Floating Dashboard** — Shows each process name, status dot (●), uptime, toggle (▶/■), and restart (↻) buttons
- **AeroEco Game Mode** — Detects fullscreen/DirectX games via `SHQueryUserNotificationState` and foreground window analysis:
  - **Pauses TempMonitor** completely during gameplay
  - **Restricts HealthApp** to `IDLE` priority, disabling heavy UI/audio calls
  - Resumes all services after game exits with hysteresis (15s cooldown)
- **Config-driven** — `aerohub_config.json` defines all managed processes with `auto_start` and `enabled` flags

---

### 2. Clipboard Manager

> `ClipboardManager/clipboard_manager.py` · ~924 lines

A full-featured clipboard history tracker with persistent storage and a searchable GUI.

- **Win32 Clipboard Listener** — Uses `WM_CLIPBOARDUPDATE` via a hidden window (64-bit safe `WNDPROC` ctypes definitions)
- **SQLite Storage** — Unlimited history with MD5 deduplication against the last entry
- **Searchable GUI** — Split-pane layout with list + preview, right-click context menu, double-click to re-copy
- **Auto-Export** — When entries exceed a configurable threshold (default 1000), the oldest batch is exported to Markdown and pruned
- **Settings Window** — Configurable max entries, export batch size, and auto-export toggle

---

### 3. Health App — Eye Break Reminder

> `HealthApp/health_app.py` · ~1688 lines

A premium desktop wellness companion with configurable break schedules, fullscreen lock overlays, and ambient audio.

- **Break Schedule** — Configurable short breaks (default 20min/15s) and long breaks (60min/60s)
- **Pre-Break Warning Toast** — Animated slide-in notification with customizable position, colors, fonts, border, and animation style (slide or fade)
- **Full-Screen Break Overlay** — Black overlay on all monitors with countdown timer, breathing text animation, and forced focus keeping
- **8D Spatial Audio** — Procedurally generates a stereo WAV with breathing-like tones and binaural panning effect. Also supports random ambient tracks from `resources/ambient/`
- **Media-Aware** — Pauses active media sessions via Windows SDK (`GlobalSystemMediaTransportControlsSessionManager`) before breaks and resumes them after. Falls back to global `VK_MEDIA_PLAY_PAUSE` key
- **Weather-Based Display Warmth** — Fetches weather from Open-Meteo API, applies color temperature via Windows gamma ramps (`SetDeviceGammaRamp`). Dynamic Kelvin adjustment based on sunset/sunrise and ambient temperature
- **Late-Night Dimming** — Gradual screen brightness reduction during configurable night hours
- **Workstation Lock Detection** — Skips breaks when the workstation is locked (`OpenInputDesktop`)
- **Settings GUI** — Full tkinter settings panel for break intervals, sound, dimming, weather coordinates, and toast appearance

---

### 4. Media Control

> `MediaControl/media_control.py` · ~886 lines

System-wide media playback controls running as three separate **Win32 notification area icons** in the taskbar.

- **3 Tray Icons** — Previous │ Play/Pause │ Next, each as an independent system tray icon with click-to-action
- **Windows SDK Integration** — Uses `winsdk.windows.media.control.SessionManager` for real-time playback status detection and per-session control
- **Dynamic Play/Pause State** — Icon automatically switches between ▶ and ⏸ based on active playback status
- **Click Animation** — Press-and-release visual feedback with 120ms revert timing
- **Theme-Aware** — Detects Windows light/dark mode + accent color via registry, regenerates all icons on theme change
- **Pycaw Fallback** — For media players that don't register SMTC sessions (VLC, MPC-HC, iTunes), falls back to pycaw audio session enumeration
- **Smart Multi-Session** — Deduplicates sessions by app ID, pauses all when multiple are playing

---

### 5. Battery Monitor

> `BatteryMonitor/battery_monitor.py` · ~662 lines

macOS-style charging notifications for Windows laptops.

- **Plug/Unplug Detection** — Plays custom WAV sound effects (`mac_connect.wav` / `mac_disconnect.wav`) on charger state change
- **Animated Toast Notifications** — macOS-style slide-in toasts with rounded corners, icon background, close-on-hover, and auto-dismiss. Multiple toasts stack vertically
- **Threshold Alerts** — Configurable low battery warning (default 20%) and full charge alert (default 93%)
- **Theme-Aware Tray Icon** — Battery-shaped icon with fill level, color coding (green=charging, gray=discharging, red=low), and a lightning bolt overlay when plugged in. Adapts to Windows light/dark theme
- **Settings GUI** — Configurable thresholds and sound toggle

---

### 6. Temperature Monitor

> `TempMonitor/temp_monitor.py` · ~911 lines

CPU/GPU thermal monitoring with a live temperature display in the system tray.

- **Multi-Backend Reader**:
  1. **LibreHardwareMonitor** — Primary. Uses pythonnet to load `LibreHardwareMonitorLib.dll` for accurate CPU, GPU, SSD, and motherboard readings
  2. **WMI** — Fallback. Reads `MSAcpi_ThermalZoneTemperature` or `OpenHardwareMonitor` WMI namespace
  3. **Simulated** — Final fallback with sine-wave oscillating dummy data for display testing
- **Color-Coded Tray Icon** — Displays temperature as a number on a colored rounded rectangle (green < 60°C, yellow < 75°C, orange < 85°C, red ≥ 85°C)
- **Temperature Alerts** — Warning and critical toast notifications with flashing animation for critical severity
- **Dynamic Tooltip** — Shows all detected sensor temperatures in the tray hover tooltip with intelligent sensor name shortening
- **Sensor Selection Menu** — Right-click menu lets you pick which sensor drives the tray icon display
- **Settings GUI** — Configurable warning/critical temperature thresholds

---

### 7. Touch Toggle

> `TouchToggle/touch_toggle.py` · ~506 lines

Instantly enables or disables the laptop touchscreen from the system tray.

- **One-Click Toggle** — Left-click the tray icon to toggle the HID touch screen device
- **Elevated Execution** — Runs `TouchToggle.ps1` via `ShellExecuteExW` with `runas` verb for proper UAC elevation (no extra console window)
- **State Detection** — Queries `Get-PnpDevice -Class 'HIDClass'` to determine current touch screen status
- **Toast FX Customization** — Sleek animated toast notifications (Slide/Fade) indicating the touchscreen status, with full control over colors, sizing, corner rounding, and border strokes.
- **Settings GUI** — Dedicated Tkinter dashboard to customize the toast appearance and preview animations in real-time.
- **Visual Feedback** — Green circle (ON) / Red circle (OFF) tray icon indicating the system state.

---

### 8. Telegram FDM Proxy

> `TgFdmProxy/tg_fdm_proxy.py` · ~2166 lines

A Telegram bot that bridges file messages to your installed download manager (FDM, IDM, or Neat DM).

- **Multi-Manager Support** — Auto-detects installed download managers via Windows Registry → `where.exe` → hardcoded fallback paths. Priority: FDM → IDM → Neat DM
- **HTTP Range Proxy** — Runs a local `aiohttp` server that streams Telegram media chunks, supporting HTTP Range headers for multi-threaded downloading
- **Parallel Chunk Downloader** — Optional parallel download mode with configurable concurrency and retry logic
- **Smart Auto-Rename** — Cleans raw filenames into `Title (Year) [Resolution].ext` format, stripping codec/audio/source noise
- **Quality Variant Selection** — Waits for multiple quality variants (configurable delay) before picking the best
- **Keyword Filters** — Block/allow lists for automated content filtering
- **Duplicate Guard** — Tracks `(chat_id, message_id)` with TTL to prevent re-triggering
- **Interactive Setup** — First-run wizard prompts for API_ID, API_HASH, and BOT_TOKEN
- **Live Event Dashboard** — In-memory structured event log with a GUI log viewer
- **Docker Support** — Includes `Dockerfile` and `docker-compose.yml`

---

### 9. Taskbar Scroll Controller

> `TaskbarScroll/taskbar_scroll.py` · ~222 lines

Scroll-wheel volume control when hovering over the Windows taskbar.

- **Taskbar Detection** — Identifies `Shell_TrayWnd` and `Shell_SecondaryTrayWnd` window classes using `WindowFromPoint` with DPI-aware cursor coordinates
- **Configurable** — Invert scroll direction and volume step multiplier via settings GUI
- **Singleton Guard** — Uses a Windows named mutex to prevent duplicate instances
- **Settings GUI** — AeroHub-themed settings window with DWM rounded corners

---

## Directory Structure

```
UTILITIES/
├── AeroHub_Core/           # Central orchestrator
│   ├── aerohub.py
│   └── aerohub_config.json
├── ClipboardManager/       # Clipboard history daemon
│   ├── clipboard_manager.py
│   ├── clipboard_history.db
│   ├── config.json
│   └── exports/
├── HealthApp/              # Eye break & wellness
│   ├── health_app.py
│   ├── settings.json
│   ├── breathing_8d.wav
│   └── resources/
│       ├── ambient/        # Break audio tracks
│       ├── on_pre_break.wav
│       └── on_stop_break.wav
├── MediaControl/           # Tray media controls
│   ├── media_control.py
│   ├── assets/
│   └── requirements.txt
├── BatteryMonitor/         # Battery notifications
│   ├── battery_monitor.py
│   ├── settings.json
│   └── sounds/             # mac_connect.wav, mac_disconnect.wav
├── TempMonitor/            # Thermal monitoring
│   └── temp_monitor.py
├── TouchToggle/            # Touchscreen toggle
│   ├── touch_toggle.py
│   ├── touch_settings.json
│   ├── TouchToggle.ps1
│   ├── TouchToggle.exe
│   └── tooltip_notifier.py
├── TgFdmProxy/             # Telegram download bridge
│   ├── tg_fdm_proxy.py
│   ├── .env
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── tg_fdm_proxy.exe
├── TaskbarScroll/          # Volume scroll control
│   ├── taskbar_scroll.py
│   └── settings.json
├── Launchers/              # Setup & startup scripts
│   ├── install.bat
│   ├── install_elevated_startup.bat
│   ├── run_aerohub.bat
│   ├── run_aerohub.vbs
│   └── check_logs.ps1
├── Logs/                   # Centralized rotating logs
├── services/               # Runtime data (sessions, DBs)
└── requirements.txt        # Python dependencies
```

---

## Installation

### Prerequisites

- **Python 3.10+** — must be on your System `PATH`
- **Windows 10 / 11**
- **pip** — included with Python

### Quick Start

```cmd
:: 1. Clone the repository
git clone https://github.com/Myselfnandha/AeroHub.git
cd AeroHub

:: 2. Install dependencies
Launchers\install.bat

:: 3. Launch AeroHub
Launchers\run_aerohub.bat
```

### Silent Startup (Administrator)

To configure AeroHub to start **automatically and silently** as Administrator on system logon (bypasses UAC prompts via Windows Task Scheduler):

```cmd
:: Right-click → Run as Administrator
Launchers\install_elevated_startup.bat
```

This creates a scheduled task (`AeroHub_ElevatedStartup`) that runs `run_aerohub.vbs` at logon with highest privileges.

### Individual Modules

Each module can run independently:

```cmd
python AeroHub_Core\aerohub.py         # Full orchestrator
python ClipboardManager\clipboard_manager.py
python HealthApp\health_app.py
python MediaControl\media_control.py
python BatteryMonitor\battery_monitor.py
python TempMonitor\temp_monitor.py
python TouchToggle\touch_toggle.py
python TgFdmProxy\tg_fdm_proxy.py
python TaskbarScroll\taskbar_scroll.py
```

---

## Dependencies

```
pywin32>=306        # Win32 API access (clipboard, COM)
psutil>=5.9         # Process management, battery info
pystray>=0.19       # System tray icons
Pillow>=10.0        # Icon generation
pygame>=2.5         # Audio playback (Health App)
requests>=2.31      # Weather API (Health App)
wmi>=1.5            # Temperature reading fallback
screen-brightness-control>=0.22  # Brightness management
pythonnet>=3.0      # LibreHardwareMonitor DLL loading
plyer>=2.1          # Cross-platform notifications
```

Additional per-module dependencies:
- **MediaControl**: `winsdk`, `pycaw`, `pywin32`
- **TaskbarScroll**: `pynput`
- **TgFdmProxy**: `telethon`, `aiohttp`, `python-dotenv`

---

## Configuration

### AeroHub Core Config

Edit `AeroHub_Core/aerohub_config.json` to control which processes auto-start:

```json
{
  "auto_start": true,
  "restart_delay_sec": 5,
  "processes": [
    {
      "id": "clipboard_manager",
      "name": "Clipboard Manager",
      "script": "ClipboardManager/clipboard_manager.py",
      "auto_start": true,
      "enabled": true
    }
  ]
}
```

### Per-Module Settings

Each module stores its settings in a local `settings.json` or `config.json` within its directory. All settings are editable via the module's tray icon right-click → Settings GUI.

---

## Design Philosophy

| Principle | Implementation |
|---|---|
| **Non-Intrusive** | All services run headless via `pythonw.exe` with `CREATE_NO_WINDOW`. No command prompts spawn unless explicitly requested |
| **Context-Aware Theming** | Reads Windows registry (`SystemUsesLightTheme`, `ColorPrevalence`, `AccentColor`) to adapt tray icons and GUIs dynamically |
| **Frictionless UX** | Hover states on all interactive elements, generous click targets, smooth fade/slide animations (ease-out cubic), no layout shifts |
| **Terminal Aesthetics** | Setup scripts use ANSI colors — Cyan for steps, Green for success, Red for errors |
| **Crash Resilience** | AeroHub Core monitors child process health every 3 seconds and auto-restarts crashed services with configurable delay |

---

## License

Private repository. All rights reserved.
````

---

### File: `README.scripts.md`
- **Path:** `README.scripts.md`
- **Estimated Tokens:** 238
- **mtime:** 1780865507.437

````markdown
Scripts and Dev Helpers

This project includes useful scripts and CI for local development, production runs, and containerization.

- `dev_run.ps1` — start the Reflex app in development mode and open the browser.
- `prod_run.ps1` — start Reflex in production mode and log to `logs/`.
- `aerohub_service.ps1` — helper to install/uninstall `AeroHub` as a Windows service using `nssm`.
- `run_docker.ps1` — build and run `docker-compose` and open the app in a browser.
- `Dockerfile` / `docker-compose.yml` — containerize the app for consistent environments.
- `.github/workflows/ci.yml` — CI pipeline for linting, compiling, and running tests.
- `.pre-commit-config.yaml` — pre-commit hooks configuration (black, isort, flake8).

Quick usage examples:

PowerShell (dev):

```powershell
.\dev_run.ps1
```

PowerShell (prod):

```powershell
.\prod_run.ps1
```

Docker:

```powershell
.\run_docker.ps1
```

CI is configured to run on pushes and PRs to `main`.
````

---

### File: `aerohub_service.ps1`
- **Path:** `aerohub_service.ps1`
- **Estimated Tokens:** 260
- **mtime:** 1780865504.641

```powershell
# aerohub_service.ps1 — helper to install/uninstall AeroHub as a Windows service using NSSM
param(
    [ValidateSet("install","remove")]
    [string]$action = "install",
    [string]$nssmPath = "nssm"
)
$script = Join-Path $PSScriptRoot "AeroHub_Core\aerohub.py"
if (-not (Test-Path $script)) { Write-Error "AeroHub_Core\aerohub.py not found in workspace."; exit 1 }
$python = (Get-Command python).Source
$serviceName = "AeroHub"
if ($action -eq "install") {
    Write-Host "Installing service $serviceName using NSSM ($nssmPath)"
    & $nssmPath install $serviceName $python $script
    & $nssmPath set $serviceName AppStdout "$(Join-Path $PSScriptRoot 'Logs\aerohub.stdout.log')"
    & $nssmPath set $serviceName AppStderr "$(Join-Path $PSScriptRoot 'Logs\aerohub.stderr.log')"
    & $nssmPath start $serviceName
    Write-Host "$serviceName installed and started."
} else {
    Write-Host "Removing service $serviceName"
    & $nssmPath stop $serviceName
    & $nssmPath remove $serviceName confirm
    Write-Host "$serviceName removed."
}
```

---

### File: `config/__init__.py`
- **Path:** `config/__init__.py`
- **Estimated Tokens:** 39
- **mtime:** 1780923521.892

```python
from .loader import load_config, load_env, expand_env
from .logging import setup_logging

__all__ = ["load_config", "load_env", "expand_env", "setup_logging"]
```

---

### File: `config/app.yaml`
- **Path:** `config/app.yaml`
- **Estimated Tokens:** 65
- **mtime:** 1780923522.093

```yaml
app:
  name: AeroHub
  env: dev
  flet_port: 8555
  health_port: 8100
  metrics_port: 9100
  control_port: 8200
  control_token: ""

logging:
  path: Logs
  file: app.log
  level: INFO
  max_bytes: 5242880
  backup_count: 3

sentry:
  enabled: false
  dsn: ""
```

---

### File: `config/loader.py`
- **Path:** `config/loader.py`
- **Estimated Tokens:** 729
- **mtime:** 1780924210.16

```python
import os
import re
import json
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

ENV_PATTERN = re.compile(r"\$\{([^}:]+)(?::([^}]+))?\}")

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = REPO_ROOT / "config" / "app.yaml"
ENV_PATH = REPO_ROOT / ".env"


def _expand_value(value: str) -> str:
    if not isinstance(value, str):
        return value

    def repl(match):
        name = match.group(1)
        default = match.group(2)
        return os.getenv(name, default if default is not None else "")

    return ENV_PATTERN.sub(repl, value)


def _expand(obj):
    if isinstance(obj, dict):
        return {k: _expand(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_expand(v) for v in obj]
    if isinstance(obj, str):
        return _expand_value(obj)
    return obj


def load_env(path: Path | str = None) -> dict:
    path = Path(path or ENV_PATH)
    env = {}
    if not path.exists():
        return env

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def _load_yaml(path: Path) -> dict:
    if yaml is None:
        raise ImportError("PyYAML is required to load YAML configuration")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_config(path: Path | str = None) -> dict:
    path = Path(path or DEFAULT_CONFIG_PATH)
    config: dict = {}
    if path.exists():
        if path.suffix in {".yaml", ".yml"}:
            config = _load_yaml(path)
        elif path.suffix == ".json":
            config = _load_json(path)
    env_config = load_env(path=ENV_PATH)
    # Set environment vars as overrides
    for key, value in env_config.items():
        if key.isupper():
            parts = key.lower().split("__")
            target = config
            for part in parts[:-1]:
                target = target.setdefault(part, {})
            target[parts[-1]] = _expand_value(value)
    return _expand(config)


def get_runtime_option(key: str, default=None):
    config = load_config()
    parts = key.split(".")
    node = config
    for part in parts:
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            return default
    return node


def expand_env(obj):
    """Public helper to expand environment variables in a data structure.

    Accepts a mapping, sequence, or string and returns a new object with
    ${VAR} placeholders replaced from the environment.
    """
    return _expand(obj)
```

---

### File: `config/logging.py`
- **Path:** `config/logging.py`
- **Estimated Tokens:** 562
- **mtime:** 1780923521.895

```python
import json
import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler

try:
    import sentry_sdk
except ImportError:  # pragma: no cover
    sentry_sdk = None


class JsonFormatter(logging.Formatter):
    def format(self, record):
        message = record.getMessage()
        extra = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": message,
            "module": record.module,
            "filename": record.filename,
            "line": record.lineno,
        }
        if record.exc_info:
            extra["exception"] = self.formatException(record.exc_info)
        return json.dumps(extra, ensure_ascii=False)


def setup_logging(app_name: str = "app", config: dict | None = None):
    config = config or {}
    root = logging.getLogger()
    if root.handlers:
        return root

    log_settings = config.get("logging", {})
    log_dir = Path(log_settings.get("path", "Logs"))
    log_file = log_settings.get("file", f"{app_name}.log")
    log_dir.mkdir(parents=True, exist_ok=True)

    level = getattr(logging, log_settings.get("level", "INFO").upper(), logging.INFO)
    formatter = JsonFormatter()

    stream = logging.StreamHandler()
    stream.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    root.addHandler(stream)

    file_handler = RotatingFileHandler(
        log_dir / log_file,
        maxBytes=int(log_settings.get("max_bytes", 5 * 1024 * 1024)),
        backupCount=int(log_settings.get("backup_count", 3)),
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)
    root.setLevel(level)

    if config.get("sentry", {}).get("enabled"):
        dsn = config.get("sentry", {}).get("dsn") or os.getenv("SENTRY_DSN")
        if dsn and sentry_sdk is not None:
            sentry_sdk.init(dsn=dsn, release=os.getenv("GITHUB_SHA"), environment=os.getenv("ENV", "dev"))
            root.info("Sentry integration enabled.")
        elif config.get("sentry", {}).get("enabled"):
            root.warning("Sentry enabled in config, but sentry-sdk is not installed.")

    return root
```

---

### File: `dev_run.ps1`
- **Path:** `dev_run.ps1`
- **Estimated Tokens:** 75
- **mtime:** 1780923522.099

```powershell
# dev_run.ps1 — start the unified project launcher in development mode
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "Starting MovieSongDownloader in development mode..."
Start-Process -NoNewWindow -FilePath powershell -ArgumentList "-File `"$root\run.ps1`" --env dev --port 8555"
```

---

### File: `docker-compose.yml`
- **Path:** `docker-compose.yml`
- **Estimated Tokens:** 83
- **mtime:** 1780923522.093

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8555:8555"
    environment:
      - FLET_WEB_PORT=8555
      - REDIS_URL=redis://redis:6379
    volumes:
      - ./:/app
    depends_on:
      - redis
    restart: unless-stopped
  redis:
    image: redis:7.2
    ports:
      - "6379:6379"
    restart: unless-stopped
```

---

### File: `prod_run.ps1`
- **Path:** `prod_run.ps1`
- **Estimated Tokens:** 75
- **mtime:** 1780923522.099

```powershell
# prod_run.ps1 — start the unified project launcher in production mode
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "Starting MovieSongDownloader in production mode..."
Start-Process -NoNewWindow -FilePath powershell -ArgumentList "-File `"$root\run.ps1`" --env prod --port 8555"
```

---

### File: `pytest.ini`
- **Path:** `pytest.ini`
- **Estimated Tokens:** 18
- **mtime:** 1781116342.958

```ini
[pytest]
pythonpath = services
norecursedirs = scratch .agent .web .git
```

---

### File: `reflex.lock/package.json`
- **Path:** `reflex.lock/package.json`
- **Estimated Tokens:** 235
- **mtime:** 1780927451.807

```json
{
  "name": "reflex",
  "type": "module",
  "scripts": {
    "dev": "react-router dev --host",
    "export": "react-router build"
  },
  "dependencies": {
    "@radix-ui/react-form": "0.1.8",
    "@radix-ui/themes": "3.3.0",
    "@react-router/node": "7.15.0",
    "isbot": "5.1.40",
    "lucide-react": "1.14.0",
    "react": "19.2.6",
    "react-debounce-input": "3.3.0",
    "react-dom": "19.2.6",
    "react-error-boundary": "6.1.1",
    "react-helmet": "6.1.0",
    "react-player": "3.4.0",
    "react-router": "7.15.0",
    "react-router-dom": "7.15.0",
    "socket.io-client": "4.8.3",
    "sonner": "2.0.7",
    "universal-cookie": "7.2.2"
  },
  "devDependencies": {
    "@emotion/react": "11.14.0",
    "@react-router/dev": "7.15.0",
    "@react-router/fs-routes": "7.15.0",
    "autoprefixer": "10.5.0",
    "postcss": "8.5.14",
    "postcss-import": "16.1.1",
    "vite": "8.0.14"
  },
  "overrides": {
    "cookie": "1.1.1"
  }
}
```

---

### File: `requirements.txt`
- **Path:** `requirements.txt`
- **Estimated Tokens:** 47
- **mtime:** 1780923522.093

```
pywin32>=306
psutil>=5.9
pystray>=0.19
Pillow>=10.0
pygame>=2.5
requests>=2.31
wmi>=1.5
screen-brightness-control>=0.22
pythonnet>=3.0
plyer>=2.1
PyYAML>=6.0
sentry-sdk>=1.22.0

reflex==0.9.4
```

---

### File: `run.ps1`
- **Path:** `run.ps1`
- **Estimated Tokens:** 182
- **mtime:** 1781116210.484

```powershell
param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("dev","prod")]
    [string]$env = "dev",
    [string]$port = "8555"
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:FLET_WEB_PORT = $port
Write-Host "Starting application in $env mode on port $port"
if ($env -eq "dev") {
    Write-Host "Launching development server..."
    Start-Process -NoNewWindow -FilePath python -ArgumentList "services/movie_song_downloader/main.py"
    Start-Sleep -Seconds 4
    Start-Process "http://127.0.0.1:$port"
} else {
    Write-Host "Launching production server..."
    Start-Process -NoNewWindow -FilePath python -ArgumentList "services/movie_song_downloader/main.py --env prod"
    Write-Host "Application started."
}
```

---

### File: `run.sh`
- **Path:** `run.sh`
- **Estimated Tokens:** 171
- **mtime:** 1780923522.092

```bash
#!/usr/bin/env bash
set -euo pipefail
ENV_MODE="dev"
PORT="8555"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --env)
      ENV_MODE="$2"
      shift 2
      ;;
    --port)
      PORT="$2"
      shift 2
      ;;
    *)
      echo "Unknown arg: $1"
      exit 1
      ;;
  esac
done

export FLET_WEB_PORT="$PORT"
echo "Starting MovieSongDownloader in $ENV_MODE mode on port $PORT"
if [ "$ENV_MODE" = "dev" ]; then
  python MovieSongDownloader/main.py &
  sleep 4
  if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "http://127.0.0.1:$PORT"
  elif command -v open >/dev/null 2>&1; then
    open "http://127.0.0.1:$PORT"
  fi
else
  python MovieSongDownloader/main.py --env prod
fi
```

---

### File: `run_app.bat`
- **Path:** `run_app.bat`
- **Estimated Tokens:** 170
- **mtime:** 1781116231.499

```
@echo off
set FLET_WEB_PORT=8555
echo ========================================================
echo Movie Song Downloader - Reflex Launcher
echo ========================================================
echo 1. Run in Production Mode (Recommended - Prevents Windows socket reload bugs)
echo 2. Run in Development Mode (With Auto-Reload)
echo ========================================================
set /p mode="Choose run mode (1 or 2, default is 1): "

if "%mode%"=="2" (
    echo Starting in Development Mode...
    python services/movie_song_downloader/main.py
) else (
    echo Starting in Production Mode...
    python services/movie_song_downloader/main.py --env prod
)
pause
```

---

### File: `run_app.ps1`
- **Path:** `run_app.ps1`
- **Estimated Tokens:** 216
- **mtime:** 1781116225.249

```powershell
$env:FLET_WEB_PORT="8555"
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Movie Song Downloader - Reflex Launcher (PowerShell)" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "1. Run in Production Mode (Recommended - Prevents Windows socket reload bugs)"
Write-Host "2. Run in Development Mode (With Auto-Reload)"
Write-Host "========================================================"
$mode = Read-Host "Choose run mode (1 or 2, default is 1)"

if ($mode -eq "2") {
    Write-Host "Starting in Development Mode..." -ForegroundColor Yellow
    python services/movie_song_downloader/main.py
} else {
    Write-Host "Starting in Production Mode..." -ForegroundColor Green
    python services/movie_song_downloader/main.py --env prod
}
```

---

### File: `run_docker.ps1`
- **Path:** `run_docker.ps1`
- **Estimated Tokens:** 78
- **mtime:** 1780865505.681

```powershell
# run_docker.ps1 — build and run docker-compose for local dev
Write-Host "Building and starting docker-compose stack (web:3000)"
docker-compose build --pull
docker-compose up -d
Start-Sleep -Seconds 3
Start-Process "http://127.0.0.1:3000"
Write-Host "Container started. Run 'docker-compose logs -f' to follow logs."
```

---

### File: `run_utility.ps1`
- **Path:** `run_utility.ps1`
- **Estimated Tokens:** 351
- **mtime:** 1781116203.924

```powershell
param(
    [Parameter(Mandatory=$true)]
    [string]$name,
    [string]$env = "dev",
    [switch]$noGui,
    [int]$port = 8555
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$utilities = @{
    "BatteryMonitor" = "toggles\battery_monitor\battery_monitor.py"
    "TempMonitor" = "toggles\temp_monitor\temp_monitor.py"
    "TouchToggle" = "toggles\touch_toggle\touch_toggle.py"
    "MediaControl" = "services\media_control\media_control.py"
    "ClipboardManager" = "services\clipboard_manager\clipboard_manager.py"
    "HealthApp" = "services\health_app\health_app.py"
    "TaskbarScroll" = "tools\taskbar_scroll\taskbar_scroll.py"
    "TgFdmProxy" = "services\tg_fdm_proxy\TgFdmProxy\tg_fdm_proxy.py"
}

if (-not $utilities.ContainsKey($name)) {
    Write-Error "Unknown utility: $name"
    exit 1
}

$scriptPath = Join-Path $root $utilities[$name]
if (-not (Test-Path $scriptPath)) {
    Write-Error "Utility script not found: $scriptPath"
    exit 1
}

$env:FLET_WEB_PORT = $port
$env:LOG_DIR = Join-Path $root "Logs"
$env:ENV = $env

$arguments = @($scriptPath)
if ($name -eq "MovieSongDownloader") {
    if ($env -eq "prod") { $arguments += "--env"; $arguments += "prod" }
}

if ($noGui.IsPresent) {
    Write-Host "Starting $name in headless mode..."
} else {
    Write-Host "Starting $name with unified environment."
}

Start-Process -FilePath python -ArgumentList $arguments -NoNewWindow
```

---

### File: `rxconfig.py`
- **Path:** `rxconfig.py`
- **Estimated Tokens:** 44
- **mtime:** 1780862784.996

```python
import reflex as rx

config = rx.Config(
    app_name="MovieSongDownloader",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.RadixThemesPlugin(),
    ],
)
```

---

### File: `scratch/check_console.py`
- **Path:** `scratch/check_console.py`
- **Estimated Tokens:** 382
- **mtime:** 1780573562.652

```python
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Listen for console logs and errors
        page.on("console", lambda msg: print(f"CONSOLE {msg.type.upper()}: {msg.text}"))
        page.on("pageerror", lambda err: print(f"PAGE ERROR: {err.message}"))
        
        print("Navigating to app URL...")
        await page.goto("http://127.0.0.1:8555/")
        
        # Wait for the app page to load
        await page.wait_for_timeout(3000)
        
        print("Navigating to Settings tab...")
        # Settings tab nav rail button (index 3)
        # Locate NavigationRail destinations
        try:
            settings_button = page.locator("text=Settings")
            await settings_button.click()
            await page.wait_for_timeout(2000)
        except Exception as e:
            print("Failed to click Settings:", e)
            
        print("Clicking Music Output Directory...")
        try:
            # Click on output directory textfield
            output_dir = page.get_by_label("Music Output Directory")
            await output_dir.click()
            await page.wait_for_timeout(2000)
        except Exception as e:
            print("Failed to click Music Output Directory:", e)
            
        print("Closing browser.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
```

---

### File: `scratch/extract_transcript.py`
- **Path:** `scratch/extract_transcript.py`
- **Estimated Tokens:** 428
- **mtime:** 1780659603.344

```python
import os
import json

log_path = r"C:\Users\NANDHA A\.gemini\antigravity-ide\brain\1237cb3f-efd0-4a57-b440-f74287d1898a\.system_generated\logs\transcript.jsonl"
output_dir = r"c:\Users\NANDHA A\Desktop\UTILITIES\scratch\extracted"
os.makedirs(output_dir, exist_ok=True)

with open(log_path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        data = json.loads(line)
        step_idx = data.get("step_index")
        tool_calls = data.get("tool_calls", [])
        if not tool_calls:
            continue
            
        for tc_idx, tc in enumerate(tool_calls):
            args = tc.get("args", {})
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    pass
            
            # Check if this tool call modifies health_app.py
            target_file = args.get("TargetFile", "")
            if "health_app.py" in target_file or any("health_app.py" in str(v) for v in args.values()):
                print(f"Step {step_idx} matches. Tool: {tc.get('name')}")
                # Save the arguments to a file
                out_path = os.path.join(output_dir, f"step_{step_idx}_tc_{tc_idx}.json")
                with open(out_path, "w", encoding="utf-8") as out:
                    json.dump(args, out, indent=2)
                
                # If there's replacement content, save it separately
                repl = args.get("ReplacementContent")
                if repl:
                    repl_path = os.path.join(output_dir, f"step_{step_idx}_replacement.py")
                    with open(repl_path, "w", encoding="utf-8") as out:
                        out.write(repl)
```

---

### File: `scratch/extracted/step_101_tc_0.json`
- **Path:** `scratch/extracted/step_101_tc_0.json`
- **Estimated Tokens:** 65
- **mtime:** 1780659608.215

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1380",
  "StartLine": "1180",
  "toolAction": "\"Viewing SettingsWindow definition\"",
  "toolSummary": "\"View SettingsWindow definition\""
}
```

---

### File: `scratch/extracted/step_103_tc_0.json`
- **Path:** `scratch/extracted/step_103_tc_0.json`
- **Estimated Tokens:** 63
- **mtime:** 1780659608.216

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1460",
  "StartLine": "1380",
  "toolAction": "\"Viewing settings field helpers\"",
  "toolSummary": "\"View settings field helpers\""
}
```

---

### File: `scratch/extracted/step_105_replacement.py`
- **Path:** `scratch/extracted/step_105_replacement.py`
- **Estimated Tokens:** 517
- **mtime:** 1780659608.219

```python
"    def _add_field(self, parent_frame, label, key, row, is_str=False):\n        tk.Label(\n            parent_frame, text=label.upper(), font=(\"Consolas\", 9),\n            bg=TH[\"bg\"], fg=TH[\"fg_dim\"], anchor=tk.W,\n        ).grid(row=row, column=0, sticky=tk.W, pady=8)\n\n        var = tk.StringVar(value=str(self.settings.get(key, \"\")))\n        tk.Entry(\n            parent_frame, textvariable=var, font=(\"Consolas\", 10),\n            bg=TH[\"bg\"], fg=TH[\"fg\"], insertbackground=TH[\"accent\"],\n            relief=tk.FLAT, highlightthickness=1,\n            highlightcolor=TH[\"accent\"], highlightbackground=TH[\"border\"],\n            width=14,\n        ).grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))\n\n        self.entries[key] = (var, is_str)\n        var.trace_add(\"write\", lambda *args: self._on_settings_modified())\n\n    def _add_combo(self, parent_frame, label, key, row, values):\n        tk.Label(\n            parent_frame, text=label.upper(), font=(\"Consolas\", 9),\n            bg=TH[\"bg\"], fg=TH[\"fg_dim\"], anchor=tk.W,\n        ).grid(row=row, column=0, sticky=tk.W, pady=8)\n\n        var = tk.StringVar(value=self.settings.get(key, values[0]))\n        ttk.Combobox(\n            parent_frame, textvariable=var, values=values,\n            font=(\"Consolas\", 10), state=\"readonly\", width=12,\n        ).grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))\n\n        self.entries[key] = (var, True)\n        var.trace_add(\"write\", lambda *args: self._on_settings_modified())\n\n    def _add_color_field(self, parent_frame, label, key, row):\n        tk.Label(\n            parent_frame, text=label.upper(), font=(\"Consolas\", 9),\n            bg=TH[\"bg\"], fg=TH[\"fg_dim\"], anchor=tk.W,\n        ).grid(row=row, column=0, sticky=tk.W, pady=8)\n\n        var = tk.StringVar(value=str(self.settings.get(key, \"\")))\n        \n        def choose_color(v=var):\n            color_code = colorchooser.askcolor(title=\"Choose color\", initialcolor=v.get())[1]\n            if 
<truncated 2761 bytes>
```

---

### File: `scratch/extracted/step_105_tc_0.json`
- **Path:** `scratch/extracted/step_105_tc_0.json`
- **Estimated Tokens:** 1,238
- **mtime:** 1780659608.218

```json
{
  "AllowMultiple": "false",
  "Description": "\"Replace input tracing in SettingsWindow to use _on_settings_modified instead of opening live desktop popups.\"",
  "EndLine": "1436",
  "Instruction": "\"Replace field adder helper methods in SettingsWindow.\"",
  "ReplacementContent": "\"    def _add_field(self, parent_frame, label, key, row, is_str=False):\\n        tk.Label(\\n            parent_frame, text=label.upper(), font=(\\\"Consolas\\\", 9),\\n            bg=TH[\\\"bg\\\"], fg=TH[\\\"fg_dim\\\"], anchor=tk.W,\\n        ).grid(row=row, column=0, sticky=tk.W, pady=8)\\n\\n        var = tk.StringVar(value=str(self.settings.get(key, \\\"\\\")))\\n        tk.Entry(\\n            parent_frame, textvariable=var, font=(\\\"Consolas\\\", 10),\\n            bg=TH[\\\"bg\\\"], fg=TH[\\\"fg\\\"], insertbackground=TH[\\\"accent\\\"],\\n            relief=tk.FLAT, highlightthickness=1,\\n            highlightcolor=TH[\\\"accent\\\"], highlightbackground=TH[\\\"border\\\"],\\n            width=14,\\n        ).grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))\\n\\n        self.entries[key] = (var, is_str)\\n        var.trace_add(\\\"write\\\", lambda *args: self._on_settings_modified())\\n\\n    def _add_combo(self, parent_frame, label, key, row, values):\\n        tk.Label(\\n            parent_frame, text=label.upper(), font=(\\\"Consolas\\\", 9),\\n            bg=TH[\\\"bg\\\"], fg=TH[\\\"fg_dim\\\"], anchor=tk.W,\\n        ).grid(row=row, column=0, sticky=tk.W, pady=8)\\n\\n        var = tk.StringVar(value=self.settings.get(key, values[0]))\\n        ttk.Combobox(\\n            parent_frame, textvariable=var, values=values,\\n            font=(\\\"Consolas\\\", 10), state=\\\"readonly\\\", width=12,\\n        ).grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))\\n\\n        self.entries[key] = (var, True)\\n        var.trace_add(\\\"write\\\", lambda *args: self._on_settings_modified())\\n\\n    def _add_color_field(self, parent_frame, label, key, row):\\n        tk.Label(\\n            parent_frame, text=label.upper(), font=(\\\"Consolas\\\", 9),\\n            bg=TH[\\\"bg\\\"], fg=TH[\\\"fg_dim\\\"], anchor=tk.W,\\n        ).grid(row=row, column=0, sticky=tk.W, pady=8)\\n\\n        var = tk.StringVar(value=str(self.settings.get(key, \\\"\\\")))\\n        \\n        def choose_color(v=var):\\n            color_code = colorchooser.askcolor(title=\\\"Choose color\\\", initialcolor=v.get())[1]\\n            if \n<truncated 2761 bytes>",
  "StartLine": "1314",
  "TargetContent": "\"    def _add_field(self, parent_frame, label, key, row, is_str=False):\\n        tk.Label(\\n            parent_frame, text=label.upper(), font=(\\\"Consolas\\\", 9),\\n            bg=TH[\\\"bg\\\"], fg=TH[\\\"fg_dim\\\"], anchor=tk.W,\\n        ).grid(row=row, column=0, sticky=tk.W, pady=8)\\n\\n        var = tk.StringVar(value=str(self.settings.get(key, \\\"\\\")))\\n        tk.Entry(\\n            parent_frame, textvariable=var, font=(\\\"Consolas\\\", 10),\\n            bg=TH[\\\"bg\\\"], fg=TH[\\\"fg\\\"], insertbackground=TH[\\\"accent\\\"],\\n            relief=tk.FLAT, highlightthickness=1,\\n            highlightcolor=TH[\\\"accent\\\"], highlightbackground=TH[\\\"border\\\"],\\n            width=14,\\n        ).grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))\\n\\n        self.entries[key] = (var, is_str)\\n        if key.startswith(\\\"toast_\\\"):\\n            var.trace_add(\\\"write\\\", lambda *args: self._schedule_preview())\\n        elif key.startswith(\\\"ht_toast_\\\"):\\n            var.trace_add(\\\"write\\\", lambda *args: self._schedule_health_preview())\\n\\n    def _add_combo(self, parent_frame, label, key, row, values):\\n        tk.Label(\\n            parent_frame, text=label.upper(), font=(\\\"Consolas\\\", 9),\\n            bg=TH[\\\"bg\\\"], fg=TH[\\\"fg_dim\\\"], anchor=tk.W,\\n        ).grid(row=row, column=0, sticky=tk.W, pady=8)\\n\\n        var = tk.StringVar(value=self.settings.get(key, values[0]))\\n        ttk.Combobox(\\n            parent_frame, textvariable=var, values=values,\\n            font=(\\\"Consolas\\\", 10), state=\\\"readonly\\\", width=12,\\n        ).grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))\\n\\n        self.entries[key] = (var, True)\\n        if key.startswith(\\\"toast_\\\"):\\n            var.trace_add(\\\"write\\\", lambda *args: self._schedule_preview())\\n        elif key.startswith(\\\"ht_toast_\\\"):\\n            var.trace_add(\\\"write\\\", lambda *args: self._schedule_health_preview())\\n\\n    def _add_color_field(self, parent_frame, label, key, row):\\n        tk.Label(\\n            parent_frame, text=label.upper(), font=(\\\"Consolas\\\", 9),\\n   \n<truncated 3675 bytes>",
  "TargetFile": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Replacing field adder traces\"",
  "toolSummary": "\"Replace field adder traces\""
}
```

---

### File: `scratch/extracted/step_107_tc_0.json`
- **Path:** `scratch/extracted/step_107_tc_0.json`
- **Estimated Tokens:** 67
- **mtime:** 1780659608.22

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1313",
  "StartLine": "1210",
  "toolAction": "\"Viewing SettingsWindow _create method\"",
  "toolSummary": "\"View SettingsWindow _create method\""
}
```

---

### File: `scratch/extracted/step_109_tc_0.json`
- **Path:** `scratch/extracted/step_109_tc_0.json`
- **Estimated Tokens:** 62
- **mtime:** 1780659608.222

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1475",
  "StartLine": "1437",
  "toolAction": "\"Viewing schedule tab builder\"",
  "toolSummary": "\"View schedule tab builder\""
}
```

---

### File: `scratch/extracted/step_10_tc_0.json`
- **Path:** `scratch/extracted/step_10_tc_0.json`
- **Estimated Tokens:** 59
- **mtime:** 1780659608.153

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "800",
  "StartLine": "1",
  "toolAction": "\"Viewing health_app.py code\"",
  "toolSummary": "\"View health_app.py\""
}
```

---

### File: `scratch/extracted/step_111_tc_0.json`
- **Path:** `scratch/extracted/step_111_tc_0.json`
- **Estimated Tokens:** 65
- **mtime:** 1780659608.224

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1438",
  "StartLine": "1400",
  "toolAction": "\"Viewing schedule tab builder start\"",
  "toolSummary": "\"View schedule tab builder start\""
}
```

---

### File: `scratch/extracted/step_113_tc_0.json`
- **Path:** `scratch/extracted/step_113_tc_0.json`
- **Estimated Tokens:** 61
- **mtime:** 1780659608.225

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1540",
  "StartLine": "1476",
  "toolAction": "\"Viewing toast tab builder\"",
  "toolSummary": "\"View toast tab builder\""
}
```

---

### File: `scratch/extracted/step_115_tc_0.json`
- **Path:** `scratch/extracted/step_115_tc_0.json`
- **Estimated Tokens:** 64
- **mtime:** 1780659608.226

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1640",
  "StartLine": "1541",
  "toolAction": "\"Viewing health toast tab builder\"",
  "toolSummary": "\"View health toast tab builder\""
}
```

---

### File: `scratch/extracted/step_117_tc_0.json`
- **Path:** `scratch/extracted/step_117_tc_0.json`
- **Estimated Tokens:** 63
- **mtime:** 1780659608.228

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1730",
  "StartLine": "1641",
  "toolAction": "\"Viewing remaining tab layouts\"",
  "toolSummary": "\"View remaining tab layouts\""
}
```

---

### File: `scratch/extracted/step_119_tc_0.json`
- **Path:** `scratch/extracted/step_119_tc_0.json`
- **Estimated Tokens:** 65
- **mtime:** 1780659608.229

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1860",
  "StartLine": "1717",
  "toolAction": "\"Viewing preview scheduling methods\"",
  "toolSummary": "\"View preview scheduling methods\""
}
```

---

### File: `scratch/extracted/step_121_replacement.py`
- **Path:** `scratch/extracted/step_121_replacement.py`
- **Estimated Tokens:** 517
- **mtime:** 1780659608.233

```python
"        # Build Frames\n        f_sched = tk.Frame(self.content_area, bg=TH[\"bg\"])\n        f_toast = tk.Frame(self.content_area, bg=TH[\"bg\"])\n        f_ht = tk.Frame(self.content_area, bg=TH[\"bg\"])\n        \n        f_bc = tk.Frame(self.content_area, bg=TH[\"bg\"])\n        f_nc = tk.Frame(self.content_area, bg=TH[\"bg\"])\n        f_nl = tk.Frame(self.content_area, bg=TH[\"bg\"])\n        f_prev = tk.Frame(self.content_area, bg=TH[\"bg\"])\n        \n        self.frames[\"Schedule\"] = f_sched\n        self.frames[\"Toast FX\"] = f_toast\n        self.frames[\"Health Toast\"] = f_ht\n        self.frames[\"Brightness Care\"] = f_bc\n        self.frames[\"Night Care\"] = f_nc\n        self.frames[\"Night Light\"] = f_nl\n        self.frames[\"Preview Hub\"] = f_prev\n\n        self._build_schedule_tab(f_sched)\n        self._build_toast_tab(f_toast)\n        self._build_health_toast_tab(f_ht)\n        self._build_brightness_care_tab(f_bc)\n        self._build_night_care_tab(f_nc)\n        self._build_night_light_tab(f_nl)\n        self._build_preview_hub_tab(f_prev)\n        \n        self.current_frame = None\n        self.nav_buttons = {}\n\n        def switch_tab(name):\n            if self.current_frame:\n                self.current_frame.pack_forget()\n                self.nav_buttons[self.current_frame_name].config(bg=TH[\"bg2\"], fg=TH[\"fg_dim\"])\n            \n            self.current_frame = self.frames[name]\n            self.current_frame_name = name\n            self.current_frame.pack(fill=tk.BOTH, expand=True, padx=32, pady=24)\n            self.nav_buttons[name].config(bg=TH[\"bg3\"], fg=TH[\"accent\"])\n            \n            # Auto-update preview canvas if switching to Preview Hub\n            if name == \"Preview Hub\":\n                self._update_preview_canvas()\n\n        self.switch_tab = switch_tab\n\n        # Navigation Buttons\n        for name in [\"Schedule\", \"Toast FX\", \"Health Toast\", \"Brightness Care\", \"Night Care\", \"Night Light\", \"Preview Hub\"]:\n     
<truncated 970 bytes>
```

---

### File: `scratch/extracted/step_121_tc_0.json`
- **Path:** `scratch/extracted/step_121_tc_0.json`
- **Estimated Tokens:** 1,258
- **mtime:** 1780659608.232

```json
{
  "AllowMultiple": "false",
  "Description": "\"Add Preview Hub tab frame, builder call, and navigation button in SettingsWindow._create().\"",
  "EndLine": "1310",
  "Instruction": "\"Add Preview Hub to the SettingsWindow sidebar and frames dictionary.\"",
  "ReplacementContent": "\"        # Build Frames\\n        f_sched = tk.Frame(self.content_area, bg=TH[\\\"bg\\\"])\\n        f_toast = tk.Frame(self.content_area, bg=TH[\\\"bg\\\"])\\n        f_ht = tk.Frame(self.content_area, bg=TH[\\\"bg\\\"])\\n        \\n        f_bc = tk.Frame(self.content_area, bg=TH[\\\"bg\\\"])\\n        f_nc = tk.Frame(self.content_area, bg=TH[\\\"bg\\\"])\\n        f_nl = tk.Frame(self.content_area, bg=TH[\\\"bg\\\"])\\n        f_prev = tk.Frame(self.content_area, bg=TH[\\\"bg\\\"])\\n        \\n        self.frames[\\\"Schedule\\\"] = f_sched\\n        self.frames[\\\"Toast FX\\\"] = f_toast\\n        self.frames[\\\"Health Toast\\\"] = f_ht\\n        self.frames[\\\"Brightness Care\\\"] = f_bc\\n        self.frames[\\\"Night Care\\\"] = f_nc\\n        self.frames[\\\"Night Light\\\"] = f_nl\\n        self.frames[\\\"Preview Hub\\\"] = f_prev\\n\\n        self._build_schedule_tab(f_sched)\\n        self._build_toast_tab(f_toast)\\n        self._build_health_toast_tab(f_ht)\\n        self._build_brightness_care_tab(f_bc)\\n        self._build_night_care_tab(f_nc)\\n        self._build_night_light_tab(f_nl)\\n        self._build_preview_hub_tab(f_prev)\\n        \\n        self.current_frame = None\\n        self.nav_buttons = {}\\n\\n        def switch_tab(name):\\n            if self.current_frame:\\n                self.current_frame.pack_forget()\\n                self.nav_buttons[self.current_frame_name].config(bg=TH[\\\"bg2\\\"], fg=TH[\\\"fg_dim\\\"])\\n            \\n            self.current_frame = self.frames[name]\\n            self.current_frame_name = name\\n            self.current_frame.pack(fill=tk.BOTH, expand=True, padx=32, pady=24)\\n            self.nav_buttons[name].config(bg=TH[\\\"bg3\\\"], fg=TH[\\\"accent\\\"])\\n            \\n            # Auto-update preview canvas if switching to Preview Hub\\n            if name == \\\"Preview Hub\\\":\\n                self._update_preview_canvas()\\n\\n        self.switch_tab = switch_tab\\n\\n        # Navigation Buttons\\n        for name in [\\\"Schedule\\\", \\\"Toast FX\\\", \\\"Health Toast\\\", \\\"Brightness Care\\\", \\\"Night Care\\\", \\\"Night Light\\\", \\\"Preview Hub\\\"]:\\n     \n<truncated 970 bytes>",
  "StartLine": "1251",
  "TargetContent": "\"        self.frames = {}\\n        \\n        # Build Frames\\n        f_sched = tk.Frame(self.content_area, bg=TH[\\\"bg\\\"])\\n        f_toast = tk.Frame(self.content_area, bg=TH[\\\"bg\\\"])\\n        f_ht = tk.Frame(self.content_area, bg=TH[\\\"bg\\\"])\\n        \\n        f_bc = tk.Frame(self.content_area, bg=TH[\\\"bg\\\"])\\n        f_nc = tk.Frame(self.content_area, bg=TH[\\\"bg\\\"])\\n        f_nl = tk.Frame(self.content_area, bg=TH[\\\"bg\\\"])\\n        \\n        self.frames[\\\"Schedule\\\"] = f_sched\\n        self.frames[\\\"Toast FX\\\"] = f_toast\\n        self.frames[\\\"Health Toast\\\"] = f_ht\\n        self.frames[\\\"Brightness Care\\\"] = f_bc\\n        self.frames[\\\"Night Care\\\"] = f_nc\\n        self.frames[\\\"Night Light\\\"] = f_nl\\n\\n        self._build_schedule_tab(f_sched)\\n        self._build_toast_tab(f_toast)\\n        self._build_health_toast_tab(f_ht)\\n        self._build_brightness_care_tab(f_bc)\\n        self._build_night_care_tab(f_nc)\\n        self._build_night_light_tab(f_nl)\\n        \\n        self.current_frame = None\\n        self.nav_buttons = {}\\n\\n        def switch_tab(name):\\n            if self.current_frame:\\n                self.current_frame.pack_forget()\\n                self.nav_buttons[self.current_frame_name].config(bg=TH[\\\"bg2\\\"], fg=TH[\\\"fg_dim\\\"])\\n            \\n            self.current_frame = self.frames[name]\\n            self.current_frame_name = name\\n            self.current_frame.pack(fill=tk.BOTH, expand=True, padx=32, pady=24)\\n            self.nav_buttons[name].config(bg=TH[\\\"bg3\\\"], fg=TH[\\\"accent\\\"])\\n\\n        # Navigation Buttons\\n        for name in [\\\"Schedule\\\", \\\"Toast FX\\\", \\\"Health Toast\\\", \\\"Brightness Care\\\", \\\"Night Care\\\", \\\"Night Light\\\"]:\\n            btn = tk.Button(\\n                self.sidebar, text=f\\\"\u25a0 {name.upper()}\\\", font=(\\\"Consolas\\\", 11, \\\"bold\\\"),\\n                bg=TH[\\\"bg2\\\"], fg=TH[\\\"fg_dim\\\"], activebackground=TH[\\\"bg3\\\"], activeforeground=TH[\\\"accent\\\"],\\n                relief=tk.FLAT, cursor=\\\"hand2\\\", anchor=\\\"w\\\", padx=24, pady=12,\\n                command=lam\n<truncated 624 bytes>",
  "TargetFile": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Integrating Preview Hub sidebar navigation\"",
  "toolSummary": "\"Integrate Preview Hub sidebar navigation\""
}
```

---

### File: `scratch/extracted/step_123_tc_0.json`
- **Path:** `scratch/extracted/step_123_tc_0.json`
- **Estimated Tokens:** 60
- **mtime:** 1780659608.235

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1550",
  "StartLine": "1450",
  "toolAction": "\"Viewing build toast tab\"",
  "toolSummary": "\"View build toast tab\""
}
```

---

### File: `scratch/extracted/step_125_replacement.py`
- **Path:** `scratch/extracted/step_125_replacement.py`
- **Estimated Tokens:** 399
- **mtime:** 1780659608.237

```python
"        sound_choices = [\n            \"cyber_alert\", \"retro_beep\", \"zen_bowl\", \"echo_ping\", \"digital_chime\",\n            \"sci_fi_sweep\", \"soft_click\", \"tech_chirp\", \"bubble_pop\", \"crystal_bell\",\n            \"mac_connect\", \"mac_disconnect\", \"SystemAsterisk\", \"SystemExclamation\",\n            \"SystemHand\", \"SystemQuestion\", \"SystemDefault\"\n        ]\n        self._add_combo(f2_right, \"Sound Effect:\", \"toast_sound_effect\", 10, sound_choices)\n        \n        f3 = tk.Frame(scrollable_frame, bg=TH[\"bg\"])\n        f3.pack(fill=tk.X, pady=(15, 0))\n        \n        self._add_grid_chk(f3, \"Enable Shadow/Glow\", \"toast_shadow\", 0)\n        self._add_grid_chk(f3, \"Enable Gradient BG\", \"toast_gradient\", 1)\n        self._add_grid_chk(f3, \"Enable Accent Stripe\", \"toast_accent_stripe\", 2)\n        self._add_grid_chk(f3, \"Show Progress Bar\", \"toast_progress_bar\", 3)\n        self._add_grid_chk(f3, \"Auto-Dismiss\", \"toast_auto_dismiss\", 4)\n        self._add_grid_chk(f3, \"Play Warning Sound\", \"toast_enable_sound\", 5)\n \n        btn_frame = tk.Frame(scrollable_frame, bg=TH[\"bg\"])\n        btn_frame.pack(fill=tk.X, pady=20)\n        \n        tk.Button(\n            btn_frame, text=\"[ PREVIEW IN HUB ]\", font=(\"Consolas\", 10, \"bold\"),\n            bg=TH[\"bg2\"], fg=TH[\"accent\"], activebackground=TH[\"bg3\"], activeforeground=TH[\"accent\"],\n            relief=tk.FLAT, cursor=\"hand2\",\n            command=lambda: self.switch_to_preview_hub(\"General Break\"), padx=20, pady=8,\n        ).pack(side=tk.RIGHT)"
```

---

### File: `scratch/extracted/step_125_tc_0.json`
- **Path:** `scratch/extracted/step_125_tc_0.json`
- **Estimated Tokens:** 952
- **mtime:** 1780659608.236

```json
{
  "AllowMultiple": "false",
  "Description": "\"Update sound choices and preview button command in _build_toast_tab.\"",
  "EndLine": "1540",
  "Instruction": "\"Update sound effect list and preview button callback in _build_toast_tab.\"",
  "ReplacementContent": "\"        sound_choices = [\\n            \\\"cyber_alert\\\", \\\"retro_beep\\\", \\\"zen_bowl\\\", \\\"echo_ping\\\", \\\"digital_chime\\\",\\n            \\\"sci_fi_sweep\\\", \\\"soft_click\\\", \\\"tech_chirp\\\", \\\"bubble_pop\\\", \\\"crystal_bell\\\",\\n            \\\"mac_connect\\\", \\\"mac_disconnect\\\", \\\"SystemAsterisk\\\", \\\"SystemExclamation\\\",\\n            \\\"SystemHand\\\", \\\"SystemQuestion\\\", \\\"SystemDefault\\\"\\n        ]\\n        self._add_combo(f2_right, \\\"Sound Effect:\\\", \\\"toast_sound_effect\\\", 10, sound_choices)\\n        \\n        f3 = tk.Frame(scrollable_frame, bg=TH[\\\"bg\\\"])\\n        f3.pack(fill=tk.X, pady=(15, 0))\\n        \\n        self._add_grid_chk(f3, \\\"Enable Shadow/Glow\\\", \\\"toast_shadow\\\", 0)\\n        self._add_grid_chk(f3, \\\"Enable Gradient BG\\\", \\\"toast_gradient\\\", 1)\\n        self._add_grid_chk(f3, \\\"Enable Accent Stripe\\\", \\\"toast_accent_stripe\\\", 2)\\n        self._add_grid_chk(f3, \\\"Show Progress Bar\\\", \\\"toast_progress_bar\\\", 3)\\n        self._add_grid_chk(f3, \\\"Auto-Dismiss\\\", \\\"toast_auto_dismiss\\\", 4)\\n        self._add_grid_chk(f3, \\\"Play Warning Sound\\\", \\\"toast_enable_sound\\\", 5)\\n \\n        btn_frame = tk.Frame(scrollable_frame, bg=TH[\\\"bg\\\"])\\n        btn_frame.pack(fill=tk.X, pady=20)\\n        \\n        tk.Button(\\n            btn_frame, text=\\\"[ PREVIEW IN HUB ]\\\", font=(\\\"Consolas\\\", 10, \\\"bold\\\"),\\n            bg=TH[\\\"bg2\\\"], fg=TH[\\\"accent\\\"], activebackground=TH[\\\"bg3\\\"], activeforeground=TH[\\\"accent\\\"],\\n            relief=tk.FLAT, cursor=\\\"hand2\\\",\\n            command=lambda: self.switch_to_preview_hub(\\\"General Break\\\"), padx=20, pady=8,\\n        ).pack(side=tk.RIGHT)\"",
  "StartLine": "1518",
  "TargetContent": "\"        sound_choices = [\\\"mac_connect\\\", \\\"mac_disconnect\\\", \\\"SystemAsterisk\\\", \\\"SystemExclamation\\\", \\\"SystemHand\\\", \\\"SystemQuestion\\\", \\\"SystemDefault\\\"]\\n        self._add_combo(f2_right, \\\"Sound Effect:\\\", \\\"toast_sound_effect\\\", 10, sound_choices)\\n        \\n        f3 = tk.Frame(scrollable_frame, bg=TH[\\\"bg\\\"])\\n        f3.pack(fill=tk.X, pady=(15, 0))\\n        \\n        self._add_grid_chk(f3, \\\"Enable Shadow/Glow\\\", \\\"toast_shadow\\\", 0)\\n        self._add_grid_chk(f3, \\\"Enable Gradient BG\\\", \\\"toast_gradient\\\", 1)\\n        self._add_grid_chk(f3, \\\"Enable Accent Stripe\\\", \\\"toast_accent_stripe\\\", 2)\\n        self._add_grid_chk(f3, \\\"Show Progress Bar\\\", \\\"toast_progress_bar\\\", 3)\\n        self._add_grid_chk(f3, \\\"Auto-Dismiss\\\", \\\"toast_auto_dismiss\\\", 4)\\n        self._add_grid_chk(f3, \\\"Play Warning Sound\\\", \\\"toast_enable_sound\\\", 5)\\n \\n        btn_frame = tk.Frame(scrollable_frame, bg=TH[\\\"bg\\\"])\\n        btn_frame.pack(fill=tk.X, pady=20)\\n        \\n        tk.Button(\\n            btn_frame, text=\\\"[ PREVIEW_UI ]\\\", font=(\\\"Consolas\\\", 10, \\\"bold\\\"),\\n            bg=TH[\\\"bg2\\\"], fg=TH[\\\"accent\\\"], activebackground=TH[\\\"bg3\\\"], activeforeground=TH[\\\"accent\\\"],\\n            relief=tk.FLAT, cursor=\\\"hand2\\\",\\n            command=self._preview_toast, padx=20, pady=8,\\n        ).pack(side=tk.RIGHT)\"",
  "TargetFile": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Updating toast tab preview and sounds\"",
  "toolSummary": "\"Update toast tab preview and sounds\""
}
```

---

### File: `scratch/extracted/step_127_tc_0.json`
- **Path:** `scratch/extracted/step_127_tc_0.json`
- **Estimated Tokens:** 62
- **mtime:** 1780659608.239

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1540",
  "StartLine": "1470",
  "toolAction": "\"Checking layout of toast tab\"",
  "toolSummary": "\"Check layout of toast tab\""
}
```

---

### File: `scratch/extracted/step_129_tc_0.json`
- **Path:** `scratch/extracted/step_129_tc_0.json`
- **Estimated Tokens:** 64
- **mtime:** 1780659608.24

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1570",
  "StartLine": "1454",
  "toolAction": "\"Viewing toast tab builder range\"",
  "toolSummary": "\"View toast tab builder range\""
}
```

---

### File: `scratch/extracted/step_12_tc_0.json`
- **Path:** `scratch/extracted/step_12_tc_0.json`
- **Estimated Tokens:** 77
- **mtime:** 1780659608.154

```json
{
  "CaseInsensitive": "true",
  "IsRegex": "false",
  "MatchPerLine": "true",
  "Query": "\"power\"",
  "SearchPath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Searching for power references\"",
  "toolSummary": "\"Search for power references\""
}
```

---

### File: `scratch/extracted/step_131_replacement.py`
- **Path:** `scratch/extracted/step_131_replacement.py`
- **Estimated Tokens:** 517
- **mtime:** 1780659608.242

```python
"    def _build_toast_tab(self, tab):\n        tk.Label(tab, text=\"UI / UX CONFIG\", font=(\"Consolas\", 14, \"bold\"), bg=TH[\"bg\"], fg=TH[\"fg\"]).pack(anchor=tk.W, pady=(0, 10))\n        \n        canvas = tk.Canvas(tab, bg=TH[\"bg\"], highlightthickness=0)\n        scrollable_frame = tk.Frame(canvas, bg=TH[\"bg\"])\n        \n        scrollable_frame.bind(\"<Configure>\", lambda e: canvas.configure(scrollregion=canvas.bbox(\"all\")))\n        canvas.create_window((0, 0), window=scrollable_frame, anchor=\"nw\")\n        \n        canvas.pack(side=\"left\", fill=\"both\", expand=True)\n\n        def _on_mousewheel(event):\n            try:\n                w = event.widget.winfo_containing(event.x_root, event.y_root)\n                while w:\n                    if isinstance(w, tk.Canvas):\n                        w.yview_scroll(int(-1*(event.delta/120)), \"units\")\n                        break\n                    w = w.master\n            except Exception:\n                pass\n        tab.winfo_toplevel().bind_all(\"<MouseWheel>\", _on_mousewheel)\n        \n        f_top = tk.Frame(scrollable_frame, bg=TH[\"bg\"])\n        f_top.pack(fill=tk.BOTH, expand=True)\n        \n        f2_left = tk.Frame(f_top, bg=TH[\"bg\"])\n        f2_left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))\n        \n        f2_right = tk.Frame(f_top, bg=TH[\"bg\"])\n        f2_right.pack(side=tk.LEFT, fill=tk.Y)\n\n        # Left Column\n        positions = [\"Top-Left\", \"Top-Center\", \"Top-Right\", \"Bottom-Left\", \"Bottom-Center\", \"Bottom-Right\", \"Middle-Left\", \"Middle-Right\", \"Custom\"]\n        animations = [\"Slide\", \"Fade\", \"Bounce\", \"Scale\", \"Typewriter\", \"Glow\", \"Drop\"]\n        fonts = [\"Segoe UI\", \"Consolas\", \"Cascadia Code\", \"Arial\", \"Verdana\"]\n        actions = [\"dismiss\", \"snooze\", \"settings\"]\n        \n        self._add_combo(f2_left, \"Position:\", \"toast_pos\", 0, positions)\n        self._add_combo(f2_left, \"Animation:\", \"toast_anim_style\", 1, animations)\n      
<truncated 3412 bytes>
```

---

### File: `scratch/extracted/step_131_tc_0.json`
- **Path:** `scratch/extracted/step_131_tc_0.json`
- **Estimated Tokens:** 1,290
- **mtime:** 1780659608.242

```json
{
  "AllowMultiple": "false",
  "Description": "\"Replace _build_toast_tab in health_app.py to fix overlapping layout code, add all 10 custom sound options, and redirect preview to the Preview Hub.\"",
  "EndLine": "1547",
  "Instruction": "\"Replace the entire _build_toast_tab method.\"",
  "ReplacementContent": "\"    def _build_toast_tab(self, tab):\\n        tk.Label(tab, text=\\\"UI / UX CONFIG\\\", font=(\\\"Consolas\\\", 14, \\\"bold\\\"), bg=TH[\\\"bg\\\"], fg=TH[\\\"fg\\\"]).pack(anchor=tk.W, pady=(0, 10))\\n        \\n        canvas = tk.Canvas(tab, bg=TH[\\\"bg\\\"], highlightthickness=0)\\n        scrollable_frame = tk.Frame(canvas, bg=TH[\\\"bg\\\"])\\n        \\n        scrollable_frame.bind(\\\"<Configure>\\\", lambda e: canvas.configure(scrollregion=canvas.bbox(\\\"all\\\")))\\n        canvas.create_window((0, 0), window=scrollable_frame, anchor=\\\"nw\\\")\\n        \\n        canvas.pack(side=\\\"left\\\", fill=\\\"both\\\", expand=True)\\n\\n        def _on_mousewheel(event):\\n            try:\\n                w = event.widget.winfo_containing(event.x_root, event.y_root)\\n                while w:\\n                    if isinstance(w, tk.Canvas):\\n                        w.yview_scroll(int(-1*(event.delta/120)), \\\"units\\\")\\n                        break\\n                    w = w.master\\n            except Exception:\\n                pass\\n        tab.winfo_toplevel().bind_all(\\\"<MouseWheel>\\\", _on_mousewheel)\\n        \\n        f_top = tk.Frame(scrollable_frame, bg=TH[\\\"bg\\\"])\\n        f_top.pack(fill=tk.BOTH, expand=True)\\n        \\n        f2_left = tk.Frame(f_top, bg=TH[\\\"bg\\\"])\\n        f2_left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))\\n        \\n        f2_right = tk.Frame(f_top, bg=TH[\\\"bg\\\"])\\n        f2_right.pack(side=tk.LEFT, fill=tk.Y)\\n\\n        # Left Column\\n        positions = [\\\"Top-Left\\\", \\\"Top-Center\\\", \\\"Top-Right\\\", \\\"Bottom-Left\\\", \\\"Bottom-Center\\\", \\\"Bottom-Right\\\", \\\"Middle-Left\\\", \\\"Middle-Right\\\", \\\"Custom\\\"]\\n        animations = [\\\"Slide\\\", \\\"Fade\\\", \\\"Bounce\\\", \\\"Scale\\\", \\\"Typewriter\\\", \\\"Glow\\\", \\\"Drop\\\"]\\n        fonts = [\\\"Segoe UI\\\", \\\"Consolas\\\", \\\"Cascadia Code\\\", \\\"Arial\\\", \\\"Verdana\\\"]\\n        actions = [\\\"dismiss\\\", \\\"snooze\\\", \\\"settings\\\"]\\n        \\n        self._add_combo(f2_left, \\\"Position:\\\", \\\"toast_pos\\\", 0, positions)\\n        self._add_combo(f2_left, \\\"Animation:\\\", \\\"toast_anim_style\\\", 1, animations)\\n      \n<truncated 3412 bytes>",
  "StartLine": "1454",
  "TargetContent": "\"    def _build_toast_tab(self, tab):\\n        tk.Label(tab, text=\\\"UI / UX CONFIG\\\", font=(\\\"Consolas\\\", 14, \\\"bold\\\"), bg=TH[\\\"bg\\\"], fg=TH[\\\"fg\\\"]).pack(anchor=tk.W, pady=(0, 10))\\n        \\n        canvas = tk.Canvas(tab, bg=TH[\\\"bg\\\"], highlightthickness=0)\\n        scrollable_frame = tk.Frame(canvas, bg=TH[\\\"bg\\\"])\\n        \\n        scrollable_frame.bind(\\\"<Configure>\\\", lambda e: canvas.configure(scrollregion=canvas.bbox(\\\"all\\\")))\\n        canvas.create_window((0, 0), window=scrollable_frame, anchor=\\\"nw\\\")\\n        \\n        canvas.pack(side=\\\"left\\\", fill=\\\"both\\\", expand=True)\\n\\n        def _on_mousewheel(event):\\n            try:\\n                w = event.widget.winfo_containing(event.x_root, event.y_root)\\n                while w:\\n                    if isinstance(w, tk.Canvas):\\n                        w.yview_scroll(int(-1*(event.delta/120)), \\\"units\\\")\\n                        break\\n                    w = w.master\\n            except Exception:\\n                pass\\n        tab.winfo_toplevel().bind_all(\\\"<MouseWheel>\\\", _on_mousewheel)\\n        \\n        f_top = tk.Frame(scrollable_frame, bg=TH[\\\"bg\\\"])\\n        f_top.pack(fill=tk.BOTH, expand=True)\\n        \\n        f2_left = tk.Frame(f_top, bg=TH[\\\"bg\\\"])\\n        f2_left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))\\n        \\n        f2_right = tk.Frame(f_top, bg=TH[\\\"bg\\\"])\\n        f2_right.pack(side=tk.LEFT, fill=tk.Y)\\n\\n        # Left Column\\n        positions = [\\\"Top-Left\\\", \\\"Top-Center\\\", \\\"Top-Right\\\", \\\"Bottom-Left\\\", \\\"Bottom-Center\\\", \\\"Bottom-Right\\\", \\\"Middle-Left\\\", \\\"Middle-Right\\\", \\\"Custom\\\"]\\n        animations = [\\\"Slide\\\", \\\"Fade\\\", \\\"Bounce\\\", \\\"Scale\\\", \\\"Typewriter\\\", \\\"Glow\\\", \\\"Drop\\\"]\\n        fonts = [\\\"Segoe UI\\\", \\\"Consolas\\\", \\\"Cascad        sound_choices = [\\n            \\\"cyber_alert\\\", \\\"retro_beep\\\", \\\"zen_bowl\\\", \\\"echo_ping\\\", \\\"digital_chime\\\",\\n            \\\"sci_fi_sweep\\\", \\\"soft_click\\\", \\\"tech_chirp\\\", \\\"bubble_pop\\\", \\\"crystal_bell\\\",\\n            \\\"mac_connect\\\", \\\"mac_disconnect\\\", \\\"SystemA\n<truncated 3398 bytes>",
  "TargetFile": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Replacing _build_toast_tab\"",
  "toolSummary": "\"Replace _build_toast_tab\""
}
```

---

### File: `scratch/extracted/step_133_tc_0.json`
- **Path:** `scratch/extracted/step_133_tc_0.json`
- **Estimated Tokens:** 67
- **mtime:** 1780659608.245

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1460",
  "StartLine": "1400",
  "toolAction": "\"Viewing grid chk and schedule tab area\"",
  "toolSummary": "\"View grid chk and schedule tab area\""
}
```

---

### File: `scratch/extracted/step_135_replacement.py`
- **Path:** `scratch/extracted/step_135_replacement.py`
- **Estimated Tokens:** 517
- **mtime:** 1780659608.248

```python
"    def _add_grid_chk(self, parent_frame, label, key, row):\n        var = tk.BooleanVar(value=self.settings.get(key, True))\n        tk.Checkbutton(\n            parent_frame, text=label.upper(), variable=var,\n            font=(\"Consolas\", 9), bg=TH[\"bg\"], fg=TH[\"fg_dim\"],\n            selectcolor=TH[\"bg2\"], activebackground=TH[\"bg\"], activeforeground=TH[\"accent\"],\n        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=8)\n        self.entries[key] = (var, \"bool\")\n        var.trace_add(\"write\", lambda *args: self._on_settings_modified())\n\n    def _build_schedule_tab(self, tab):\n        tk.Label(tab, text=\"SYSTEM PARAMETERS\", font=(\"Consolas\", 14, \"bold\"), bg=TH[\"bg\"], fg=TH[\"fg\"]).pack(anchor=tk.W, pady=(0, 20))\n        \n        # We will split it into two columns or just standard grid\n        f1 = tk.Frame(tab, bg=TH[\"bg\"])\n        f1.pack(fill=tk.X)\n\n        self._add_field(f1, \"Short break interval (min):\", \"short_break_interval_min\", 0)\n        self._add_field(f1, \"Short break duration (sec):\", \"short_break_duration_sec\", 1)\n        self._add_field(f1, \"Long break interval (min):\", \"long_break_interval_min\", 2)\n        self._add_field(f1, \"Long break duration (sec):\", \"long_break_duration_sec\", 3)\n        self._add_field(f1, \"Pre-warning (sec):\", \"pre_warning_sec\", 4)\n        self._add_field(f1, \"Latitude:\", \"latitude\", 5)\n        self._add_field(f1, \"Longitude:\", \"longitude\", 6)\n\n        audio_sources = [\"default\", \"random\", \"campfire\", \"forest\", \"night\", \"ocean\", \"rain\", \"waterfall\"]\n        self._add_combo(f1, \"Break Audio Source:\", \"break_audio_source\", 7, audio_sources)\n\n        tk.Label(tab, text=\"MODULES\", font=(\"Consolas\", 14, \"bold\"), bg=TH[\"bg\"], fg=TH[\"fg\"]).pack(anchor=tk.W, pady=(30, 10))\n\n        chk_frame = tk.Frame(tab, bg=TH[\"bg\"])\n        chk_frame.pack(fill=tk.X)\n\n        self._add_chk(chk_frame, \"Enable breathing sound\", \"enable_sound\")\n        self._add_chk
<truncated 146 bytes>
```

---

### File: `scratch/extracted/step_135_tc_0.json`
- **Path:** `scratch/extracted/step_135_tc_0.json`
- **Estimated Tokens:** 737
- **mtime:** 1780659608.247

```json
{
  "AllowMultiple": "false",
  "Description": "\"Restore _add_grid_chk and _build_schedule_tab methods.\"",
  "EndLine": "1419",
  "Instruction": "\"Restore _add_grid_chk and _build_schedule_tab methods.\"",
  "ReplacementContent": "\"    def _add_grid_chk(self, parent_frame, label, key, row):\\n        var = tk.BooleanVar(value=self.settings.get(key, True))\\n        tk.Checkbutton(\\n            parent_frame, text=label.upper(), variable=var,\\n            font=(\\\"Consolas\\\", 9), bg=TH[\\\"bg\\\"], fg=TH[\\\"fg_dim\\\"],\\n            selectcolor=TH[\\\"bg2\\\"], activebackground=TH[\\\"bg\\\"], activeforeground=TH[\\\"accent\\\"],\\n        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=8)\\n        self.entries[key] = (var, \\\"bool\\\")\\n        var.trace_add(\\\"write\\\", lambda *args: self._on_settings_modified())\\n\\n    def _build_schedule_tab(self, tab):\\n        tk.Label(tab, text=\\\"SYSTEM PARAMETERS\\\", font=(\\\"Consolas\\\", 14, \\\"bold\\\"), bg=TH[\\\"bg\\\"], fg=TH[\\\"fg\\\"]).pack(anchor=tk.W, pady=(0, 20))\\n        \\n        # We will split it into two columns or just standard grid\\n        f1 = tk.Frame(tab, bg=TH[\\\"bg\\\"])\\n        f1.pack(fill=tk.X)\\n\\n        self._add_field(f1, \\\"Short break interval (min):\\\", \\\"short_break_interval_min\\\", 0)\\n        self._add_field(f1, \\\"Short break duration (sec):\\\", \\\"short_break_duration_sec\\\", 1)\\n        self._add_field(f1, \\\"Long break interval (min):\\\", \\\"long_break_interval_min\\\", 2)\\n        self._add_field(f1, \\\"Long break duration (sec):\\\", \\\"long_break_duration_sec\\\", 3)\\n        self._add_field(f1, \\\"Pre-warning (sec):\\\", \\\"pre_warning_sec\\\", 4)\\n        self._add_field(f1, \\\"Latitude:\\\", \\\"latitude\\\", 5)\\n        self._add_field(f1, \\\"Longitude:\\\", \\\"longitude\\\", 6)\\n\\n        audio_sources = [\\\"default\\\", \\\"random\\\", \\\"campfire\\\", \\\"forest\\\", \\\"night\\\", \\\"ocean\\\", \\\"rain\\\", \\\"waterfall\\\"]\\n        self._add_combo(f1, \\\"Break Audio Source:\\\", \\\"break_audio_source\\\", 7, audio_sources)\\n\\n        tk.Label(tab, text=\\\"MODULES\\\", font=(\\\"Consolas\\\", 14, \\\"bold\\\"), bg=TH[\\\"bg\\\"], fg=TH[\\\"fg\\\"]).pack(anchor=tk.W, pady=(30, 10))\\n\\n        chk_frame = tk.Frame(tab, bg=TH[\\\"bg\\\"])\\n        chk_frame.pack(fill=tk.X)\\n\\n        self._add_chk(chk_frame, \\\"Enable breathing sound\\\", \\\"enable_sound\\\")\\n        self._add_chk\n<truncated 146 bytes>",
  "StartLine": "1417",
  "TargetContent": "\"    def _add_grid_chk(self, parent_frame, label, key, row):\\n        var = tk.BooleanVar(value=self.settings.get(key,     def _build_toast_tab(self, tab):\"",
  "TargetFile": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Restoring grid chk and schedule tab\"",
  "toolSummary": "\"Restore grid chk and schedule tab\""
}
```

---

### File: `scratch/extracted/step_137_tc_0.json`
- **Path:** `scratch/extracted/step_137_tc_0.json`
- **Estimated Tokens:** 64
- **mtime:** 1780659608.25

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1465",
  "StartLine": "1445",
  "toolAction": "\"Checking build toast tab header\"",
  "toolSummary": "\"Check build toast tab header\""
}
```

---

### File: `scratch/extracted/step_139_replacement.py`
- **Path:** `scratch/extracted/step_139_replacement.py`
- **Estimated Tokens:** 45
- **mtime:** 1780659608.254

```python
"    def _build_toast_tab(self, tab):\n        tk.Label(tab, text=\"UI / UX CONFIG\", font=(\"Consolas\", 14, \"bold\"), bg=TH[\"bg\"], fg=TH[\"fg\"]).pack(anchor=tk.W, pady=(0, 10))"
```

---

### File: `scratch/extracted/step_139_tc_0.json`
- **Path:** `scratch/extracted/step_139_tc_0.json`
- **Estimated Tokens:** 234
- **mtime:** 1780659608.251

```json
{
  "AllowMultiple": "false",
  "Description": "\"Restore missing _build_toast_tab function header.\"",
  "EndLine": "1454",
  "Instruction": "\"Restore _build_toast_tab header.\"",
  "ReplacementContent": "\"    def _build_toast_tab(self, tab):\\n        tk.Label(tab, text=\\\"UI / UX CONFIG\\\", font=(\\\"Consolas\\\", 14, \\\"bold\\\"), bg=TH[\\\"bg\\\"], fg=TH[\\\"fg\\\"]).pack(anchor=tk.W, pady=(0, 10))\"",
  "StartLine": "1452",
  "TargetContent": "\"        self._add_chk(chk_frame, \\\"Run breaks during games\\\", \\\"run_during_game\\\")\\n        tk.Label(tab, text=\\\"UI / UX CONFIG\\\", font=(\\\"Consolas\\\", 14, \\\"bold\\\"), bg=TH[\\\"bg\\\"], fg=TH[\\\"fg\\\"]).pack(anchor=tk.W, pady=(0, 10))\"",
  "TargetFile": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Restoring _build_toast_tab header\"",
  "toolSummary": "\"Restore _build_toast_tab header\""
}
```

---

### File: `scratch/extracted/step_141_tc_0.json`
- **Path:** `scratch/extracted/step_141_tc_0.json`
- **Estimated Tokens:** 65
- **mtime:** 1780659608.254

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1455",
  "StartLine": "1445",
  "toolAction": "\"Checking checkbuttons restoration\"",
  "toolSummary": "\"Check checkbuttons restoration\""
}
```

---

### File: `scratch/extracted/step_143_replacement.py`
- **Path:** `scratch/extracted/step_143_replacement.py`
- **Estimated Tokens:** 42
- **mtime:** 1780659608.259

```python
"        self._add_chk(chk_frame, \"Dim screen during breaks\", \"enable_dimming\")\n        self._add_chk(chk_frame, \"Run breaks during games\", \"run_during_game\")"
```

---

### File: `scratch/extracted/step_143_tc_0.json`
- **Path:** `scratch/extracted/step_143_tc_0.json`
- **Estimated Tokens:** 188
- **mtime:** 1780659608.256

```json
{
  "AllowMultiple": "false",
  "Description": "\"Restore Run breaks during games checkbutton.\"",
  "EndLine": "1452",
  "Instruction": "\"Restore Run breaks during games checkbutton.\"",
  "ReplacementContent": "\"        self._add_chk(chk_frame, \\\"Dim screen during breaks\\\", \\\"enable_dimming\\\")\\n        self._add_chk(chk_frame, \\\"Run breaks during games\\\", \\\"run_during_game\\\")\"",
  "StartLine": "1451",
  "TargetContent": "\"        self._add_chk(chk_frame, \\\"Dim screen during breaks\\\", \\\"enable_dimming\\\")\"",
  "TargetFile": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Restoring games run checkbutton\"",
  "toolSummary": "\"Restore games run checkbutton\""
}
```

---

### File: `scratch/extracted/step_145_tc_0.json`
- **Path:** `scratch/extracted/step_145_tc_0.json`
- **Estimated Tokens:** 64
- **mtime:** 1780659608.266

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1670",
  "StartLine": "1550",
  "toolAction": "\"Viewing health toast tab builder\"",
  "toolSummary": "\"View health toast tab builder\""
}
```

---

### File: `scratch/extracted/step_147_tc_0.json`
- **Path:** `scratch/extracted/step_147_tc_0.json`
- **Estimated Tokens:** 64
- **mtime:** 1780659608.273

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1690",
  "StartLine": "1671",
  "toolAction": "\"Viewing health toast builder end\"",
  "toolSummary": "\"View health toast builder end\""
}
```

---

### File: `scratch/extracted/step_149_replacement.py`
- **Path:** `scratch/extracted/step_149_replacement.py`
- **Estimated Tokens:** 397
- **mtime:** 1780659608.287

```python
"        sound_choices = [\n            \"cyber_alert\", \"retro_beep\", \"zen_bowl\", \"echo_ping\", \"digital_chime\",\n            \"sci_fi_sweep\", \"soft_click\", \"tech_chirp\", \"bubble_pop\", \"crystal_bell\",\n            \"mac_connect\", \"mac_disconnect\", \"SystemAsterisk\", \"SystemExclamation\",\n            \"SystemHand\", \"SystemQuestion\", \"SystemDefault\"\n        ]\n        self._add_combo(f_vis_right, \"Sound Effect:\", \"ht_toast_sound_effect\", 10, sound_choices)\n \n        f3 = tk.Frame(f_vis, bg=TH[\"bg\"])\n        f3.pack(fill=tk.X, pady=(15, 0))\n        \n        self._add_grid_chk(f3, \"Enable Shadow/Glow\", \"ht_toast_shadow\", 0)\n        self._add_grid_chk(f3, \"Enable Gradient BG\", \"ht_toast_gradient\", 1)\n        self._add_grid_chk(f3, \"Enable Accent Stripe\", \"ht_toast_accent_stripe\", 2)\n        self._add_grid_chk(f3, \"Show Progress Bar\", \"ht_toast_progress_bar\", 3)\n        self._add_grid_chk(f3, \"Auto-Dismiss\", \"ht_toast_auto_dismiss\", 4)\n        self._add_grid_chk(f3, \"Play Sound\", \"ht_toast_enable_sound\", 5)\n \n        btn_frame = tk.Frame(scrollable_frame, bg=TH[\"bg\"])\n        btn_frame.pack(fill=tk.X, pady=(10, 0))\n \n        tk.Button(\n            btn_frame, text=\"[ PREVIEW IN HUB ]\", font=(\"Consolas\", 10, \"bold\"),\n            bg=TH[\"bg2\"], fg=TH[\"accent\"], activebackground=TH[\"bg3\"], activeforeground=TH[\"accent\"],\n            relief=tk.FLAT, cursor=\"hand2\",\n            command=lambda: self.switch_to_preview_hub(\"Health Tip\"), padx=20, pady=8,\n        ).pack(side=tk.RIGHT)"
```

---

### File: `scratch/extracted/step_149_tc_0.json`
- **Path:** `scratch/extracted/step_149_tc_0.json`
- **Estimated Tokens:** 963
- **mtime:** 1780659608.282

```json
{
  "AllowMultiple": "false",
  "Description": "\"Update health toast tab: add all 10 custom sound options and redirect preview to the Preview Hub.\"",
  "EndLine": "1683",
  "Instruction": "\"Modify sound choices and preview button in _build_health_toast_tab.\"",
  "ReplacementContent": "\"        sound_choices = [\\n            \\\"cyber_alert\\\", \\\"retro_beep\\\", \\\"zen_bowl\\\", \\\"echo_ping\\\", \\\"digital_chime\\\",\\n            \\\"sci_fi_sweep\\\", \\\"soft_click\\\", \\\"tech_chirp\\\", \\\"bubble_pop\\\", \\\"crystal_bell\\\",\\n            \\\"mac_connect\\\", \\\"mac_disconnect\\\", \\\"SystemAsterisk\\\", \\\"SystemExclamation\\\",\\n            \\\"SystemHand\\\", \\\"SystemQuestion\\\", \\\"SystemDefault\\\"\\n        ]\\n        self._add_combo(f_vis_right, \\\"Sound Effect:\\\", \\\"ht_toast_sound_effect\\\", 10, sound_choices)\\n \\n        f3 = tk.Frame(f_vis, bg=TH[\\\"bg\\\"])\\n        f3.pack(fill=tk.X, pady=(15, 0))\\n        \\n        self._add_grid_chk(f3, \\\"Enable Shadow/Glow\\\", \\\"ht_toast_shadow\\\", 0)\\n        self._add_grid_chk(f3, \\\"Enable Gradient BG\\\", \\\"ht_toast_gradient\\\", 1)\\n        self._add_grid_chk(f3, \\\"Enable Accent Stripe\\\", \\\"ht_toast_accent_stripe\\\", 2)\\n        self._add_grid_chk(f3, \\\"Show Progress Bar\\\", \\\"ht_toast_progress_bar\\\", 3)\\n        self._add_grid_chk(f3, \\\"Auto-Dismiss\\\", \\\"ht_toast_auto_dismiss\\\", 4)\\n        self._add_grid_chk(f3, \\\"Play Sound\\\", \\\"ht_toast_enable_sound\\\", 5)\\n \\n        btn_frame = tk.Frame(scrollable_frame, bg=TH[\\\"bg\\\"])\\n        btn_frame.pack(fill=tk.X, pady=(10, 0))\\n \\n        tk.Button(\\n            btn_frame, text=\\\"[ PREVIEW IN HUB ]\\\", font=(\\\"Consolas\\\", 10, \\\"bold\\\"),\\n            bg=TH[\\\"bg2\\\"], fg=TH[\\\"accent\\\"], activebackground=TH[\\\"bg3\\\"], activeforeground=TH[\\\"accent\\\"],\\n            relief=tk.FLAT, cursor=\\\"hand2\\\",\\n            command=lambda: self.switch_to_preview_hub(\\\"Health Tip\\\"), padx=20, pady=8,\\n        ).pack(side=tk.RIGHT)\"",
  "StartLine": "1660",
  "TargetContent": "\"        sound_choices = [\\\"mac_connect\\\", \\\"mac_disconnect\\\", \\\"SystemAsterisk\\\", \\\"SystemExclamation\\\", \\\"SystemHand\\\", \\\"SystemQuestion\\\", \\\"SystemDefault\\\"]\\n        self._add_combo(f_vis_right, \\\"Sound Effect:\\\", \\\"ht_toast_sound_effect\\\", 10, sound_choices)\\n \\n        f3 = tk.Frame(f_vis, bg=TH[\\\"bg\\\"])\\n        f3.pack(fill=tk.X, pady=(15, 0))\\n        \\n        self._add_grid_chk(f3, \\\"Enable Shadow/Glow\\\", \\\"ht_toast_shadow\\\", 0)\\n        self._add_grid_chk(f3, \\\"Enable Gradient BG\\\", \\\"ht_toast_gradient\\\", 1)\\n        self._add_grid_chk(f3, \\\"Enable Accent Stripe\\\", \\\"ht_toast_accent_stripe\\\", 2)\\n        self._add_grid_chk(f3, \\\"Show Progress Bar\\\", \\\"ht_toast_progress_bar\\\", 3)\\n        self._add_grid_chk(f3, \\\"Auto-Dismiss\\\", \\\"ht_toast_auto_dismiss\\\", 4)\\n        self._add_grid_chk(f3, \\\"Play Sound\\\", \\\"ht_toast_enable_sound\\\", 5)\\n \\n        btn_frame = tk.Frame(scrollable_frame, bg=TH[\\\"bg\\\"])\\n        btn_frame.pack(fill=tk.X, pady=(10, 0))\\n \\n        tk.Button(\\n            btn_frame, text=\\\"[ PREVIEW_HEALTH_TOAST ]\\\", font=(\\\"Consolas\\\", 10, \\\"bold\\\"),\\n            bg=TH[\\\"bg2\\\"], fg=TH[\\\"accent\\\"], activebackground=TH[\\\"bg3\\\"], activeforeground=TH[\\\"accent\\\"],\\n            relief=tk.FLAT, cursor=\\\"hand2\\\",\\n            command=self._preview_health_toast, padx=20, pady=8,\\n        ).pack(side=tk.RIGHT)\"",
  "TargetFile": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Updating health toast tab preview and sounds\"",
  "toolSummary": "\"Update health toast tab preview and sounds\""
}
```

---

### File: `scratch/extracted/step_14_tc_0.json`
- **Path:** `scratch/extracted/step_14_tc_0.json`
- **Estimated Tokens:** 77
- **mtime:** 1780659608.166

```json
{
  "CaseInsensitive": "true",
  "IsRegex": "false",
  "MatchPerLine": "true",
  "Query": "\"toast\"",
  "SearchPath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Searching for toast references\"",
  "toolSummary": "\"Search for toast references\""
}
```

---

### File: `scratch/extracted/step_164_tc_0.json`
- **Path:** `scratch/extracted/step_164_tc_0.json`
- **Estimated Tokens:** 76
- **mtime:** 1780659608.297

```json
{
  "IsRegex": "false",
  "MatchPerLine": "true",
  "Query": "\"_build_health_toast_tab\"",
  "SearchPath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Searching for tab builder\"",
  "toolSummary": "\"Searching for _build_health_toast_tab\""
}
```

---

### File: `scratch/extracted/step_166_tc_0.json`
- **Path:** `scratch/extracted/step_166_tc_0.json`
- **Estimated Tokens:** 75
- **mtime:** 1780659608.303

```json
{
  "IsRegex": "false",
  "MatchPerLine": "true",
  "Query": "\"class SettingsWindow\"",
  "SearchPath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Searching for SettingsWindow\"",
  "toolSummary": "\"Searching for SettingsWindow class\""
}
```

---

### File: `scratch/extracted/step_168_tc_0.json`
- **Path:** `scratch/extracted/step_168_tc_0.json`
- **Estimated Tokens:** 81
- **mtime:** 1780659608.31

```json
{
  "CaseInsensitive": "true",
  "IsRegex": "false",
  "MatchPerLine": "true",
  "Query": "\"Settings\"",
  "SearchPath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Searching for Settings in health_app.py\"",
  "toolSummary": "\"Searching for settings keyword\""
}
```

---

### File: `scratch/extracted/step_170_tc_0.json`
- **Path:** `scratch/extracted/step_170_tc_0.json`
- **Estimated Tokens:** 62
- **mtime:** 1780659608.316

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "100",
  "StartLine": "1",
  "toolAction": "\"Viewing health_app.py header\"",
  "toolSummary": "\"Viewing health_app.py header\""
}
```

---

### File: `scratch/extracted/step_184_tc_0.json`
- **Path:** `scratch/extracted/step_184_tc_0.json`
- **Estimated Tokens:** 72
- **mtime:** 1780659608.326

```json
{
  "IsRegex": "true",
  "MatchPerLine": "true",
  "Query": "\"^class \\\\w+\"",
  "SearchPath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Searching for classes in health_app.py\"",
  "toolSummary": "\"Searching for classes\""
}
```

---

### File: `scratch/extracted/step_186_tc_0.json`
- **Path:** `scratch/extracted/step_186_tc_0.json`
- **Estimated Tokens:** 72
- **mtime:** 1780659608.332

```json
{
  "IsRegex": "false",
  "MatchPerLine": "true",
  "Query": "\"def \"",
  "SearchPath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Searching for functions in health_app.py\"",
  "toolSummary": "\"Searching for def keyword\""
}
```

---

### File: `scratch/extracted/step_188_tc_0.json`
- **Path:** `scratch/extracted/step_188_tc_0.json`
- **Estimated Tokens:** 66
- **mtime:** 1780659608.34

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "200",
  "StartLine": "101",
  "toolAction": "\"Viewing health_app.py lines 101-200\"",
  "toolSummary": "\"Viewing health_app.py lines 101-200\""
}
```

---

### File: `scratch/extracted/step_18_tc_0.json`
- **Path:** `scratch/extracted/step_18_tc_0.json`
- **Estimated Tokens:** 62
- **mtime:** 1780659608.167

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1600",
  "StartLine": "801",
  "toolAction": "\"Viewing health_app.py logic\"",
  "toolSummary": "\"View health_app.py logic\""
}
```

---

### File: `scratch/extracted/step_190_tc_0.json`
- **Path:** `scratch/extracted/step_190_tc_0.json`
- **Estimated Tokens:** 74
- **mtime:** 1780659608.346

```json
{
  "IsRegex": "false",
  "MatchPerLine": "true",
  "Query": "\"class \"",
  "SearchPath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Searching for class keyword\"",
  "toolSummary": "\"Searching for class keyword in health_app.py\""
}
```

---

### File: `scratch/extracted/step_192_tc_0.json`
- **Path:** `scratch/extracted/step_192_tc_0.json`
- **Estimated Tokens:** 98
- **mtime:** 1780659608.352

```json
{
  "CommandLine": "\"python -c \\\"import sys; [print(f'{i+1}: {line.strip()}') for i, line in enumerate(open('HealthApp/health_app.py', encoding='utf-8')) if 'class ' in line]\\\"\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Finding classes via Python script\"",
  "toolSummary": "\"Finding classes in health_app.py\""
}
```

---

### File: `scratch/extracted/step_194_tc_0.json`
- **Path:** `scratch/extracted/step_194_tc_0.json`
- **Estimated Tokens:** 67
- **mtime:** 1780659608.358

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1898",
  "StartLine": "1198",
  "toolAction": "\"Viewing SettingsWindow class in health_app.py\"",
  "toolSummary": "\"Viewing SettingsWindow code\""
}
```

---

### File: `scratch/extracted/step_196_tc_0.json`
- **Path:** `scratch/extracted/step_196_tc_0.json`
- **Estimated Tokens:** 104
- **mtime:** 1780659608.36

```json
{
  "CommandLine": "\"python -c \\\"import sys; [print(f'{i+1}: {line.strip()}') for i, line in enumerate(open('HealthApp/health_app.py', encoding='utf-8')) if '_build_preview_hub_tab' in line]\\\"\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Finding preview hub builder\"",
  "toolSummary": "\"Finding preview hub builder in health_app.py\""
}
```

---

### File: `scratch/extracted/step_198_tc_0.json`
- **Path:** `scratch/extracted/step_198_tc_0.json`
- **Estimated Tokens:** 103
- **mtime:** 1780659608.362

```json
{
  "CommandLine": "\"python -c \\\"import sys; [print(f'{i+1198}: {line.strip()}') for i, line in enumerate(open('HealthApp/health_app.py', encoding='utf-8').readlines()[1197:1910]) if 'def ' in line]\\\"\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Finding SettingsWindow methods\"",
  "toolSummary": "\"Finding SettingsWindow methods\""
}
```

---

### File: `scratch/extracted/step_202_tc_0.json`
- **Path:** `scratch/extracted/step_202_tc_0.json`
- **Estimated Tokens:** 105
- **mtime:** 1780659608.363

```json
{
  "CommandLine": "\"python -c \\\"import sys; [print(f'{i+1}: {line.strip()}') for i, line in enumerate(open('HealthApp/health_app.py', encoding='utf-8')) if 'DEFAULT_SETTINGS' in line]\\\"\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Finding DEFAULT_SETTINGS in health_app.py\"",
  "toolSummary": "\"Finding DEFAULT_SETTINGS in health_app.py\""
}
```

---

### File: `scratch/extracted/step_204_tc_0.json`
- **Path:** `scratch/extracted/step_204_tc_0.json`
- **Estimated Tokens:** 69
- **mtime:** 1780659608.364

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "450",
  "StartLine": "328",
  "toolAction": "\"Viewing DEFAULT_SETTINGS in health_app.py\"",
  "toolSummary": "\"Viewing DEFAULT_SETTINGS in health_app.py\""
}
```

---

### File: `scratch/extracted/step_20_tc_0.json`
- **Path:** `scratch/extracted/step_20_tc_0.json`
- **Estimated Tokens:** 64
- **mtime:** 1780659608.169

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "2400",
  "StartLine": "1601",
  "toolAction": "\"Viewing health_app.py main loop\"",
  "toolSummary": "\"View health_app.py main loop\""
}
```

---

### File: `scratch/extracted/step_212_tc_0.json`
- **Path:** `scratch/extracted/step_212_tc_0.json`
- **Estimated Tokens:** 715
- **mtime:** 1780659608.367

```json
{
  "ArtifactMetadata": "{\"ArtifactType\":\"task\",\"RequestFeedback\":true,\"Summary\":\"Tasks checklist for the Health App Redesign and Upgrades, including Sequential Toast Queue, Sleep Resume Timer Reset, Sound Customization, and a Dedicated Settings Preview Hub tab.\"}",
  "CodeContent": "\"# Tasks: Health App Redesign & Upgrades\\n\\n## Dependencies\\n- **Sequential Toast Queue** (US1) is required before desktop notification preview triggers.\\n- **WAV Sound Synthesis** (US3) is required before sound test triggers.\\n- **Modern Layout Cards** (US4) is required before building the Preview Hub (US5).\\n\\n## Parallel Opportunities\\n- **US1** (Sequential Queue) and **US2** (Sleep/Wake detection) can be developed in parallel since they touch different parts of `toast_utils.py` and the main scheduler loops.\\n- **US3** (Sound Customization assets) can be worked on concurrently with the UI redesign.\\n\\n---\\n\\n## Phase 1: Setup & Sound Assets\\n\\n- [ ] T001 Verify or create sound assets directory `HealthApp/resources/sounds/`\\n- [ ] T002 Implement a programmatic sound synthesizer helper in `HealthApp/health_app.py` to generate 10 clean, sci-fi/tech WAV sound effects if not already present\\n\\n## Phase 2: Core Logic Upgrades (Queue & Sleep Resume)\\n\\n- [ ] T003 [P] Implement thread-safe sequential `ToastQueue` class with 1.5s delay inside `toast_utils.py`\\n- [ ] T004 [P] Hook `BaseToast.show()` into the `ToastQueue` so all notifications queue up sequentially\\n- [ ] T005 [P] Implement loop time delta tracking (`time.time() - last_loop > 10.0`) in scheduler loops in `HealthApp/health_app.py` to reset warning states and break timers upon system wake-from-sleep\\n\\n## Phase 3: Settings UI Cyberpunk Redesign\\n\\n- [ ] T006 [P] Remove `trace_add` screen popups on settings input field modifications to prevent toast windows popping up on the desktop while editing\\n- [ ] T007 Redesign `SettingsWindow` sidebar navigation and content tab layouts with neon cyan accents (`#00f0ff`) and sharp, flat cards (`bg=TH[\\\"bg2\\\"]`, border width 1, color `TH[\\\"border\\\"]`)\\n- [ ] T008 Update sound configuration dropdowns and checkboxes across \\\"Toast FX\\\", \\\"Health Toast\\\", \\\"Brightness Care\\\", and \\\"Night Care\\\" tabs to support the 10 custom synthesized sound effects\\n\\n## Phase 4: Dedicated Preview Hub\\n\\n- [ ] T009 Implement `_build_previ\n<truncated 830 bytes>",
  "Description": "\"Create spec-kit style tasks.md file detailing the required steps for Health App settings redesign, toast queue, sleep reset, and preview hub.\"",
  "IsArtifact": "true",
  "Overwrite": "true",
  "TargetFile": "\"C:\\\\Users\\\\NANDHA A\\\\.gemini\\\\antigravity-ide\\\\brain\\\\1237cb3f-efd0-4a57-b440-f74287d1898a\\\\tasks.md\"",
  "toolAction": "\"Writing tasks file\"",
  "toolSummary": "\"Writing tasks.md\""
}
```

---

### File: `scratch/extracted/step_214_tc_0.json`
- **Path:** `scratch/extracted/step_214_tc_0.json`
- **Estimated Tokens:** 679
- **mtime:** 1780659608.368

```json
{
  "ArtifactMetadata": "{\"ArtifactType\":\"task\",\"RequestFeedback\":true,\"Summary\":\"Perfected tasks checklist with explicit file paths and spec-kit formatting for Health App Redesign and Upgrades.\"}",
  "CodeContent": "\"# Tasks: Health App Redesign & Upgrades\\n\\n## Dependencies\\n- **Sequential Toast Queue** (US1) is required before desktop notification preview triggers.\\n- **WAV Sound Synthesis** (US3) is required before sound test triggers.\\n- **Modern Layout Cards** (US4) is required before building the Preview Hub (US5).\\n\\n## Parallel Opportunities\\n- **US1** (Sequential Queue) and **US2** (Sleep/Wake detection) can be developed in parallel since they touch different parts of `toast_utils.py` and the main scheduler loops.\\n- **US3** (Sound Customization assets) can be worked on concurrently with the UI redesign.\\n\\n---\\n\\n## Phase 1: Setup & Sound Assets\\n\\n- [ ] T001 Verify or create sound assets directory `HealthApp/resources/sounds/`\\n- [ ] T002 Implement a programmatic sound synthesizer helper in `HealthApp/health_app.py` to generate 10 clean, sci-fi/tech WAV sound effects if not already present\\n\\n## Phase 2: Core Logic Upgrades (Queue & Sleep Resume)\\n\\n- [ ] T003 [P] Implement thread-safe sequential `ToastQueue` class with 1.5s delay inside `toast_utils.py`\\n- [ ] T004 [P] Hook `BaseToast.show()` inside `toast_utils.py` and `HealthApp/health_app.py` into the `ToastQueue` so all notifications queue up sequentially\\n- [ ] T005 [P] Implement loop time delta tracking (`time.time() - last_loop > 10.0`) in scheduler loops in `HealthApp/health_app.py` to reset warning states and break timers upon system wake-from-sleep\\n\\n## Phase 3: Settings UI Cyberpunk Redesign\\n\\n- [ ] T006 [P] Remove `trace_add` screen popups on settings input field modifications in `HealthApp/health_app.py` to prevent toast windows popping up on the desktop while editing\\n- [ ] T007 Redesign `SettingsWindow` sidebar navigation and content tab layouts in `HealthApp/health_app.py` with neon cyan accents (`#00f0ff`) and sharp, flat cards (`bg=TH[\\\"bg2\\\"]`, border width 1, color `TH[\\\"border\\\"]`)\\n- [ ] T008 Update sound configuration dropdowns and checkboxes across \\\"Toast FX\\\", \\\"Health Toast\\\", \\\"Brightness Care\\\", and \\\"Night Care\\\" tabs in `HealthApp\n<truncated 1120 bytes>",
  "Description": "\"Overwrite tasks.md with exact file paths for all checklist tasks.\"",
  "IsArtifact": "true",
  "Overwrite": "true",
  "TargetFile": "\"C:\\\\Users\\\\NANDHA A\\\\.gemini\\\\antigravity-ide\\\\brain\\\\1237cb3f-efd0-4a57-b440-f74287d1898a\\\\tasks.md\"",
  "toolAction": "\"Perfecting tasks file\"",
  "toolSummary": "\"Updating tasks.md\""
}
```

---

### File: `scratch/extracted/step_216_tc_0.json`
- **Path:** `scratch/extracted/step_216_tc_0.json`
- **Estimated Tokens:** 675
- **mtime:** 1780659608.371

```json
{
  "ArtifactMetadata": "{\"ArtifactType\":\"task\",\"RequestFeedback\":true,\"Summary\":\"Syncing task.md with tasks.md containing the spec-kit checklist formatting.\"}",
  "CodeContent": "\"# Tasks: Health App Redesign & Upgrades\\n\\n## Dependencies\\n- **Sequential Toast Queue** (US1) is required before desktop notification preview triggers.\\n- **WAV Sound Synthesis** (US3) is required before sound test triggers.\\n- **Modern Layout Cards** (US4) is required before building the Preview Hub (US5).\\n\\n## Parallel Opportunities\\n- **US1** (Sequential Queue) and **US2** (Sleep/Wake detection) can be developed in parallel since they touch different parts of `toast_utils.py` and the main scheduler loops.\\n- **US3** (Sound Customization assets) can be worked on concurrently with the UI redesign.\\n\\n---\\n\\n## Phase 1: Setup & Sound Assets\\n\\n- [ ] T001 Verify or create sound assets directory `HealthApp/resources/sounds/`\\n- [ ] T002 Implement a programmatic sound synthesizer helper in `HealthApp/health_app.py` to generate 10 clean, sci-fi/tech WAV sound effects if not already present\\n\\n## Phase 2: Core Logic Upgrades (Queue & Sleep Resume)\\n\\n- [ ] T003 [P] Implement thread-safe sequential `ToastQueue` class with 1.5s delay inside `toast_utils.py`\\n- [ ] T004 [P] Hook `BaseToast.show()` inside `toast_utils.py` and `HealthApp/health_app.py` into the `ToastQueue` so all notifications queue up sequentially\\n- [ ] T005 [P] Implement loop time delta tracking (`time.time() - last_loop > 10.0`) in scheduler loops in `HealthApp/health_app.py` to reset warning states and break timers upon system wake-from-sleep\\n\\n## Phase 3: Settings UI Cyberpunk Redesign\\n\\n- [ ] T006 [P] Remove `trace_add` screen popups on settings input field modifications in `HealthApp/health_app.py` to prevent toast windows popping up on the desktop while editing\\n- [ ] T007 Redesign `SettingsWindow` sidebar navigation and content tab layouts in `HealthApp/health_app.py` with neon cyan accents (`#00f0ff`) and sharp, flat cards (`bg=TH[\\\"bg2\\\"]`, border width 1, color `TH[\\\"border\\\"]`)\\n- [ ] T008 Update sound configuration dropdowns and checkboxes across \\\"Toast FX\\\", \\\"Health Toast\\\", \\\"Brightness Care\\\", and \\\"Night Care\\\" tabs in `HealthApp\n<truncated 1120 bytes>",
  "Description": "\"Overwrite task.md in the brain directory with the matching spec-kit tasks checklist content.\"",
  "IsArtifact": "true",
  "Overwrite": "true",
  "TargetFile": "\"C:\\\\Users\\\\NANDHA A\\\\.gemini\\\\antigravity-ide\\\\brain\\\\1237cb3f-efd0-4a57-b440-f74287d1898a\\\\task.md\"",
  "toolAction": "\"Syncing task file\"",
  "toolSummary": "\"Updating task.md\""
}
```

---

### File: `scratch/extracted/step_22_tc_0.json`
- **Path:** `scratch/extracted/step_22_tc_0.json`
- **Estimated Tokens:** 58
- **mtime:** 1780659608.171

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "StartLine": "2401",
  "toolAction": "\"Viewing rest of health_app.py\"",
  "toolSummary": "\"View rest of health_app.py\""
}
```

---

### File: `scratch/extracted/step_230_tc_0.json`
- **Path:** `scratch/extracted/step_230_tc_0.json`
- **Estimated Tokens:** 112
- **mtime:** 1780659608.373

```json
{
  "CommandLine": "\"python -c \\\"import sys; [print(f'{i+1}: {line.strip()}') for i, line in enumerate(open('HealthApp/health_app.py', encoding='utf-8')) if 'ensure_sound_effects' in line or 'synthesize' in line]\\\"\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Searching for sound synthesis methods\"",
  "toolSummary": "\"Searching for sound methods in health_app.py\""
}
```

---

### File: `scratch/extracted/step_232_tc_0.json`
- **Path:** `scratch/extracted/step_232_tc_0.json`
- **Estimated Tokens:** 63
- **mtime:** 1780659608.374

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "680",
  "StartLine": "570",
  "toolAction": "\"Viewing sound methods in health_app.py\"",
  "toolSummary": "\"Viewing sound methods\""
}
```

---

### File: `scratch/extracted/step_234_tc_0.json`
- **Path:** `scratch/extracted/step_234_tc_0.json`
- **Estimated Tokens:** 67
- **mtime:** 1780659608.376

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "750",
  "StartLine": "681",
  "toolAction": "\"Viewing remainder of _synthesize_wav\"",
  "toolSummary": "\"Viewing remaining sound synthesis code\""
}
```

---

### File: `scratch/extracted/step_238_tc_0.json`
- **Path:** `scratch/extracted/step_238_tc_0.json`
- **Estimated Tokens:** 109
- **mtime:** 1780659608.377

```json
{
  "CommandLine": "\"python -c \\\"import sys; [print(f'{i+1}: {line.strip()}') for i, line in enumerate(open('HealthApp/health_app.py', encoding='utf-8')) if '_scheduler_loop' in line or '_health_toast_loop' in line]\\\"\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Finding loop definitions\"",
  "toolSummary": "\"Finding loop definitions in health_app.py\""
}
```

---

### File: `scratch/extracted/step_240_tc_0.json`
- **Path:** `scratch/extracted/step_240_tc_0.json`
- **Estimated Tokens:** 68
- **mtime:** 1780659608.379

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "2200",
  "StartLine": "2100",
  "toolAction": "\"Viewing scheduler loop methods\"",
  "toolSummary": "\"Viewing scheduler and health toast loop code\""
}
```

---

### File: `scratch/extracted/step_242_tc_0.json`
- **Path:** `scratch/extracted/step_242_tc_0.json`
- **Estimated Tokens:** 105
- **mtime:** 1780659608.38

```json
{
  "CommandLine": "\"python -c \\\"import sys; [print(f'{i+1}: {line.strip()}') for i, line in enumerate(open('HealthApp/health_app.py', encoding='utf-8')) if '_on_settings_modified' in line]\\\"\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Finding settings modification handler\"",
  "toolSummary": "\"Finding _on_settings_modified references\""
}
```

---

### File: `scratch/extracted/step_244_tc_0.json`
- **Path:** `scratch/extracted/step_244_tc_0.json`
- **Estimated Tokens:** 65
- **mtime:** 1780659608.382

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1585",
  "StartLine": "1530",
  "toolAction": "\"Viewing corrupted code area\"",
  "toolSummary": "\"Viewing potential syntax error area\""
}
```

---

### File: `scratch/extracted/step_246_tc_0.json`
- **Path:** `scratch/extracted/step_246_tc_0.json`
- **Estimated Tokens:** 65
- **mtime:** 1780659608.384

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1545",
  "StartLine": "1475",
  "toolAction": "\"Viewing _build_toast_tab first half\"",
  "toolSummary": "\"Viewing _build_toast_tab code\""
}
```

---

### File: `scratch/extracted/step_248_tc_0.json`
- **Path:** `scratch/extracted/step_248_tc_0.json`
- **Estimated Tokens:** 65
- **mtime:** 1780659608.385

```json
{
  "CommandLine": "\"python -m py_compile HealthApp/health_app.py\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Checking file compilation\"",
  "toolSummary": "\"Compiling health_app.py\""
}
```

---

### File: `scratch/extracted/step_250_replacement.py`
- **Path:** `scratch/extracted/step_250_replacement.py`
- **Estimated Tokens:** 126
- **mtime:** 1780659608.388

```python
"        btn_frame = tk.Frame(scrollable_frame, bg=TH[\"bg\"])\n        btn_frame.pack(fill=tk.X, pady=20)\n        \n        tk.Button(\n            btn_frame, text=\"[ PREVIEW IN HUB ]\", font=(\"Consolas\", 10, \"bold\"),\n            bg=TH[\"bg2\"], fg=TH[\"accent\"], activebackground=TH[\"bg3\"], activeforeground=TH[\"accent\"],\n            relief=tk.FLAT, cursor=\"hand2\",\n            command=lambda: self.switch_to_preview_hub(\"General Break\"), padx=20, pady=8,\n        ).pack(side=tk.RIGHT)"
```

---

### File: `scratch/extracted/step_250_tc_0.json`
- **Path:** `scratch/extracted/step_250_tc_0.json`
- **Estimated Tokens:** 851
- **mtime:** 1780659608.387

```json
{
  "AllowMultiple": "false",
  "Description": "\"Fix syntax error in _build_toast_tab where duplicate lines and broken formatting were left over.\"",
  "EndLine": "1575",
  "Instruction": "\"Remove duplicate and broken code after the PREVIEW IN HUB button pack statement.\"",
  "ReplacementContent": "\"        btn_frame = tk.Frame(scrollable_frame, bg=TH[\\\"bg\\\"])\\n        btn_frame.pack(fill=tk.X, pady=20)\\n        \\n        tk.Button(\\n            btn_frame, text=\\\"[ PREVIEW IN HUB ]\\\", font=(\\\"Consolas\\\", 10, \\\"bold\\\"),\\n            bg=TH[\\\"bg2\\\"], fg=TH[\\\"accent\\\"], activebackground=TH[\\\"bg3\\\"], activeforeground=TH[\\\"accent\\\"],\\n            relief=tk.FLAT, cursor=\\\"hand2\\\",\\n            command=lambda: self.switch_to_preview_hub(\\\"General Break\\\"), padx=20, pady=8,\\n        ).pack(side=tk.RIGHT)\"",
  "StartLine": "1535",
  "TargetContent": "\"        btn_frame = tk.Frame(scrollable_frame, bg=TH[\\\"bg\\\"])\\n        btn_frame.pack(fill=tk.X, pady=20)\\n        \\n        tk.Button(\\n            btn_frame, text=\\\"[ PREVIEW IN HUB ]\\\", font=(\\\"Consolas\\\", 10, \\\"bold\\\"),\\n            bg=TH[\\\"bg2\\\"], fg=TH[\\\"accent\\\"], activebackground=TH[\\\"bg3\\\"], activeforeground=TH[\\\"accent\\\"],\\n            relief=tk.FLAT, cursor=\\\"hand2\\\",\\n            command=lambda: self.switch_to_preview_hub(\\\"General Break\\\"), padx=20, pady=8,\\n        ).pack(side=tk.RIGHT)d(f2_right, \\\"Border Radius (px):\\\", \\\"toast_radius\\\", 1)\\n        self._add_field(f2_right, \\\"Padding X (px):\\\", \\\"toast_padding_x\\\", 2)\\n        self._add_field(f2_right, \\\"Padding Y (px):\\\", \\\"toast_padding_y\\\", 3)\\n        self._add_field(f2_right, \\\"Opacity (0.1 - 1.0):\\\", \\\"toast_opacity\\\", 4)\\n        self._add_field(f2_right, \\\"Border Width (px):\\\", \\\"toast_border_width\\\", 5)\\n        self._add_color_field(f2_right, \\\"Border Color:\\\", \\\"toast_border_color\\\", 6)\\n        self._add_color_field(f2_right, \\\"Gradient End Color:\\\", \\\"toast_gradient_end\\\", 7)\\n        self._add_combo(f2_right, \\\"Click Action:\\\", \\\"toast_click_action\\\", 8, actions)\\n        self._add_field(f2_right, \\\"Duration (sec):\\\", \\\"toast_duration\\\", 9)\\n        \\n        sound_choices = [\\\"mac_connect\\\", \\\"mac_disconnect\\\", \\\"SystemAsterisk\\\", \\\"SystemExclamation\\\", \\\"SystemHand\\\", \\\"SystemQuestion\\\", \\\"SystemDefault\\\"]\\n        self._add_combo(f2_right, \\\"Sound Effect:\\\", \\\"toast_sound_effect\\\", 10, sound_choices)\\n        \\n        f3 = tk.Frame(scrollable_frame, bg=TH[\\\"bg\\\"])\\n        f3.pack(fill=tk.X, pady=(15, 0))\\n        \\n        self._add_grid_chk(f3, \\\"Enable Shadow/Glow\\\", \\\"toast_shadow\\\", 0)\\n        self._add_grid_chk(f3, \\\"Enable Gradient BG\\\", \\\"toast_gradient\\\", 1)\\n        self._add_grid_chk(f3, \\\"Enable Accent Stripe\\\", \\\"toast_accent_stripe\\\", 2)\\n        self._add_grid_chk(f3, \\\"Show Progress Bar\\\", \\\"toast_progress_bar\\\", 3)\\n        self._add_grid_chk(f3, \\\"Auto-Dismiss\\\", \\\"toast_auto_dismiss\\\", 4)\\n        self._add_\n<truncated 535 bytes>",
  "TargetFile": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Fixing syntax error in health_app.py\"",
  "toolSummary": "\"Fixing syntax error\""
}
```

---

### File: `scratch/extracted/step_252_tc_0.json`
- **Path:** `scratch/extracted/step_252_tc_0.json`
- **Estimated Tokens:** 65
- **mtime:** 1780659608.39

```json
{
  "CommandLine": "\"python -m py_compile HealthApp/health_app.py\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Checking file compilation\"",
  "toolSummary": "\"Compiling health_app.py\""
}
```

---

### File: `scratch/extracted/step_254_tc_0.json`
- **Path:** `scratch/extracted/step_254_tc_0.json`
- **Estimated Tokens:** 69
- **mtime:** 1780659608.391

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1715",
  "StartLine": "1685",
  "toolAction": "\"Viewing brightness and night care tabs\"",
  "toolSummary": "\"Viewing brightness and night care tab code\""
}
```

---

### File: `scratch/extracted/step_256_tc_0.json`
- **Path:** `scratch/extracted/step_256_tc_0.json`
- **Estimated Tokens:** 70
- **mtime:** 1780659608.392

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1684",
  "StartLine": "1630",
  "toolAction": "\"Viewing brightness and night care builders\"",
  "toolSummary": "\"Viewing brightness and night care tab code\""
}
```

---

### File: `scratch/extracted/step_262_tc_0.json`
- **Path:** `scratch/extracted/step_262_tc_0.json`
- **Estimated Tokens:** 108
- **mtime:** 1780659608.395

```json
{
  "CommandLine": "\"python -c \\\"import sys; [print(f'{i+1}: {line.strip()}') for i, line in enumerate(open('HealthApp/health_app.py', encoding='utf-8')) if 'BrightnessWarningToast' in line]\\\"\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Finding BrightnessWarningToast references\"",
  "toolSummary": "\"Finding BrightnessWarningToast in health_app.py\""
}
```

---

### File: `scratch/extracted/step_264_tc_0.json`
- **Path:** `scratch/extracted/step_264_tc_0.json`
- **Estimated Tokens:** 67
- **mtime:** 1780659608.396

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1930",
  "StartLine": "1887",
  "toolAction": "\"Viewing BrightnessWarningToast class\"",
  "toolSummary": "\"Viewing BrightnessWarningToast code\""
}
```

---

### File: `scratch/extracted/step_266_tc_0.json`
- **Path:** `scratch/extracted/step_266_tc_0.json`
- **Estimated Tokens:** 107
- **mtime:** 1780659608.398

```json
{
  "CommandLine": "\"python -c \\\"import sys; [print(f'{i+1}: {line.strip()}') for i, line in enumerate(open('HealthApp/health_app.py', encoding='utf-8')) if 'nc_toast' in line or 'Night Care' in line]\\\"\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Finding Night Care references\"",
  "toolSummary": "\"Finding Night Care references in health_app.py\""
}
```

---

### File: `scratch/extracted/step_268_tc_0.json`
- **Path:** `scratch/extracted/step_268_tc_0.json`
- **Estimated Tokens:** 122
- **mtime:** 1780659608.399

```json
{
  "CommandLine": "\"python -c \\\"import sys; [print(f'{i+1}: {line.strip().encode(\\\\'ascii\\\\', \\\\'replace\\\\').decode(\\\\'ascii\\\\')}') for i, line in enumerate(open('HealthApp/health_app.py', encoding='utf-8')) if 'nc_toast' in line or 'Night Care' in line]\\\"\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Searching for Night Care usage\"",
  "toolSummary": "\"Finding Night Care in health_app.py\""
}
```

---

### File: `scratch/extracted/step_270_tc_0.json`
- **Path:** `scratch/extracted/step_270_tc_0.json`
- **Estimated Tokens:** 121
- **mtime:** 1780659608.401

```json
{
  "CommandLine": "\"python -c \\\"for i, l in enumerate(open('HealthApp/health_app.py', encoding='utf-8')): (('nc_toast' in l or 'Night Care' in l) and print(f'{i+1}: {l.strip().encode(\\\\\\\"ascii\\\\\\\", \\\\\\\"ignore\\\\\\\").decode(\\\\\\\"ascii\\\\\\\")}') )\\\"\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Searching for Night Care usage\"",
  "toolSummary": "\"Finding Night Care in health_app.py\""
}
```

---

### File: `scratch/extracted/step_272_tc_0.json`
- **Path:** `scratch/extracted/step_272_tc_0.json`
- **Estimated Tokens:** 123
- **mtime:** 1780659608.402

```json
{
  "CommandLine": "\"python -c \\\"exec(\\\\\\\"import sys\\\\nfor i, l in enumerate(open('HealthApp/health_app.py', encoding='utf-8')):\\\\n if 'nc_toast' in l or 'Night Care' in l:\\\\n  print(str(i+1) + ': ' + l.strip().encode('ascii', 'ignore').decode('ascii'))\\\\\\\")\\\"\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Searching for Night Care usage\"",
  "toolSummary": "\"Finding Night Care in health_app.py\""
}
```

---

### File: `scratch/extracted/step_274_tc_0.json`
- **Path:** `scratch/extracted/step_274_tc_0.json`
- **Estimated Tokens:** 274
- **mtime:** 1780659608.404

```json
{
  "ArtifactMetadata": "{\"ArtifactType\":\"other\",\"RequestFeedback\":false,\"Summary\":\"Scratch script to search for Night Care toast references in health_app.py\"}",
  "CodeContent": "\"import os\\nimport sys\\n\\nfilepath = r\\\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\\\"\\nwith open(filepath, \\\"r\\\", encoding=\\\"utf-8\\\") as f:\\n    for i, line in enumerate(f):\\n        if \\\"nc_toast\\\" in line or \\\"Night Care\\\" in line or \\\"_trigger_night_care\\\" in line:\\n            clean_line = line.strip().encode(\\\"ascii\\\", \\\"replace\\\").decode(\\\"ascii\\\")\\n            print(f\\\"{i+1}: {clean_line}\\\")\\n\"",
  "Description": "\"Create scratch script to search health_app.py for Night Care references safely.\"",
  "IsArtifact": "false",
  "Overwrite": "true",
  "TargetFile": "\"C:\\\\Users\\\\NANDHA A\\\\.gemini\\\\antigravity-ide\\\\brain\\\\1237cb3f-efd0-4a57-b440-f74287d1898a\\\\scratch\\\\search_night_care.py\"",
  "toolAction": "\"Creating scratch script\"",
  "toolSummary": "\"Creating search_night_care.py\""
}
```

---

### File: `scratch/extracted/step_278_tc_0.json`
- **Path:** `scratch/extracted/step_278_tc_0.json`
- **Estimated Tokens:** 259
- **mtime:** 1780659608.405

```json
{
  "ArtifactMetadata": "{\"ArtifactType\":\"other\",\"RequestFeedback\":false,\"Summary\":\"Scratch script to find all nc_ or night occurrences in health_app.py\"}",
  "CodeContent": "\"import os\\nimport sys\\n\\nfilepath = r\\\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\\\"\\nwith open(filepath, \\\"r\\\", encoding=\\\"utf-8\\\") as f:\\n    for i, line in enumerate(f):\\n        if \\\"nc_\\\" in line or \\\"night_\\\" in line or \\\"Night\\\" in line:\\n            clean_line = line.strip().encode(\\\"ascii\\\", \\\"replace\\\").decode(\\\"ascii\\\")\\n            print(f\\\"{i+1}: {clean_line}\\\")\\n\"",
  "Description": "\"Search health_app.py for night-related variables.\"",
  "IsArtifact": "false",
  "Overwrite": "true",
  "TargetFile": "\"C:\\\\Users\\\\NANDHA A\\\\.gemini\\\\antigravity-ide\\\\brain\\\\1237cb3f-efd0-4a57-b440-f74287d1898a\\\\scratch\\\\search_night_care.py\"",
  "toolAction": "\"Updating scratch script\"",
  "toolSummary": "\"Updating search_night_care.py\""
}
```

---

### File: `scratch/extracted/step_282_tc_0.json`
- **Path:** `scratch/extracted/step_282_tc_0.json`
- **Estimated Tokens:** 64
- **mtime:** 1780659608.408

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "2330",
  "StartLine": "2270",
  "toolAction": "\"Viewing _night_care_loop method\"",
  "toolSummary": "\"Viewing _night_care_loop code\""
}
```

---

### File: `scratch/extracted/step_284_tc_0.json`
- **Path:** `scratch/extracted/step_284_tc_0.json`
- **Estimated Tokens:** 68
- **mtime:** 1780659608.409

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1270",
  "StartLine": "1234",
  "toolAction": "\"Viewing frames initialization\"",
  "toolSummary": "\"Viewing frames initialization in SettingsWindow\""
}
```

---

### File: `scratch/extracted/step_286_replacement.py`
- **Path:** `scratch/extracted/step_286_replacement.py`
- **Estimated Tokens:** 54
- **mtime:** 1780659608.412

```python
"    def __init__(self, parent, settings:\n        dict, on_save):\n        self.parent = parent\n        self.settings = settings\n        self.on_save = on_save\n        self.entries = {}\n        self.frames = {}"
```

---

### File: `scratch/extracted/step_286_tc_0.json`
- **Path:** `scratch/extracted/step_286_tc_0.json`
- **Estimated Tokens:** 240
- **mtime:** 1780659608.411

```json
{
  "AllowMultiple": "false",
  "Description": "\"Initialize self.frames = {} in SettingsWindow.__init__ to prevent AttributeError when building frames.\"",
  "EndLine": "1205",
  "Instruction": "\"Add self.frames = {} inside __init__.\"",
  "ReplacementContent": "\"    def __init__(self, parent, settings:\\n        dict, on_save):\\n        self.parent = parent\\n        self.settings = settings\\n        self.on_save = on_save\\n        self.entries = {}\\n        self.frames = {}\"",
  "StartLine": "1198",
  "TargetContent": "\"    def __init__(self, parent, settings:\\n        dict, on_save):\\n        self.parent = parent\\n        self.settings = settings\\n        self.on_save = on_save\\n        self.entries = {}\"",
  "TargetFile": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Adding frames dictionary to SettingsWindow\"",
  "toolSummary": "\"Modifying SettingsWindow.__init__\""
}
```

---

### File: `scratch/extracted/step_288_tc_0.json`
- **Path:** `scratch/extracted/step_288_tc_0.json`
- **Estimated Tokens:** 67
- **mtime:** 1780659608.413

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1890",
  "StartLine": "1840",
  "toolAction": "\"Viewing end of SettingsWindow class\"",
  "toolSummary": "\"Viewing end of SettingsWindow class\""
}
```

---

### File: `scratch/extracted/step_290_replacement.py`
- **Path:** `scratch/extracted/step_290_replacement.py`
- **Estimated Tokens:** 518
- **mtime:** 1780659608.416

```python
"    def _create_card(self, parent_frame, title_text, row, col, columnspan=1):\n        card = tk.Frame(\n            parent_frame, bg=TH[\"bg2\"], \n            highlightthickness=1, highlightbackground=TH[\"border\"], \n            padx=16, pady=16\n        )\n        card.grid(row=row, column=col, columnspan=columnspan, sticky=tk.NSEW, padx=8, pady=8)\n        parent_frame.grid_columnconfigure(col, weight=1)\n        \n        tk.Label(\n            card, text=title_text.upper(), font=(\"Consolas\", 10, \"bold\"), \n            bg=TH[\"bg2\"], fg=TH[\"accent\"], anchor=tk.W\n        ).pack(anchor=tk.W, pady=(0, 12))\n        \n        content_frame = tk.Frame(card, bg=TH[\"bg2\"])\n        content_frame.pack(fill=tk.BOTH, expand=True)\n        return card, content_frame\n\n    def _add_field(self, parent_frame, label, key, row, is_str=False):\n        bg = parent_frame.cget(\"bg\")\n        tk.Label(\n            parent_frame, text=label.upper(), font=(\"Consolas\", 9),\n            bg=bg, fg=TH[\"fg_dim\"], anchor=tk.W,\n        ).grid(row=row, column=0, sticky=tk.W, pady=8)\n\n        var = tk.StringVar(value=str(self.settings.get(key, \"\")))\n        tk.Entry(\n            parent_frame, textvariable=var, font=(\"Consolas\", 10),\n            bg=TH[\"bg\"], fg=TH[\"fg\"], insertbackground=TH[\"accent\"],\n            relief=tk.FLAT, highlightthickness=1,\n            highlightcolor=TH[\"accent\"], highlightbackground=TH[\"border\"],\n            width=14,\n        ).grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))\n\n        self.entries[key] = (var, is_str)\n        var.trace_add(\"write\", lambda *args: self._on_settings_modified())\n\n    def _add_combo(self, parent_frame, label, key, row, values):\n        bg = parent_frame.cget(\"bg\")\n        tk.Label(\n            parent_frame, text=label.upper(), font=(\"Consolas\", 9),\n            bg=bg, fg=TH[\"fg_dim\"], anchor=tk.W,\n        ).grid(row=row, column=0, sticky=tk.W, pady=8)\n\n        var = tk.StringVar(value=self.settings.get(key, valu
<truncated 44010 bytes>
```

---

### File: `scratch/extracted/step_290_tc_0.json`
- **Path:** `scratch/extracted/step_290_tc_0.json`
- **Estimated Tokens:** 1,314
- **mtime:** 1780659608.415

```json
{
  "AllowMultiple": "false",
  "Description": "\"Redesign settings UI in health_app.py using modern geometric Card layout panels, fix trace_add live preview bugs by routing to dynamic _on_settings_modified, add missing Preview Hub tab methods (with Tkinter vector canvas drawing), and sound selection settings dropdowns for Brightness Care and Night Care.\"",
  "EndLine": "1857",
  "Instruction": "\"Replace the entire settings GUI builder methods block with the card redesigned layout and new Preview Hub methods.\"",
  "ReplacementContent": "\"    def _create_card(self, parent_frame, title_text, row, col, columnspan=1):\\n        card = tk.Frame(\\n            parent_frame, bg=TH[\\\"bg2\\\"], \\n            highlightthickness=1, highlightbackground=TH[\\\"border\\\"], \\n            padx=16, pady=16\\n        )\\n        card.grid(row=row, column=col, columnspan=columnspan, sticky=tk.NSEW, padx=8, pady=8)\\n        parent_frame.grid_columnconfigure(col, weight=1)\\n        \\n        tk.Label(\\n            card, text=title_text.upper(), font=(\\\"Consolas\\\", 10, \\\"bold\\\"), \\n            bg=TH[\\\"bg2\\\"], fg=TH[\\\"accent\\\"], anchor=tk.W\\n        ).pack(anchor=tk.W, pady=(0, 12))\\n        \\n        content_frame = tk.Frame(card, bg=TH[\\\"bg2\\\"])\\n        content_frame.pack(fill=tk.BOTH, expand=True)\\n        return card, content_frame\\n\\n    def _add_field(self, parent_frame, label, key, row, is_str=False):\\n        bg = parent_frame.cget(\\\"bg\\\")\\n        tk.Label(\\n            parent_frame, text=label.upper(), font=(\\\"Consolas\\\", 9),\\n            bg=bg, fg=TH[\\\"fg_dim\\\"], anchor=tk.W,\\n        ).grid(row=row, column=0, sticky=tk.W, pady=8)\\n\\n        var = tk.StringVar(value=str(self.settings.get(key, \\\"\\\")))\\n        tk.Entry(\\n            parent_frame, textvariable=var, font=(\\\"Consolas\\\", 10),\\n            bg=TH[\\\"bg\\\"], fg=TH[\\\"fg\\\"], insertbackground=TH[\\\"accent\\\"],\\n            relief=tk.FLAT, highlightthickness=1,\\n            highlightcolor=TH[\\\"accent\\\"], highlightbackground=TH[\\\"border\\\"],\\n            width=14,\\n        ).grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))\\n\\n        self.entries[key] = (var, is_str)\\n        var.trace_add(\\\"write\\\", lambda *args: self._on_settings_modified())\\n\\n    def _add_combo(self, parent_frame, label, key, row, values):\\n        bg = parent_frame.cget(\\\"bg\\\")\\n        tk.Label(\\n            parent_frame, text=label.upper(), font=(\\\"Consolas\\\", 9),\\n            bg=bg, fg=TH[\\\"fg_dim\\\"], anchor=tk.W,\\n        ).grid(row=row, column=0, sticky=tk.W, pady=8)\\n\\n        var = tk.StringVar(value=self.settings.get(key, valu\n<truncated 44010 bytes>",
  "StartLine": "1321",
  "TargetContent": "\"    def _add_field(self, parent_frame, label, key, row, is_str=False):\\n        tk.Label(\\n            parent_frame, text=label.upper(), font=(\\\"Consolas\\\", 9),\\n            bg=TH[\\\"bg\\\"], fg=TH[\\\"fg_dim\\\"], anchor=tk.W,\\n        ).grid(row=row, column=0, sticky=tk.W, pady=8)\\n\\n        var = tk.StringVar(value=str(self.settings.get(key, \\\"\\\")))\\n        tk.Entry(\\n            parent_frame, textvariable=var, font=(\\\"Consolas\\\", 10),\\n            bg=TH[\\\"bg\\\"], fg=TH[\\\"fg\\\"], insertbackground=TH[\\\"accent\\\"],\\n            relief=tk.FLAT, highlightthickness=1,\\n            highlightcolor=TH[\\\"accent\\\"], highlightbackground=TH[\\\"border\\\"],\\n            width=14,\\n        ).grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))\\n\\n        self.entries[key] = (var, is_str)\\n        var.trace_add(\\\"write\\\", lambda *args: self._on_settings_modified())\\n\\n    def _add_combo(self, parent_frame, label, key, row, values):\\n        tk.Label(\\n            parent_frame, text=label.upper(), font=(\\\"Consolas\\\", 9),\\n            bg=TH[\\\"bg\\\"], fg=TH[\\\"fg_dim\\\"], anchor=tk.W,\\n        ).grid(row=row, column=0, sticky=tk.W, pady=8)\\n\\n        var = tk.StringVar(value=self.settings.get(key, values[0]))\\n        ttk.Combobox(\\n            parent_frame, textvariable=var, values=values,\\n            font=(\\\"Consolas\\\", 10), state=\\\"readonly\\\", width=12,\\n        ).grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))\\n\\n        self.entries[key] = (var, True)\\n        var.trace_add(\\\"write\\\", lambda *args: self._on_settings_modified())\\n\\n    def _add_color_field(self, parent_frame, label, key, row):\\n        tk.Label(\\n            parent_frame, text=label.upper(), font=(\\\"Consolas\\\", 9),\\n            bg=TH[\\\"bg\\\"], fg=TH[\\\"fg_dim\\\"], anchor=tk.W,\\n        ).grid(row=row, column=0, sticky=tk.W, pady=8)\\n\\n        var = tk.StringVar(value=str(self.settings.get(key, \\\"\\\")))\\n        \\n        def choose_color(v=var):\\n            color_code = colorchooser.askcolor(title=\\\"Choose color\\\", initialcolor=v.get())[1]\\n            if \n<truncated 27069 bytes>",
  "TargetFile": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Redesigning Settings UI layout and adding Preview Hub methods\"",
  "toolSummary": "\"Redesigning settings UI and adding preview hub\""
}
```

---

### File: `scratch/extracted/step_292_tc_0.json`
- **Path:** `scratch/extracted/step_292_tc_0.json`
- **Estimated Tokens:** 65
- **mtime:** 1780659608.418

```json
{
  "CommandLine": "\"python -m py_compile HealthApp/health_app.py\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Checking file compilation\"",
  "toolSummary": "\"Compiling health_app.py\""
}
```

---

### File: `scratch/extracted/step_294_tc_0.json`
- **Path:** `scratch/extracted/step_294_tc_0.json`
- **Estimated Tokens:** 78
- **mtime:** 1780659608.419

```json
{
  "CommandLine": "\"python -c \\\"print(len(open('HealthApp/health_app.py', encoding='utf-8').readlines()))\\\"\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Counting file lines\"",
  "toolSummary": "\"Counting lines in health_app.py\""
}
```

---

### File: `scratch/extracted/step_296_tc_0.json`
- **Path:** `scratch/extracted/step_296_tc_0.json`
- **Estimated Tokens:** 63
- **mtime:** 1780659608.421

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1285",
  "StartLine": "1270",
  "toolAction": "\"Viewing typo region in health_app.py\"",
  "toolSummary": "\"Viewing typo region\""
}
```

---

### File: `scratch/extracted/step_298_tc_0.json`
- **Path:** `scratch/extracted/step_298_tc_0.json`
- **Estimated Tokens:** 63
- **mtime:** 1780659608.422

```json
{
  "CommandLine": "\"git restore HealthApp/health_app.py\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Restoring health_app.py\"",
  "toolSummary": "\"Restoring health_app.py\""
}
```

---

### File: `scratch/extracted/step_300_tc_0.json`
- **Path:** `scratch/extracted/step_300_tc_0.json`
- **Estimated Tokens:** 65
- **mtime:** 1780659608.424

```json
{
  "CommandLine": "\"python -m py_compile HealthApp/health_app.py\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Checking file compilation\"",
  "toolSummary": "\"Compiling health_app.py\""
}
```

---

### File: `scratch/extracted/step_302_replacement.py`
- **Path:** `scratch/extracted/step_302_replacement.py`
- **Estimated Tokens:** 54
- **mtime:** 1780659608.426

```python
"    def __init__(self, parent, settings:\n        dict, on_save):\n        self.parent = parent\n        self.settings = settings\n        self.on_save = on_save\n        self.entries = {}\n        self.frames = {}"
```

---

### File: `scratch/extracted/step_302_tc_0.json`
- **Path:** `scratch/extracted/step_302_tc_0.json`
- **Estimated Tokens:** 231
- **mtime:** 1780659608.425

```json
{
  "AllowMultiple": "false",
  "Description": "\"Re-add self.frames = {} to SettingsWindow.__init__ after git restore.\"",
  "EndLine": "1205",
  "Instruction": "\"Add self.frames = {} inside __init__.\"",
  "ReplacementContent": "\"    def __init__(self, parent, settings:\\n        dict, on_save):\\n        self.parent = parent\\n        self.settings = settings\\n        self.on_save = on_save\\n        self.entries = {}\\n        self.frames = {}\"",
  "StartLine": "1198",
  "TargetContent": "\"    def __init__(self, parent, settings:\\n        dict, on_save):\\n        self.parent = parent\\n        self.settings = settings\\n        self.on_save = on_save\\n        self.entries = {}\"",
  "TargetFile": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Adding frames dictionary to SettingsWindow\"",
  "toolSummary": "\"Modifying SettingsWindow.__init__\""
}
```

---

### File: `scratch/extracted/step_304_tc_0.json`
- **Path:** `scratch/extracted/step_304_tc_0.json`
- **Estimated Tokens:** 65
- **mtime:** 1780659608.427

```json
{
  "CommandLine": "\"python -m py_compile HealthApp/health_app.py\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Checking file compilation\"",
  "toolSummary": "\"Compiling health_app.py\""
}
```

---

### File: `scratch/extracted/step_306_tc_0.json`
- **Path:** `scratch/extracted/step_306_tc_0.json`
- **Estimated Tokens:** 111
- **mtime:** 1780659608.429

```json
{
  "CommandLine": "\"python -c \\\"import sys; [print(f'{i+1}: {line.strip()}') for i, line in enumerate(open('HealthApp/health_app.py', encoding='utf-8')) if 'class SettingsWindow' in line or 'def _add_field' in line]\\\"\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Finding class and method lines\"",
  "toolSummary": "\"Finding SettingsWindow and _add_field lines\""
}
```

---

### File: `scratch/extracted/step_308_tc_0.json`
- **Path:** `scratch/extracted/step_308_tc_0.json`
- **Estimated Tokens:** 115
- **mtime:** 1780659608.43

```json
{
  "CommandLine": "\"python -c \\\"import sys; [print(f'{i+1}: {line.strip()}') for i, line in enumerate(open('HealthApp/health_app.py', encoding='utf-8')) if 'ensure_sound_effects' in line or 'ToastQueue' in line]\\\"\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Finding sound and queue references\"",
  "toolSummary": "\"Finding ensure_sound_effects and ToastQueue in health_app.py\""
}
```

---

### File: `scratch/extracted/step_314_tc_0.json`
- **Path:** `scratch/extracted/step_314_tc_0.json`
- **Estimated Tokens:** 66
- **mtime:** 1780659608.432

```json
{
  "CommandLine": "\"git diff HealthApp/health_app.py\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Running git diff for health_app.py\"",
  "toolSummary": "\"Checking health_app.py diff\""
}
```

---

### File: `scratch/extracted/step_318_tc_0.json`
- **Path:** `scratch/extracted/step_318_tc_0.json`
- **Estimated Tokens:** 83
- **mtime:** 1780659608.433

```json
{
  "CommandLine": "\"python -c \\\"print('ensure_sound_effects' in open('HealthApp/health_app.py', encoding='utf-8').read())\\\"\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Checking string presence\"",
  "toolSummary": "\"Checking for ensure_sound_effects\""
}
```

---

### File: `scratch/extracted/step_320_tc_0.json`
- **Path:** `scratch/extracted/step_320_tc_0.json`
- **Estimated Tokens:** 65
- **mtime:** 1780659608.434

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "120",
  "StartLine": "75",
  "toolAction": "\"Viewing health_app.py top section\"",
  "toolSummary": "\"Viewing health_app.py top section\""
}
```

---

### File: `scratch/extracted/step_322_tc_0.json`
- **Path:** `scratch/extracted/step_322_tc_0.json`
- **Estimated Tokens:** 109
- **mtime:** 1780659608.436

```json
{
  "CommandLine": "\"python -c \\\"import sys; [print(f'{i+1}: {line.strip()}') for i, line in enumerate(open('HealthApp/health_app.py', encoding='utf-8')) if 'wave' in line or 'breathing' in line]\\\"\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Finding breathing audio references\"",
  "toolSummary": "\"Finding breathing audio references in health_app.py\""
}
```

---

### File: `scratch/extracted/step_324_tc_0.json`
- **Path:** `scratch/extracted/step_324_tc_0.json`
- **Estimated Tokens:** 68
- **mtime:** 1780659608.437

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "430",
  "StartLine": "410",
  "toolAction": "\"Viewing end of generate_breathing_sound\"",
  "toolSummary": "\"Viewing generate_breathing_sound code\""
}
```

---

### File: `scratch/extracted/step_326_tc_0.json`
- **Path:** `scratch/extracted/step_326_tc_0.json`
- **Estimated Tokens:** 64
- **mtime:** 1780659608.439

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1733",
  "StartLine": "1690",
  "toolAction": "\"Viewing end of health_app.py\"",
  "toolSummary": "\"Viewing health_app.py end section\""
}
```

---

### File: `scratch/extracted/step_328_tc_0.json`
- **Path:** `scratch/extracted/step_328_tc_0.json`
- **Estimated Tokens:** 95
- **mtime:** 1780659608.441

```json
{
  "CommandLine": "\"python -c \\\"import sys; [print(f'{i+1}: {line.strip()}') for i, line in enumerate(open('HealthApp/health_app.py', encoding='utf-8')) if 'def run' in line]\\\"\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Finding def run line\"",
  "toolSummary": "\"Finding def run in health_app.py\""
}
```

---

### File: `scratch/extracted/step_330_tc_0.json`
- **Path:** `scratch/extracted/step_330_tc_0.json`
- **Estimated Tokens:** 60
- **mtime:** 1780659608.442

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1690",
  "StartLine": "1650",
  "toolAction": "\"Viewing def run method\"",
  "toolSummary": "\"Viewing def run code\""
}
```

---

### File: `scratch/extracted/step_332_tc_0.json`
- **Path:** `scratch/extracted/step_332_tc_0.json`
- **Estimated Tokens:** 109
- **mtime:** 1780659608.444

```json
{
  "CommandLine": "\"python -c \\\"import sys; [print(f'{i+1}: {line.strip()}') for i, line in enumerate(open('HealthApp/health_app.py', encoding='utf-8')) if 'def _scheduler_loop' in line or 'def _health_toast_loop' in line]\\\"\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Finding loops in health_app.py\"",
  "toolSummary": "\"Finding loops in health_app.py\""
}
```

---

### File: `scratch/extracted/step_334_tc_0.json`
- **Path:** `scratch/extracted/step_334_tc_0.json`
- **Estimated Tokens:** 101
- **mtime:** 1780659608.445

```json
{
  "CommandLine": "\"python -c \\\"import sys; [print(f'{i+1}: {line.strip()}') for i, line in enumerate(open('HealthApp/health_app.py', encoding='utf-8')) if '_health_toast' in line]\\\"\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Finding health toast occurrences\"",
  "toolSummary": "\"Finding _health_toast in health_app.py\""
}
```

---

### File: `scratch/extracted/step_336_tc_0.json`
- **Path:** `scratch/extracted/step_336_tc_0.json`
- **Estimated Tokens:** 99
- **mtime:** 1780659608.446

```json
{
  "CommandLine": "\"python -c \\\"import sys; [print(f'{i+1}: {line.strip()}') for i, line in enumerate(open('HealthApp/health_app.py', encoding='utf-8')) if 'def _' in line and 'loop' in line]\\\"\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Finding loop methods\"",
  "toolSummary": "\"Finding methods with _ and loop\""
}
```

---

### File: `scratch/extracted/step_338_tc_0.json`
- **Path:** `scratch/extracted/step_338_tc_0.json`
- **Estimated Tokens:** 100
- **mtime:** 1780659608.447

```json
{
  "CommandLine": "\"python -c \\\"import sys; [print(f'{i+1}: {line.strip()}') for i, line in enumerate(open('HealthApp/health_app.py', encoding='utf-8')) if 'def ' in line and i > 430]\\\"\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "2000",
  "toolAction": "\"Finding HealthApp methods\"",
  "toolSummary": "\"Finding all def lines in health_app.py\""
}
```

---

### File: `scratch/extracted/step_340_tc_0.json`
- **Path:** `scratch/extracted/step_340_tc_0.json`
- **Estimated Tokens:** 411
- **mtime:** 1780659608.449

```json
{
  "ArtifactMetadata": "{\"ArtifactType\":\"other\",\"RequestFeedback\":false,\"Summary\":\"Scratch script to search transcript.jsonl for previous health_app.py contents\"}",
  "CodeContent": "\"import os\\nimport json\\n\\nlog_dir = r\\\"C:\\\\Users\\\\NANDHA A\\\\.gemini\\\\antigravity-ide\\\\brain\\\\1237cb3f-efd0-4a57-b440-f74287d1898a\\\\.system_generated\\\\logs\\\"\\nlog_path = os.path.join(log_dir, \\\"transcript.jsonl\\\")\\n\\nif os.path.exists(log_path):\\n    print(\\\"Transcript found! Searching...\\\")\\n    with open(log_path, \\\"r\\\", encoding=\\\"utf-8\\\") as f:\\n        for i, line in enumerate(f):\\n            if \\\"ensure_sound_effects\\\" in line or \\\"_health_toast_loop\\\" in line:\\n                print(f\\\"Line {i+1} matches!\\\")\\n                try:\\n                    data = json.loads(line)\\n                    # Print preview of the content\\n                    content = str(data.get(\\\"content\\\", \\\"\\\"))[:200]\\n                    print(f\\\"  Type: {data.get('type')}, Content preview: {content}\\\")\\n                except Exception as e:\\n                    print(f\\\"  Error parsing JSON: {e}\\\")\\nelse:\\n    print(f\\\"Transcript not found at {log_path}\\\")\\n\"",
  "Description": "\"Search transcript.jsonl to find previous edits.\"",
  "IsArtifact": "false",
  "Overwrite": "true",
  "TargetFile": "\"C:\\\\Users\\\\NANDHA A\\\\.gemini\\\\antigravity-ide\\\\brain\\\\1237cb3f-efd0-4a57-b440-f74287d1898a\\\\scratch\\\\search_night_care.py\"",
  "toolAction": "\"Searching transcript log\"",
  "toolSummary": "\"Updating search_night_care.py to search logs\""
}
```

---

### File: `scratch/extracted/step_34_tc_0.json`
- **Path:** `scratch/extracted/step_34_tc_0.json`
- **Estimated Tokens:** 736
- **mtime:** 1780659608.173

```json
{
  "ArtifactMetadata": "{\"ArtifactType\":\"implementation_plan\",\"RequestFeedback\":false,\"Summary\":\"Approved implementation plan for Health App upgrades including sequential toast queue (1.5s delay), sleep/resume timer resets, custom sounds downloaded from the web into a new folder with synthetic fallback, custom visual preview hub, and dashboard UI redesign.\"}",
  "CodeContent": "\"# Implementation Plan - Health App Upgrades & Redesign (APPROVED)\\n\\nThis plan covers implementing a sequential toast queue, sleep/resume detection to reset break times, custom sound downloading/generation, a dedicated preview section in the settings UI, and a general visual redesign of the settings dashboard.\\n\\n## Approved Decisions & Feedback\\n\\n- **Queue Delay**: A minimum delay of 1.5 seconds will be enforced between consecutive toast notifications.\\n- **Sound Storage & Source**: A new folder `HealthApp/resources/sounds/` will be created. We will implement a downloader script to fetch public-domain WAV files, with a robust fallback to high-quality synthetic sound generation if downloads fail.\\n- **Preview Hub**: The settings UI will feature a live canvas mock showing real-time rendering of the toast design alongside testing buttons.\\n\\n---\\n\\n## Proposed Changes\\n\\n### Core System\\n\\n#### [MODIFY] [toast_utils.py](file:///c:/Users/NANDHA%20A/Desktop/UTILITIES/toast_utils.py)\\n- Modify `BaseToast` to integrate with a new global `ToastQueue` thread-safe manager.\\n- Implement `ToastQueue` inside `BaseToast` that manages queuing and displaying toasts sequentially.\\n- When `BaseToast.show()` is called, instead of displaying the window immediately, it will add the toast to the queue.\\n- The queue will process items one by one, showing a toast, waiting for it to be dismissed, and then waiting for 1.5 seconds before showing the next toast.\\n\\n#### [MODIFY] [health_app.py](file:///c:/Users/NANDHA%20A/Desktop/UTILITIES/HealthApp/health_app.py)\\n- **Sleep/Hibernate/Resume Detection**:\\n  - In `_scheduler_loop` and `_health_toast_loop`, track the loop iteration timestamp.\\n  - If `time.time() - last_time > 10.0`, log a resume event and reset break timers (`_last_short_break = time.time()`, `_last_long_break = time.time()`, `_last_health_toast = time.time()`).\\n  - This prevents break screens or notifications from appearing immediately after waking up.\\n- **Sound Customization**:\\n  - Create a new directory `HealthApp/r\n<truncated 1537 bytes>",
  "Description": "\"Update the implementation plan to reflect the approved user decisions and mark request_feedback as false.\"",
  "IsArtifact": "true",
  "Overwrite": "true",
  "TargetFile": "\"C:\\\\Users\\\\NANDHA A\\\\.gemini\\\\antigravity-ide\\\\brain\\\\1237cb3f-efd0-4a57-b440-f74287d1898a\\\\implementation_plan.md\"",
  "toolAction": "\"Updating approved implementation plan\"",
  "toolSummary": "\"Update approved implementation plan\""
}
```

---

### File: `scratch/extracted/step_381_tc_0.json`
- **Path:** `scratch/extracted/step_381_tc_0.json`
- **Estimated Tokens:** 65
- **mtime:** 1780659608.452

```json
{
  "CommandLine": "\"git diff HealthApp/health_app.py\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "5000",
  "toolAction": "\"Running git diff on health_app.py\"",
  "toolSummary": "\"Check diff of health_app.py\""
}
```

---

### File: `scratch/extracted/step_397_tc_0.json`
- **Path:** `scratch/extracted/step_397_tc_0.json`
- **Estimated Tokens:** 62
- **mtime:** 1780659608.455

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "800",
  "StartLine": "1",
  "toolAction": "\"Viewing health_app.py code\"",
  "toolSummary": "\"Read health_app.py lines 1-800\""
}
```

---

### File: `scratch/extracted/step_413_tc_0.json`
- **Path:** `scratch/extracted/step_413_tc_0.json`
- **Estimated Tokens:** 103
- **mtime:** 1780659608.456

```json
{
  "CaseInsensitive": "true",
  "IsRegex": "false",
  "MatchPerLine": "true",
  "Query": "\"health_app.py\"",
  "SearchPath": "\"C:\\\\Users\\\\NANDHA A\\\\.gemini\\\\antigravity-ide\\\\brain\\\\1237cb3f-efd0-4a57-b440-f74287d1898a\\\\.system_generated\\\\logs\\\\transcript.jsonl\"",
  "toolAction": "\"Searching transcript for health_app.py\"",
  "toolSummary": "\"Search transcript.jsonl for health_app.py\""
}
```

---

### File: `scratch/extracted/step_419_tc_0.json`
- **Path:** `scratch/extracted/step_419_tc_0.json`
- **Estimated Tokens:** 80
- **mtime:** 1780659608.458

```json
{
  "CaseInsensitive": "false",
  "IsRegex": "false",
  "MatchPerLine": "true",
  "Query": "\"BaseToast(\"",
  "SearchPath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Searching for BaseToast calls\"",
  "toolSummary": "\"Search BaseToast in health_app.py\""
}
```

---

### File: `scratch/extracted/step_421_tc_0.json`
- **Path:** `scratch/extracted/step_421_tc_0.json`
- **Estimated Tokens:** 81
- **mtime:** 1780659608.459

```json
{
  "CaseInsensitive": "false",
  "IsRegex": "false",
  "MatchPerLine": "true",
  "Query": "\"BaseToast\"",
  "SearchPath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Searching for BaseToast references\"",
  "toolSummary": "\"Search BaseToast in health_app.py\""
}
```

---

### File: `scratch/extracted/step_423_tc_0.json`
- **Path:** `scratch/extracted/step_423_tc_0.json`
- **Estimated Tokens:** 62
- **mtime:** 1780659608.461

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "60",
  "StartLine": "1",
  "toolAction": "\"Viewing health_app.py imports\"",
  "toolSummary": "\"Read health_app.py imports\""
}
```

---

### File: `scratch/extracted/step_433_tc_0.json`
- **Path:** `scratch/extracted/step_433_tc_0.json`
- **Estimated Tokens:** 89
- **mtime:** 1780659608.462

```json
{
  "CaseInsensitive": "false",
  "IsRegex": "false",
  "MatchPerLine": "true",
  "Query": "\"def generate_breathing_sound\"",
  "SearchPath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Locating generate_breathing_sound\"",
  "toolSummary": "\"Locate generate_breathing_sound in health_app.py\""
}
```

---

### File: `scratch/extracted/step_435_tc_0.json`
- **Path:** `scratch/extracted/step_435_tc_0.json`
- **Estimated Tokens:** 66
- **mtime:** 1780659608.465

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "430",
  "StartLine": "370",
  "toolAction": "\"Viewing health_app.py line 370 to 430\"",
  "toolSummary": "\"Read health_app.py lines 370-430\""
}
```

---

### File: `scratch/extracted/step_437_tc_0.json`
- **Path:** `scratch/extracted/step_437_tc_0.json`
- **Estimated Tokens:** 84
- **mtime:** 1780659608.467

```json
{
  "CaseInsensitive": "false",
  "IsRegex": "false",
  "MatchPerLine": "true",
  "Query": "\"def _scheduler_loop\"",
  "SearchPath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Searching for _scheduler_loop\"",
  "toolSummary": "\"Search _scheduler_loop in health_app.py\""
}
```

---

### File: `scratch/extracted/step_439_tc_0.json`
- **Path:** `scratch/extracted/step_439_tc_0.json`
- **Estimated Tokens:** 85
- **mtime:** 1780659608.468

```json
{
  "CaseInsensitive": "false",
  "IsRegex": "false",
  "MatchPerLine": "true",
  "Query": "\"_scheduler_loop\"",
  "SearchPath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Searching for _scheduler_loop references\"",
  "toolSummary": "\"Search _scheduler_loop in health_app.py\""
}
```

---

### File: `scratch/extracted/step_441_tc_0.json`
- **Path:** `scratch/extracted/step_441_tc_0.json`
- **Estimated Tokens:** 67
- **mtime:** 1780659608.47

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1733",
  "StartLine": "1300",
  "toolAction": "\"Viewing health_app.py scheduler loops\"",
  "toolSummary": "\"Read health_app.py lines 1300-1733\""
}
```

---

### File: `scratch/extracted/step_445_tc_0.json`
- **Path:** `scratch/extracted/step_445_tc_0.json`
- **Estimated Tokens:** 66
- **mtime:** 1780659608.471

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1311",
  "StartLine": "900",
  "toolAction": "\"Viewing SettingsWindow implementation\"",
  "toolSummary": "\"Read health_app.py lines 900-1311\""
}
```

---

### File: `scratch/extracted/step_447_tc_0.json`
- **Path:** `scratch/extracted/step_447_tc_0.json`
- **Estimated Tokens:** 101
- **mtime:** 1780659608.472

```json
{
  "CommandLine": "\"python -c \\\"import sys; [print(f'{i+1}: {line.strip()}') for i, line in enumerate(open('HealthApp/health_app.py', encoding='utf-8')) if 'toast' in line.lower()]\\\"\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "5000",
  "toolAction": "\"Finding toast references in health_app.py\"",
  "toolSummary": "\"Search toast in health_app.py\""
}
```

---

### File: `scratch/extracted/step_449_tc_0.json`
- **Path:** `scratch/extracted/step_449_tc_0.json`
- **Estimated Tokens:** 122
- **mtime:** 1780659608.475

```json
{
  "CommandLine": "\"python -c \\\"import sys, io; sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8'); [print(f'{i+1}: {line.strip()}') for i, line in enumerate(open('HealthApp/health_app.py', encoding='utf-8')) if 'toast' in line.lower()]\\\"\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "5000",
  "toolAction": "\"Finding toast references in health_app.py with UTF-8\"",
  "toolSummary": "\"Search toast in health_app.py\""
}
```

---

### File: `scratch/extracted/step_451_tc_0.json`
- **Path:** `scratch/extracted/step_451_tc_0.json`
- **Estimated Tokens:** 115
- **mtime:** 1780659608.476

```json
{
  "CommandLine": "\"python -c \\\"import sys; f=open('HealthApp/health_app.py', encoding='utf-8'); [print(f'{i+1}: {line.strip()}') for i, line in enumerate(f) if 'loop' in line.lower() or 'brightness' in line.lower() or 'night' in line.lower()]\\\"\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "5000",
  "toolAction": "\"Checking loops in health_app.py\"",
  "toolSummary": "\"Search loops in health_app.py\""
}
```

---

### File: `scratch/extracted/step_459_tc_0.json`
- **Path:** `scratch/extracted/step_459_tc_0.json`
- **Estimated Tokens:** 229
- **mtime:** 1780659608.478

```json
{
  "CommandLine": "\"python -c \\\"import json; f=open(r'C:\\\\Users\\\\NANDHA A\\\\.gemini\\\\antigravity-ide\\\\brain\\\\1237cb3f-efd0-4a57-b440-f74287d1898a\\\\.system_generated\\\\logs\\\\transcript.jsonl', encoding='utf-8'); [print(f'Index: {i}, Step: {data.get(\\\\\\\"step_index\\\\\\\")}, Source: {data.get(\\\\\\\"source\\\\\\\")}, Type: {data.get(\\\\\\\"type\\\\\\\")}, Tool: {data.get(\\\\\\\"tool_calls\\\\\\\")[0].get(\\\\\\\"name\\\\\\\") if data.get(\\\\\\\"tool_calls\\\\\\\") else None}') for i, line in enumerate(f) for data in [json.loads(line)] if data.get(\\\\\\\"tool_calls\\\\\\\") and any('health_app.py' in str(tc) for tc in data.get(\\\\\\\"tool_calls\\\\\\\"))]\\\"\"",
  "Cwd": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\"",
  "WaitMsBeforeAsync": "5000",
  "toolAction": "\"Finding health_app.py edits in transcript\"",
  "toolSummary": "\"Find health_app.py edits in logs\""
}
```

---

### File: `scratch/extracted/step_461_tc_0.json`
- **Path:** `scratch/extracted/step_461_tc_0.json`
- **Estimated Tokens:** 578
- **mtime:** 1780659608.48

```json
{
  "CodeContent": "\"import os\\nimport json\\n\\nlog_path = r\\\"C:\\\\Users\\\\NANDHA A\\\\.gemini\\\\antigravity-ide\\\\brain\\\\1237cb3f-efd0-4a57-b440-f74287d1898a\\\\.system_generated\\\\logs\\\\transcript.jsonl\\\"\\noutput_dir = r\\\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\scratch\\\\extracted\\\"\\nos.makedirs(output_dir, exist_ok=True)\\n\\nwith open(log_path, \\\"r\\\", encoding=\\\"utf-8\\\") as f:\\n    for i, line in enumerate(f):\\n        data = json.loads(line)\\n        step_idx = data.get(\\\"step_index\\\")\\n        tool_calls = data.get(\\\"tool_calls\\\", [])\\n        if not tool_calls:\\n            continue\\n            \\n        for tc_idx, tc in enumerate(tool_calls):\\n            args = tc.get(\\\"args\\\", {})\\n            if isinstance(args, str):\\n                try:\\n                    args = json.loads(args)\\n                except Exception:\\n                    pass\\n            \\n            # Check if this tool call modifies health_app.py\\n            target_file = args.get(\\\"TargetFile\\\", \\\"\\\")\\n            if \\\"health_app.py\\\" in target_file or any(\\\"health_app.py\\\" in str(v) for v in args.values()):\\n                print(f\\\"Step {step_idx} matches. Tool: {tc.get('name')}\\\")\\n                # Save the arguments to a file\\n                out_path = os.path.join(output_dir, f\\\"step_{step_idx}_tc_{tc_idx}.json\\\")\\n                with open(out_path, \\\"w\\\", encoding=\\\"utf-8\\\") as out:\\n                    json.dump(args, out, indent=2)\\n                \\n                # If there's replacement content, save it separately\\n                repl = args.get(\\\"ReplacementContent\\\")\\n                if repl:\\n                    repl_path = os.path.join(output_dir, f\\\"step_{step_idx}_replacement.py\\\")\\n                    with open(repl_path, \\\"w\\\", encoding=\\\"utf-8\\\") as out:\\n                        out.write(repl)\\n\"",
  "Description": "\"Script to extract health_app.py modifications from logs\"",
  "IsArtifact": "false",
  "Overwrite": "true",
  "TargetFile": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\scratch\\\\extract_transcript.py\"",
  "toolAction": "\"Writing extract_transcript.py\"",
  "toolSummary": "\"Create extraction script\""
}
```

---

### File: `scratch/extracted/step_52_tc_0.json`
- **Path:** `scratch/extracted/step_52_tc_0.json`
- **Estimated Tokens:** 54
- **mtime:** 1780659608.176

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\tests\\\\test_health_app.py\"",
  "toolAction": "\"Viewing test_health_app.py\"",
  "toolSummary": "\"View test_health_app.py\""
}
```

---

### File: `scratch/extracted/step_62_tc_0.json`
- **Path:** `scratch/extracted/step_62_tc_0.json`
- **Estimated Tokens:** 60
- **mtime:** 1780659608.178

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "377",
  "StartLine": "327",
  "toolAction": "\"Viewing DEFAULT_SETTINGS\"",
  "toolSummary": "\"View DEFAULT_SETTINGS\""
}
```

---

### File: `scratch/extracted/step_65_tc_0.json`
- **Path:** `scratch/extracted/step_65_tc_0.json`
- **Estimated Tokens:** 63
- **mtime:** 1780659608.18

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "455",
  "StartLine": "430",
  "toolAction": "\"Viewing end of DEFAULT_SETTINGS\"",
  "toolSummary": "\"View end of DEFAULT_SETTINGS\""
}
```

---

### File: `scratch/extracted/step_67_replacement.py`
- **Path:** `scratch/extracted/step_67_replacement.py`
- **Estimated Tokens:** 516
- **mtime:** 1780659608.183

```python
"DEFAULT_SETTINGS = {\n    \"short_break_interval_min\": 20,\n    \"short_break_duration_sec\": 15,\n    \"long_break_interval_min\": 60,\n    \"long_break_duration_sec\": 60,\n    \"pre_warning_sec\": 30,\n    \"enable_sound\": True,\n    \"enable_dimming\": True,\n    \"enable_weather_warmth\": True,\n    \"latitude\": 13.08,\n    \"longitude\": 80.27,\n    \"paused\": False,\n    \"night_light_start_hour\": 18,\n    \"night_light_end_hour\": 6,\n    \"run_during_game\": True,\n    \"toast_pos\": \"Center\",\n    \"toast_custom_x\": 100,\n    \"toast_custom_y\": 100,\n    \"toast_width\": 260,\n    \"toast_height\": 60,\n    \"toast_bg_color\": \"#252525\",\n    \"toast_fg_color\": \"#ffffff\",\n    \"toast_accent_color\": \"#00f0ff\",\n    \"toast_font_size\": 11,\n    \"toast_font_weight\": \"bold\",\n    \"toast_font_family\": \"Segoe UI\",\n    \"toast_emoji\": \"👁️\",\n    \"toast_radius\": 16,\n    \"toast_padding_x\": 12,\n    \"toast_padding_y\": 10,\n    \"toast_anim_style\": \"Slide\",\n    \"toast_opacity\": 0.92,\n    \"toast_border_width\": 0,\n    \"toast_border_color\": \"#00f0ff\",\n    \"toast_gradient\": False,\n    \"toast_gradient_end\": \"#101625\",\n    \"toast_shadow\": True,\n    \"toast_accent_stripe\": False,\n    \"toast_text_align\": \"left\",\n    \"toast_auto_dismiss\": True,\n    \"toast_click_action\": \"dismiss\",\n    \"toast_progress_bar\": False,\n    \"toast_enable_sound\": True,\n    \"toast_sound_effect\": \"mac_connect\",\n    \"wellness_points\": 0,\n    \"current_streak\": 0,\n    \"ht_enabled\": True,\n    \"ht_interval_min\": 10,\n    \"ht_duration_sec\": 5,\n    \"ht_cat_breathing\": True,\n    \"ht_cat_eye_care\": True,\n    \"ht_cat_posture\": True,\n    \"ht_cat_stretch\": True,\n    \"ht_cat_hydration\": True,\n    \"ht_cat_mental\": True,\n    \"ht_cat_hands_wrists\": True,\n    \"ht_toast_pos\": \"Right\",\n    \"ht_toast_custom_x\": 100,\n    \"ht_toast_custom_y\": 100,\n    \"ht_toast_width\": 280,\n    \"ht_toast_height\": 70,\n    \"ht_toast_bg_color\"
<truncated 2473 bytes>
```

---

### File: `scratch/extracted/step_67_tc_0.json`
- **Path:** `scratch/extracted/step_67_tc_0.json`
- **Estimated Tokens:** 1,353
- **mtime:** 1780659608.181

```json
{
  "AllowMultiple": "false",
  "Description": "\"Update DEFAULT_SETTINGS: change purple accents to cyan and add custom sound keys for Brightness Care and Night Care.\"",
  "EndLine": "447",
  "Instruction": "\"Replace DEFAULT_SETTINGS dictionary.\"",
  "ReplacementContent": "\"DEFAULT_SETTINGS = {\\n    \\\"short_break_interval_min\\\": 20,\\n    \\\"short_break_duration_sec\\\": 15,\\n    \\\"long_break_interval_min\\\": 60,\\n    \\\"long_break_duration_sec\\\": 60,\\n    \\\"pre_warning_sec\\\": 30,\\n    \\\"enable_sound\\\": True,\\n    \\\"enable_dimming\\\": True,\\n    \\\"enable_weather_warmth\\\": True,\\n    \\\"latitude\\\": 13.08,\\n    \\\"longitude\\\": 80.27,\\n    \\\"paused\\\": False,\\n    \\\"night_light_start_hour\\\": 18,\\n    \\\"night_light_end_hour\\\": 6,\\n    \\\"run_during_game\\\": True,\\n    \\\"toast_pos\\\": \\\"Center\\\",\\n    \\\"toast_custom_x\\\": 100,\\n    \\\"toast_custom_y\\\": 100,\\n    \\\"toast_width\\\": 260,\\n    \\\"toast_height\\\": 60,\\n    \\\"toast_bg_color\\\": \\\"#252525\\\",\\n    \\\"toast_fg_color\\\": \\\"#ffffff\\\",\\n    \\\"toast_accent_color\\\": \\\"#00f0ff\\\",\\n    \\\"toast_font_size\\\": 11,\\n    \\\"toast_font_weight\\\": \\\"bold\\\",\\n    \\\"toast_font_family\\\": \\\"Segoe UI\\\",\\n    \\\"toast_emoji\\\": \\\"\ud83d\udc41\ufe0f\\\",\\n    \\\"toast_radius\\\": 16,\\n    \\\"toast_padding_x\\\": 12,\\n    \\\"toast_padding_y\\\": 10,\\n    \\\"toast_anim_style\\\": \\\"Slide\\\",\\n    \\\"toast_opacity\\\": 0.92,\\n    \\\"toast_border_width\\\": 0,\\n    \\\"toast_border_color\\\": \\\"#00f0ff\\\",\\n    \\\"toast_gradient\\\": False,\\n    \\\"toast_gradient_end\\\": \\\"#101625\\\",\\n    \\\"toast_shadow\\\": True,\\n    \\\"toast_accent_stripe\\\": False,\\n    \\\"toast_text_align\\\": \\\"left\\\",\\n    \\\"toast_auto_dismiss\\\": True,\\n    \\\"toast_click_action\\\": \\\"dismiss\\\",\\n    \\\"toast_progress_bar\\\": False,\\n    \\\"toast_enable_sound\\\": True,\\n    \\\"toast_sound_effect\\\": \\\"mac_connect\\\",\\n    \\\"wellness_points\\\": 0,\\n    \\\"current_streak\\\": 0,\\n    \\\"ht_enabled\\\": True,\\n    \\\"ht_interval_min\\\": 10,\\n    \\\"ht_duration_sec\\\": 5,\\n    \\\"ht_cat_breathing\\\": True,\\n    \\\"ht_cat_eye_care\\\": True,\\n    \\\"ht_cat_posture\\\": True,\\n    \\\"ht_cat_stretch\\\": True,\\n    \\\"ht_cat_hydration\\\": True,\\n    \\\"ht_cat_mental\\\": True,\\n    \\\"ht_cat_hands_wrists\\\": True,\\n    \\\"ht_toast_pos\\\": \\\"Right\\\",\\n    \\\"ht_toast_custom_x\\\": 100,\\n    \\\"ht_toast_custom_y\\\": 100,\\n    \\\"ht_toast_width\\\": 280,\\n    \\\"ht_toast_height\\\": 70,\\n    \\\"ht_toast_bg_color\\\"\n<truncated 2473 bytes>",
  "StartLine": "328",
  "TargetContent": "\"DEFAULT_SETTINGS = {\\n    \\\"short_break_interval_min\\\": 20,\\n    \\\"short_break_duration_sec\\\": 15,\\n    \\\"long_break_interval_min\\\": 60,\\n    \\\"long_break_duration_sec\\\": 60,\\n    \\\"pre_warning_sec\\\": 30,\\n    \\\"enable_sound\\\": True,\\n    \\\"enable_dimming\\\": True,\\n    \\\"enable_weather_warmth\\\": True,\\n    \\\"latitude\\\": 13.08,\\n    \\\"longitude\\\": 80.27,\\n    \\\"paused\\\": False,\\n    \\\"night_light_start_hour\\\": 18,\\n    \\\"night_light_end_hour\\\": 6,\\n    \\\"run_during_game\\\": True,\\n    \\\"toast_pos\\\": \\\"Center\\\",\\n    \\\"toast_custom_x\\\": 100,\\n    \\\"toast_custom_y\\\": 100,\\n    \\\"toast_width\\\": 260,\\n    \\\"toast_height\\\": 60,\\n    \\\"toast_bg_color\\\": \\\"#252525\\\",\\n    \\\"toast_fg_color\\\": \\\"#ffffff\\\",\\n    \\\"toast_accent_color\\\": \\\"#7c3aed\\\",\\n    \\\"toast_font_size\\\": 11,\\n    \\\"toast_font_weight\\\": \\\"bold\\\",\\n    \\\"toast_font_family\\\": \\\"Segoe UI\\\",\\n    \\\"toast_emoji\\\": \\\"\ud83d\udc41\ufe0f\\\",\\n    \\\"toast_radius\\\": 16,\\n    \\\"toast_padding_x\\\": 12,\\n    \\\"toast_padding_y\\\": 10,\\n    \\\"toast_anim_style\\\": \\\"Slide\\\",\\n    \\\"toast_opacity\\\": 0.92,\\n    \\\"toast_border_width\\\": 0,\\n    \\\"toast_border_color\\\": \\\"#7c3aed\\\",\\n    \\\"toast_gradient\\\": False,\\n    \\\"toast_gradient_end\\\": \\\"#101625\\\",\\n    \\\"toast_shadow\\\": True,\\n    \\\"toast_accent_stripe\\\": False,\\n    \\\"toast_text_align\\\": \\\"left\\\",\\n    \\\"toast_auto_dismiss\\\": True,\\n    \\\"toast_click_action\\\": \\\"dismiss\\\",\\n    \\\"toast_progress_bar\\\": False,\\n    \\\"toast_enable_sound\\\": True,\\n    \\\"toast_sound_effect\\\": \\\"mac_connect\\\",\\n    \\\"wellness_points\\\": 0,\\n    \\\"current_streak\\\": 0,\\n    \\\"ht_enabled\\\": True,\\n    \\\"ht_interval_min\\\": 10,\\n    \\\"ht_duration_sec\\\": 5,\\n    \\\"ht_cat_breathing\\\": True,\\n    \\\"ht_cat_eye_care\\\": True,\\n    \\\"ht_cat_posture\\\": True,\\n    \\\"ht_cat_stretch\\\": True,\\n    \\\"ht_cat_hydration\\\": True,\\n    \\\"ht_cat_mental\\\": True,\\n    \\\"ht_cat_hands_wrists\\\": True,\\n    \\\"ht_toast_pos\\\": \\\"Right\\\",\\n    \\\"ht_toast_custom_x\\\": 100,\\n    \\\"ht_toast_custom_y\\\": 100,\\n    \\\"ht_toast_width\\\": 280,\\n    \\\"ht_toast_height\\\": 70,\\n    \\\"ht_toast_bg_color\\\"\n<truncated 2299 bytes>",
  "TargetFile": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Replacing DEFAULT_SETTINGS\"",
  "toolSummary": "\"Replace DEFAULT_SETTINGS\""
}
```

---

### File: `scratch/extracted/step_69_tc_0.json`
- **Path:** `scratch/extracted/step_69_tc_0.json`
- **Estimated Tokens:** 68
- **mtime:** 1780659608.184

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "575",
  "StartLine": "520",
  "toolAction": "\"Viewing generate_breathing_sound function\"",
  "toolSummary": "\"View generate_breathing_sound function\""
}
```

---

### File: `scratch/extracted/step_71_tc_0.json`
- **Path:** `scratch/extracted/step_71_tc_0.json`
- **Estimated Tokens:** 66
- **mtime:** 1780659608.185

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "585",
  "StartLine": "570",
  "toolAction": "\"Viewing generate_breathing_sound end\"",
  "toolSummary": "\"View generate_breathing_sound end\""
}
```

---

### File: `scratch/extracted/step_73_replacement.py`
- **Path:** `scratch/extracted/step_73_replacement.py`
- **Estimated Tokens:** 517
- **mtime:** 1780659608.189

```python
"def generate_breathing_sound(duration_sec:\n    int = 65):\n    \"\"\"Generate a stereo WAV with breathing-like tones and 8D panning effect.\"\"\"\n    if os.path.exists(BREATHING_WAV):\n        return\n\n    logger.info(\"Generating 8D breathing sound...\")\n    sample_rate = 44100\n    n_samples = sample_rate * duration_sec\n    samples = []\n    breath_cycle = 4.0\n    freq_base = 220\n    pan_speed = 0.15\n\n    for i in range(n_samples):\n        t = i / sample_rate\n        breath_phase = (t % breath_cycle) / breath_cycle\n\n        if breath_phase < 0.5:\n            envelope = math.sin(breath_phase * math.pi)\n        else:\n            envelope = math.sin(breath_phase * math.pi) * 0.6\n\n        envelope = max(0, envelope) * 0.35\n\n        tone = (\n            math.sin(2 * math.pi * freq_base * t) * 0.4\n            + math.sin(2 * math.pi * freq_base * 1.5 * t) * 0.2\n            + math.sin(2 * math.pi * freq_base * 2 * t) * 0.15\n            + math.sin(2 * math.pi * freq_base * 0.5 * t) * 0.25\n        )\n\n        pan = math.sin(2 * math.pi * pan_speed * t)\n        left_vol = math.sqrt(0.5 * (1 + pan))\n        right_vol = math.sqrt(0.5 * (1 - pan))\n\n        sample_val = tone * envelope\n        left_sample = max(-32767, min(32767, int(sample_val * left_vol * 32767)))\n        right_sample = max(-32767, min(32767, int(sample_val * right_vol * 32767)))\n\n        samples.append(left_sample)\n        samples.append(right_sample)\n\n    with wave.open(BREATHING_WAV, \"w\") as wav:\n        wav.setnchannels(2)\n        wav.setsampwidth(2)\n        wav.setframerate(sample_rate)\n        wav.writeframes(struct.pack(f\"<{len(samples)}h\", *samples))\n\n    logger.info(f\"8D breathing sound saved: {BREATHING_WAV}\")\n\n\ndef ensure_sound_effects():\n    \"\"\"Download sound effects from the web, with local synthesis as a robust fallback.\"\"\"\n    sounds_dir = os.path.join(SCRIPT_DIR, \"resources\", \"sounds\")\n    os.makedirs(sounds_dir, exist_ok=True)\n    \n    sounds = {\n        \"cyber_alert.wav\
<truncated 7540 bytes>
```

---

### File: `scratch/extracted/step_73_tc_0.json`
- **Path:** `scratch/extracted/step_73_tc_0.json`
- **Estimated Tokens:** 1,133
- **mtime:** 1780659608.187

```json
{
  "AllowMultiple": "false",
  "Description": "\"Add ensure_sound_effects and _synthesize_wav functions.\"",
  "EndLine": "577",
  "Instruction": "\"Add ensure_sound_effects and _synthesize_wav after generate_breathing_sound.\"",
  "ReplacementContent": "\"def generate_breathing_sound(duration_sec:\\n    int = 65):\\n    \\\"\\\"\\\"Generate a stereo WAV with breathing-like tones and 8D panning effect.\\\"\\\"\\\"\\n    if os.path.exists(BREATHING_WAV):\\n        return\\n\\n    logger.info(\\\"Generating 8D breathing sound...\\\")\\n    sample_rate = 44100\\n    n_samples = sample_rate * duration_sec\\n    samples = []\\n    breath_cycle = 4.0\\n    freq_base = 220\\n    pan_speed = 0.15\\n\\n    for i in range(n_samples):\\n        t = i / sample_rate\\n        breath_phase = (t % breath_cycle) / breath_cycle\\n\\n        if breath_phase < 0.5:\\n            envelope = math.sin(breath_phase * math.pi)\\n        else:\\n            envelope = math.sin(breath_phase * math.pi) * 0.6\\n\\n        envelope = max(0, envelope) * 0.35\\n\\n        tone = (\\n            math.sin(2 * math.pi * freq_base * t) * 0.4\\n            + math.sin(2 * math.pi * freq_base * 1.5 * t) * 0.2\\n            + math.sin(2 * math.pi * freq_base * 2 * t) * 0.15\\n            + math.sin(2 * math.pi * freq_base * 0.5 * t) * 0.25\\n        )\\n\\n        pan = math.sin(2 * math.pi * pan_speed * t)\\n        left_vol = math.sqrt(0.5 * (1 + pan))\\n        right_vol = math.sqrt(0.5 * (1 - pan))\\n\\n        sample_val = tone * envelope\\n        left_sample = max(-32767, min(32767, int(sample_val * left_vol * 32767)))\\n        right_sample = max(-32767, min(32767, int(sample_val * right_vol * 32767)))\\n\\n        samples.append(left_sample)\\n        samples.append(right_sample)\\n\\n    with wave.open(BREATHING_WAV, \\\"w\\\") as wav:\\n        wav.setnchannels(2)\\n        wav.setsampwidth(2)\\n        wav.setframerate(sample_rate)\\n        wav.writeframes(struct.pack(f\\\"<{len(samples)}h\\\", *samples))\\n\\n    logger.info(f\\\"8D breathing sound saved: {BREATHING_WAV}\\\")\\n\\n\\ndef ensure_sound_effects():\\n    \\\"\\\"\\\"Download sound effects from the web, with local synthesis as a robust fallback.\\\"\\\"\\\"\\n    sounds_dir = os.path.join(SCRIPT_DIR, \\\"resources\\\", \\\"sounds\\\")\\n    os.makedirs(sounds_dir, exist_ok=True)\\n    \\n    sounds = {\\n        \\\"cyber_alert.wav\\\n<truncated 7540 bytes>",
  "StartLine": "527",
  "TargetContent": "\"def generate_breathing_sound(duration_sec:\\n    int = 65):\\n    \\\"\\\"\\\"Generate a stereo WAV with breathing-like tones and 8D panning effect.\\\"\\\"\\\"\\n    if os.path.exists(BREATHING_WAV):\\n        return\\n\\n    logger.info(\\\"Generating 8D breathing sound...\\\")\\n    sample_rate = 44100\\n    n_samples = sample_rate * duration_sec\\n    samples = []\\n    breath_cycle = 4.0\\n    freq_base = 220\\n    pan_speed = 0.15\\n\\n    for i in range(n_samples):\\n        t = i / sample_rate\\n        breath_phase = (t % breath_cycle) / breath_cycle\\n\\n        if breath_phase < 0.5:\\n            envelope = math.sin(breath_phase * math.pi)\\n        else:\\n            envelope = math.sin(breath_phase * math.pi) * 0.6\\n\\n        envelope = max(0, envelope) * 0.35\\n\\n        tone = (\\n            math.sin(2 * math.pi * freq_base * t) * 0.4\\n            + math.sin(2 * math.pi * freq_base * 1.5 * t) * 0.2\\n            + math.sin(2 * math.pi * freq_base * 2 * t) * 0.15\\n            + math.sin(2 * math.pi * freq_base * 0.5 * t) * 0.25\\n        )\\n\\n        pan = math.sin(2 * math.pi * pan_speed * t)\\n        left_vol = math.sqrt(0.5 * (1 + pan))\\n        right_vol = math.sqrt(0.5 * (1 - pan))\\n\\n        sample_val = tone * envelope\\n        left_sample = max(-32767, min(32767, int(sample_val * left_vol * 32767)))\\n        right_sample = max(-32767, min(32767, int(sample_val * right_vol * 32767)))\\n\\n        samples.append(left_sample)\\n        samples.append(right_sample)\\n\\n    with wave.open(BREATHING_WAV, \\\"w\\\") as wav:\\n        wav.setnchannels(2)\\n        wav.setsampwidth(2)\\n        wav.setframerate(sample_rate)\\n        wav.writeframes(struct.pack(f\\\"<{len(samples)}h\\\", *samples))\\n\\n    logger.info(f\\\"8D breathing sound saved: {BREATHING_WAV}\\\")\"",
  "TargetFile": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Adding sound generation functions\"",
  "toolSummary": "\"Add sound generation functions\""
}
```

---

### File: `scratch/extracted/step_75_tc_0.json`
- **Path:** `scratch/extracted/step_75_tc_0.json`
- **Estimated Tokens:** 74
- **mtime:** 1780659608.19

```json
{
  "CaseInsensitive": "false",
  "IsRegex": "false",
  "MatchPerLine": "true",
  "Query": "\"def run(self):\"",
  "SearchPath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Locating run method\"",
  "toolSummary": "\"Locate run method\""
}
```

---

### File: `scratch/extracted/step_77_tc_0.json`
- **Path:** `scratch/extracted/step_77_tc_0.json`
- **Estimated Tokens:** 90
- **mtime:** 1780659608.192

```json
{
  "CaseInsensitive": "false",
  "IsRegex": "false",
  "MatchPerLine": "true",
  "Query": "\"generate_breathing_sound()\"",
  "SearchPath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Searching for generate_breathing_sound calls\"",
  "toolSummary": "\"Search for generate_breathing_sound calls\""
}
```

---

### File: `scratch/extracted/step_79_tc_0.json`
- **Path:** `scratch/extracted/step_79_tc_0.json`
- **Estimated Tokens:** 91
- **mtime:** 1780659608.193

```json
{
  "CaseInsensitive": "false",
  "IsRegex": "false",
  "MatchPerLine": "true",
  "Query": "\"generate_breathing_sound\"",
  "SearchPath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Searching for generate_breathing_sound reference\"",
  "toolSummary": "\"Search for generate_breathing_sound reference\""
}
```

---

### File: `scratch/extracted/step_81_tc_0.json`
- **Path:** `scratch/extracted/step_81_tc_0.json`
- **Estimated Tokens:** 62
- **mtime:** 1780659608.194

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "2670",
  "StartLine": "2500",
  "toolAction": "\"Viewing run method location\"",
  "toolSummary": "\"View run method location\""
}
```

---

### File: `scratch/extracted/step_83_replacement.py`
- **Path:** `scratch/extracted/step_83_replacement.py`
- **Estimated Tokens:** 511
- **mtime:** 1780659608.197

```python
"    def run(self):\n        logger.info(\"=\" * 50)\n        logger.info(\"Health App starting...\")\n        self._start_udp_listener()\n        logger.info(f\"Settings: {json.dumps(self.settings, indent=2)}\")\n\n        generate_breathing_sound()\n        ensure_sound_effects()\n\n        boot = datetime.datetime.fromtimestamp(psutil.boot_time())\n        uptime = datetime.datetime.now() - boot\n        logger.info(f\"System uptime: {uptime}\")\n\n        # Initialize the media controller early\n        get_media_controller()\n\n        icon_image = create_health_icon(self._paused)\n        self.tray_icon = pystray.Icon(\n            name=\"HealthApp\",\n            icon=icon_image,\n            title=f\"Health App — Streak: {self.settings.get('current_streak', 0)} 🔥 | Points: {self.settings.get('wellness_points', 0)} 💎\",\n            menu=pystray.Menu(\n                pystray.MenuItem(\"👁️ Take Break Now\", self._on_take_break),\n                pystray.MenuItem(\"⏭ Skip Next Break\", self._on_skip),\n                pystray.Menu.SEPARATOR,\n                pystray.MenuItem(\"⚙️ Settings\", self._on_settings),\n                pystray.MenuItem(\n                    lambda item: \"▶ Resume\" if self._paused else \"⏸ Pause\",\n                    self._on_pause_resume,\n                ),\n                pystray.Menu.SEPARATOR,\n                pystray.MenuItem(\"Quit\", self._on_quit),\n            ),\n        )\n\n        scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)\n        scheduler_thread.start()\n\n        health_toast_thread = threading.Thread(target=self._health_toast_loop, daemon=True)\n        health_toast_thread.start()\n        \n        bc_thread = threading.Thread(target=self._brightness_care_loop, daemon=True)\n        bc_thread.start()\n\n        nc_thread = threading.Thread(target=self._night_care_loop, daemon=True)\n        nc_thread.start()\n\n        logger.info(\"Tray icon running detached.\")\n        self.tray_icon.run_detached()
<truncated 533 bytes>
```

---

### File: `scratch/extracted/step_83_tc_0.json`
- **Path:** `scratch/extracted/step_83_tc_0.json`
- **Estimated Tokens:** 1,237
- **mtime:** 1780659608.196

```json
{
  "AllowMultiple": "false",
  "Description": "\"Call ensure_sound_effects() in HealthApp.run() and debug main block.\"",
  "EndLine": "2645",
  "Instruction": "\"Call ensure_sound_effects() in HealthApp.run() and debug main block.\"",
  "ReplacementContent": "\"    def run(self):\\n        logger.info(\\\"=\\\" * 50)\\n        logger.info(\\\"Health App starting...\\\")\\n        self._start_udp_listener()\\n        logger.info(f\\\"Settings: {json.dumps(self.settings, indent=2)}\\\")\\n\\n        generate_breathing_sound()\\n        ensure_sound_effects()\\n\\n        boot = datetime.datetime.fromtimestamp(psutil.boot_time())\\n        uptime = datetime.datetime.now() - boot\\n        logger.info(f\\\"System uptime: {uptime}\\\")\\n\\n        # Initialize the media controller early\\n        get_media_controller()\\n\\n        icon_image = create_health_icon(self._paused)\\n        self.tray_icon = pystray.Icon(\\n            name=\\\"HealthApp\\\",\\n            icon=icon_image,\\n            title=f\\\"Health App \u2014 Streak: {self.settings.get('current_streak', 0)} \ud83d\udd25 | Points: {self.settings.get('wellness_points', 0)} \ud83d\udc8e\\\",\\n            menu=pystray.Menu(\\n                pystray.MenuItem(\\\"\ud83d\udc41\ufe0f Take Break Now\\\", self._on_take_break),\\n                pystray.MenuItem(\\\"\u23ed Skip Next Break\\\", self._on_skip),\\n                pystray.Menu.SEPARATOR,\\n                pystray.MenuItem(\\\"\u2699\ufe0f Settings\\\", self._on_settings),\\n                pystray.MenuItem(\\n                    lambda item: \\\"\u25b6 Resume\\\" if self._paused else \\\"\u23f8 Pause\\\",\\n                    self._on_pause_resume,\\n                ),\\n                pystray.Menu.SEPARATOR,\\n                pystray.MenuItem(\\\"Quit\\\", self._on_quit),\\n            ),\\n        )\\n\\n        scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)\\n        scheduler_thread.start()\\n\\n        health_toast_thread = threading.Thread(target=self._health_toast_loop, daemon=True)\\n        health_toast_thread.start()\\n        \\n        bc_thread = threading.Thread(target=self._brightness_care_loop, daemon=True)\\n        bc_thread.start()\\n\\n        nc_thread = threading.Thread(target=self._night_care_loop, daemon=True)\\n        nc_thread.start()\\n\\n        logger.info(\\\"Tray icon running detached.\\\")\\n        self.tray_icon.run_detached()\n<truncated 533 bytes>",
  "StartLine": "2577",
  "TargetContent": "\"    def run(self):\\n        logger.info(\\\"=\\\" * 50)\\n        logger.info(\\\"Health App starting...\\\")\\n        self._start_udp_listener()\\n        logger.info(f\\\"Settings: {json.dumps(self.settings, indent=2)}\\\")\\n\\n        generate_breathing_sound()\\n\\n        boot = datetime.datetime.fromtimestamp(psutil.boot_time())\\n        uptime = datetime.datetime.now() - boot\\n        logger.info(f\\\"System uptime: {uptime}\\\")\\n\\n        # Initialize the media controller early\\n        get_media_controller()\\n\\n        icon_image = create_health_icon(self._paused)\\n        self.tray_icon = pystray.Icon(\\n            name=\\\"HealthApp\\\",\\n            icon=icon_image,\\n            title=f\\\"Health App \u2014 Streak: {self.settings.get('current_streak', 0)} \ud83d\udd25 | Points: {self.settings.get('wellness_points', 0)} \ud83d\udc8e\\\",\\n            menu=pystray.Menu(\\n                pystray.MenuItem(\\\"\ud83d\udc41\ufe0f Take Break Now\\\", self._on_take_break),\\n                pystray.MenuItem(\\\"\u23ed Skip Next Break\\\", self._on_skip),\\n                pystray.Menu.SEPARATOR,\\n                pystray.MenuItem(\\\"\u2699\ufe0f Settings\\\", self._on_settings),\\n                pystray.MenuItem(\\n                    lambda item: \\\"\u25b6 Resume\\\" if self._paused else \\\"\u23f8 Pause\\\",\\n                    self._on_pause_resume,\\n                ),\\n                pystray.Menu.SEPARATOR,\\n                pystray.MenuItem(\\\"Quit\\\", self._on_quit),\\n            ),\\n        )\\n\\n        scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)\\n        scheduler_thread.start()\\n\\n        health_toast_thread = threading.Thread(target=self._health_toast_loop, daemon=True)\\n        health_toast_thread.start()\\n        \\n        bc_thread = threading.Thread(target=self._brightness_care_loop, daemon=True)\\n        bc_thread.start()\\n\\n        nc_thread = threading.Thread(target=self._night_care_loop, daemon=True)\\n        nc_thread.start()\\n\\n        logger.info(\\\"Tray icon running detached.\\\")\\n        self.tray_icon.run_detached()\\n\\n        self.root = tk.Tk()\\\n<truncated 469 bytes>",
  "TargetFile": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Calling ensure_sound_effects\"",
  "toolSummary": "\"Call ensure_sound_effects\""
}
```

---

### File: `scratch/extracted/step_85_tc_0.json`
- **Path:** `scratch/extracted/step_85_tc_0.json`
- **Estimated Tokens:** 63
- **mtime:** 1780659608.198

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "2110",
  "StartLine": "2000",
  "toolAction": "\"Viewing loops in health_app.py\"",
  "toolSummary": "\"View loops in health_app.py\""
}
```

---

### File: `scratch/extracted/step_87_replacement.py`
- **Path:** `scratch/extracted/step_87_replacement.py`
- **Estimated Tokens:** 517
- **mtime:** 1780659608.201

```python
"    def _scheduler_loop(self):\n        \"\"\"Background thread: schedule breaks based on configured intervals.\"\"\"\n        logger.info(\"Break scheduler started.\")\n        last_weather_check = 0\n        last_loop_time = time.time()\n\n        while self._running:\n            try:\n                now = time.time()\n                elapsed = now - last_loop_time\n                last_loop_time = now\n                \n                if elapsed > 10.0:\n                    logger.info(f\"[RESUME] System sleep/hibernate/suspend detected in scheduler loop (elapsed={elapsed:.1f}s). Resetting break timers.\")\n                    self._last_short_break = now\n                    self._last_long_break = now\n                    self._short_warn_shown = False\n                    self._long_warn_shown = False\n                \n                if not system_utils.is_system_awake_and_unlocked():\n                    time.sleep(2)\n                    continue\n\n                self._maybe_update_weather(now, last_weather_check)\n                if not self._game_mode and self.settings.get(\"nl_enabled\", True) and now - last_weather_check > 1800:\n                    last_weather_check = now\n\n                self._maybe_reapply_gamma(now)\n\n                if self._paused:\n                    time.sleep(1)\n                    self._last_short_break += 1\n                    self._last_long_break += 1\n                    continue\n\n                if self._game_mode and not self.settings.get(\"run_during_game\", True):\n                    self._handle_game_mode_postpone(now)\n                    time.sleep(5)\n                    continue\n\n                if self._handle_lock_screen(now):\n                    continue\n\n                self._check_and_trigger_breaks(now)\n\n            except Exception as e:\n                logger.error(f\"Scheduler error: {e}\")\n\n            time.sleep(1)\n\n    def _health_toast_loop(self):\n        \"\"\"Background thread: show health toast reminders periodicall
<truncated 1525 bytes>
```

---

### File: `scratch/extracted/step_87_tc_0.json`
- **Path:** `scratch/extracted/step_87_tc_0.json`
- **Estimated Tokens:** 1,220
- **mtime:** 1780659608.2

```json
{
  "AllowMultiple": "false",
  "Description": "\"Implement sleep/wake detection in _scheduler_loop and _health_toast_loop.\"",
  "EndLine": "2108",
  "Instruction": "\"Implement sleep/wake detection in _scheduler_loop and _health_toast_loop.\"",
  "ReplacementContent": "\"    def _scheduler_loop(self):\\n        \\\"\\\"\\\"Background thread: schedule breaks based on configured intervals.\\\"\\\"\\\"\\n        logger.info(\\\"Break scheduler started.\\\")\\n        last_weather_check = 0\\n        last_loop_time = time.time()\\n\\n        while self._running:\\n            try:\\n                now = time.time()\\n                elapsed = now - last_loop_time\\n                last_loop_time = now\\n                \\n                if elapsed > 10.0:\\n                    logger.info(f\\\"[RESUME] System sleep/hibernate/suspend detected in scheduler loop (elapsed={elapsed:.1f}s). Resetting break timers.\\\")\\n                    self._last_short_break = now\\n                    self._last_long_break = now\\n                    self._short_warn_shown = False\\n                    self._long_warn_shown = False\\n                \\n                if not system_utils.is_system_awake_and_unlocked():\\n                    time.sleep(2)\\n                    continue\\n\\n                self._maybe_update_weather(now, last_weather_check)\\n                if not self._game_mode and self.settings.get(\\\"nl_enabled\\\", True) and now - last_weather_check > 1800:\\n                    last_weather_check = now\\n\\n                self._maybe_reapply_gamma(now)\\n\\n                if self._paused:\\n                    time.sleep(1)\\n                    self._last_short_break += 1\\n                    self._last_long_break += 1\\n                    continue\\n\\n                if self._game_mode and not self.settings.get(\\\"run_during_game\\\", True):\\n                    self._handle_game_mode_postpone(now)\\n                    time.sleep(5)\\n                    continue\\n\\n                if self._handle_lock_screen(now):\\n                    continue\\n\\n                self._check_and_trigger_breaks(now)\\n\\n            except Exception as e:\\n                logger.error(f\\\"Scheduler error: {e}\\\")\\n\\n            time.sleep(1)\\n\\n    def _health_toast_loop(self):\\n        \\\"\\\"\\\"Background thread: show health toast reminders periodicall\n<truncated 1525 bytes>",
  "StartLine": "2038",
  "TargetContent": "\"    def _scheduler_loop(self):\\n        \\\"\\\"\\\"Background thread: schedule breaks based on configured intervals.\\\"\\\"\\\"\\n        logger.info(\\\"Break scheduler started.\\\")\\n        last_weather_check = 0\\n\\n        while self._running:\\n            try:\\n                now = time.time()\\n                \\n                if not system_utils.is_system_awake_and_unlocked():\\n                    time.sleep(2)\\n                    continue\\n\\n                self._maybe_update_weather(now, last_weather_check)\\n                if not self._game_mode and self.settings.get(\\\"nl_enabled\\\", True) and now - last_weather_check > 1800:\\n                    last_weather_check = now\\n\\n                self._maybe_reapply_gamma(now)\\n\\n                if self._paused:\\n                    time.sleep(1)\\n                    self._last_short_break += 1\\n                    self._last_long_break += 1\\n                    continue\\n\\n                if self._game_mode and not self.settings.get(\\\"run_during_game\\\", True):\\n                    self._handle_game_mode_postpone(now)\\n                    time.sleep(5)\\n                    continue\\n\\n                if self._handle_lock_screen(now):\\n                    continue\\n\\n                self._check_and_trigger_breaks(now)\\n\\n            except Exception as e:\\n                logger.error(f\\\"Scheduler error: {e}\\\")\\n\\n            time.sleep(1)\\n\\n    def _health_toast_loop(self):\\n        \\\"\\\"\\\"Background thread: show health toast reminders periodically.\\\"\\\"\\\"\\n        logger.info(\\\"Health toast scheduler started.\\\")\\n        self._last_health_toast = time.time()\\n\\n        while self._running:\\n            try:\\n                if not system_utils.is_system_awake_and_unlocked():\\n                    time.sleep(2)\\n                    continue\\n                if not self.settings.get(\\\"ht_enabled\\\", True):\\n                    time.sleep(1)\\n                    continue\\n\\n                if self._paused:\\n                    time.sleep(1)\\n                    self._last_healt\n<truncated 544 bytes>",
  "TargetFile": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Adding sleep checks in scheduler and health loops\"",
  "toolSummary": "\"Add sleep checks in loops\""
}
```

---

### File: `scratch/extracted/step_89_tc_0.json`
- **Path:** `scratch/extracted/step_89_tc_0.json`
- **Estimated Tokens:** 63
- **mtime:** 1780659608.202

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1930",
  "StartLine": "1870",
  "toolAction": "\"Viewing BrightnessWarningToast\"",
  "toolSummary": "\"View BrightnessWarningToast\""
}
```

---

### File: `scratch/extracted/step_91_tc_0.json`
- **Path:** `scratch/extracted/step_91_tc_0.json`
- **Estimated Tokens:** 65
- **mtime:** 1780659608.205

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "1945",
  "StartLine": "1925",
  "toolAction": "\"Viewing BrightnessWarningToast end\"",
  "toolSummary": "\"View BrightnessWarningToast end\""
}
```

---

### File: `scratch/extracted/step_93_replacement.py`
- **Path:** `scratch/extracted/step_93_replacement.py`
- **Estimated Tokens:** 516
- **mtime:** 1780659608.209

```python
"class BrightnessWarningToast:\n    def __init__(self, parent, settings, on_skip, on_decrease):\n        self.parent = parent\n        self.settings = settings\n        self.on_skip = on_skip\n        self.on_decrease = on_decrease\n        self.window = None\n\n    def show(self):\n        try:\n            from toast_utils import ToastQueue\n            ToastQueue.add(self)\n        except Exception:\n            self._create_toast()\n\n    def _create_toast(self):\n        self.window = tk.Toplevel(self.parent)\n        self.window.title(\"Brightness Warning\")\n        self.window.overrideredirect(True)\n        self.window.attributes(\"-topmost\", True)\n        self.window.configure(bg=\"#1a1a2e\")\n        \n        w, h = 320, 130\n        sw = self.window.winfo_screenwidth()\n        sh = self.window.winfo_screenheight()\n        self.window.geometry(f\"{w}x{h}+{sw-w-20}+{sh-h-60}\")\n        \n        try:\n            apply_dwm_rounding(self.window)\n        except Exception:\n            pass\n\n        tk.Label(self.window, text=\"⚠️ BRIGHTNESS TOO HIGH\", font=(\"Consolas\", 12, \"bold\"), bg=\"#1a1a2e\", fg=\"#ff2a2a\").pack(pady=(15, 5))\n        tk.Label(self.window, text=\"Reduce brightness for eye health?\", font=(\"Consolas\", 10), bg=\"#1a1a2e\", fg=\"#e2e8f0\").pack()\n        \n        bf = tk.Frame(self.window, bg=\"#1a1a2e\")\n        bf.pack(pady=15)\n        \n        tk.Button(bf, text=\"SKIP\", command=self._skip, bg=\"#16213e\", fg=\"#e2e8f0\", relief=tk.FLAT, cursor=\"hand2\", padx=15, pady=4).pack(side=tk.LEFT, padx=10)\n        tk.Button(bf, text=\"DECREASE\", command=self._decrease, bg=\"#00f0ff\", fg=\"#000000\", relief=tk.FLAT, cursor=\"hand2\", padx=15, pady=4).pack(side=tk.LEFT, padx=10)\n\n        # Notify queue on destruction\n        def on_destroy(event):\n            if event.widget == self.window:\n                try:\n                    from toast_utils import ToastQueue\n                    ToastQueue.on_toast_closed(self.parent)\n                except Exceptio
<truncated 1602 bytes>
```

---

### File: `scratch/extracted/step_93_tc_0.json`
- **Path:** `scratch/extracted/step_93_tc_0.json`
- **Estimated Tokens:** 1,169
- **mtime:** 1780659608.206

```json
{
  "AllowMultiple": "false",
  "Description": "\"Integrate BrightnessWarningToast with ToastQueue and add sound customization support.\"",
  "EndLine": "1934",
  "Instruction": "\"Replace BrightnessWarningToast class definition to add sound play and ToastQueue integration.\"",
  "ReplacementContent": "\"class BrightnessWarningToast:\\n    def __init__(self, parent, settings, on_skip, on_decrease):\\n        self.parent = parent\\n        self.settings = settings\\n        self.on_skip = on_skip\\n        self.on_decrease = on_decrease\\n        self.window = None\\n\\n    def show(self):\\n        try:\\n            from toast_utils import ToastQueue\\n            ToastQueue.add(self)\\n        except Exception:\\n            self._create_toast()\\n\\n    def _create_toast(self):\\n        self.window = tk.Toplevel(self.parent)\\n        self.window.title(\\\"Brightness Warning\\\")\\n        self.window.overrideredirect(True)\\n        self.window.attributes(\\\"-topmost\\\", True)\\n        self.window.configure(bg=\\\"#1a1a2e\\\")\\n        \\n        w, h = 320, 130\\n        sw = self.window.winfo_screenwidth()\\n        sh = self.window.winfo_screenheight()\\n        self.window.geometry(f\\\"{w}x{h}+{sw-w-20}+{sh-h-60}\\\")\\n        \\n        try:\\n            apply_dwm_rounding(self.window)\\n        except Exception:\\n            pass\\n\\n        tk.Label(self.window, text=\\\"\u26a0\ufe0f BRIGHTNESS TOO HIGH\\\", font=(\\\"Consolas\\\", 12, \\\"bold\\\"), bg=\\\"#1a1a2e\\\", fg=\\\"#ff2a2a\\\").pack(pady=(15, 5))\\n        tk.Label(self.window, text=\\\"Reduce brightness for eye health?\\\", font=(\\\"Consolas\\\", 10), bg=\\\"#1a1a2e\\\", fg=\\\"#e2e8f0\\\").pack()\\n        \\n        bf = tk.Frame(self.window, bg=\\\"#1a1a2e\\\")\\n        bf.pack(pady=15)\\n        \\n        tk.Button(bf, text=\\\"SKIP\\\", command=self._skip, bg=\\\"#16213e\\\", fg=\\\"#e2e8f0\\\", relief=tk.FLAT, cursor=\\\"hand2\\\", padx=15, pady=4).pack(side=tk.LEFT, padx=10)\\n        tk.Button(bf, text=\\\"DECREASE\\\", command=self._decrease, bg=\\\"#00f0ff\\\", fg=\\\"#000000\\\", relief=tk.FLAT, cursor=\\\"hand2\\\", padx=15, pady=4).pack(side=tk.LEFT, padx=10)\\n\\n        # Notify queue on destruction\\n        def on_destroy(event):\\n            if event.widget == self.window:\\n                try:\\n                    from toast_utils import ToastQueue\\n                    ToastQueue.on_toast_closed(self.parent)\\n                except Exceptio\n<truncated 1602 bytes>",
  "StartLine": "1893",
  "TargetContent": "\"class BrightnessWarningToast:\\n    def __init__(self, parent, on_skip, on_decrease):\\n        self.parent = parent\\n        self.on_skip = on_skip\\n        self.on_decrease = on_decrease\\n\\n    def show(self):\\n        self.window = tk.Toplevel(self.parent)\\n        self.window.title(\\\"Brightness Warning\\\")\\n        self.window.overrideredirect(True)\\n        self.window.attributes(\\\"-topmost\\\", True)\\n        self.window.configure(bg=\\\"#1a1a2e\\\")\\n        \\n        w, h = 320, 130\\n        sw = self.window.winfo_screenwidth()\\n        sh = self.window.winfo_screenheight()\\n        self.window.geometry(f\\\"{w}x{h}+{sw-w-20}+{sh-h-60}\\\")\\n        \\n        try:\\n            apply_dwm_rounding(self.window)\\n        except Exception:\\n            pass\\n\\n        tk.Label(self.window, text=\\\"\u26a0\ufe0f BRIGHTNESS TOO HIGH\\\", font=(\\\"Consolas\\\", 12, \\\"bold\\\"), bg=\\\"#1a1a2e\\\", fg=\\\"#ff2a2a\\\").pack(pady=(15, 5))\\n        tk.Label(self.window, text=\\\"Reduce brightness for eye health?\\\", font=(\\\"Consolas\\\", 10), bg=\\\"#1a1a2e\\\", fg=\\\"#e2e8f0\\\").pack()\\n        \\n        bf = tk.Frame(self.window, bg=\\\"#1a1a2e\\\")\\n        bf.pack(pady=15)\\n        \\n        tk.Button(bf, text=\\\"SKIP\\\", command=self._skip, bg=\\\"#16213e\\\", fg=\\\"#e2e8f0\\\", relief=tk.FLAT, cursor=\\\"hand2\\\", padx=15, pady=4).pack(side=tk.LEFT, padx=10)\\n        tk.Button(bf, text=\\\"DECREASE\\\", command=self._decrease, bg=\\\"#00f0ff\\\", fg=\\\"#000000\\\", relief=tk.FLAT, cursor=\\\"hand2\\\", padx=15, pady=4).pack(side=tk.LEFT, padx=10)\\n\\n    def _skip(self):\\n        self.window.destroy()\\n        if self.on_skip:\\n            self.on_skip()\\n\\n    def _decrease(self):\\n        self.window.destroy()\\n        if self.on_decrease:\\n            self.on_decrease()\"",
  "TargetFile": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Integrating BrightnessWarningToast with ToastQueue\"",
  "toolSummary": "\"Integrate BrightnessWarningToast with ToastQueue\""
}
```

---

### File: `scratch/extracted/step_95_tc_0.json`
- **Path:** `scratch/extracted/step_95_tc_0.json`
- **Estimated Tokens:** 64
- **mtime:** 1780659608.21

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "2575",
  "StartLine": "2555",
  "toolAction": "\"Viewing brightness warning call\"",
  "toolSummary": "\"View brightness warning call\""
}
```

---

### File: `scratch/extracted/step_97_tc_0.json`
- **Path:** `scratch/extracted/step_97_tc_0.json`
- **Estimated Tokens:** 64
- **mtime:** 1780659608.212

```json
{
  "AbsolutePath": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "EndLine": "2640",
  "StartLine": "2576",
  "toolAction": "\"Viewing process gui queue method\"",
  "toolSummary": "\"View process gui queue method\""
}
```

---

### File: `scratch/extracted/step_99_replacement.py`
- **Path:** `scratch/extracted/step_99_replacement.py`
- **Estimated Tokens:** 26
- **mtime:** 1780659608.214

```python
"                    BrightnessWarningToast(self.root, self.settings, _on_bc_skip, _on_bc_decrease).show()"
```

---

### File: `scratch/extracted/step_99_tc_0.json`
- **Path:** `scratch/extracted/step_99_tc_0.json`
- **Estimated Tokens:** 180
- **mtime:** 1780659608.213

```json
{
  "AllowMultiple": "false",
  "Description": "\"Pass settings dictionary to BrightnessWarningToast in _process_gui_queue.\"",
  "EndLine": "2627",
  "Instruction": "\"Pass settings to BrightnessWarningToast.\"",
  "ReplacementContent": "\"                    BrightnessWarningToast(self.root, self.settings, _on_bc_skip, _on_bc_decrease).show()\"",
  "StartLine": "2622",
  "TargetContent": "\"                    BrightnessWarningToast(self.root, _on_bc_skip, _on_bc_decrease).show()\"",
  "TargetFile": "\"c:\\\\Users\\\\NANDHA A\\\\Desktop\\\\UTILITIES\\\\HealthApp\\\\health_app.py\"",
  "toolAction": "\"Passing settings to BrightnessWarningToast\"",
  "toolSummary": "\"Pass settings to BrightnessWarningToast\""
}
```

---

### File: `scratch/find_port_8555.py`
- **Path:** `scratch/find_port_8555.py`
- **Estimated Tokens:** 85
- **mtime:** 1780925206.114

```python
import psutil
port = 8555
procs = []
for c in psutil.net_connections(kind='inet'):
    if c.laddr and c.laddr.port == port:
        try:
            p = psutil.Process(c.pid)
            procs.append((c.pid, p.name(), p.cmdline(), c.status))
        except Exception:
            procs.append((c.pid, '<unknown>', [], c.status))
print(procs)
```

---

### File: `scratch/inspect_filepicker.py`
- **Path:** `scratch/inspect_filepicker.py`
- **Estimated Tokens:** 23
- **mtime:** 1780573334.858

```python
import flet as ft
picker = ft.FilePicker()
print("Control Type:", picker._get_control_name())
```

---

### File: `scratch/inspect_reflex_api.py`
- **Path:** `scratch/inspect_reflex_api.py`
- **Estimated Tokens:** 166
- **mtime:** 1780924950.188

```python
import importlib.machinery
import importlib.util
from pathlib import Path
import sys

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

p = root / 'MovieSongDownloader' / 'MovieSongDownloader.py'
loader = importlib.machinery.SourceFileLoader('movieapp', str(p))
spec = importlib.util.spec_from_loader(loader.name, loader)
mod = importlib.util.module_from_spec(spec)
loader.exec_module(mod)

print('app', mod.app)
api = getattr(mod.app, '_api', None)
print('api type', type(api))
print('has get', hasattr(api, 'get'))
print('has add_route', hasattr(api, 'add_route'))
print('dir get', [name for name in dir(api) if 'get' in name.lower()])
```

---

### File: `scratch/step74.txt`
- **Path:** `scratch/step74.txt`
- **Estimated Tokens:** 972
- **mtime:** 1780659552.916

```
Created At: 2026-06-05T11:27:33Z
Completed At: 2026-06-05T11:27:36Z
The following changes were made by the replace_file_content tool to: c:\Users\NANDHA A\Desktop\UTILITIES\HealthApp\health_app.py. If relevant, proactively run terminal commands to execute this code for the USER. Don't ask for permission.
[diff_block_start]
@@ -576,6 +576,194 @@
     logger.info(f"8D breathing sound saved: {BREATHING_WAV}")

 

 

+def ensure_sound_effects():

+    """Download sound effects from the web, with local synthesis as a robust fallback."""

+    sounds_dir = os.path.join(SCRIPT_DIR, "resources", "sounds")

+    os.makedirs(sounds_dir, exist_ok=True)

+    

+    sounds = {

+        "cyber_alert.wav": "cyber_alert",

+        "retro_beep.wav": "retro_beep",

+        "zen_bowl.wav": "zen_bowl",

+        "echo_ping.wav": "echo_ping",

+        "digital_chime.wav": "digital_chime",

+        "sci_fi_sweep.wav": "sci_fi_sweep",

+        "soft_click.wav": "soft_click",

+        "tech_chirp.wav": "tech_chirp",

+        "bubble_pop.wav": "bubble_pop",

+        "crystal_bell.wav": "crystal_bell"

+    }

+

+    # Public domain short WAV files

+    sound_urls = {

+        "cyber_alert.wav": "https://raw.githubusercontent.com/iondrimba/images-and-sounds/master/sound-effects/success.wav",

+        "retro_beep.wav": "https://raw.githubusercontent.com/iondrimba/images-and-sounds/master/sound-effects/click.wav",

+        "zen_bowl.wav": "https://raw.githubusercontent.com/sfiera/wav-samples/master/input/pcm08m.wav",

+        "echo_ping.wav": "https://raw.githubusercontent.com/nandhaa/AeroHub/main/BatteryMonitor/sounds/mac_connect.wav",

+    }

+

+    import urllib.request

+    

+    for filename, sound_type in sounds.items():

+        filepath = os.path.join(sounds_dir, filename)

+        if os.path.exists(filepath):

+            continue

+            

+        downloaded = False

+        url = sound_urls.get(filename)

+        if url:

+            try:

+                logger.info(f"Attempting to download {fil
<truncated 4877 bytes>
th.pi * freq * t_pulse)

+            decay = math.exp(-15.0 * t_pulse)

+            samples.append(int(val * decay * 12000))

+    elif sound_type == "bubble_pop":

+        duration = 0.15

+        n_samples = int(sample_rate * duration)

+        for i in range(n_samples):

+            t = i / sample_rate

+            freq = 300 + 1500 * (t / duration)

+            val = math.sin(2 * math.pi * freq * t)

+            env = math.exp(-15.0 * t)

+            samples.append(int(val * env * 16384))

+    elif sound_type == "crystal_bell":

+        duration = 1.0

+        n_samples = int(sample_rate * duration)

+        for i in range(n_samples):

+            t = i / sample_rate

+            val = (math.sin(2 * math.pi * 2000 * t) * 0.7 + 

+                   math.sin(2 * math.pi * 3000 * t) * 0.3)

+            decay = math.exp(-6.0 * t)

+            samples.append(int(val * decay * 16384))

+    else:

+        duration = 0.2

+        n_samples = int(sample_rate * duration)

+        for i in range(n_samples):

+            t = i / sample_rate

+            val = math.sin(2 * math.pi * 440 * t)

+            samples.append(int(val * 8192))

+            

+    with wave.open(filepath, "wb") as w:

+        w.setnchannels(channels)

+        w.setsampwidth(sampwidth)

+        w.setframerate(sample_rate)

+        w.writeframes(struct.pack(f"<{len(samples)}h", *samples))

+

+

 # ══════════════════════════════════════════════════════════

 #  Weather & Color Temperature

 # ══════════════════════════════════════════════════════════

[diff_block_end]

Please note that the above snippet only shows the MODIFIED lines from the last change. It shows up to 3 lines of unchanged lines before and after the modified lines. The actual file contents may have many more lines not shown.
```

---

### File: `scratch/test_aiosqlite.py`
- **Path:** `scratch/test_aiosqlite.py`
- **Estimated Tokens:** 227
- **mtime:** 1780589502.1

```python
import asyncio
import aiosqlite
from pathlib import Path

async def test():
    db_path = Path(r"c:\Users\NANDHA A\Desktop\UTILITIES\MovieSongDownloader\db.sqlite3")
    print(f"Connecting to database at {db_path}...", flush=True)
    try:
        conn = await asyncio.wait_for(aiosqlite.connect(db_path), timeout=5.0)
        print("Connected! Running PRAGMA...", flush=True)
        await asyncio.wait_for(conn.execute("PRAGMA journal_mode=WAL;"), timeout=5.0)
        print("PRAGMA WAL set! Querying schema_migrations...", flush=True)
        async with conn.execute("SELECT version FROM schema_migrations") as cursor:
            rows = await asyncio.wait_for(cursor.fetchall(), timeout=5.0)
            print(f"Success! Rows: {rows}", flush=True)
        await conn.close()
    except Exception as e:
        print(f"Error occurred: {e}", flush=True)

if __name__ == "__main__":
    asyncio.run(test())
```

---

### File: `scratch/test_picker.py`
- **Path:** `scratch/test_picker.py`
- **Estimated Tokens:** 143
- **mtime:** 1780573143.993

```python
import flet as ft
import os

def main(page: ft.Page):
    page.title = "FilePicker Test"
    
    # Let's test different ways of registering FilePicker
    picker = ft.FilePicker()
    
    # Option 1: Append to overlay immediately before page is shown
    page.overlay.append(picker)
    
    def on_click(e):
        picker.get_directory_path()
        
    btn = ft.ElevatedButton("Pick Directory", on_click=on_click)
    page.add(btn)

if __name__ == "__main__":
    os.environ["FLET_WEB_PORT"] = "8560"
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8560)
```

---

### File: `scratch/test_startup.py`
- **Path:** `scratch/test_startup.py`
- **Estimated Tokens:** 189
- **mtime:** 1780589604.891

```python
import asyncio
import sys
import logging

logging.basicConfig(level=logging.INFO)

async def test():
    print("Setting up paths...", flush=True)
    sys.path.insert(0, "c:/Users/NANDHA A/Desktop/UTILITIES")
    
    print("Importing app...", flush=True)
    from MovieSongDownloader.MovieSongDownloader import startup_event
    
    print("Running startup_event() with 10s timeout...", flush=True)
    try:
        await asyncio.wait_for(startup_event(), timeout=10.0)
        print("Startup event completed successfully!", flush=True)
    except asyncio.TimeoutError:
        print("Timeout! Startup event hung!", flush=True)
    except Exception as e:
        print(f"Error occurred: {e}", flush=True)

if __name__ == "__main__":
    asyncio.run(test())
```

---

### File: `services/.gitignore`
- **Path:** `services/.gitignore`
- **Estimated Tokens:** 14
- **mtime:** 1781124219.38

```
.states
.web
*.py[cod]
assets/external/
__pycache__/
*.db
```

---

### File: `services/MovieSongDownloader/MovieSongDownloader.py`
- **Path:** `services/MovieSongDownloader/MovieSongDownloader.py`
- **Estimated Tokens:** 2,930
- **mtime:** 1780928588.348

```python
# MovieSongDownloader/MovieSongDownloader.py

import reflex as rx
import time

from MovieSongDownloader.ui.state import AppState
from MovieSongDownloader.ui import style
from MovieSongDownloader.ui.home import home_view, watchlist_view
from MovieSongDownloader.ui.search import search_view
from MovieSongDownloader.ui.songs import songs_view
from MovieSongDownloader.ui.downloads import downloads_view
from MovieSongDownloader.ui.settings import settings_view


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
        from MovieSongDownloader.core.job_queue import job_queue

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
    logger = logging.getLogger("MovieSongDownloader.FastAPI")
    try:
        from MovieSongDownloader.core.database import db

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

    logger = logging.getLogger("MovieSongDownloader.FastAPI")
    logger.info("Initializing database migrations via FastAPI startup hook...")
    try:
        from MovieSongDownloader.core.database import db

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
        from MovieSongDownloader.services.download_service import download_service

        logger.info("Starting background download service worker...")
        await download_service.start()
    except Exception as e:
        logger.error(f"Failed to start download service worker: {e}")


@app._api.on_event("shutdown")
async def shutdown_event():
    import logging

    logger = logging.getLogger("MovieSongDownloader.FastAPI")
    logger.info(
        "Stopping background download service worker via FastAPI shutdown hook..."
    )
    try:
        from MovieSongDownloader.services.download_service import download_service

        await download_service.stop()
    except Exception as e:
        logger.error(f"Error stopping download service worker: {e}")
```

---

### File: `services/MovieSongDownloader/Unknown.lrc`
- **Path:** `services/MovieSongDownloader/Unknown.lrc`
- **Estimated Tokens:** 721
- **mtime:** 1780556746.346

```
[00:00.16] ம்ம், வரியா
[00:09.61] மவனுக்கு காத்தளுக்க
[00:10.89] கஞ்சனுக்கு செஞ்சருக்க
[00:11.87] செய்தோருக்கு செய்கொடுக்க
[00:12.88] நன்னோருக்கு நன்னருக்க
[00:14.17] 
[00:52.57] ஹே, சடாருனு உருமும் வேங்கை இது
[00:54.73] உன் அடாவடி அடக்கும் ஆளு இது
[00:57.02] Boom! படாருனு வெடிக்கும் வேளையில
[00:59.27] பத்த வச்சுகிட்ட வந்து தொலைக்காதே
[01:01.57] ஹே, சடாருனு உருமும் வேங்கை இது
[01:03.75] உன் அடாவடி அடக்கும் ஆளு இது
[01:06.07] Boom! படாருனு வெடிக்கும் வேளையில
[01:08.31] பத்த வச்சுகிட்ட வந்து தொலைக்காதே
[01:10.67] ஹே தப்பு தப்பா கணக்க நீ போட்டே
[01:13.48] சூரியன சுட்டுதள்ள பாத்தே
[01:15.66] வச்சிக்காத உனக்கினி ஆப்பே, ஹே-ஹே,-ஹே-ஹே-ஹே,-ஹே
[01:19.86] ஹே தம்பி போயி gate'ah கொஞ்சம் சாத்தே
[01:22.44] கையி காலு கண்ணு ரெண்டும் பாத்தே
[01:24.75] வீசபோது ராட்சச காத்தே, ஹே-ஹே,-ஹே-ஹே-ஹே,-ஹே
[01:28.70] ம்ம், வரியா
[01:33.38] ம்ம், வரியா
[01:37.95] ம்ம், வரியா
[01:42.39] ம்ம், வரியா
[01:47.04] பரியேறி நின்னவன்தானே உருமாறி வந்துருக்கானே
[01:51.58] பட நூறு பாத்தவன்தானே, பதற விடுவானே
[01:56.01] நரி மொத்தம் வெரட்டிடத்தானே அரிமாவா வந்துருக்கானே
[02:00.57] பகையெல்லாம் எரிச்சிடத்தானே நெருப்பா சிரிப்பானே
[02:05.48] 
[02:25.26] சாத்தான் பணிஞ்சு ஓட்டான் தல வெடிச்சு
[02:27.57] போட்டான் சுளுக்கு பாட்டன்தான் நமக்கு
[02:29.82] காட்டான் அடிச்ச டாட்டாதான் உனக்கு, ஹே
[02:33.95] ரத்த தோட்டா தெறிக்கும் வெட்டா கொரல் ஒலிக்கும்
[02:36.54] கேட்டா அலறும் பாத்தா கொல நடுங்கும்
[02:38.92] छोटा புளிப்பு அவளோதான் உனக்கு, ஹே
[02:43.45] ஹே, சடாருனு உருமும் வேங்கை இது
[02:45.61] உன் அடாவடி அடக்கும் ஆளு இது
[02:47.80] Boom! படாருனு வெடிக்கும் நேரம் இது
[02:50.11] அய்யன் முன்ன நீ வந்து கொறைக்காதே
[02:52.42] ஹே, சடாருனு உருமும் வேங்கை இது
[02:54.64] உன் அடாவடி அடக்கும் ஆளு இது
[02:56.99] Boom! படாருனு வெடிக்கும் நேரம் இது
[02:59.49] சிங்கம் வாயில தல குடுக்காதே
[03:01.58] ஹே, சடாருனு உருமும் வேங்கை இது
[03:03.85] உன் அடாவடி அடக்கும் ஆளு இது
[03:06.11] Boom! படாருனு வெடிக்கும் நேரம் இது
[03:10.03] Crown on fire, he bounces when the night gets cold
[03:12.74] Blade of truth cuttin' through the lies they've told
[03:14.87] King of justice hear the innocent cry his name
[03:17.20] Chills the weak while he sets the dark in flame
[03:19.28] வெரப்பா எலும்ப எண்ணி
[03:22.60] எடைக்கு போடும் எமன் இங்க பார், எமன் இங்க பார்
[03:28.49] மொறச்சா தெறிச்சு நீயும் செதறு silent'ah
[03:37.76] சாத்தான் பணிஞ்சு ஓட்டான் தல வெடிச்சு
[03:39.94] போட்டான் சுளுக்கு பாட்டன்தான் நமக்கு
[03:42.30] காட்டான் அடிச்ச டாட்டாதான் உனக்கு, ஹே
[03:46.60] ரத்த தோட்டா தெறிக்கும் வெட்டா கொரல் ஒலிக்கும்
[03:49.03] கேட்டா அலறும் பாத்தா கொல நடுங்கும்
[03:51.31] छोटा புளிப்பு அவளோதான் உனக்கு, ஹே
[03:58.27] ஹே, சடாருனு உருமும் வேங்கை இது
[04:00.49] உன் அடாவடி அடக்கும் ஆளு இது
[04:02.77] Boom! படாருனு வெடிக்கும் நேரம் இது
[04:04.90] சிங்கம் வாயில தல குடுக்காதே
[04:07.15] ஹே, சடாருனு உருமும் வேங்கை இது
[04:09.40] உன் அடாவடி அடக்கும் ஆளு இது
[04:11.72] Boom! படாருனு வெடிக்கும் நேரம் இது
[04:13.89] கருப்பன் வர்றான் வழிமறிக்காதே
[04:17.11] 
```

---

### File: `services/MovieSongDownloader/Unknown.txt`
- **Path:** `services/MovieSongDownloader/Unknown.txt`
- **Estimated Tokens:** 46
- **mtime:** 1780556618.382

```
இது God'u mode'u
இது God'u mode'u
இது God'u mode'u ஓசையே நிக்காதே
கர பத்தும் ஜனம் மொத்தோம் பேர கத்தும் கொல சத்தம்
கர பத்தும் ஜனம் மொத்தோம் பேர கத்தும் கொல சத்தம்
கர பத்தும் ஜனம் மொத்தோம்
```

---

### File: `services/MovieSongDownloader/__init__.py`
- **Path:** `services/MovieSongDownloader/__init__.py`
- **Estimated Tokens:** 549
- **mtime:** 1780856038.253

```python
# MovieSongDownloader Package Init

import os
import sys


# Synchronously bootstrap DoH DNS resolver to bypass ISP block.
# We do this at the very beginning of package import to override the socket resolution.
def _early_bootstrap_dns():
    import sqlite3
    from pathlib import Path

    app_dir = Path(__file__).resolve().parent
    db_path = app_dir / "db.sqlite3"
    doh_enabled = True
    dns_provider = "cloudflare"
    try:
        if db_path.exists():
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute(
                "SELECT key, value FROM settings WHERE key IN ('doh_enabled', 'dns_provider')"
            )
            rows = cursor.fetchall()
            for key, val in rows:
                if key == "doh_enabled":
                    doh_enabled = val == "true"
                elif key == "dns_provider":
                    dns_provider = val
            conn.close()
    except Exception:
        pass

    if doh_enabled:
        try:
            from MovieSongDownloader.core.dns_resolver import bootstrap_dns_sync

            bootstrap_dns_sync(dns_provider)
        except Exception as e:
            print(f"Error early-bootstrapping DoH DNS resolver: {e}", file=sys.stderr)


_early_bootstrap_dns()

# Apply runtime patches for Windows paths / ampersands inside yt-dlp & deezload
import yt_dlp  # noqa: E402

sys.modules["youtube_dl"] = yt_dlp

# Prepend local bin directory to system PATH for FFmpeg binaries
bin_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")

# Patch deezload query string parsing for Windows paths / ampersands
try:
    import deezload.base

    original_extract = deezload.base.extract_video_id

    def patched_extract_video_id(qs: str):
        try:
            qs_decoded = qs.encode("utf-8").decode("unicode-escape")
        except Exception:
            qs_decoded = qs
        qs_decoded = qs_decoded.replace(r"\u0026", "&").replace("\\u0026", "&")
        return original_extract(qs_decoded)

    deezload.base.extract_video_id = patched_extract_video_id
except Exception:
    pass
```

---

### File: `services/MovieSongDownloader/build_prod.ps1`
- **Path:** `services/MovieSongDownloader/build_prod.ps1`
- **Estimated Tokens:** 248
- **mtime:** 1780923522.093

```powershell
param(
    [int]$port = 8555
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:FLET_WEB_PORT = "$port"
$logdir = Join-Path $root "logs"
if (-not (Test-Path $logdir)) { New-Item -ItemType Directory -Path $logdir | Out-Null }
$timestamp = (Get-Date).ToString('yyyyMMdd-HHmmss')
$logfile = Join-Path $logdir "build_prod_$timestamp.log"

Write-Host "Building MovieSongDownloader production bundle..."
Write-Host "Logs: $logfile"

try {
    python -m pip install --upgrade pip | Out-Null
    python -m pip install -r requirements.txt | Out-Null
    python MovieSongDownloader/main.py --env prod 2>&1 | Tee-Object -FilePath $logfile
    Write-Host "Production run successful. Packaging artifacts..."
    $archive = Join-Path $logdir "MovieSongDownloader-production-$timestamp.zip"
    Compress-Archive -Path "$root\MovieSongDownloader\*" -DestinationPath $archive -Force
    Write-Host "Packaged production artifact: $archive"
} catch {
    Write-Error "Build failed: $_"
    exit 1
}
```

---

### File: `services/MovieSongDownloader/build_prod.sh`
- **Path:** `services/MovieSongDownloader/build_prod.sh`
- **Estimated Tokens:** 117
- **mtime:** 1780923522.093

```bash
#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
export FLET_WEB_PORT="8555"
echo "Building MovieSongDownloader production bundle..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python "$ROOT_DIR/main.py" --env prod
archive="$ROOT_DIR/../logs/MovieSongDownloader-production-$(date +%Y%m%d%H%M%S).zip"
mkdir -p "$ROOT_DIR/../logs"
zip -r "$archive" "$ROOT_DIR"
echo "Packaged production artifact: $archive"
```

---

### File: `services/MovieSongDownloader/config.py`
- **Path:** `services/MovieSongDownloader/config.py`
- **Estimated Tokens:** 543
- **mtime:** 1780856038.256

```python
from pathlib import Path

APP_NAME = "MovieSongDownloader"
APP_VERSION = "2.0.0"

APP_DIR = Path(__file__).resolve().parent
DATABASE_DIR = APP_DIR / ".db"
DATABASE_PATH = DATABASE_DIR / "db.sqlite3"
SETTINGS_BACKUP_PATH = DATABASE_DIR / "settings_backup.json"

LOGS_DIR = APP_DIR / ".logs"
CACHE_DIR = APP_DIR / ".cache"
POSTERS_CACHE_DIR = CACHE_DIR / "posters"
COVERS_CACHE_DIR = CACHE_DIR / "covers"

for directory in [
    DATABASE_DIR,
    LOGS_DIR,
    CACHE_DIR,
    POSTERS_CACHE_DIR,
    COVERS_CACHE_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)

APP_LOG_PATH = LOGS_DIR / "app.log"
DOWNLOADS_LOG_PATH = LOGS_DIR / "downloads.log"
PROVIDERS_LOG_PATH = LOGS_DIR / "providers.log"

DEFAULT_DOWNLOAD_DIR = str(Path.home() / "Music" / "MovieSongDownloader")

# Data source URLs
WIKIPEDIA_EN_API = "https://en.wikipedia.org/w/api.php"
WIKIPEDIA_TA_API = "https://ta.wikipedia.org/w/api.php"
OMDB_BASE_URL = "https://www.omdbapi.com/"

DEFAULT_SETTINGS = {
    "omdb_api_key": "",
    "deezer_arl": "",
    "download_provider": "spotiflac",
    "scraping_limit": "5",
    "last_fetch_date": "",
    # Download
    "audio_format": "mp3",
    "bitrate": "320",
    "output_dir": DEFAULT_DOWNLOAD_DIR,
    "filename_format": "{TrackNum} - {Title}",
    "folder_format": "{Year}/{Movie}/Songs",
    "download_mode": "accurate",
    "max_concurrent": "2",
    # Lyrics
    "lyrics_priority": '["lrclib", "syncedlyrics", "musixmatch", "genius"]',
    "save_lrc_file": "true",
    "embed_lyrics": "true",
    # UI
    "theme": "dark",
    "default_tab": "home",
    "language_region": "en-US",
    # Watchlist
    "check_interval_hours": "24",
    "auto_download": "true",
    "notify_on_found": "true",
    # DNS (bypass ISP blocks)
    "doh_enabled": "true",
    "dns_provider": "cloudflare",
}

# Cyberpunk Cyan Design Tokens
COLOR_ACCENT = "#06B6D4"  # Cyan accent
COLOR_ACCENT_LIGHT = "#22D3EE"  # Light cyan for hover/focus
COLOR_TEXT_PRIMARY = "#FFFFFF"  # Crisp white
COLOR_TEXT_MUTED = "#94A3B8"  # Muted cool gray
COLOR_BG_PRIMARY = "#0B0F19"  # Deep dark blue/gray
COLOR_BG_SECONDARY = "#111827"  # Dark gray
COLOR_BORDER = "#1F2937"  # Dark gray border
```

---

### File: `services/MovieSongDownloader/core/__init__.py`
- **Path:** `services/MovieSongDownloader/core/__init__.py`
- **Estimated Tokens:** 3
- **mtime:** 1780474573.814

```python
# Core Module
```

---

### File: `services/MovieSongDownloader/core/cache_manager.py`
- **Path:** `services/MovieSongDownloader/core/cache_manager.py`
- **Estimated Tokens:** 1,430
- **mtime:** 1780856038.258

```python
import os
import hashlib
import json
import logging
from datetime import datetime, timedelta
from typing import Optional
import httpx
from MovieSongDownloader.config import POSTERS_CACHE_DIR, COVERS_CACHE_DIR
from MovieSongDownloader.core.database import db

logger = logging.getLogger("MovieSongDownloader.CacheManager")


class DownloadCache:
    @staticmethod
    def generate_hash(artist: str, title: str, album: str, duration_ms: int) -> str:
        raw = f"{artist.lower()}|{title.lower()}|{album.lower()}|{duration_ms}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    async def check(self, track_hash: str) -> Optional[dict]:
        conn = await db.get_connection()
        try:
            async with conn.execute(
                "SELECT file_path, format, downloaded_at FROM download_cache WHERE track_hash = ?",
                (track_hash,),
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    if os.path.exists(row[0]):
                        return {
                            "file_path": row[0],
                            "format": row[1],
                            "downloaded_at": row[2],
                        }
                    await conn.execute(
                        "DELETE FROM download_cache WHERE track_hash = ?", (track_hash,)
                    )
                    await conn.commit()
                    logger.warning(f"Pruned stale cache entry: {track_hash}")
            return None
        finally:
            await conn.close()

    async def add(self, track_hash: str, file_path: str, fmt: str) -> None:
        conn = await db.get_connection()
        try:
            await conn.execute(
                "INSERT OR REPLACE INTO download_cache (track_hash, file_path, format) VALUES (?, ?, ?)",
                (track_hash, file_path, fmt),
            )
            await conn.commit()
        finally:
            await conn.close()


class ImageCache:
    def __init__(self):
        self.poster_dir = POSTERS_CACHE_DIR
        self.cover_dir = COVERS_CACHE_DIR

    async def get_or_download(self, url: str, category: str) -> Optional[str]:
        if not url:
            return None
        target_dir = self.poster_dir if category == "poster" else self.cover_dir
        url_hash = hashlib.md5(url.encode("utf-8")).hexdigest()
        ext = "png"
        clean_url = url.split("?")[0]
        if "." in clean_url:
            potential = clean_url.rsplit(".", 1)[-1].lower()
            if potential in ("jpg", "jpeg", "png", "webp"):
                ext = potential
        local_path = target_dir / f"{url_hash}.{ext}"
        if local_path.exists():
            return str(local_path)
        headers = {
            "User-Agent": "MovieSongDownloader/2.0 (contact: nandha.dev@gmail.com)"
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url, headers=headers)
                if resp.status_code == 200:
                    with open(local_path, "wb") as f:
                        f.write(resp.content)
                    return str(local_path)
                logger.warning(f"Image download HTTP {resp.status_code}: {url}")
        except Exception as e:
            logger.error(f"Image download failed: {e}")
        return None


class APICache:
    async def get(self, cache_key: str) -> Optional[dict]:
        conn = await db.get_connection()
        try:
            async with conn.execute(
                "SELECT json_payload, expires_at FROM api_cache WHERE cache_key = ?",
                (cache_key,),
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    if datetime.now() < datetime.fromisoformat(row[1]):
                        try:
                            return json.loads(row[0])
                        except json.JSONDecodeError:
                            logger.error(f"Corrupt cache key: {cache_key}")
                    else:
                        await conn.execute(
                            "DELETE FROM api_cache WHERE cache_key = ?", (cache_key,)
                        )
                        await conn.commit()
            return None
        finally:
            await conn.close()

    async def set(
        self,
        cache_key: str,
        provider: str,
        payload: dict,
        ttl: int = 86400,
        expires_in_seconds: Optional[int] = None,
    ) -> None:
        if expires_in_seconds is not None:
            ttl = expires_in_seconds
        conn = await db.get_connection()
        try:
            expires_at = (datetime.now() + timedelta(seconds=ttl)).isoformat()
            await conn.execute(
                "INSERT OR REPLACE INTO api_cache (cache_key, provider, json_payload, expires_at) VALUES (?, ?, ?, ?)",
                (cache_key, provider, json.dumps(payload), expires_at),
            )
            await conn.commit()
        finally:
            await conn.close()

    async def verify_scraped_data(
        self, cache_key: str, new_data: dict, fields: list
    ) -> dict:
        """Compare freshly scraped data against cached version.
        Returns merged result preferring cached values for stable fields (IDs)
        and new values for volatile fields (ratings, availability)."""
        cached = await self.get(cache_key)
        if cached is None:
            return new_data

        merged = {**cached}
        for field in fields:
            if field in new_data:
                merged[field] = new_data[field]
        return merged


download_cache = DownloadCache()
image_cache = ImageCache()
api_cache = APICache()
```

---

### File: `services/MovieSongDownloader/core/database.py`
- **Path:** `services/MovieSongDownloader/core/database.py`
- **Estimated Tokens:** 690
- **mtime:** 1780494706.304

```python
import re
import aiosqlite
import logging
from pathlib import Path
from MovieSongDownloader.config import DATABASE_PATH

logger = logging.getLogger("MovieSongDownloader.Database")


class DatabaseManager:
    def __init__(self, db_path: Path = DATABASE_PATH):
        self.db_path = db_path

    async def get_connection(self) -> aiosqlite.Connection:
        conn = await aiosqlite.connect(self.db_path)
        conn.row_factory = aiosqlite.Row
        await conn.execute("PRAGMA journal_mode=WAL;")
        await conn.execute("PRAGMA synchronous=NORMAL;")
        await conn.execute("PRAGMA foreign_keys=ON;")
        return conn

    async def run_migrations(self, max_version: int = 99) -> None:
        migrations_dir = Path(__file__).resolve().parent / "migrations"
        if not migrations_dir.exists():
            logger.warning("Migrations directory not found, skipping.")
            return

        conn = await self.get_connection()
        try:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version INTEGER PRIMARY KEY,
                    applied_at TEXT DEFAULT (datetime('now'))
                );
            """)
            await conn.commit()

            async with conn.execute("SELECT version FROM schema_migrations") as cursor:
                applied_versions = {row[0] for row in await cursor.fetchall()}

            migration_files = []
            for filepath in migrations_dir.glob("*.sql"):
                match = re.match(r"^(\d+)_(.+)\.sql$", filepath.name)
                if match:
                    version = int(match.group(1))
                    migration_files.append((version, filepath))

            migration_files.sort(key=lambda x: x[0])

            for version, filepath in migration_files:
                if version > max_version:
                    continue
                if version not in applied_versions:
                    logger.info(f"Applying migration v{version}: {filepath.name}")
                    try:
                        sql_content = filepath.read_text(encoding="utf-8")
                        await conn.executescript(sql_content)
                        await conn.execute(
                            "INSERT INTO schema_migrations (version) VALUES (?)",
                            (version,),
                        )
                        await conn.commit()
                        logger.info(f"Migration v{version} applied.")
                    except Exception as e:
                        await conn.rollback()
                        logger.error(f"Migration {filepath.name} failed: {e}")
                        raise
        finally:
            await conn.close()


db = DatabaseManager()
```

---

### File: `services/MovieSongDownloader/core/dns_resolver.py`
- **Path:** `services/MovieSongDownloader/core/dns_resolver.py`
- **Estimated Tokens:** 2,345
- **mtime:** 1780861103.717

```python
import socket
import logging
import ssl
import json
import urllib.request
import httpx
from typing import Dict, Optional

logger = logging.getLogger("MovieSongDownloader.DnsResolver")

_original_getaddrinfo = socket.getaddrinfo
_dns_overrides: Dict[str, str] = {}
_active_doh_url: str = "https://cloudflare-dns.com/dns-query"

DOH_PROVIDERS = {
    "cloudflare": "https://cloudflare-dns.com/dns-query",
    "google": "https://dns.google/dns-query",
    "quad9": "https://dns.quad9.net:5053/dns-query",
}

DOMAINS_TO_RESOLVE = [
    "www.jiosaavn.com",
    "www.omdbapi.com",
]


def _patched_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    """Intercepts DNS lookups for blocked domains, returns DoH-resolved IPs.
    TLS SNI still uses the original hostname so HTTPS works correctly."""
    if host is None:
        return _original_getaddrinfo(host, port, family, type, proto, flags)

    if isinstance(host, bytes):
        host_str = host.decode("utf-8", errors="ignore")
    elif isinstance(host, str):
        host_str = host
    else:
        host_str = str(host)

    clean_host = host_str.rstrip(".")

    # Fast bypass for numeric IPs, localhost, and local network domains
    is_numeric = False
    try:
        # Check if valid IPv4
        socket.inet_aton(clean_host)
        is_numeric = True
    except Exception:
        pass
    if not is_numeric:
        try:
            # Check if valid IPv6
            socket.inet_pton(socket.AF_INET6, clean_host)
            is_numeric = True
        except Exception:
            pass

    is_local = (
        not clean_host
        or clean_host.lower() in ("localhost", "none", "127.0.0.1", "::1", "0.0.0.0")
        or clean_host.endswith(".local")
        or is_numeric
        or "." not in clean_host
    )

    if is_local:
        return _original_getaddrinfo(clean_host, port, family, type, proto, flags)

    resolved = _dns_overrides.get(clean_host)
    if resolved:
        logger.debug(f"DNS override: {clean_host} -> {resolved}")
        try:
            return _original_getaddrinfo(resolved, port, family, type, proto, flags)
        except Exception as e:
            logger.warning(
                f"DNS override original getaddrinfo failed for {resolved}: {e}. Retrying with AI_NUMERICHOST."
            )
            try:
                f = socket.AF_INET if family in (0, socket.AF_INET) else family
                t = type or socket.SOCK_STREAM
                p = proto or socket.IPPROTO_TCP
                return _original_getaddrinfo(
                    resolved, port, f, t, p, socket.AI_NUMERICHOST
                )
            except Exception as e2:
                logger.error(
                    f"DNS override backup getaddrinfo failed for {resolved}: {e2}. Using manual fallback."
                )
                f = socket.AF_INET if family in (0, socket.AF_INET) else family
                t = type or socket.SOCK_STREAM
                p = proto or socket.IPPROTO_TCP
                return [(f, t, p, "", (resolved, port))]

    # For non-overridden hosts, strip trailing dots and attempt system resolution.
    # If the system resolver fails (e.g. Jio/ISP blocks or DNS poisoning), fall back
    # dynamically to DNS-over-HTTPS in real-time.
    try:
        return _original_getaddrinfo(clean_host, port, family, type, proto, flags)
    except Exception as e:
        # Avoid recursive calls if it's the DoH provider domain itself failing
        if (
            clean_host in _dns_overrides
            or "dns-query" in clean_host
            or "cloudflare-dns.com" in clean_host
            or "dns.google" in clean_host
        ):
            raise e

        logger.warning(
            f"System DNS lookup failed for {clean_host}: {e}. Attempting real-time DoH fallback..."
        )
        resolved = _resolve_via_doh_sync(clean_host, _active_doh_url)
        if resolved:
            _dns_overrides[clean_host] = resolved
            logger.info(
                f"Dynamically resolved {clean_host} -> {resolved} via DoH fallback."
            )
            try:
                return _original_getaddrinfo(resolved, port, family, type, proto, flags)
            except Exception as e2:
                logger.warning(
                    "Dynamic DNS override original getaddrinfo failed for %s: %s. "
                    "Retrying with AI_NUMERICHOST.",
                    resolved,
                    e2,
                )
                try:
                    f = socket.AF_INET if family in (0, socket.AF_INET) else family
                    t = type or socket.SOCK_STREAM
                    p = proto or socket.IPPROTO_TCP
                    return _original_getaddrinfo(
                        resolved, port, f, t, p, socket.AI_NUMERICHOST
                    )
                except Exception as e3:
                    logger.error(
                        f"Dynamic DNS override backup getaddrinfo failed for {resolved}: {e3}. Using manual fallback."
                    )
                    f = socket.AF_INET if family in (0, socket.AF_INET) else family
                    t = type or socket.SOCK_STREAM
                    p = proto or socket.IPPROTO_TCP
                    return [(f, t, p, "", (resolved, port))]

        # If DoH resolution fails too, raise the original getaddrinfo exception
        if clean_host != host:
            try:
                return _original_getaddrinfo(host, port, family, type, proto, flags)
            except Exception:
                raise e
        raise e


async def _resolve_via_doh(hostname: str, doh_url: str) -> Optional[str]:
    """Resolves a hostname to an IPv4 address using DNS-over-HTTPS (RFC 8484 JSON)."""
    params = {"name": hostname, "type": "A"}
    headers = {"Accept": "application/dns-json"}
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(doh_url, params=params, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                for answer in data.get("Answer", []):
                    if answer.get("type") == 1:
                        ip = answer["data"]
                        logger.info(f"DoH resolved {hostname} -> {ip}")
                        return ip
    except Exception as e:
        logger.warning(f"DoH resolution failed for {hostname}: {e}")
    return None


async def bootstrap_dns(provider: str = "cloudflare") -> None:
    """Pre-resolves blocked domains via DoH and patches socket.getaddrinfo.
    Call once at app startup before any API requests."""
    global _active_doh_url
    doh_url = DOH_PROVIDERS.get(provider, DOH_PROVIDERS["cloudflare"])
    _active_doh_url = doh_url
    logger.info(f"Bootstrapping DNS via DoH provider: {provider} ({doh_url})")

    for domain in DOMAINS_TO_RESOLVE:
        ip = await _resolve_via_doh(domain, doh_url)
        if ip:
            _dns_overrides[domain] = ip

    if _dns_overrides:
        socket.getaddrinfo = _patched_getaddrinfo
        logger.info(
            f"DNS overrides active for {len(_dns_overrides)} domain(s): {list(_dns_overrides.keys())}"
        )
    else:
        logger.warning(
            "No DNS overrides resolved. Some providers may be unreachable if ISP blocks DNS."
        )


def _resolve_via_doh_sync(hostname: str, doh_url: str) -> Optional[str]:
    """Resolves a hostname to an IPv4 address synchronously using DNS-over-HTTPS."""
    url = f"{doh_url}?name={hostname}&type=A"
    req = urllib.request.Request(url, headers={"Accept": "application/dns-json"})
    try:
        ctx = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=ctx, timeout=5.0) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                for answer in data.get("Answer", []):
                    if answer.get("type") == 1:
                        ip = answer["data"]
                        logger.info(f"DoH resolved {hostname} -> {ip} (sync)")
                        return ip
    except Exception as e:
        logger.warning(f"DoH resolution failed synchronously for {hostname}: {e}")
    return None


def bootstrap_dns_sync(provider: str = "cloudflare") -> None:
    """Pre-resolves blocked domains synchronously via DoH and patches socket.getaddrinfo.
    Call at early startup before any libraries perform DNS lookups."""
    global _active_doh_url
    doh_url = DOH_PROVIDERS.get(provider, DOH_PROVIDERS["cloudflare"])
    _active_doh_url = doh_url
    logger.info(
        f"Synchronously bootstrapping DNS via DoH provider: {provider} ({doh_url})"
    )

    for domain in DOMAINS_TO_RESOLVE:
        ip = _resolve_via_doh_sync(domain, doh_url)
        if ip:
            _dns_overrides[domain] = ip

    if _dns_overrides:
        socket.getaddrinfo = _patched_getaddrinfo
        logger.info(
            f"DNS overrides active for {len(_dns_overrides)} domain(s): {list(_dns_overrides.keys())}"
        )
    else:
        logger.warning(
            "No DNS overrides resolved. Some providers may be unreachable if ISP blocks DNS."
        )


def clear_dns_overrides() -> None:
    """Restores original DNS resolution."""
    _dns_overrides.clear()
    socket.getaddrinfo = _original_getaddrinfo
    logger.info("DNS overrides cleared, restored system resolver.")
```

---

### File: `services/MovieSongDownloader/core/event_bus.py`
- **Path:** `services/MovieSongDownloader/core/event_bus.py`
- **Estimated Tokens:** 467
- **mtime:** 1780856038.246

```python
import asyncio
import logging
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Any

logger = logging.getLogger("MovieSongDownloader.EventBus")


@dataclass
class Event:
    type: str
    data: Dict[str, Any] = field(default_factory=dict)


class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._lock = asyncio.Lock()

    async def subscribe(self, event_type: str, callback: Callable) -> None:
        async with self._lock:
            self._subscribers.setdefault(event_type, []).append(callback)

    async def unsubscribe(self, event_type: str, callback: Callable) -> None:
        async with self._lock:
            if event_type in self._subscribers:
                try:
                    self._subscribers[event_type].remove(callback)
                except ValueError:
                    pass

    async def publish(self, event: Event) -> None:
        async with self._lock:
            callbacks = list(self._subscribers.get(event.type, []))
        for cb in callbacks:
            try:
                if asyncio.iscoroutinefunction(cb):
                    await cb(event)
                else:
                    cb(event)
            except Exception as e:
                logger.error(f"Callback error for {event.type}: {e}", exc_info=True)

    def publish_fire_and_forget(self, event: Event) -> None:
        callbacks = list(self._subscribers.get(event.type, []))
        for cb in callbacks:
            try:
                if asyncio.iscoroutinefunction(cb):
                    asyncio.create_task(cb(event))
                else:
                    cb(event)
            except Exception as e:
                logger.error(
                    f"Fire-and-forget error for {event.type}: {e}", exc_info=True
                )


event_bus = EventBus()
```

---

### File: `services/MovieSongDownloader/core/job_queue.py`
- **Path:** `services/MovieSongDownloader/core/job_queue.py`
- **Estimated Tokens:** 1,943
- **mtime:** 1780861103.717

```python
import asyncio
import logging
from typing import Optional, List, Dict
from MovieSongDownloader.core.database import db
from MovieSongDownloader.core.models import DownloadJob
from MovieSongDownloader.core.event_bus import event_bus, Event
from MovieSongDownloader.config import DOWNLOADS_LOG_PATH

downloads_logger = logging.getLogger("MovieSongDownloader.Downloads")
if not downloads_logger.handlers:
    handler = logging.FileHandler(DOWNLOADS_LOG_PATH, encoding="utf-8")
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    downloads_logger.addHandler(handler)
    downloads_logger.setLevel(logging.INFO)

_JOBS_JOIN_QUERY = """
    SELECT j.id, j.track_id, j.status, j.progress, j.output_path, j.format,
           j.error_message, j.retry_count,
           t.title, t.artist, a.title, m.title, a.cover_cached_path
    FROM download_jobs j
    JOIN tracks t ON j.track_id = t.id
    JOIN albums a ON t.album_id = a.id
    JOIN movies m ON a.movie_id = m.id
"""


def _row_to_job(row) -> DownloadJob:
    return DownloadJob(
        id=row[0],
        track_id=row[1],
        status=row[2],
        progress=row[3],
        output_path=row[4],
        format=row[5],
        error_message=row[6],
        retry_count=row[7],
        track_title=row[8],
        track_artist=row[9],
        album_title=row[10],
        movie_title=row[11],
        cover_cached_path=row[12],
    )


class JobQueue:
    def __init__(self):
        self._active_tasks: Dict[int, asyncio.Task] = {}
        self._lock = asyncio.Lock()

    async def enqueue(self, track_id: int, format: str = "mp3") -> int:
        conn = await db.get_connection()
        try:
            cursor = await conn.execute(
                "INSERT INTO download_jobs (track_id, format, status, progress) VALUES (?, ?, 'queued', 0.0)",
                (track_id, format),
            )
            job_id = cursor.lastrowid
            await conn.commit()
            downloads_logger.info(
                f"Enqueued job {job_id} for track {track_id} ({format})"
            )
            async with conn.execute(
                "SELECT title FROM tracks WHERE id = ?", (track_id,)
            ) as c:
                r = await c.fetchone()
                title = r[0] if r else f"Track {track_id}"
            event_bus.publish_fire_and_forget(
                Event("job.queued", {"job_id": job_id, "track_title": title})
            )
            return job_id
        finally:
            await conn.close()

    async def dequeue(self) -> Optional[DownloadJob]:
        conn = await db.get_connection()
        try:
            query = (
                _JOBS_JOIN_QUERY
                + " WHERE j.status = 'queued' ORDER BY j.created_at ASC LIMIT 1"
            )
            async with conn.execute(query) as cursor:
                row = await cursor.fetchone()
                return _row_to_job(row) if row else None
        finally:
            await conn.close()

    async def update_progress(self, job_id: int, progress: float, status: str) -> None:
        conn = await db.get_connection()
        try:
            await conn.execute(
                "UPDATE download_jobs SET progress=?, status=?, updated_at=datetime('now') WHERE id=?",
                (progress, status, job_id),
            )
            await conn.commit()
            event_bus.publish_fire_and_forget(
                Event(
                    "job.progress",
                    {
                        "job_id": job_id,
                        "progress": progress,
                        "status": status,
                    },
                )
            )
        finally:
            await conn.close()

    async def mark_completed(self, job_id: int, output_path: str) -> None:
        conn = await db.get_connection()
        try:
            await conn.execute(
                "UPDATE download_jobs SET progress=100.0, status='completed', output_path=?, "
                "error_message=NULL, updated_at=datetime('now') WHERE id=?",
                (output_path, job_id),
            )
            await conn.commit()
            downloads_logger.info(f"Job {job_id} completed -> {output_path}")
            event_bus.publish_fire_and_forget(
                Event("job.completed", {"job_id": job_id, "output_path": output_path})
            )
        finally:
            await conn.close()

    async def mark_failed(self, job_id: int, error: str) -> None:
        conn = await db.get_connection()
        try:
            await conn.execute(
                "UPDATE download_jobs SET status='failed', error_message=?, "
                "retry_count=retry_count+1, updated_at=datetime('now') WHERE id=?",
                (error, job_id),
            )
            await conn.commit()
            downloads_logger.error(f"Job {job_id} failed: {error}")
            event_bus.publish_fire_and_forget(
                Event("job.failed", {"job_id": job_id, "error": error})
            )
        finally:
            await conn.close()

    async def pause(self, job_id: int) -> None:
        conn = await db.get_connection()
        try:
            await conn.execute(
                "UPDATE download_jobs SET status='paused', updated_at=datetime('now') WHERE id=? AND status='queued'",
                (job_id,),
            )
            await conn.commit()
            event_bus.publish_fire_and_forget(
                Event(
                    "job.progress",
                    {"job_id": job_id, "progress": 0.0, "status": "paused"},
                )
            )
        finally:
            await conn.close()

    async def resume(self, job_id: int) -> None:
        conn = await db.get_connection()
        try:
            await conn.execute(
                "UPDATE download_jobs SET status='queued', updated_at=datetime('now') "
                "WHERE id=? AND status IN ('paused','failed','cancelled')",
                (job_id,),
            )
            await conn.commit()
            event_bus.publish_fire_and_forget(
                Event(
                    "job.progress",
                    {"job_id": job_id, "progress": 0.0, "status": "queued"},
                )
            )
        finally:
            await conn.close()

    async def cancel(self, job_id: int) -> None:
        conn = await db.get_connection()
        try:
            await conn.execute(
                "UPDATE download_jobs SET status='cancelled', updated_at=datetime('now') WHERE id=?",
                (job_id,),
            )
            await conn.commit()
            downloads_logger.info(f"Cancelled job {job_id}")
            async with self._lock:
                task = self._active_tasks.get(job_id)
            if task and not task.done():
                task.cancel()
            event_bus.publish_fire_and_forget(
                Event(
                    "job.progress",
                    {"job_id": job_id, "progress": 0.0, "status": "cancelled"},
                )
            )
        finally:
            await conn.close()

    async def register_task(self, job_id: int, task: asyncio.Task) -> None:
        async with self._lock:
            self._active_tasks[job_id] = task

    async def unregister_task(self, job_id: int) -> None:
        async with self._lock:
            self._active_tasks.pop(job_id, None)

    async def get_all_jobs(self) -> List[DownloadJob]:
        conn = await db.get_connection()
        try:
            query = _JOBS_JOIN_QUERY + " ORDER BY j.created_at DESC"
            async with conn.execute(query) as cursor:
                return [_row_to_job(row) for row in await cursor.fetchall()]
        finally:
            await conn.close()


job_queue = JobQueue()
```

---

### File: `services/MovieSongDownloader/core/migrations/001_initial.sql`
- **Path:** `services/MovieSongDownloader/core/migrations/001_initial.sql`
- **Estimated Tokens:** 1,074
- **mtime:** 1780401662.737

```sql
-- Migration: 001_initial
-- Date: 2026-06-02

-- Create schema_migrations tracker
CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY,
    applied_at TEXT DEFAULT (datetime('now'))
);

-- Movies Business Data
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tmdb_id INTEGER UNIQUE NOT NULL,
    title TEXT NOT NULL,
    year INTEGER,
    poster_url TEXT,
    poster_cached_path TEXT,
    overview TEXT,
    language TEXT,
    genres TEXT,          -- JSON Array of string
    ott_providers TEXT,   -- JSON Array of dicts
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_movies_tmdb ON movies(tmdb_id);
CREATE INDEX IF NOT EXISTS idx_movies_year ON movies(year);

-- Albums Business Data
CREATE TABLE IF NOT EXISTS albums (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
    spotify_id TEXT UNIQUE,
    title TEXT NOT NULL,
    artist TEXT,
    cover_url TEXT,
    cover_cached_path TEXT,
    total_tracks INTEGER,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_albums_spotify ON albums(spotify_id);
CREATE INDEX IF NOT EXISTS idx_albums_movie ON albums(movie_id);

-- Tracks Business Data
CREATE TABLE IF NOT EXISTS tracks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    album_id INTEGER REFERENCES albums(id) ON DELETE CASCADE,
    spotify_id TEXT UNIQUE,
    title TEXT NOT NULL,
    artist TEXT,
    duration_ms INTEGER,
    track_number INTEGER,
    preview_url TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_tracks_spotify ON tracks(spotify_id);
CREATE INDEX IF NOT EXISTS idx_tracks_album ON tracks(album_id);

-- Download Job Queue
CREATE TABLE IF NOT EXISTS download_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    track_id INTEGER REFERENCES tracks(id) ON DELETE CASCADE,
    status TEXT NOT NULL DEFAULT 'queued', -- queued, downloading, fetching_lyrics, embedding_cover, embedding_metadata, saving_lrc, generating_playlist, completed, failed, paused, cancelled
    progress REAL DEFAULT 0.0,
    output_path TEXT,
    format TEXT DEFAULT 'mp3',
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON download_jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_track ON download_jobs(track_id);

-- Lyrics Fallback Output Results
CREATE TABLE IF NOT EXISTS lyrics_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    track_id INTEGER REFERENCES tracks(id) ON DELETE CASCADE,
    provider TEXT,        -- lrclib | syncedlyrics | musixmatch | genius
    lyrics_type TEXT,     -- synced | plain | none
    content TEXT,
    confidence REAL,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_lyrics_track ON lyrics_results(track_id);

-- Watchlist tracker
CREATE TABLE IF NOT EXISTS watchlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tmdb_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    expected_release TEXT,
    last_checked TEXT,
    auto_download INTEGER DEFAULT 1,
    status TEXT DEFAULT 'watching', -- watching | found | downloaded | expired
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_watchlist_tmdb ON watchlist(tmdb_id);

-- Settings Key-Value Configuration Store
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    category TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_settings_category ON settings(category);

-- Download Deduplication Cache
CREATE TABLE IF NOT EXISTS download_cache (
    track_hash TEXT PRIMARY KEY, -- SHA256(artist + title + album + duration)
    file_path TEXT NOT NULL,
    format TEXT NOT NULL,
    downloaded_at TEXT DEFAULT (datetime('now'))
);

-- Raw API Response Cache (Metadata cache decoupling)
CREATE TABLE IF NOT EXISTS api_cache (
    cache_key TEXT PRIMARY KEY,
    provider TEXT NOT NULL,
    json_payload TEXT NOT NULL,
    expires_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_api_cache_expires ON api_cache(expires_at);
CREATE INDEX IF NOT EXISTS idx_api_cache_provider ON api_cache(provider);
```

---

### File: `services/MovieSongDownloader/core/migrations/002_provider_health.sql`
- **Path:** `services/MovieSongDownloader/core/migrations/002_provider_health.sql`
- **Estimated Tokens:** 95
- **mtime:** 1780401669.059

```sql
-- Migration: 002_provider_health
-- Date: 2026-06-02

CREATE TABLE IF NOT EXISTS provider_health (
    provider TEXT NOT NULL,
    category TEXT NOT NULL,      -- movie | soundtrack | lyrics | download
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    total_latency_ms INTEGER DEFAULT 0,
    last_checked TEXT,
    PRIMARY KEY (provider, category)
);
```

---

### File: `services/MovieSongDownloader/core/migrations/003_cache.sql`
- **Path:** `services/MovieSongDownloader/core/migrations/003_cache.sql`
- **Estimated Tokens:** 75
- **mtime:** 1780401673.784

```sql
-- Migration: 003_cache
-- Date: 2026-06-02

-- Unified search index virtual table (FTS5)
CREATE VIRTUAL TABLE IF NOT EXISTS search_index USING fts5(
    source,        -- tmdb | spotify
    source_id,     -- external ID
    title,
    artist,
    year,
    type           -- movie | album | track
);
```

---

### File: `services/MovieSongDownloader/core/migrations/004_scraper_sources.sql`
- **Path:** `services/MovieSongDownloader/core/migrations/004_scraper_sources.sql`
- **Estimated Tokens:** 213
- **mtime:** 1780494673.786

```sql
-- Migration: 004_scraper_sources
-- Date: 2026-06-03
-- Adds source tracking columns for Wikipedia/JioSaavn/OMDb migration

-- Movies: add source tracking + enrichment fields
ALTER TABLE movies ADD COLUMN source TEXT DEFAULT 'wikipedia';
ALTER TABLE movies ADD COLUMN source_id TEXT DEFAULT '';
ALTER TABLE movies ADD COLUMN rating TEXT;
ALTER TABLE movies ADD COLUMN cast_info TEXT;

-- Albums: add source tracking
ALTER TABLE albums ADD COLUMN source TEXT DEFAULT 'jiosaavn';
ALTER TABLE albums ADD COLUMN source_id TEXT DEFAULT '';

-- Tracks: add source tracking + direct download URL
ALTER TABLE tracks ADD COLUMN source TEXT DEFAULT 'jiosaavn';
ALTER TABLE tracks ADD COLUMN source_id TEXT DEFAULT '';
ALTER TABLE tracks ADD COLUMN download_url TEXT;

-- Watchlist: add generic source_id
ALTER TABLE watchlist ADD COLUMN source_id TEXT DEFAULT '';
```

---

### File: `services/MovieSongDownloader/core/migrations/005_release_date_enrichment.sql`
- **Path:** `services/MovieSongDownloader/core/migrations/005_release_date_enrichment.sql`
- **Estimated Tokens:** 67
- **mtime:** 1780513434.911

```sql
-- Migration: 005_release_date_enrichment
-- Date: 2026-06-04
-- Adds release_date to movies, composer to albums, and isrc to tracks

ALTER TABLE movies ADD COLUMN release_date TEXT;
ALTER TABLE albums ADD COLUMN composer TEXT;
ALTER TABLE tracks ADD COLUMN isrc TEXT;
```

---

### File: `services/MovieSongDownloader/core/models.py`
- **Path:** `services/MovieSongDownloader/core/models.py`
- **Estimated Tokens:** 694
- **mtime:** 1780856038.25

```python
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Movie:
    id: Optional[int] = None
    tmdb_id: int = 0  # Legacy, kept for backward compat
    source: str = "wikipedia"  # "wikipedia" | "omdb" | "tmdb"
    source_id: str = ""  # Wikipedia page ID or OMDb imdbID
    title: str = ""
    year: Optional[int] = None
    poster_url: Optional[str] = None
    poster_cached_path: Optional[str] = None
    overview: Optional[str] = None
    language: Optional[str] = None
    rating: Optional[str] = None  # IMDb rating from OMDb
    cast_info: Optional[str] = None  # Comma-separated top cast
    release_date: Optional[str] = None
    genres: List[str] = field(default_factory=list)
    ott_providers: List[dict] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Album:
    id: Optional[int] = None
    movie_id: Optional[int] = None
    spotify_id: Optional[str] = None  # Legacy
    source: str = "jiosaavn"  # "jiosaavn" | "spotify"
    source_id: str = ""  # JioSaavn album ID
    title: str = ""
    artist: Optional[str] = None
    cover_url: Optional[str] = None
    cover_cached_path: Optional[str] = None
    total_tracks: Optional[int] = None
    composer: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class Track:
    id: Optional[int] = None
    album_id: Optional[int] = None
    spotify_id: Optional[str] = None  # Legacy
    source: str = "jiosaavn"  # "jiosaavn" | "spotify"
    source_id: str = ""  # JioSaavn track ID
    title: str = ""
    artist: Optional[str] = None
    duration_ms: int = 0
    track_number: int = 0
    preview_url: Optional[str] = None
    download_url: Optional[str] = None  # Direct stream URL from JioSaavn
    isrc: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class DownloadJob:
    id: Optional[int] = None
    track_id: int = 0
    status: str = "queued"
    progress: float = 0.0
    output_path: Optional[str] = None
    format: str = "mp3"
    error_message: Optional[str] = None
    retry_count: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    # Joined metadata for UI display
    track_title: Optional[str] = None
    track_artist: Optional[str] = None
    album_title: Optional[str] = None
    movie_title: Optional[str] = None
    cover_cached_path: Optional[str] = None


@dataclass
class WatchlistItem:
    id: Optional[int] = None
    tmdb_id: int = 0  # Legacy, kept for backward compat
    source_id: str = ""
    title: str = ""
    expected_release: Optional[str] = None
    last_checked: Optional[str] = None
    auto_download: bool = True
    status: str = "watching"
    created_at: Optional[str] = None
```

---

### File: `services/MovieSongDownloader/core/rate_limiter.py`
- **Path:** `services/MovieSongDownloader/core/rate_limiter.py`
- **Estimated Tokens:** 463
- **mtime:** 1780856038.252

```python
import asyncio
import time
import logging
from MovieSongDownloader.config import PROVIDERS_LOG_PATH

providers_logger = logging.getLogger("MovieSongDownloader.Providers")
if not providers_logger.handlers:
    handler = logging.FileHandler(PROVIDERS_LOG_PATH, encoding="utf-8")
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    providers_logger.addHandler(handler)
    providers_logger.setLevel(logging.INFO)


class RateLimiter:
    def __init__(self, rps: float, name: str):
        self.delay = 1.0 / rps if rps > 0 else 0.0
        self.last_called = 0.0
        self.name = name
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        if self.delay <= 0:
            return
        async with self._lock:
            now = time.time()
            wait = self.delay - (now - self.last_called)
            if wait > 0:
                providers_logger.debug(
                    f"provider={self.name} rate_limit sleep_ms={int(wait * 1000)}"
                )
                await asyncio.sleep(wait)
            self.last_called = time.time()


class GlobalRateLimiters:
    def __init__(self):
        self._limiters = {
            "wikipedia": RateLimiter(5.0, "wikipedia"),
            "jiosaavn": RateLimiter(2.0, "jiosaavn"),
            "omdb": RateLimiter(3.0, "omdb"),
            "lyrics": RateLimiter(2.0, "lyrics"),
            "deezspot": RateLimiter(1.0, "deezspot"),
        }
        self._lock = asyncio.Lock()

    async def acquire(self, provider: str) -> None:
        key = provider.lower()
        async with self._lock:
            if key not in self._limiters:
                self._limiters[key] = RateLimiter(2.0, key)
            limiter = self._limiters[key]
        await limiter.acquire()


rate_limiter = GlobalRateLimiters()
```

---

### File: `services/MovieSongDownloader/core/settings_manager.py`
- **Path:** `services/MovieSongDownloader/core/settings_manager.py`
- **Estimated Tokens:** 1,018
- **mtime:** 1780856038.255

```python
import json
import logging
from pathlib import Path
from MovieSongDownloader.config import SETTINGS_BACKUP_PATH, DEFAULT_SETTINGS
from MovieSongDownloader.core.database import db

logger = logging.getLogger("MovieSongDownloader.SettingsManager")

CATEGORY_MAP = {
    "tmdb_api_key": "api",
    "tmdb_base_url": "api",
    "spotify_client_id": "api",
    "spotify_client_secret": "api",
    "deezer_arl": "api",
    "audio_format": "download",
    "bitrate": "download",
    "output_dir": "download",
    "filename_format": "download",
    "folder_format": "download",
    "download_mode": "download",
    "max_concurrent": "download",
    "lyrics_priority": "lyrics",
    "save_lrc_file": "lyrics",
    "embed_lyrics": "lyrics",
    "theme": "ui",
    "default_tab": "ui",
    "language_region": "ui",
    "check_interval_hours": "watchlist",
    "auto_download": "watchlist",
    "notify_on_found": "watchlist",
    "last_fetch_date": "watchlist",
    "doh_enabled": "network",
    "dns_provider": "network",
}


def _get_category(key: str) -> str:
    return CATEGORY_MAP.get(key, "ui")


class SettingsManager:
    def __init__(self, backup_path: Path = SETTINGS_BACKUP_PATH):
        self.backup_path = backup_path

    async def get_all(self) -> dict:
        conn = await db.get_connection()
        try:
            async with conn.execute("SELECT key, value FROM settings") as cursor:
                rows = await cursor.fetchall()
            if not rows:
                logger.warning("Settings empty. Attempting backup restore...")
                restored = await self.restore_from_backup()
                if not restored:
                    logger.info("Seeding defaults...")
                    await self._seed_defaults(conn)
                    restored = DEFAULT_SETTINGS.copy()
                else:
                    await self._save_many_to_conn(conn, restored)
                return restored
            return {row[0]: row[1] for row in rows}
        finally:
            await conn.close()

    async def get(self, key: str) -> str:
        all_s = await self.get_all()
        return all_s.get(key, DEFAULT_SETTINGS.get(key, ""))

    async def set(self, key: str, value: str) -> None:
        conn = await db.get_connection()
        try:
            await conn.execute(
                "INSERT OR REPLACE INTO settings (key, value, category) VALUES (?, ?, ?)",
                (key, str(value), _get_category(key)),
            )
            await conn.commit()
            updated = await self.get_all()
            await self.export_backup(updated)
        finally:
            await conn.close()

    async def save_many(self, settings_dict: dict) -> None:
        conn = await db.get_connection()
        try:
            await self._save_many_to_conn(conn, settings_dict)
            updated = await self.get_all()
            await self.export_backup(updated)
        finally:
            await conn.close()

    async def _save_many_to_conn(self, conn, data: dict) -> None:
        for k, v in data.items():
            await conn.execute(
                "INSERT OR REPLACE INTO settings (key, value, category) VALUES (?, ?, ?)",
                (k, str(v), _get_category(k)),
            )
        await conn.commit()

    async def _seed_defaults(self, conn) -> None:
        await self._save_many_to_conn(conn, DEFAULT_SETTINGS)
        await self.export_backup(DEFAULT_SETTINGS)

    async def export_backup(self, data: dict) -> None:
        try:
            with open(self.backup_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logger.error(f"Backup export failed: {e}")

    async def restore_from_backup(self) -> dict:
        if not self.backup_path.exists():
            return {}
        try:
            with open(self.backup_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Backup restore failed: {e}")
            return {}


settings_manager = SettingsManager()
```

---

### File: `services/MovieSongDownloader/dev_run.ps1`
- **Path:** `services/MovieSongDownloader/dev_run.ps1`
- **Estimated Tokens:** 86
- **mtime:** 1780923522.093

```powershell
param(
    [int]$port = 8555
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:FLET_WEB_PORT = "$port"
Write-Host "Starting MovieSongDownloader in DEVELOPMENT mode with hot reload"
Start-Process -NoNewWindow -FilePath python -ArgumentList "MovieSongDownloader/main.py"
Start-Sleep -Seconds 4
Start-Process "http://127.0.0.1:$port"
```

---

### File: `services/MovieSongDownloader/main.py`
- **Path:** `services/MovieSongDownloader/main.py`
- **Estimated Tokens:** 2,011
- **mtime:** 1781124203.228

```python
# MovieSongDownloader/main.py

import argparse
import importlib
import os
import signal
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path

from importlib.abc import MetaPathFinder

sub_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.dirname(os.path.dirname(sub_dir))
services_dir = os.path.join(workspace_root, "services")

# Remove subdirectory from path to avoid package naming collision
if sub_dir in sys.path:
    sys.path.remove(sub_dir)

# Add workspace root and services directory to path
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)
if services_dir not in sys.path:
    sys.path.insert(0, services_dir)

# Register Redirector so MovieSongDownloader -> movie_song_downloader works seamlessly
class MovieSongDownloaderRedirector(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname.startswith("MovieSongDownloader"):
            real_name = fullname.replace("MovieSongDownloader", "movie_song_downloader", 1)
            mod = importlib.import_module(real_name)
            sys.modules[fullname] = mod
            return mod.__spec__
        return None

sys.meta_path.insert(0, MovieSongDownloaderRedirector())

# Import shared config loader from root
from config.loader import load_config, load_env  # noqa: E402

# Import MovieSongDownloader package first to trigger early DNS override bootstrap inside __init__.py
import MovieSongDownloader  # noqa: F401, E402


class DevConfigWatcher:
    def __init__(self, root_dir: Path, callback):
        self.root_dir = root_dir
        self.callback = callback
        self.files = [self.root_dir.parent / ".env", self.root_dir / "rxconfig.py"]
        self.mod_times = {path: path.stat().st_mtime for path in self.files if path.exists()}
        self.running = True

    def watch(self):
        while self.running:
            for path in self.files:
                if path.exists():
                    mtime = path.stat().st_mtime
                    if self.mod_times.get(path) != mtime:
                        self.mod_times[path] = mtime
                        self.callback(path)
            time.sleep(2)

    def stop(self):
        self.running = False


def apply_env_from_config(root_dir: Path):
    runtime = load_config()
    env_settings = runtime.get("app", {})
    os.environ.setdefault("FLET_WEB_PORT", str(env_settings.get("flet_port", 8555)))
    os.environ.setdefault("ENV", env_settings.get("env", "dev"))
    env_file = root_dir.parent / ".env"
    for key, value in load_env(env_file).items():
        if key not in os.environ:
            os.environ[key] = value


def reload_rxconfig(root_dir: Path):
    try:
        import rxconfig

        importlib.reload(rxconfig)
        print("Reloaded rxconfig.py", flush=True)
    except Exception as exc:
        print(f"Failed to reload rxconfig: {exc}", file=sys.stderr, flush=True)


def is_port_free(port: int) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("0.0.0.0", port))
        return True
    except OSError:
        return False


def find_free_port(start_port: int = 8555, max_port: int = 8600) -> int:
    for port in range(start_port, max_port + 1):
        if is_port_free(port):
            return port
    raise RuntimeError(f"No free ports found between {start_port} and {max_port}")


def get_processes_on_port(port: int) -> list[int]:
    try:
        import psutil
    except ImportError:
        return []

    pids = set()
    for conn in psutil.net_connections(kind="inet"):
        if conn.laddr and conn.laddr.port == port and conn.pid and conn.pid != os.getpid():
            pids.add(conn.pid)
    return sorted(pids)


def kill_process(pid: int) -> bool:
    try:
        import psutil
        proc = psutil.Process(pid)
        proc.terminate()
        proc.wait(timeout=3)
        return True
    except Exception:
        pass

    if sys.platform.startswith("win"):
        try:
            subprocess.run(
                ["taskkill", "/PID", str(pid), "/F", "/T"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except Exception:
            return False

    try:
        os.kill(pid, signal.SIGTERM)
        return True
    except Exception:
        return False


def release_port(port: int) -> bool:
    if is_port_free(port):
        return True

    pids = get_processes_on_port(port)
    if not pids:
        return False

    killed = []
    for pid in pids:
        if kill_process(pid):
            killed.append(pid)

    if killed:
        print(
            f"Stopped existing process(es) {', '.join(str(pid) for pid in killed)} "
            f"using port {port}",
            flush=True,
        )
        time.sleep(1)

    return is_port_free(port)


def main():
    root_dir = Path(__file__).resolve().parent
    repo_root = root_dir.parent
    print(f"Launching Reflex App from workspace root: {repo_root}", flush=True)

    apply_env_from_config(root_dir)
    parser = argparse.ArgumentParser(description="Movie Song Downloader launcher")
    parser.add_argument("--env", choices=["dev", "prod"], default="dev")
    parser.add_argument("--frontend-port", dest="frontend_port", default=os.environ.get("FLET_WEB_PORT"))
    args, extra_args = parser.parse_known_args(sys.argv[1:])

    requested_port = int(args.frontend_port) if args.frontend_port else None
    frontend_port = requested_port
    if requested_port is None:
        configured_port = int(os.environ.get("FLET_WEB_PORT", 8555))
        if is_port_free(configured_port):
            frontend_port = configured_port
        elif release_port(configured_port):
            frontend_port = configured_port
        else:
            fallback_port = find_free_port(configured_port + 1)
            print(
                f"Configured port {configured_port} is unavailable, using fallback port {fallback_port}",
                flush=True,
            )
            frontend_port = fallback_port
    else:
        if not is_port_free(requested_port):
            if release_port(requested_port):
                frontend_port = requested_port
            else:
                fallback_port = find_free_port(requested_port + 1)
                print(
                    f"Requested port {requested_port} is unavailable and could not be released, using fallback port {fallback_port}",
                    flush=True,
                )
                frontend_port = fallback_port

    cmd = ["reflex", "run"]
    if frontend_port:
        cmd.extend(["--frontend-port", str(frontend_port)])
    if args.env == "prod":
        cmd.append("--env")
        cmd.append("prod")
    cmd.extend(extra_args)

    if args.env == "dev":
        def on_config_change(path: Path):
            if path.name == ".env":
                apply_env_from_config(root_dir)
                print("Reloaded .env settings", flush=True)
            elif path.name == "rxconfig.py":
                reload_rxconfig(root_dir)

        watcher = DevConfigWatcher(root_dir, on_config_change)
        watcher_thread = threading.Thread(target=watcher.watch, daemon=True)
        watcher_thread.start()

    print(f"Running command: {' '.join(cmd)}", flush=True)
    try:
        env = os.environ.copy()
        env["PYTHONPATH"] = f"{workspace_root}{os.pathsep}{services_dir}{os.pathsep}{env.get('PYTHONPATH', '')}"
        subprocess.run(cmd, cwd=repo_root, env=env, check=True)
    except KeyboardInterrupt:
        print("\nExiting Reflex Application...", flush=True)
    except subprocess.CalledProcessError as exc:
        print(f"Reflex exited with {exc.returncode}", file=sys.stderr, flush=True)
        sys.exit(exc.returncode)
    finally:
        if args.env == "dev":
            watcher.stop()


if __name__ == "__main__":
    main()
```

---

### File: `services/MovieSongDownloader/movie.json`
- **Path:** `services/MovieSongDownloader/movie.json`
- **Estimated Tokens:** 214
- **mtime:** 1780556746.662

```json
{
    "tmdb_id": 3574151120,
    "title": "Karuppu",
    "year": 2026,
    "overview": "Karuppu (transl.\u2009Black) is a 2026 Indian Tamil-language fantasy action film directed by RJ Balaji from a screenplay he co-wrote with Rathna Kumar, Ashwin Ravichandran, Rahul Raj, T. S. Gopi Krishnan and Karan Aravind Kumar. Produced by Dream Warrior Pictures, the film stars Suriya, Trisha Krishnan and Balaji, alongside Indrans, Natty Subramaniam, Swasika, Sshivada and Supreeth Reddy. In the film, the guardian deity Vettai Karuppu disguises himself as a lawyer to fight corruption in a court syste",
    "language": "ta",
    "genres": [],
    "ott_providers": [
        {
            "id": 2,
            "name": "Amazon Prime"
        },
        {
            "id": 6,
            "name": "Aha"
        }
    ],
    "exported_at": "2026-06-04T12:35:46.659080"
}
```

---

### File: `services/MovieSongDownloader/playlist.m3u`
- **Path:** `services/MovieSongDownloader/playlist.m3u`
- **Estimated Tokens:** 19
- **mtime:** 1780556746.673

```
#EXTM3U
#PLAYLIST:Karuppu (Original Motion Picture Soundtrack)

Unknown.mp3
```

---

### File: `services/MovieSongDownloader/providers/__init__.py`
- **Path:** `services/MovieSongDownloader/providers/__init__.py`
- **Estimated Tokens:** 4
- **mtime:** 1780474576.991

```python
# Providers Module
```

---

### File: `services/MovieSongDownloader/providers/base.py`
- **Path:** `services/MovieSongDownloader/providers/base.py`
- **Estimated Tokens:** 420
- **mtime:** 1780856038.259

```python
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Callable
from MovieSongDownloader.core.models import Movie, Album, Track


class BaseMovieProvider(ABC):
    @abstractmethod
    async def search(self, query: str, **filters) -> List[Movie]:
        pass

    @abstractmethod
    async def get_today_releases(self, region: str = "IN") -> List[Movie]:
        pass

    @abstractmethod
    async def get_watch_providers(
        self, source_id: str, region: str = "IN"
    ) -> List[dict]:
        pass


class BaseSoundtrackProvider(ABC):
    @abstractmethod
    async def get_soundtrack(
        self, movie_title: str, year: Optional[int] = None
    ) -> List[Album]:
        pass


class BaseDownloadProvider(ABC):
    @abstractmethod
    async def download(
        self,
        track: Track,
        format: str,
        output_dir: str,
        filename_template: str,
        on_progress: Optional[Callable[[float, str], None]] = None,
    ) -> str:
        pass


class BaseLyricsProvider(ABC):
    @abstractmethod
    async def fetch(self, title: str, artist: str) -> Tuple[Optional[str], str]:
        pass


class BaseTaggingProvider(ABC):
    @abstractmethod
    async def embed_cover(self, file_path: str, image_path: str) -> None:
        pass

    @abstractmethod
    async def embed_lyrics(
        self, file_path: str, lyrics_content: str, is_synced: bool = False
    ) -> None:
        pass

    @abstractmethod
    async def embed_metadata(
        self,
        file_path: str,
        title: str,
        artist: str,
        album: str,
        year: Optional[int] = None,
        track_num: int = 1,
    ) -> None:
        pass
```

---

### File: `services/MovieSongDownloader/providers/deezspot_provider.py`
- **Path:** `services/MovieSongDownloader/providers/deezspot_provider.py`
- **Estimated Tokens:** 1,030
- **mtime:** 1780856038.261

```python
import os
import sys
import httpx
import logging
import asyncio
from typing import Optional, Callable

if "youtube_dl" not in sys.modules:
    import yt_dlp

    sys.modules["youtube_dl"] = yt_dlp

bin_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bin"
)
if bin_dir not in os.environ.get("PATH", ""):
    os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")

import deezload.base  # noqa: E402

if not getattr(deezload.base.extract_video_id, "__patched__", False):
    _orig = deezload.base.extract_video_id

    def _patched(qs: str):
        try:
            qs = qs.encode("utf-8").decode("unicode-escape")
        except Exception:
            pass
        qs = qs.replace(r"\u0026", "&").replace("\\u0026", "&")
        return _orig(qs)

    _patched.__patched__ = True
    deezload.base.extract_video_id = _patched

from MovieSongDownloader.providers.base import BaseDownloadProvider  # noqa: E402
from MovieSongDownloader.core.models import Track  # noqa: E402
from MovieSongDownloader.core.rate_limiter import rate_limiter  # noqa: E402

logger = logging.getLogger("MovieSongDownloader.DeezspotProvider")


class DeezspotProvider(BaseDownloadProvider):
    async def _resolve_deezer_id(self, title: str, artist: str) -> Optional[int]:
        await rate_limiter.acquire("lyrics")
        clean_title = title.replace('"', "").replace("'", "")
        clean_artist = artist.split(",")[0].strip()
        url = "https://api.deezer.com/search"

        for params in [
            {"q": f'track:"{clean_title}" artist:"{clean_artist}"'},
            {"q": f"{clean_artist} {clean_title}"},
        ]:
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.get(url, params=params)
                    if resp.status_code == 200:
                        data = resp.json()
                        if data.get("data"):
                            return data["data"][0]["id"]
            except Exception as e:
                logger.error(f"Deezer search error: {e}")
        return None

    async def download(
        self,
        track: Track,
        format: str,
        output_dir: str,
        filename_template: str,
        on_progress: Optional[Callable[[float, str], None]] = None,
    ) -> str:
        deezer_id = await self._resolve_deezer_id(track.title, track.artist)
        if not deezer_id:
            raise Exception(
                f"Could not resolve '{track.title}' by '{track.artist}' on Deezer."
            )

        deezer_url = f"https://www.deezer.com/track/{deezer_id}"
        await rate_limiter.acquire("deezspot")
        logger.info(f"Downloading Deezer ID {deezer_id} ({format})...")

        def _task():
            from deezload.base import Loader, LoadStatus

            loader = Loader(
                urls=[deezer_url],
                output_dir=output_dir,
                format=format.lower(),
                tree=False,
                slugify=False,
            )
            path = None
            ok = False
            err = None
            for status, t, i, prog in loader.load_gen():
                if on_progress:
                    on_progress(
                        float(int(prog * 100)), f"deezload_{status.name.lower()}"
                    )
                if status in (LoadStatus.FINISHED, LoadStatus.SKIPPED):
                    path = t.path
                    ok = True
                elif status == LoadStatus.FAILED:
                    err = "Track not found on YouTube."
                elif status == LoadStatus.ERROR:
                    err = "deezload internal error."
            if not ok:
                raise Exception(err or "Download failed.")
            return path

        loop = asyncio.get_running_loop()
        local_path = await loop.run_in_executor(None, _task)
        if not local_path or not os.path.exists(local_path):
            raise FileNotFoundError(f"File not found after download: {local_path}")
        logger.info(f"Downloaded -> {local_path}")
        return local_path
```

---

### File: `services/MovieSongDownloader/providers/jiosaavn_provider.py`
- **Path:** `services/MovieSongDownloader/providers/jiosaavn_provider.py`
- **Estimated Tokens:** 2,497
- **mtime:** 1780856038.265

```python
import logging
import hashlib
from typing import List, Optional
from jiosaavnpy import JioSaavn

from MovieSongDownloader.providers.base import BaseSoundtrackProvider
from MovieSongDownloader.core.models import Album, Track
from MovieSongDownloader.core.rate_limiter import rate_limiter, providers_logger
from MovieSongDownloader.core.cache_manager import api_cache

logger = logging.getLogger("MovieSongDownloader.JioSaavnProvider")


class JioSaavnProvider(BaseSoundtrackProvider):
    def __init__(self):
        self._client = JioSaavn()

    async def get_soundtrack(
        self, movie_title: str, year: Optional[int] = None
    ) -> List[Album]:
        """Search JioSaavn for soundtrack albums matching movie title."""
        query = movie_title
        if year:
            query = f"{movie_title} {year}"

        cache_key = f"jiosaavn:album_search:{hashlib.md5(query.encode()).hexdigest()}"
        cached = await api_cache.get(cache_key)
        if cached is not None:
            return self._parse_cached_albums(cached)

        await rate_limiter.acquire("jiosaavn")
        try:
            results = self._client.search_albums(query, limit=8)
            if not results:
                return []

            albums = []
            for item in results:
                cover = None
                thumbs = item.get("thumbnails", {}).get("quality", {})
                cover = (
                    thumbs.get("500x500")
                    or thumbs.get("150x150")
                    or thumbs.get("50x50")
                )

                album = Album(
                    source="jiosaavn",
                    source_id=item.get("album_id", ""),
                    spotify_id=None,
                    title=item.get("title", ""),
                    artist=item.get("artists", "Unknown"),
                    cover_url=cover,
                    total_tracks=int(item.get("track_count", 0)),
                )
                albums.append(album)

            # Cache raw results
            await api_cache.set(cache_key, "jiosaavn", results, ttl=86400)
            providers_logger.info(
                f"provider=jiosaavn success=True endpoint=search_albums results={len(albums)}"
            )
            return albums

        except Exception as e:
            providers_logger.error(
                f'provider=jiosaavn success=False error="{e}" endpoint=search_albums'
            )
            logger.error(f"JioSaavn album search failed: {e}")
            return []

    async def get_tracks(self, album_id: str) -> List[Track]:
        """Fetch all tracks for a JioSaavn album."""
        cache_key = f"jiosaavn:album_tracks:{album_id}"
        cached = await api_cache.get(cache_key)
        if cached is not None:
            return self._parse_cached_tracks(cached)

        await rate_limiter.acquire("jiosaavn")
        try:
            info = self._client.album_info(album_id)
            if not info or "tracks" not in info:
                return []

            raw_tracks = info["tracks"]
            tracks = []
            for idx, item in enumerate(raw_tracks, start=1):
                # Get best quality stream URL
                streams = item.get("stream_urls", {})
                best_url = (
                    streams.get("very_high_quality")
                    or streams.get("high_quality")
                    or streams.get("medium_quality")
                    or streams.get("low_quality")
                )

                duration_sec = int(item.get("duration", 0))

                tracks.append(
                    Track(
                        source="jiosaavn",
                        source_id=item.get("track_id", ""),
                        spotify_id=None,
                        title=item.get("title", ""),
                        artist=item.get("primary_artists", "Unknown"),
                        duration_ms=duration_sec * 1000,
                        track_number=idx,
                        preview_url=streams.get("low_quality"),
                        download_url=best_url,
                    )
                )

            await api_cache.set(cache_key, "jiosaavn", raw_tracks, ttl=86400)
            providers_logger.info(
                f"provider=jiosaavn success=True endpoint=album_info tracks={len(tracks)}"
            )
            return tracks

        except Exception as e:
            providers_logger.error(
                f'provider=jiosaavn success=False error="{e}" endpoint=album_info'
            )
            logger.error(f"JioSaavn album tracks failed: {e}")
            return []

    async def get_album_details(self, album_id: str) -> Optional[Album]:
        """Fetch album metadata from JioSaavn."""
        cache_key = f"jiosaavn:album_detail:{album_id}"
        cached = await api_cache.get(cache_key)
        if cached is not None and isinstance(cached, dict):
            return self._dict_to_album(cached)

        await rate_limiter.acquire("jiosaavn")
        try:
            info = self._client.album_info(album_id)
            if not info:
                return None

            cover = None
            thumbs = info.get("thumbnails", {}).get("quality", {})
            cover = thumbs.get("500x500") or thumbs.get("150x150")

            album = Album(
                source="jiosaavn",
                source_id=info.get("album_id", album_id),
                title=info.get("title", ""),
                artist=info.get("primary_artists", "Unknown"),
                cover_url=cover,
                total_tracks=len(info.get("tracks", [])),
            )

            await api_cache.set(
                cache_key,
                "jiosaavn",
                {
                    "album_id": album.source_id,
                    "title": album.title,
                    "artist": album.artist,
                    "cover_url": album.cover_url,
                    "total_tracks": album.total_tracks,
                },
                ttl=86400,
            )

            return album

        except Exception as e:
            logger.error(f"JioSaavn album details failed: {e}")
            return None

    async def search_songs(self, query: str, limit: int = 10) -> List[Track]:
        """Direct song search on JioSaavn."""
        cache_key = f"jiosaavn:song_search:{hashlib.md5(query.encode()).hexdigest()}"
        cached = await api_cache.get(cache_key)
        if cached is not None:
            return self._parse_cached_tracks(cached)

        await rate_limiter.acquire("jiosaavn")
        try:
            results = self._client.search_songs(query, limit=limit)
            if not results:
                return []

            tracks = []
            for idx, item in enumerate(results, start=1):
                streams = item.get("stream_urls", {})
                best_url = (
                    streams.get("very_high_quality")
                    or streams.get("high_quality")
                    or streams.get("medium_quality")
                )
                duration_sec = int(item.get("duration", 0))

                tracks.append(
                    Track(
                        source="jiosaavn",
                        source_id=item.get("track_id", ""),
                        title=item.get("title", ""),
                        artist=item.get("primary_artists", "Unknown"),
                        duration_ms=duration_sec * 1000,
                        track_number=idx,
                        preview_url=streams.get("low_quality"),
                        download_url=best_url,
                    )
                )

            await api_cache.set(cache_key, "jiosaavn", results, ttl=86400)
            return tracks

        except Exception as e:
            logger.error(f"JioSaavn song search failed: {e}")
            return []

    def _parse_cached_albums(self, cached_data: list) -> List[Album]:
        """Convert cached raw JioSaavn album dicts back to Album objects."""
        albums = []
        for item in cached_data:
            cover = None
            thumbs = item.get("thumbnails", {}).get("quality", {})
            cover = thumbs.get("500x500") or thumbs.get("150x150")
            albums.append(
                Album(
                    source="jiosaavn",
                    source_id=item.get("album_id", ""),
                    title=item.get("title", ""),
                    artist=item.get("artists", "Unknown"),
                    cover_url=cover,
                    total_tracks=int(item.get("track_count", 0)),
                )
            )
        return albums

    def _parse_cached_tracks(self, cached_data: list) -> List[Track]:
        """Convert cached raw JioSaavn track dicts back to Track objects."""
        tracks = []
        for idx, item in enumerate(cached_data, start=1):
            streams = item.get("stream_urls", {})
            best_url = (
                streams.get("very_high_quality")
                or streams.get("high_quality")
                or streams.get("medium_quality")
            )
            duration_sec = int(item.get("duration", 0))
            tracks.append(
                Track(
                    source="jiosaavn",
                    source_id=item.get("track_id", ""),
                    title=item.get("title", ""),
                    artist=item.get("primary_artists", "Unknown"),
                    duration_ms=duration_sec * 1000,
                    track_number=idx,
                    preview_url=streams.get("low_quality"),
                    download_url=best_url,
                )
            )
        return tracks

    @staticmethod
    def _dict_to_album(d: dict) -> Album:
        return Album(
            source="jiosaavn",
            source_id=d.get("album_id", ""),
            title=d.get("title", ""),
            artist=d.get("artist", "Unknown"),
            cover_url=d.get("cover_url"),
            total_tracks=d.get("total_tracks", 0),
        )
```

---

### File: `services/MovieSongDownloader/providers/lyrics_provider.py`
- **Path:** `services/MovieSongDownloader/providers/lyrics_provider.py`
- **Estimated Tokens:** 591
- **mtime:** 1780856038.287

```python
import asyncio
import re
import logging
import time
import json
from typing import Tuple, Optional
import syncedlyrics
from MovieSongDownloader.providers.base import BaseLyricsProvider
from MovieSongDownloader.core.settings_manager import settings_manager
from MovieSongDownloader.core.rate_limiter import rate_limiter, providers_logger

logger = logging.getLogger("MovieSongDownloader.LyricsProvider")


class LyricsProvider(BaseLyricsProvider):
    def __init__(self):
        self._lrc_re = re.compile(r"\[\d{2,}:\d{2}(?:\.\d{1,3})?\]")

    def _is_synced(self, text: str) -> bool:
        return bool(text) and len(self._lrc_re.findall(text)) >= 3

    @staticmethod
    def _search(query: str, provider: str) -> Optional[str]:
        try:
            return syncedlyrics.search(query, providers=[provider])
        except Exception:
            return None

    async def fetch(self, title: str, artist: str) -> Tuple[Optional[str], str]:
        raw = await settings_manager.get("lyrics_priority")
        try:
            providers = json.loads(raw)
        except Exception:
            providers = ["lrclib", "syncedlyrics", "musixmatch", "genius"]

        query = f"{title} {artist}"
        for prov in providers:
            await rate_limiter.acquire("lyrics")
            t0 = time.time()
            try:
                target = prov.lower()
                if target == "syncedlyrics":
                    result = await asyncio.to_thread(syncedlyrics.search, query)
                else:
                    result = await asyncio.to_thread(self._search, query, target)
                ms = int((time.time() - t0) * 1000)
                if result:
                    providers_logger.info(
                        f"provider=lyrics_{prov} latency={ms}ms success=True response_size={len(result)}"
                    )
                    ltype = "synced" if self._is_synced(result) else "plain"
                    return result, ltype
                providers_logger.info(
                    f"provider=lyrics_{prov} latency={ms}ms success=False response_size=0"
                )
            except Exception as e:
                ms = int((time.time() - t0) * 1000)
                providers_logger.error(
                    f'provider=lyrics_{prov} latency={ms}ms success=False error="{e}"'
                )
        return None, "none"
```

---

### File: `services/MovieSongDownloader/providers/metadata_normalizer.py`
- **Path:** `services/MovieSongDownloader/providers/metadata_normalizer.py`
- **Estimated Tokens:** 362
- **mtime:** 1780856038.289

```python
import re
from rapidfuzz import fuzz

NOISE_PATTERNS = [
    r"\(From\s+.*?\)",
    r"\(Remastered\s*\d*\)",
    r"\(Official\s+Audio\)",
    r"\[Extended\s+Version\]",
    r"\(Deluxe\s*Edition?\)",
    r"\(feat\.\s+.*?\)",
    r'\(From\s+"[^"]*"\)',
    r"\(Original\s+Motion\s+Picture\s+Soundtrack\)",
]


def normalize_title(title: str) -> str:
    # Strip Wikipedia parenthetical suffixes (e.g. "(film)", "(2026 film)", "(soundtrack)")
    title = re.sub(
        r"\s*\((?:film|\d{4}(?:\s+film)?|soundtrack|tamil\s+film|original\s+motion\s+picture\s+soundtrack|album)\)",
        "",
        title,
        flags=re.IGNORECASE,
    )

    for p in NOISE_PATTERNS:
        title = re.sub(p, "", title, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", title).strip()


def confidence_score(source: dict, target: dict) -> int:
    src_t = normalize_title(source.get("title", "")).lower()
    tgt_t = normalize_title(target.get("title", "")).lower()
    score = int(fuzz.ratio(src_t, tgt_t) * 0.50)
    score += int(
        fuzz.ratio(source.get("artist", "").lower(), target.get("artist", "").lower())
        * 0.30
    )
    sa, ta = source.get("album", "").lower(), target.get("album", "").lower()
    score += int(fuzz.ratio(sa, ta) * 0.10) if sa and ta else 10
    dur = abs(source.get("duration_ms", 0) - target.get("duration_ms", 0))
    score += 10 if dur <= 3000 else (5 if dur <= 5000 else (2 if dur <= 10000 else 0))
    return score
```

---

### File: `services/MovieSongDownloader/providers/musicbrainz_provider.py`
- **Path:** `services/MovieSongDownloader/providers/musicbrainz_provider.py`
- **Estimated Tokens:** 1,641
- **mtime:** 1780856038.294

```python
import logging
import httpx
import hashlib
import time
from typing import List, Dict, Optional, Tuple
from MovieSongDownloader.core.rate_limiter import rate_limiter, providers_logger
from MovieSongDownloader.core.cache_manager import api_cache
from MovieSongDownloader.core.models import Album, Track

logger = logging.getLogger("MovieSongDownloader.MusicBrainzProvider")

USER_AGENT = "MovieSongDownloader/2.0 (contact: nandha.dev@gmail.com)"


class MusicBrainzProvider:
    async def _mb_request(
        self, url: str, params: dict, cache_ttl: int = 2592000
    ) -> Optional[dict]:
        """Make a request to MusicBrainz API with caching and strict 1 req/sec rate limit."""
        params["fmt"] = "json"
        param_str = "".join(f"{k}={params[k]}" for k in sorted(params))
        cache_key = f"musicbrainz:{hashlib.md5((url + param_str).encode()).hexdigest()}"

        cached = await api_cache.get(cache_key)
        if cached is not None:
            return cached

        # MusicBrainz guidelines mandate strict rate limits (1 req/sec)
        await rate_limiter.acquire("musicbrainz")
        t0 = time.time()
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.get(
                    url, params=params, headers={"User-Agent": USER_AGENT}
                )
                ms = int((time.time() - t0) * 1000)
                if resp.status_code == 200:
                    data = resp.json()
                    providers_logger.info(
                        f"provider=musicbrainz latency={ms}ms success=True"
                    )
                    await api_cache.set(cache_key, "musicbrainz", data, cache_ttl)
                    return data
                providers_logger.error(
                    f"provider=musicbrainz latency={ms}ms success=False status={resp.status_code}"
                )
        except Exception as e:
            ms = int((time.time() - t0) * 1000)
            providers_logger.error(
                f'provider=musicbrainz latency={ms}ms success=False error="{e}"'
            )
            logger.error(f"MusicBrainz API request failed: {e}")
        return None

    async def enrich_album(
        self, album: Album, tracks: List[Track]
    ) -> Tuple[Optional[str], Dict[str, str]]:
        """
        Enrich Album with composer info and Tracks with ISRC codes from MusicBrainz.
        Returns: (composer_name, {track_title: isrc_code})
        """
        composer = None
        isrc_map = {}

        # 1. Search release groups
        query = f'release-group:"{album.title}" AND type:soundtrack'
        if album.artist and album.artist != "Unknown":
            # Add artist if known to narrow down
            query += f' AND artist:"{album.artist}"'

        search_data = await self._mb_request(
            "https://musicbrainz.org/ws/2/release-group/", {"query": query}
        )

        if not search_data or not search_data.get("release-groups"):
            # Try a broader search without soundtrack filter
            query_broad = f'release-group:"{album.title}"'
            search_data = await self._mb_request(
                "https://musicbrainz.org/ws/2/release-group/", {"query": query_broad}
            )
            if not search_data or not search_data.get("release-groups"):
                return None, {}

        rg = search_data["release-groups"][0]
        rg_id = rg["id"]

        # If artist-credit lists the composer, capture it
        artist_credit = rg.get("artist-credit", [])
        if artist_credit:
            composer = artist_credit[0].get("artist", {}).get("name")

        # 2. Browse releases for this release group to find tracks/recordings and relations
        browse_data = await self._mb_request(
            "https://musicbrainz.org/ws/2/release",
            {
                "release-group": rg_id,
                "inc": "recordings+artist-rels+work-rels+isrcs+work-level-rels",
            },
        )

        if not browse_data or not browse_data.get("releases"):
            return composer, {}

        # Look through releases
        for rel in browse_data["releases"]:
            # Check release relations for composer if not resolved
            if not composer:
                for rel_item in rel.get("relations", []):
                    if rel_item.get("type") == "composer" and rel_item.get("artist"):
                        composer = rel_item["artist"].get("name")
                        break

            # Collect recordings and ISRCs
            media_list = rel.get("media", [])
            for media in media_list:
                for mb_track in media.get("tracks", []):
                    title = mb_track.get("title", "")
                    recording = mb_track.get("recording", {})
                    isrcs = recording.get("isrcs", [])

                    if isrcs:
                        isrc_map[title.lower().strip()] = isrcs[0]

                    # Check recording level relations for composer if still not found
                    if not composer:
                        for rec_rel in recording.get("relations", []):
                            if rec_rel.get("type") == "composer" and rec_rel.get(
                                "artist"
                            ):
                                composer = rec_rel["artist"].get("name")
                                break

        # Match ISRCs back to JioSaavn tracks by title matching
        final_isrcs = {}
        for t in tracks:
            t_title_clean = t.title.lower().strip()
            # Try exact match first
            if t_title_clean in isrc_map:
                final_isrcs[t.title] = isrc_map[t_title_clean]
            else:
                # Try partial match (e.g. "Song Name (From film)" vs "Song Name")
                matched = False
                for mb_title, isrc in isrc_map.items():
                    if mb_title in t_title_clean or t_title_clean in mb_title:
                        final_isrcs[t.title] = isrc
                        matched = True
                        break
                if not matched:
                    # Try cleaning common suffixes
                    clean_jio = t_title_clean.split("(")[0].strip()
                    for mb_title, isrc in isrc_map.items():
                        clean_mb = mb_title.split("(")[0].strip()
                        if clean_jio == clean_mb:
                            final_isrcs[t.title] = isrc
                            break

        return composer, final_isrcs
```

---

### File: `services/MovieSongDownloader/providers/omdb_provider.py`
- **Path:** `services/MovieSongDownloader/providers/omdb_provider.py`
- **Estimated Tokens:** 1,309
- **mtime:** 1780856038.303

```python
import time
import httpx
import logging
import hashlib
from typing import List, Optional

from MovieSongDownloader.core.models import Movie
from MovieSongDownloader.core.settings_manager import settings_manager
from MovieSongDownloader.core.rate_limiter import rate_limiter, providers_logger
from MovieSongDownloader.core.cache_manager import api_cache
from MovieSongDownloader.config import OMDB_BASE_URL

logger = logging.getLogger("MovieSongDownloader.OMDbProvider")


class OMDbProvider:
    """Optional fallback provider for movie ratings, cast, and plot via OMDb API."""

    async def _request(self, params: dict, cache_ttl: int = 2592000) -> Optional[dict]:
        """Make OMDb API request with caching. TTL default 30 days."""
        api_key = await settings_manager.get("omdb_api_key")
        if not api_key:
            logger.debug("OMDb API key not configured.")
            return None

        full_params = {**params, "apikey": api_key}
        param_str = "".join(f"{k}={params[k]}" for k in sorted(params))
        cache_key = f"omdb:{hashlib.md5(param_str.encode()).hexdigest()}"

        cached = await api_cache.get(cache_key)
        if cached is not None:
            return cached

        await rate_limiter.acquire("omdb")
        t0 = time.time()
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                resp = await client.get(OMDB_BASE_URL, params=full_params)
                ms = int((time.time() - t0) * 1000)
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("Response") == "True":
                        providers_logger.info(
                            f"provider=omdb latency={ms}ms success=True"
                        )
                        await api_cache.set(cache_key, "omdb", data, cache_ttl)
                        return data
                    providers_logger.warning(
                        f'provider=omdb latency={ms}ms response=False error="{data.get("Error")}"'
                    )
                else:
                    providers_logger.error(
                        f"provider=omdb latency={ms}ms success=False status={resp.status_code}"
                    )
        except Exception as e:
            ms = int((time.time() - t0) * 1000)
            providers_logger.error(
                f'provider=omdb latency={ms}ms success=False error="{e}"'
            )
            logger.error(f"OMDb request failed: {e}")
        return None

    async def search(self, query: str, year: Optional[int] = None) -> List[Movie]:
        """Search OMDb for movies."""
        params = {"s": query, "type": "movie"}
        if year:
            params["y"] = str(year)

        data = await self._request(params, cache_ttl=86400)
        if not data or "Search" not in data:
            return []

        movies = []
        for item in data["Search"]:
            yr = None
            try:
                yr = int(item.get("Year", "0").split("–")[0])
            except (ValueError, IndexError):
                pass

            movies.append(
                Movie(
                    source="omdb",
                    source_id=item.get("imdbID", ""),
                    title=item.get("Title", ""),
                    year=yr,
                    poster_url=item.get("Poster")
                    if item.get("Poster") != "N/A"
                    else None,
                )
            )
        return movies

    async def get_details(self, imdb_id: str) -> Optional[dict]:
        """Fetch full movie details from OMDb by IMDb ID."""
        params = {"i": imdb_id, "plot": "short"}
        return await self._request(params, cache_ttl=2592000)

    async def enrich_movie(self, movie: Movie) -> Movie:
        """Enrich a Movie object with OMDb data (rating, cast, poster, overview).
        Tries by title+year if no imdb_id available."""
        data = None

        # If we have an IMDb ID, use it directly
        if movie.source == "omdb" and movie.source_id:
            data = await self.get_details(movie.source_id)

        # Otherwise search by title
        if not data:
            params = {"t": movie.title, "type": "movie"}
            if movie.year:
                params["y"] = str(movie.year)
            data = await self._request(params, cache_ttl=2592000)

        if not data:
            return movie

        # Enrich fields
        if not movie.poster_url or movie.poster_url == "N/A":
            poster = data.get("Poster")
            if poster and poster != "N/A":
                movie.poster_url = poster

        movie.rating = data.get("imdbRating")
        movie.cast_info = data.get("Actors")

        if not movie.overview:
            movie.overview = data.get("Plot")

        if not movie.genres:
            genres_str = data.get("Genre", "")
            if genres_str and genres_str != "N/A":
                movie.genres = [g.strip() for g in genres_str.split(",")]

        if not movie.language:
            movie.language = data.get("Language")

        # Store IMDb ID for future lookups
        if data.get("imdbID") and not movie.source_id:
            movie.source_id = data["imdbID"]

        return movie
```

---

### File: `services/MovieSongDownloader/providers/spotiflac_provider.py`
- **Path:** `services/MovieSongDownloader/providers/spotiflac_provider.py`
- **Estimated Tokens:** 2,481
- **mtime:** 1781123459.224

```python
import os
import httpx
import re
import logging
import asyncio
import shutil
from typing import Optional, Callable
from urllib.parse import quote_plus

from MovieSongDownloader.providers.base import BaseDownloadProvider
from MovieSongDownloader.core.models import Track
from MovieSongDownloader.core.settings_manager import settings_manager

logger = logging.getLogger("MovieSongDownloader.SpotiFLACProvider")


class SpotiFLACProvider(BaseDownloadProvider):
    def _get_subprocess_env(self) -> dict:
        """
        Prepares environment variables for subprocesses, ensuring ffmpeg is in PATH
        and preventing UnicodeEncodeError in python CLI tools.
        """
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUTF8"] = "1"
        
        # Add local bin directory to PATH
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        bin_dir = os.path.join(base_dir, "bin")
        if os.path.exists(bin_dir):
            env["PATH"] = bin_dir + os.pathsep + env.get("PATH", "")
            
        return env

    async def _resolve_spotify_url(self, title: str, artist: str) -> str:
        """
        Queries DuckDuckGo HTML search to resolve a song's title & artist to a Spotify track URL.
        """
        clean_title = title.replace('"', "").replace("'", "")
        clean_artist = artist.split(",")[0].strip()
        query = f'site:open.spotify.com/track "{clean_artist}" "{clean_title}"'
        url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36"
            )
        }

        logger.info(
            f"Resolving Spotify track URL for '{title}' by '{artist}' via DDG..."
        )

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url, headers=headers)
                if resp.status_code == 200:
                    matches = re.findall(
                        r"open\.spotify\.com/track/([a-zA-Z0-9]+)", resp.text
                    )
                    if matches:
                        spotify_id = matches[0]
                        resolved_url = f"https://open.spotify.com/track/{spotify_id}"
                        logger.info(f"Resolved track successfully to: {resolved_url}")
                        return resolved_url
        except Exception as e:
            logger.error(f"DDG Spotify resolution request failed: {e}")

        # Fallback to a broader search query if exact match failed
        query_broad = f"site:open.spotify.com/track {clean_artist} {clean_title}"
        url_broad = f"https://html.duckduckgo.com/html/?q={quote_plus(query_broad)}"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url_broad, headers=headers)
                if resp.status_code == 200:
                    matches = re.findall(
                        r"open\.spotify\.com/track/([a-zA-Z0-9]+)", resp.text
                    )
                    if matches:
                        spotify_id = matches[0]
                        resolved_url = f"https://open.spotify.com/track/{spotify_id}"
                        logger.info(
                            f"Resolved track via broad query to: {resolved_url}"
                        )
                        return resolved_url
        except Exception as e:
            logger.error(f"DDG Spotify broad resolution request failed: {e}")

        raise Exception(
            f"Could not resolve a Spotify track URL for '{title}' by '{artist}'."
        )

    async def _transcode_audio(
        self, input_path: str, output_path: str, format_str: str, bitrate: str = "320"
    ) -> None:
        """
        Transcodes the input audio file to the target format using ffmpeg.
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ffmpeg_path = os.path.join(base_dir, "bin", "ffmpeg.exe")
        if not os.path.exists(ffmpeg_path):
            ffmpeg_path = "ffmpeg"  # fallback to path

        format_str = format_str.lower()
        cmd = [ffmpeg_path, "-y", "-i", input_path, "-vn"]

        if format_str == "mp3":
            cmd.extend(["-ar", "44100", "-ac", "2", "-b:a", f"{bitrate}k", output_path])
        elif format_str == "flac":
            cmd.extend([output_path])
        elif format_str in ("m4a", "aac"):
            cmd.extend(["-c:a", "copy", output_path])
        else:
            cmd.extend([output_path])

        logger.info(f"SpotiFLAC Transcode: {' '.join(cmd)}")
        env = self._get_subprocess_env()
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, env=env
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            err_msg = stderr.decode(errors="ignore")
            logger.error(f"ffmpeg transcoding failed: {err_msg}")
            raise Exception(f"Transcoding failed: {err_msg}")

    async def download(
        self,
        track: Track,
        format: str,
        output_dir: str,
        filename_template: str,
        on_progress: Optional[Callable[[float, str], None]] = None,
    ) -> str:
        """
        Downloads a track using spotiflac globally installed CLI command.
        """
        # Resolve Spotify track URL
        if track.source == "spotify" and track.source_id:
            spotify_url = f"https://open.spotify.com/track/{track.source_id}"
        else:
            spotify_url = await self._resolve_spotify_url(track.title, track.artist)

        # We will download the track into a temporary subfolder to identify the generated file
        temp_subfolder = os.path.join(
            output_dir, f"spotiflac_temp_{track.source_id or 'unknown'}"
        )
        if os.path.exists(temp_subfolder):
            shutil.rmtree(temp_subfolder, ignore_errors=True)
        os.makedirs(temp_subfolder, exist_ok=True)

        if on_progress:
            on_progress(20.0, "spotiflac_starting")

        cmd = ["spotiflac", spotify_url, temp_subfolder]

        # Check settings for Deezer ARL or other service prioritization (optional parameter)
        deezer_arl = await settings_manager.get("deezer_arl")
        # We can specify service priority or other custom flags if desired
        # e.g., --service deezer
        services = []
        if deezer_arl:
            # If Deezer ARL is configured, we prioritize deezer download
            services.append("deezer")

        # Default priority: tidal, qobuz, deezer, amazon
        # We can pass them as args if spotiflac CLI supports --service flag
        if services:
            cmd.extend(["--service"] + services)

        logger.info(f"Executing SpotiFLAC Command: {' '.join(cmd)}")

        if on_progress:
            on_progress(40.0, "spotiflac_downloading")

        try:
            env = self._get_subprocess_env()
            process = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, env=env
            )
            stdout, stderr = await process.communicate()

            stdout_str = stdout.decode(errors="ignore")
            stderr_str = stderr.decode(errors="ignore")

            logger.info(f"spotiflac stdout: {stdout_str}")
            if process.returncode != 0:
                logger.error(f"spotiflac stderr: {stderr_str}")
                raise Exception(
                    f"SpotiFLAC download failed with exit code {process.returncode}: {stderr_str}"
                )

        except Exception as e:
            shutil.rmtree(temp_subfolder, ignore_errors=True)
            raise e

        if on_progress:
            on_progress(80.0, "spotiflac_postprocessing")

        # Scan for the downloaded audio file
        audio_extensions = (".flac", ".mp3", ".m4a", ".aac", ".ogg", ".wav")
        downloaded_file = None
        for root, _, files in os.walk(temp_subfolder):
            for file in files:
                if file.lower().endswith(audio_extensions):
                    downloaded_file = os.path.join(root, file)
                    break
            if downloaded_file:
                break

        if not downloaded_file or not os.path.exists(downloaded_file):
            shutil.rmtree(temp_subfolder, ignore_errors=True)
            raise Exception(
                "SpotiFLAC executed successfully, but no audio file was generated in the output directory."
            )

        # Resolve target path in output_dir
        file_ext = os.path.splitext(downloaded_file)[1].lower()
        target_ext = f".{format.lower()}"

        # Check if we need transcoding (e.g. SpotiFLAC downloaded FLAC but format is MP3)
        if file_ext != target_ext:
            logger.info(
                f"Transcoding SpotiFLAC output {file_ext} to target {target_ext}..."
            )
            bitrate = await settings_manager.get("bitrate") or "320"
            temp_transcoded = os.path.join(temp_subfolder, f"transcoded{target_ext}")
            await self._transcode_audio(
                downloaded_file, temp_transcoded, format, bitrate
            )
            downloaded_file = temp_transcoded

        # Copy the file to the parent output_dir (or return its path so download_service moves it)
        final_temp_path = os.path.join(
            output_dir, f"spotiflac_result_{track.source_id}{target_ext}"
        )
        if os.path.exists(final_temp_path):
            os.remove(final_temp_path)

        shutil.move(downloaded_file, final_temp_path)
        shutil.rmtree(temp_subfolder, ignore_errors=True)

        return final_temp_path
```

---

### File: `services/MovieSongDownloader/providers/spotify_provider.py`
- **Path:** `services/MovieSongDownloader/providers/spotify_provider.py`
- **Estimated Tokens:** 1,557
- **mtime:** 1780861103.721

```python
import httpx
import re
import json
import logging
from typing import Tuple, List, Optional
from MovieSongDownloader.core.models import Movie, Album, Track

logger = logging.getLogger("MovieSongDownloader.SpotifyProvider")


class SpotifyProvider:
    def __init__(self):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36"
            )
        }

    def _get_cover_url(self, vi: dict) -> Optional[str]:
        if not vi or "image" not in vi:
            return None
        images = vi["image"]
        if not images:
            return None
        # Sort images by maxWidth/maxHeight descending to get the best quality
        sorted_imgs = sorted(
            images,
            key=lambda x: (x.get("maxWidth", 0) or 0) * (x.get("maxHeight", 0) or 0),
            reverse=True,
        )
        return sorted_imgs[0].get("url")

    async def get_spotify_album_or_track(
        self, spotify_url_or_id: str
    ) -> Tuple[Movie, Album, List[Track]]:
        """
        Parses the Spotify URL or ID to scrape the public embed metadata.
        Returns:
            Tuple[Movie, Album, List[Track]]
        """
        # Detect ID and Type
        match = re.search(r"(album|track)/([a-zA-Z0-9]+)", spotify_url_or_id)
        if match:
            item_type = match.group(1)
            item_id = match.group(2)
        else:
            # Assume it's a raw ID, default to album
            item_type = "album"
            item_id = spotify_url_or_id

        embed_url = f"https://open.spotify.com/embed/{item_type}/{item_id}"

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(embed_url, headers=self.headers)
            if resp.status_code != 200:
                raise Exception(
                    f"Failed to fetch Spotify embed page: status {resp.status_code}"
                )

        html = resp.text
        json_match = re.search(
            r'<script id="__NEXT_DATA__"[^>]* type="application/json">(.*?)</script>',
            html,
            re.DOTALL,
        )
        if not json_match:
            raise Exception(
                "Failed to extract metadata from Spotify embed page: __NEXT_DATA__ not found."
            )

        try:
            data = json.loads(json_match.group(1))
        except Exception as e:
            raise Exception(f"Failed to parse Spotify embed JSON metadata: {e}")

        state_data = (
            data.get("props", {}).get("pageProps", {}).get("state", {}).get("data", {})
        )
        entity = state_data.get("entity", {})
        if not entity:
            raise Exception("Invalid Spotify embed JSON structure: 'entity' not found.")

        # Check for error status
        if data.get("props", {}).get("pageProps", {}).get("status") == 404:
            raise Exception("Spotify item not found (404). Check the URL/ID.")

        title = entity.get("title") or entity.get("name") or "Unknown"
        cover_url = self._get_cover_url(entity.get("visualIdentity", {}))

        if item_type == "album":
            artist_name = entity.get("subtitle") or "Unknown Artist"
            movie = Movie(
                source="spotify",
                source_id=item_id,
                title=title,
                poster_url=cover_url,
                overview=f"Spotify Album: {title} by {artist_name}",
            )
            album = Album(
                source="spotify",
                source_id=item_id,
                spotify_id=item_id,
                title=title,
                artist=artist_name,
                cover_url=cover_url,
                total_tracks=len(entity.get("trackList", [])),
            )

            tracks = []
            for idx, t in enumerate(entity.get("trackList", []), start=1):
                t_uri = t.get("uri", "")
                t_id = t_uri.split(":")[-1] if ":" in t_uri else t.get("uid", "")

                # Extract preview URL if available
                preview_url = (
                    t.get("audioPreview", {}).get("url")
                    if t.get("audioPreview")
                    else None
                )

                tracks.append(
                    Track(
                        source="spotify",
                        source_id=t_id,
                        spotify_id=t_id,
                        title=t.get("title", "Unknown Track"),
                        artist=t.get("subtitle") or artist_name,
                        duration_ms=t.get("duration", 0),
                        track_number=idx,
                        preview_url=preview_url,
                    )
                )
            return movie, album, tracks

        else:  # track
            artists_list = entity.get("artists", [])
            artist_name = (
                ", ".join([a.get("name", "") for a in artists_list])
                if artists_list
                else "Unknown Artist"
            )

            # For a single track, wrap it in a dummy album of size 1
            movie = Movie(
                source="spotify",
                source_id=item_id,
                title=title,
                poster_url=cover_url,
                overview=f"Spotify Track: {title} by {artist_name}",
            )
            album = Album(
                source="spotify",
                source_id=item_id,
                spotify_id=item_id,
                title=title,
                artist=artist_name,
                cover_url=cover_url,
                total_tracks=1,
            )

            preview_url = (
                entity.get("audioPreview", {}).get("url")
                if entity.get("audioPreview")
                else None
            )

            track = Track(
                source="spotify",
                source_id=item_id,
                spotify_id=item_id,
                title=title,
                artist=artist_name,
                duration_ms=entity.get("duration", 0),
                track_number=1,
                preview_url=preview_url,
            )
            return movie, album, [track]
```

---

### File: `services/MovieSongDownloader/providers/tagging_provider.py`
- **Path:** `services/MovieSongDownloader/providers/tagging_provider.py`
- **Estimated Tokens:** 913
- **mtime:** 1780856038.315

```python
import os
import logging
from typing import Optional
from MovieSongDownloader.providers.base import BaseTaggingProvider
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, USLT, TIT2, TPE1, TALB, TYER, TRCK, ID3NoHeaderError
from mutagen.flac import FLAC, Picture

logger = logging.getLogger("MovieSongDownloader.TaggingProvider")


class TaggingProvider(BaseTaggingProvider):
    async def embed_cover(self, file_path: str, image_path: str) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio not found: {file_path}")
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        with open(image_path, "rb") as f:
            img_data = f.read()
        mime = "image/png" if image_path.lower().endswith(".png") else "image/jpeg"
        ext = file_path.rsplit(".", 1)[-1].lower()

        if ext == "mp3":
            audio = self._get_mp3(file_path)
            for k in [k for k in audio.tags.keys() if k.startswith("APIC")]:
                audio.tags.pop(k)
            audio.tags.add(
                APIC(encoding=3, mime=mime, type=3, desc="Front Cover", data=img_data)
            )
            audio.save()
        elif ext == "flac":
            audio = FLAC(file_path)
            audio.clear_pictures()
            pic = Picture()
            pic.data, pic.type, pic.mime, pic.desc = img_data, 3, mime, "Front Cover"
            audio.add_picture(pic)
            audio.save()

    async def embed_lyrics(
        self, file_path: str, lyrics_content: str, is_synced: bool = False
    ) -> None:
        if not os.path.exists(file_path) or not lyrics_content:
            return
        ext = file_path.rsplit(".", 1)[-1].lower()
        if ext == "mp3":
            audio = self._get_mp3(file_path)
            for k in [k for k in audio.tags.keys() if k.startswith("USLT")]:
                audio.tags.pop(k)
            audio.tags.add(
                USLT(encoding=3, lang="eng", desc="Lyrics", text=lyrics_content)
            )
            audio.save()
        elif ext == "flac":
            audio = FLAC(file_path)
            audio["lyrics"] = lyrics_content
            audio["unsyncedlyrics"] = lyrics_content
            audio.save()

    async def embed_metadata(
        self,
        file_path: str,
        title: str,
        artist: str,
        album: str,
        year: Optional[int] = None,
        track_num: int = 1,
    ) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio not found: {file_path}")
        ext = file_path.rsplit(".", 1)[-1].lower()
        if ext == "mp3":
            audio = self._get_mp3(file_path)
            audio.tags.add(TIT2(encoding=3, text=title))
            audio.tags.add(TPE1(encoding=3, text=artist))
            audio.tags.add(TALB(encoding=3, text=album))
            audio.tags.add(TRCK(encoding=3, text=str(track_num)))
            if year:
                audio.tags.add(TYER(encoding=3, text=str(year)))
            audio.save()
        elif ext == "flac":
            audio = FLAC(file_path)
            audio["title"] = title
            audio["artist"] = artist
            audio["album"] = album
            audio["tracknumber"] = str(track_num)
            if year:
                audio["date"] = str(year)
            audio.save()

    @staticmethod
    def _get_mp3(path: str) -> MP3:
        try:
            audio = MP3(path, ID3=ID3)
        except ID3NoHeaderError:
            audio = MP3(path)
            audio.add_tags()
        if audio.tags is None:
            audio.add_tags()
        return audio
```

---

### File: `services/MovieSongDownloader/providers/wikidata_provider.py`
- **Path:** `services/MovieSongDownloader/providers/wikidata_provider.py`
- **Estimated Tokens:** 1,060
- **mtime:** 1780856515.522

```python
import logging
import httpx
import hashlib
import time
from typing import List, Dict, Optional
from MovieSongDownloader.core.rate_limiter import rate_limiter, providers_logger
from MovieSongDownloader.core.cache_manager import api_cache

logger = logging.getLogger("MovieSongDownloader.WikidataProvider")

USER_AGENT = "MovieSongDownloader/2.0 (contact: nandha.dev@gmail.com)"


class WikidataProvider:
    async def _wikidata_request(
        self, params: dict, cache_ttl: int = 604800
    ) -> Optional[dict]:
        """Make a request to Wikidata API with caching and rate limiting."""
        params["format"] = "json"
        param_str = "".join(f"{k}={params[k]}" for k in sorted(params))
        cache_key = f"wikidata:{hashlib.md5(param_str.encode()).hexdigest()}"

        cached = await api_cache.get(cache_key)
        if cached is not None:
            return cached

        await rate_limiter.acquire("wikidata")
        t0 = time.time()
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.get(
                    "https://www.wikidata.org/w/api.php",
                    params=params,
                    headers={"User-Agent": USER_AGENT},
                )
                ms = int((time.time() - t0) * 1000)
                if resp.status_code == 200:
                    data = resp.json()
                    providers_logger.info(
                        f"provider=wikidata latency={ms}ms success=True"
                    )
                    await api_cache.set(cache_key, "wikidata", data, cache_ttl)
                    return data
                providers_logger.error(
                    f"provider=wikidata latency={ms}ms success=False status={resp.status_code}"
                )
        except Exception as e:
            ms = int((time.time() - t0) * 1000)
            providers_logger.error(
                f'provider=wikidata latency={ms}ms success=False error="{e}"'
            )
            logger.error(f"Wikidata API request failed: {e}")
        return None

    async def get_posters_batch(
        self, wikipedia_titles: List[str], lang: str = "en"
    ) -> Dict[str, str]:
        """
        Query Wikidata API in batches to resolve P18 (image) property for Wikipedia page titles.
        Returns a dictionary mapping {wikipedia_title: poster_url}.
        """
        if not wikipedia_titles:
            return {}

        results = {}
        site = "enwiki" if lang == "en" else "tawiki"

        # Wikipedia allows batching up to 50 items
        batch_size = 40
        for i in range(0, len(wikipedia_titles), batch_size):
            batch = wikipedia_titles[i:i+batch_size]
            params = {
                "action": "wbgetentities",
                "sites": site,
                "titles": "|".join(batch),
                "props": "claims|sitelinks",
            }

            data = await self._wikidata_request(params, cache_ttl=86400 * 7)
            if not data or "entities" not in data:
                continue

            entities = data["entities"]
            for entity_id, entity_data in entities.items():
                if entity_id == "-1":
                    continue

                # Retrieve the original title from sitelinks to map correctly
                sitelinks = entity_data.get("sitelinks", {})
                wiki_site = sitelinks.get(site, {})
                title = wiki_site.get("title")
                if not title:
                    continue

                claims = entity_data.get("claims", {})
                p18_claims = claims.get("P18", [])
                if p18_claims:
                    # Get filename from the claim
                    mainsnak = p18_claims[0].get("mainsnak", {})
                    datavalue = mainsnak.get("datavalue", {})
                    filename = datavalue.get("value")
                    if filename:
                        # Construct Wikimedia Commons Special:FilePath URL
                        # Special:FilePath redirects directly to the raw media URL
                        url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{filename}"
                        results[title] = url

        return results
```

---

### File: `services/MovieSongDownloader/requirements.txt`
- **Path:** `services/MovieSongDownloader/requirements.txt`
- **Estimated Tokens:** 42
- **mtime:** 1780574049.314

```
reflex>=0.5.0
httpx>=0.27.0
yt-dlp>=2024.0.0
deezload>=0.2.0
mutagen>=1.47.0
aiosqlite>=0.20.0
syncedlyrics>=1.0.0
jiosaavnpy>=0.1.3
beautifulsoup4>=4.12.0
lxml>=5.0.0
```

---

### File: `services/MovieSongDownloader/scripts/run_migrations.py`
- **Path:** `services/MovieSongDownloader/scripts/run_migrations.py`
- **Estimated Tokens:** 100
- **mtime:** 1780924764.321

```python
import asyncio
import traceback

from MovieSongDownloader.core.database import db

async def main():
    try:
        print('Running migrations...', flush=True)
        await db.run_migrations()
        print('Migrations applied successfully', flush=True)
    except Exception as e:
        print('Migration failed:', e)
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(main())
```

---

### File: `services/MovieSongDownloader/services/__init__.py`
- **Path:** `services/MovieSongDownloader/services/__init__.py`
- **Estimated Tokens:** 4
- **mtime:** 1780474579.015

```python
# Services Module
```

---

### File: `services/MovieSongDownloader/services/download_service.py`
- **Path:** `services/MovieSongDownloader/services/download_service.py`
- **Estimated Tokens:** 4,107
- **mtime:** 1780861103.744

```python
import os
import shutil
import asyncio
import logging
import json
from typing import Optional
from pathlib import Path
import httpx

from MovieSongDownloader.core.database import db
from MovieSongDownloader.core.models import DownloadJob, Movie, Album, Track
from MovieSongDownloader.core.job_queue import job_queue
from MovieSongDownloader.core.cache_manager import download_cache, image_cache
from MovieSongDownloader.core.settings_manager import settings_manager
from MovieSongDownloader.providers.deezspot_provider import DeezspotProvider
from MovieSongDownloader.providers.spotiflac_provider import SpotiFLACProvider
from MovieSongDownloader.providers.lyrics_provider import LyricsProvider
from MovieSongDownloader.providers.tagging_provider import TaggingProvider
from MovieSongDownloader.services.folder_service import FolderService

logger = logging.getLogger("MovieSongDownloader.DownloadService")


class DownloadService:
    def __init__(self):
        self.download_provider = DeezspotProvider()
        self.lyrics_provider = LyricsProvider()
        self.tagging_provider = TaggingProvider()
        self.folder_service = FolderService()
        self._worker_task: Optional[asyncio.Task] = None
        self._running = False

    async def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._worker_task = asyncio.create_task(self._worker())
        logger.info("Download worker started.")

    async def stop(self) -> None:
        self._running = False
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass
        logger.info("Download worker stopped.")

    async def _worker(self) -> None:
        while self._running:
            try:
                job = await job_queue.dequeue()
                if job:
                    task = asyncio.create_task(self._process(job))
                    await job_queue.register_task(job.id, task)
                    try:
                        await task
                    except asyncio.CancelledError:
                        await self._cleanup(job)
                    finally:
                        await job_queue.unregister_task(job.id)
                else:
                    await asyncio.sleep(2.0)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Worker error: {e}", exc_info=True)
                await asyncio.sleep(5.0)

    async def _transcode_audio(
        self, input_path: str, output_path: str, format: str, bitrate: str = "320"
    ) -> None:
        # Locate local ffmpeg binary
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ffmpeg_path = os.path.join(base_dir, "bin", "ffmpeg.exe")
        if not os.path.exists(ffmpeg_path):
            ffmpeg_path = "ffmpeg"  # fallback to system PATH

        format = format.lower()
        cmd = [ffmpeg_path, "-y", "-i", input_path, "-vn"]

        if format == "mp3":
            cmd.extend(["-ar", "44100", "-ac", "2", "-b:a", f"{bitrate}k", output_path])
        elif format == "flac":
            cmd.extend([output_path])
        elif format in ("m4a", "aac"):
            cmd.extend(["-c:a", "copy", output_path])
        else:
            cmd.extend([output_path])

        logger.info(f"Running transcode: {' '.join(cmd)}")

        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            err_msg = stderr.decode(errors="ignore")
            logger.error(f"ffmpeg transcoding failed: {err_msg}")
            raise Exception(f"Transcoding failed: {err_msg}")

    async def _process(self, job: DownloadJob) -> None:
        conn = await db.get_connection()
        try:
            async with conn.execute(
                "SELECT m.tmdb_id, m.title, m.year, m.poster_url, m.poster_cached_path, m.overview, "
                "m.language, m.genres, m.ott_providers, m.source, m.source_id, m.rating, m.cast_info "
                "FROM movies m JOIN albums a ON a.movie_id=m.id JOIN tracks t ON t.album_id=a.id "
                "WHERE t.id=?",
                (job.track_id,),
            ) as c:
                r = await c.fetchone()
                if not r:
                    await job_queue.mark_failed(job.id, "Movie/Album metadata missing.")
                    return
                movie = Movie(
                    tmdb_id=r[0],
                    title=r[1],
                    year=r[2],
                    poster_url=r[3],
                    poster_cached_path=r[4],
                    overview=r[5],
                    language=r[6],
                    genres=json.loads(r[7]) if r[7] else [],
                    ott_providers=json.loads(r[8]) if r[8] else [],
                    source=r[9],
                    source_id=r[10],
                    rating=r[11],
                    cast_info=r[12],
                )
            async with conn.execute(
                "SELECT a.id, a.spotify_id, a.title, a.artist, a.cover_url, a.cover_cached_path, "
                "a.total_tracks, a.source, a.source_id "
                "FROM albums a JOIN tracks t ON t.album_id=a.id WHERE t.id=?",
                (job.track_id,),
            ) as c:
                r = await c.fetchone()
                album = Album(
                    id=r[0],
                    spotify_id=r[1],
                    title=r[2],
                    artist=r[3],
                    cover_url=r[4],
                    cover_cached_path=r[5],
                    total_tracks=r[6],
                    source=r[7],
                    source_id=r[8],
                )
            async with conn.execute(
                "SELECT id, spotify_id, title, artist, duration_ms, track_number, preview_url, "
                "source, source_id, download_url FROM tracks WHERE id=?",
                (job.track_id,),
            ) as c:
                r = await c.fetchone()
                track = Track(
                    id=r[0],
                    spotify_id=r[1],
                    title=r[2],
                    artist=r[3],
                    duration_ms=r[4],
                    track_number=r[5],
                    preview_url=r[6],
                    source=r[7],
                    source_id=r[8],
                    download_url=r[9],
                )
        finally:
            await conn.close()

        # Cache dedup check
        track_hash = download_cache.generate_hash(
            track.artist, track.title, album.title, track.duration_ms
        )
        target_dir, abs_path = await self.folder_service.get_target_path(
            movie, album, track, job.format
        )
        hit = await download_cache.check(track_hash)

        if hit:
            await job_queue.update_progress(job.id, 50.0, "copying_from_cache")
            try:
                os.makedirs(target_dir, exist_ok=True)
                shutil.copy2(hit["file_path"], abs_path)
                await self.folder_service.write_movie_metadata(movie, target_dir)
                await self.folder_service.generate_m3u_playlist(target_dir, album.title)
                await job_queue.mark_completed(job.id, abs_path)
                return
            except Exception as e:
                logger.error(f"Cache copy failed: {e}")

        # Download
        temp_dir = os.path.join(Path(__file__).resolve().parent.parent, "cache", "temp")
        os.makedirs(temp_dir, exist_ok=True)
        await job_queue.update_progress(job.id, 10.0, "downloading")

        temp_path = None
        for attempt in range(3):
            temp_raw_path = None
            try:
                provider_setting = (
                    await settings_manager.get("download_provider") or "spotiflac"
                )
                use_cdn = (
                    track.download_url
                    and provider_setting != "spotiflac"
                    and job.format.lower() != "flac"
                )

                if use_cdn:
                    logger.info(
                        f"Downloading directly from JioSaavn CDN: {track.download_url}"
                    )
                    temp_raw_path = os.path.join(temp_dir, f"temp_{job.id}_raw.mp4")

                    async with httpx.AsyncClient(timeout=30.0) as client:
                        async with client.stream("GET", track.download_url) as resp:
                            if resp.status_code != 200:
                                raise Exception(
                                    f"Failed to fetch saavncdn URL: status {resp.status_code}"
                                )
                            total_bytes = int(resp.headers.get("content-length", 0))
                            downloaded_bytes = 0
                            with open(temp_raw_path, "wb") as f:
                                async for chunk in resp.iter_bytes(chunk_size=65536):
                                    f.write(chunk)
                                    downloaded_bytes += len(chunk)
                                    if total_bytes > 0:
                                        pct = (downloaded_bytes / total_bytes) * 100.0
                                        # Scale progress from 10% to 50% of the overall download pipeline
                                        scaled_prog = 10.0 + (pct / 100.0) * 40.0
                                        await job_queue.update_progress(
                                            job.id, scaled_prog, "downloading"
                                        )

                    bitrate = await settings_manager.get("bitrate") or "320"
                    dest_ext = job.format.lower()
                    temp_dest_path = os.path.join(temp_dir, f"temp_{job.id}.{dest_ext}")

                    await self._transcode_audio(
                        temp_raw_path, temp_dest_path, job.format, bitrate
                    )

                    if os.path.exists(temp_raw_path):
                        os.remove(temp_raw_path)

                    temp_path = temp_dest_path
                else:
                    if provider_setting == "spotiflac":
                        logger.info("Using SpotiFLAC download provider.")
                        provider = SpotiFLACProvider()
                    else:
                        logger.info("Using Deezspot download provider.")
                        provider = self.download_provider

                    loop = asyncio.get_running_loop()

                    async def provider_progress(prog_pct: float, status_str: str):
                        # Scale progress from 10% to 50%
                        scaled_prog = 10.0 + (prog_pct / 100.0) * 40.0
                        await job_queue.update_progress(
                            job.id, scaled_prog, "downloading"
                        )

                    def sync_progress(prog_pct: float, status_str: str):
                        asyncio.run_coroutine_threadsafe(
                            provider_progress(prog_pct, status_str), loop
                        )

                    temp_path = await provider.download(
                        track=track,
                        format=job.format,
                        output_dir=temp_dir,
                        filename_template="",
                        on_progress=sync_progress,
                    )

                if await self._verify(temp_path, job.format):
                    break
                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)
                temp_path = None
            except Exception as e:
                logger.error(f"Download attempt {attempt + 1} failed: {e}")
                if temp_raw_path and os.path.exists(temp_raw_path):
                    try:
                        os.remove(temp_raw_path)
                    except Exception:
                        pass
                if temp_path and os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except Exception:
                        pass
                temp_path = None
            await asyncio.sleep(2.0)

        if not temp_path:
            await job_queue.mark_failed(
                job.id, "Download integrity failed after 3 retries."
            )
            return

        # Lyrics
        await job_queue.update_progress(job.id, 60.0, "fetching_lyrics")
        lyrics, ltype = await self.lyrics_provider.fetch(track.title, track.artist)
        if lyrics:
            conn = await db.get_connection()
            try:
                await conn.execute(
                    "INSERT INTO lyrics_results (track_id, provider, lyrics_type, content) "
                    "VALUES (?, 'waterfall', ?, ?)",
                    (track.id, ltype, lyrics),
                )
                await conn.commit()
            finally:
                await conn.close()

        # Cover art
        await job_queue.update_progress(job.id, 75.0, "embedding_cover")
        cover = None
        if album.cover_url:
            cover = await image_cache.get_or_download(album.cover_url, "cover")
        if not cover and movie.poster_url:
            cover = await image_cache.get_or_download(movie.poster_url, "poster")
        if cover:
            try:
                await self.tagging_provider.embed_cover(temp_path, cover)
            except Exception as e:
                logger.error(f"Cover embed failed: {e}")

        # Metadata + lyrics tags
        await job_queue.update_progress(job.id, 85.0, "embedding_metadata")
        if lyrics and await settings_manager.get("embed_lyrics") == "true":
            try:
                await self.tagging_provider.embed_lyrics(
                    temp_path, lyrics, ltype == "synced"
                )
            except Exception as e:
                logger.error(f"Lyrics embed failed: {e}")
        try:
            await self.tagging_provider.embed_metadata(
                temp_path,
                track.title,
                track.artist,
                album.title,
                movie.year,
                track.track_number,
            )
        except Exception as e:
            logger.error(f"Metadata embed failed: {e}")

        # Move to destination
        await job_queue.update_progress(job.id, 95.0, "copying_to_destination")
        try:
            os.makedirs(target_dir, exist_ok=True)
            shutil.move(temp_path, abs_path)
            if lyrics and await settings_manager.get("save_lrc_file") == "true":
                ext = "lrc" if ltype == "synced" else "txt"
                with open(
                    abs_path.rsplit(".", 1)[0] + f".{ext}", "w", encoding="utf-8"
                ) as f:
                    f.write(lyrics)
            await download_cache.add(track_hash, abs_path, job.format)
            await self.folder_service.write_movie_metadata(movie, target_dir)
            await self.folder_service.generate_m3u_playlist(target_dir, album.title)
            await job_queue.mark_completed(job.id, abs_path)
        except Exception as e:
            await job_queue.mark_failed(job.id, f"Save error: {e}")

    async def _verify(self, path: str, fmt: str) -> bool:
        if not path or not os.path.exists(path):
            return False
        sz = os.path.getsize(path)
        if sz < (500 * 1024 if fmt.lower() == "mp3" else 2 * 1024 * 1024):
            return False
        if fmt.lower() == "flac":
            try:
                from mutagen.flac import FLAC

                FLAC(path)
            except Exception:
                return False
        return True

    async def _cleanup(self, job: DownloadJob) -> None:
        temp_dir = os.path.join(Path(__file__).resolve().parent.parent, "cache", "temp")
        if os.path.exists(temp_dir):
            for f in os.listdir(temp_dir):
                try:
                    fp = os.path.join(temp_dir, f)
                    if os.path.isfile(fp):
                        os.remove(fp)
                except Exception:
                    pass


download_service = DownloadService()
```

---

### File: `services/MovieSongDownloader/services/folder_service.py`
- **Path:** `services/MovieSongDownloader/services/folder_service.py`
- **Estimated Tokens:** 835
- **mtime:** 1780856038.246

```python
import os
import re
import json
import logging
from datetime import datetime
from typing import Tuple
from pathlib import Path
from MovieSongDownloader.core.models import Movie, Album, Track
from MovieSongDownloader.core.settings_manager import settings_manager

logger = logging.getLogger("MovieSongDownloader.FolderService")


class FolderService:
    @staticmethod
    def sanitize_name(name: str) -> str:
        if not name:
            return "Unknown"
        s = re.sub(r'[\\/:*?"<>|]', "-", name)
        return re.sub(r"\s+", " ", s).strip() or "Unknown"

    async def get_target_path(
        self, movie: Movie, album: Album, track: Track, fmt: str = "mp3"
    ) -> Tuple[str, str]:
        output_dir = await settings_manager.get("output_dir")
        folder_tpl = await settings_manager.get("folder_format")
        file_tpl = await settings_manager.get("filename_format")

        tokens = {
            "{Year}": str(movie.year) if movie.year else "Unknown",
            "{Movie}": self.sanitize_name(movie.title),
            "{Artist}": self.sanitize_name(track.artist),
            "{Album}": self.sanitize_name(album.title),
            "{TrackNum}": f"{track.track_number:02d}",
            "{Title}": self.sanitize_name(track.title),
        }

        resolved_folder = folder_tpl
        resolved_file = file_tpl
        for k, v in tokens.items():
            resolved_folder = resolved_folder.replace(k, v)
            resolved_file = resolved_file.replace(k, v)

        parts = [self.sanitize_name(p) for p in resolved_folder.split("/") if p.strip()]
        target_dir = Path(output_dir) / Path(*parts)
        filename = f"{self.sanitize_name(resolved_file)}.{fmt.lower()}"
        return str(target_dir), str(target_dir / filename)

    async def write_movie_metadata(self, movie: Movie, target_dir: str) -> None:
        os.makedirs(target_dir, exist_ok=True)
        path = os.path.join(target_dir, "movie.json")
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "tmdb_id": movie.tmdb_id,
                        "title": movie.title,
                        "year": movie.year,
                        "overview": movie.overview,
                        "language": movie.language,
                        "genres": movie.genres,
                        "ott_providers": movie.ott_providers,
                        "exported_at": datetime.now().isoformat(),
                    },
                    f,
                    indent=4,
                )
        except Exception as e:
            logger.error(f"movie.json write failed: {e}")

    async def generate_m3u_playlist(self, target_dir: str, album_title: str) -> None:
        if not os.path.exists(target_dir):
            return
        files = sorted(
            f for f in os.listdir(target_dir) if f.lower().endswith((".mp3", ".flac"))
        )
        if not files:
            return
        try:
            with open(
                os.path.join(target_dir, "playlist.m3u"), "w", encoding="utf-8"
            ) as f:
                f.write(f"#EXTM3U\n#PLAYLIST:{album_title}\n\n")
                for name in files:
                    f.write(f"{name}\n")
        except Exception as e:
            logger.error(f"playlist.m3u failed: {e}")
```

---

### File: `services/MovieSongDownloader/services/soundtrack_service.py`
- **Path:** `services/MovieSongDownloader/services/soundtrack_service.py`
- **Estimated Tokens:** 1,599
- **mtime:** 1780861103.721

```python
import logging
from typing import List, Optional
from MovieSongDownloader.providers.jiosaavn_provider import JioSaavnProvider
from MovieSongDownloader.core.models import Album, Track
from MovieSongDownloader.providers.metadata_normalizer import normalize_title
from MovieSongDownloader.core.database import db

logger = logging.getLogger("MovieSongDownloader.SoundtrackService")


class SoundtrackService:
    def __init__(self, provider: Optional[JioSaavnProvider] = None):
        self.provider = provider or JioSaavnProvider()

    async def find_soundtracks(
        self,
        movie_title: str,
        movie_year: Optional[int] = None,
        movie_id: Optional[int] = None,
    ) -> List[Album]:
        """Search JioSaavn for soundtrack albums matching the movie, with DB cache support."""
        if movie_id:
            conn = await db.get_connection()
            db_albums = []
            try:
                async with conn.execute(
                    (
                        "SELECT id, movie_id, spotify_id, title, artist, cover_url, "
                        "cover_cached_path, total_tracks, source, source_id FROM albums "
                        "WHERE movie_id = ?"
                    ),
                    (movie_id,),
                ) as c:
                    rows = await c.fetchall()
                    for r in rows:
                        db_albums.append(
                            Album(
                                id=r[0],
                                movie_id=r[1],
                                spotify_id=r[2],
                                title=r[3],
                                artist=r[4],
                                cover_url=r[5],
                                cover_cached_path=r[6],
                                total_tracks=r[7],
                                source=r[8],
                                source_id=r[9],
                            )
                        )
            except Exception as e:
                logger.error(f"Error loading albums from DB: {e}")
            finally:
                await conn.close()
            if db_albums:
                logger.info(
                    f"Loaded {len(db_albums)} albums from local database cache for movie ID {movie_id}."
                )
                return db_albums

        if not movie_title:
            return []
        cleaned = normalize_title(movie_title)
        albums = await self.provider.get_soundtrack(cleaned, year=movie_year)
        if not albums and movie_year:
            # Retry without year filter
            albums = await self.provider.get_soundtrack(cleaned, year=None)
        return albums

    async def get_tracks_for_album(
        self, album_id: str, db_album_id: Optional[int] = None
    ) -> List[Track]:
        """Get all tracks for a JioSaavn or Spotify album, with DB cache support."""
        if db_album_id:
            conn = await db.get_connection()
            db_tracks = []
            try:
                async with conn.execute(
                    (
                        "SELECT id, album_id, spotify_id, title, artist, duration_ms, "
                        "track_number, preview_url, source, source_id, download_url "
                        "FROM tracks WHERE album_id = ?"
                    ),
                    (db_album_id,),
                ) as c:
                    rows = await c.fetchall()
                    for r in rows:
                        db_tracks.append(
                            Track(
                                id=r[0],
                                album_id=r[1],
                                spotify_id=r[2],
                                title=r[3],
                                artist=r[4],
                                duration_ms=r[5],
                                track_number=r[6],
                                preview_url=r[7],
                                source=r[8],
                                source_id=r[9],
                                download_url=r[10],
                            )
                        )
            except Exception as e:
                logger.error(f"Error loading tracks from DB: {e}")
            finally:
                await conn.close()
            if db_tracks:
                logger.info(
                    f"Loaded {len(db_tracks)} tracks from local database cache for album ID {db_album_id}."
                )
                return db_tracks

        if not album_id:
            return []

        # Check album source from DB if db_album_id is provided
        source = "jiosaavn"
        spotify_url = None
        if db_album_id:
            conn = await db.get_connection()
            try:
                async with conn.execute(
                    "SELECT source, source_id FROM albums WHERE id = ?", (db_album_id,)
                ) as c:
                    row = await c.fetchone()
                    if row:
                        source = row[0]
                        if source == "spotify":
                            spotify_url = row[1]
            except Exception as e:
                logger.error(f"Error checking album source: {e}")
            finally:
                await conn.close()

        # Route to SpotifyProvider if source is Spotify
        if source == "spotify" or "spotify.com" in album_id or len(album_id) == 22:
            from MovieSongDownloader.providers.spotify_provider import SpotifyProvider

            spotify_prov = SpotifyProvider()
            url_or_id = spotify_url or album_id
            try:
                _, _, tracks = await spotify_prov.get_spotify_album_or_track(url_or_id)
                return tracks
            except Exception as e:
                logger.error(f"Failed to fetch Spotify tracks for {url_or_id}: {e}")
                return []

        tracks = await self.provider.get_tracks(album_id)
        for t in tracks:
            t.title = normalize_title(t.title)
        return tracks

    async def get_album_details(self, album_id: str) -> Optional[Album]:
        """Get album metadata from JioSaavn."""
        return await self.provider.get_album_details(album_id)

    async def search_songs(self, query: str, limit: int = 10) -> List[Track]:
        """Direct song search on JioSaavn."""
        return await self.provider.search_songs(query, limit=limit)
```

---

### File: `services/MovieSongDownloader/services/watchlist_service.py`
- **Path:** `services/MovieSongDownloader/services/watchlist_service.py`
- **Estimated Tokens:** 1,862
- **mtime:** 1780861103.721

```python
import logging
from datetime import datetime
from typing import List
from MovieSongDownloader.core.database import db
from MovieSongDownloader.core.models import WatchlistItem, Movie, Album, Track
from MovieSongDownloader.providers.wikipedia_provider import WikipediaProvider
from MovieSongDownloader.services.soundtrack_service import SoundtrackService
from MovieSongDownloader.core.job_queue import job_queue

logger = logging.getLogger("MovieSongDownloader.WatchlistService")


class WatchlistService:
    def __init__(self, wiki=None, soundtrack=None):
        self.wiki = wiki or WikipediaProvider()
        self.soundtrack = soundtrack or SoundtrackService()

    async def add_to_watchlist(self, movie: Movie, auto_download: bool = True) -> int:
        conn = await db.get_connection()
        try:
            c = await conn.execute(
                (
                    "INSERT INTO watchlist (tmdb_id, source_id, title, expected_release, "
                    "auto_download, status, last_checked) "
                    "VALUES (?, ?, ?, ?, ?, 'watching', datetime('now'))"
                ),
                (
                    movie.tmdb_id,
                    movie.source_id,
                    movie.title,
                    movie.year,
                    1 if auto_download else 0,
                ),
            )
            await conn.commit()
            return c.lastrowid
        finally:
            await conn.close()

    async def get_watchlist(self) -> List[WatchlistItem]:
        conn = await db.get_connection()
        try:
            async with conn.execute(
                (
                    "SELECT id, tmdb_id, title, expected_release, last_checked, "
                    "auto_download, status, created_at FROM watchlist"
                )
            ) as c:
                return [
                    WatchlistItem(
                        id=r[0],
                        tmdb_id=r[1],
                        title=r[2],
                        expected_release=r[3],
                        last_checked=r[4],
                        auto_download=bool(r[5]),
                        status=r[6],
                        created_at=r[7],
                    )
                    for r in await c.fetchall()
                ]
        finally:
            await conn.close()

    async def check_releases_and_trigger(self) -> None:
        items = await self.get_watchlist()
        conn = await db.get_connection()
        try:
            for item in items:
                if item.status != "watching":
                    continue
                try:
                    results = await self.wiki.search(item.title)
                    target = next(
                        (m for m in results if m.title.lower() == item.title.lower()),
                        None,
                    )
                    if not target:
                        continue
                    await conn.execute(
                        "UPDATE watchlist SET last_checked=datetime('now') WHERE id=?",
                        (item.id,),
                    )
                    await conn.commit()
                    if target.year and target.year <= datetime.now().year:
                        status = "found"
                        if item.auto_download:
                            albums = await self.soundtrack.find_soundtracks(
                                item.title, movie_year=target.year
                            )
                            if albums:
                                best = albums[0]
                                tracks = await self.soundtrack.get_tracks_for_album(
                                    best.source_id
                                )
                                mid = await self._ensure_movie(conn, target)
                                aid = await self._ensure_album(conn, mid, best)
                                for t in tracks:
                                    tid = await self._ensure_track(conn, aid, t)
                                    await job_queue.enqueue(tid)
                                status = "downloaded"
                        await conn.execute(
                            "UPDATE watchlist SET status=? WHERE id=?",
                            (status, item.id),
                        )
                        await conn.commit()
                except Exception as e:
                    logger.error(f"Watchlist check error for {item.title}: {e}")
        finally:
            await conn.close()

    async def _ensure_movie(self, conn, m: Movie) -> int:
        async with conn.execute(
            "SELECT id FROM movies WHERE source_id=? AND source=?",
            (m.source_id, m.source),
        ) as c:
            r = await c.fetchone()
            if r:
                return r[0]
        # Fallback: check by title+year
        async with conn.execute(
            "SELECT id FROM movies WHERE title=? AND year=?", (m.title, m.year)
        ) as c:
            r = await c.fetchone()
            if r:
                return r[0]
        c = await conn.execute(
            (
                "INSERT INTO movies (tmdb_id, source, source_id, title, year, poster_url, "
                "overview, language, rating, cast_info) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)"
            ),
            (
                m.tmdb_id,
                m.source,
                m.source_id,
                m.title,
                m.year,
                m.poster_url,
                m.overview,
                m.language,
                m.rating,
                m.cast_info,
            ),
        )
        return c.lastrowid

    async def _ensure_album(self, conn, movie_id: int, a: Album) -> int:
        async with conn.execute(
            "SELECT id FROM albums WHERE source_id=? AND source=?",
            (a.source_id, a.source),
        ) as c:
            r = await c.fetchone()
            if r:
                return r[0]
        c = await conn.execute(
            (
                "INSERT INTO albums (movie_id, spotify_id, source, source_id, title, artist, "
                "cover_url, total_tracks) VALUES (?,?,?,?,?,?,?,?)"
            ),
            (
                movie_id,
                a.spotify_id,
                a.source,
                a.source_id,
                a.title,
                a.artist,
                a.cover_url,
                a.total_tracks,
            ),
        )
        return c.lastrowid

    async def _ensure_track(self, conn, album_id: int, t: Track) -> int:
        async with conn.execute(
            "SELECT id FROM tracks WHERE source_id=? AND source=?",
            (t.source_id, t.source),
        ) as c:
            r = await c.fetchone()
            if r:
                return r[0]
        c = await conn.execute(
            (
                "INSERT INTO tracks (album_id, spotify_id, source, source_id, title, artist, "
                "duration_ms, track_number, preview_url, download_url) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)"
            ),
            (
                album_id,
                t.spotify_id,
                t.source,
                t.source_id,
                t.title,
                t.artist,
                t.duration_ms,
                t.track_number,
                t.preview_url,
                t.download_url,
            ),
        )
        return c.lastrowid
```

---

### File: `services/MovieSongDownloader/settings_backup.json`
- **Path:** `services/MovieSongDownloader/settings_backup.json`
- **Estimated Tokens:** 17
- **mtime:** 1780590896.318

```json
{
    "last_fetch_date": "2000-01-01",
    "omdb_api_key": "test_key"
}
```

---

### File: `services/MovieSongDownloader/test_output/spotiflac_result_1nHTOlxSEyyrLH6wzzMJTd.mp3`
- **Path:** `services/MovieSongDownloader/test_output/spotiflac_result_1nHTOlxSEyyrLH6wzzMJTd.mp3`
- **Estimated Tokens:** 3
- **mtime:** 1781123079.716

```
mock final file
```

---

### File: `services/MovieSongDownloader/test_output/spotiflac_temp_1nHTOlxSEyyrLH6wzzMJTd/track1.flac`
- **Path:** `services/MovieSongDownloader/test_output/spotiflac_temp_1nHTOlxSEyyrLH6wzzMJTd/track1.flac`
- **Estimated Tokens:** 3
- **mtime:** 1781123079.711

```
mock audio data
```

---

### File: `services/MovieSongDownloader/test_output/spotiflac_temp_1nHTOlxSEyyrLH6wzzMJTd/transcoded.mp3`
- **Path:** `services/MovieSongDownloader/test_output/spotiflac_temp_1nHTOlxSEyyrLH6wzzMJTd/transcoded.mp3`
- **Estimated Tokens:** 5
- **mtime:** 1781123079.712

```
mock transcoded audio
```

---

### File: `services/MovieSongDownloader/tests/__init__.py`
- **Path:** `services/MovieSongDownloader/tests/__init__.py`
- **Estimated Tokens:** 3
- **mtime:** 1780474585.197

```python
# Tests Module
```

---

### File: `services/MovieSongDownloader/tests/conftest.py`
- **Path:** `services/MovieSongDownloader/tests/conftest.py`
- **Estimated Tokens:** 468
- **mtime:** 1781117033.179

```python
# ruff: noqa: E402
import os
import sys
import importlib
from importlib.abc import MetaPathFinder

# Add workspace root and services directory to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
services_dir = os.path.join(workspace_root, "services")

if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)
if services_dir not in sys.path:
    sys.path.insert(0, services_dir)

# Register Redirector so MovieSongDownloader -> movie_song_downloader works seamlessly
class MovieSongDownloaderRedirector(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname.startswith("MovieSongDownloader"):
            real_name = fullname.replace("MovieSongDownloader", "movie_song_downloader", 1)
            mod = importlib.import_module(real_name)
            sys.modules[fullname] = mod
            return mod.__spec__
        return None

# Only insert if not already present
if not any(isinstance(finder, MovieSongDownloaderRedirector) for finder in sys.meta_path):
    sys.meta_path.insert(0, MovieSongDownloaderRedirector())

import pytest
import MovieSongDownloader.config
from MovieSongDownloader.core.database import db


@pytest.fixture(scope="session", autouse=True)
def use_test_database(tmp_path_factory):
    # Redirect DATABASE_PATH to a temporary test database file
    test_db_dir = tmp_path_factory.mktemp("test_db_dir")
    test_db_path = test_db_dir / "test_db.sqlite3"

    # Patch the configuration path and the instantiated database manager path
    MovieSongDownloader.config.DATABASE_PATH = test_db_path
    db.db_path = test_db_path

    yield

    # Cleanup after the test session finishes
    if test_db_path.exists():
        try:
            os.remove(test_db_path)
        except Exception:
            pass
```

---

### File: `services/MovieSongDownloader/tests/test_cache.py`
- **Path:** `services/MovieSongDownloader/tests/test_cache.py`
- **Estimated Tokens:** 277
- **mtime:** 1780856038.263

```python
import pytest
from MovieSongDownloader.core.database import db
from MovieSongDownloader.core.cache_manager import download_cache, api_cache


@pytest.mark.asyncio
async def test_api_cache_operations():
    # Force initialization first
    await db.run_migrations()

    key = "test_spotify_endpoint"
    payload = {"data": [1, 2, 3]}

    # Check cache miss
    miss = await api_cache.get(key)
    assert miss is None

    # Save cache with 5 seconds expiry
    await api_cache.set(key, "spotify", payload, expires_in_seconds=5)

    # Check cache hit
    hit = await api_cache.get(key)
    assert hit == payload

    # Save cache with -1 seconds expiry (expired)
    await api_cache.set(key, "spotify", payload, expires_in_seconds=-1)

    # Check cache expired (should return None)
    expired = await api_cache.get(key)
    assert expired is None


@pytest.mark.asyncio
async def test_download_cache_hash():
    h1 = download_cache.generate_hash("Artist", "Song", "Album", 200000)
    h2 = download_cache.generate_hash("artist", "song", "album", 200000)

    # Check case-insensitivity
    assert h1 == h2
```

---

### File: `services/MovieSongDownloader/tests/test_cache_verification.py`
- **Path:** `services/MovieSongDownloader/tests/test_cache_verification.py`
- **Estimated Tokens:** 328
- **mtime:** 1780856038.264

```python
import pytest
from MovieSongDownloader.core.database import db
from MovieSongDownloader.core.cache_manager import api_cache


@pytest.mark.asyncio
async def test_cache_verification_logic():
    await db.run_migrations()

    # Mock DB cache clear
    conn = await db.get_connection()
    try:
        await conn.execute("DELETE FROM api_cache")
        await conn.commit()
    finally:
        await conn.close()

    cache_key = "test_verification_key"
    cached_data = {
        "id": "123",
        "title": "Old Title",
        "rating": "7.5",
        "cast": "Old Cast",
    }

    # Verify when cache is empty, returns new data directly
    result = await api_cache.verify_scraped_data(
        cache_key, cached_data, ["rating", "cast"]
    )
    assert result == cached_data

    # Set initial cache
    await api_cache.set(cache_key, "test", cached_data)

    new_data = {"id": "456", "title": "New Title", "rating": "8.5", "cast": "New Cast"}

    # Verify fields (volatile fields rating/cast are updated, but id/title are kept from cached_data)
    result = await api_cache.verify_scraped_data(
        cache_key, new_data, ["rating", "cast"]
    )
    assert result["id"] == "123"
    assert result["title"] == "Old Title"
    assert result["rating"] == "8.5"
    assert result["cast"] == "New Cast"
```

---

### File: `services/MovieSongDownloader/tests/test_event_bus.py`
- **Path:** `services/MovieSongDownloader/tests/test_event_bus.py`
- **Estimated Tokens:** 174
- **mtime:** 1780856038.272

```python
import pytest
from MovieSongDownloader.core.event_bus import EventBus, Event


@pytest.mark.asyncio
async def test_event_bus_pub_sub():
    bus = EventBus()
    received_data = []

    async def callback(event: Event):
        received_data.append(event.data)

    # Subscribe callback to event
    await bus.subscribe("test.event", callback)

    # Publish event
    await bus.publish(Event("test.event", {"val": 42}))

    assert len(received_data) == 1
    assert received_data[0]["val"] == 42

    # Unsubscribe
    await bus.unsubscribe("test.event", callback)
    await bus.publish(Event("test.event", {"val": 100}))

    # Received list should not change
    assert len(received_data) == 1
```

---

### File: `services/MovieSongDownloader/tests/test_folder_service.py`
- **Path:** `services/MovieSongDownloader/tests/test_folder_service.py`
- **Estimated Tokens:** 375
- **mtime:** 1780856038.29

```python
import pytest
from MovieSongDownloader.services.folder_service import FolderService
from MovieSongDownloader.core.models import Movie, Album, Track


def test_sanitize_name():
    # Remove Windows invalid characters
    assert (
        FolderService.sanitize_name("Leo: Naan Ready? *FLAC*")
        == "Leo- Naan Ready- -FLAC-"
    )
    assert FolderService.sanitize_name("Artist / Title") == "Artist - Title"
    assert FolderService.sanitize_name("") == "Unknown"


@pytest.mark.asyncio
async def test_target_path_generation(monkeypatch):
    service = FolderService()

    # Mock settings manager keys
    from MovieSongDownloader.core.settings_manager import settings_manager

    async def mock_get(key):
        if key == "output_dir":
            return "C:/Downloads"
        elif key == "folder_format":
            return "{Year}/{Movie}/Songs"
        elif key == "filename_format":
            return "{TrackNum} - {Title}"
        return ""

    monkeypatch.setattr(settings_manager, "get", mock_get)

    movie = Movie(title="Inception", year=2010)
    album = Album(title="Inception OST")
    track = Track(title="Time", track_number=5, artist="Hans Zimmer")

    target_dir, file_path = await service.get_target_path(movie, album, track, "mp3")

    # Verify proper replacements and path construction
    assert (
        "C:\\Downloads\\2010\\Inception\\Songs" in target_dir
        or "C:/Downloads/2010/Inception/Songs" in target_dir
    )
    assert "05 - Time.mp3" in file_path
```

---

### File: `services/MovieSongDownloader/tests/test_jiosaavn_provider.py`
- **Path:** `services/MovieSongDownloader/tests/test_jiosaavn_provider.py`
- **Estimated Tokens:** 666
- **mtime:** 1780856038.293

```python
import pytest
from unittest.mock import patch
from MovieSongDownloader.core.database import db
from MovieSongDownloader.providers.jiosaavn_provider import JioSaavnProvider


@pytest.mark.asyncio
async def test_jiosaavn_search_album():
    await db.run_migrations()

    # Mock DB cache clear
    conn = await db.get_connection()
    try:
        await conn.execute("DELETE FROM api_cache")
        await conn.commit()
    finally:
        await conn.close()

    provider = JioSaavnProvider()

    # Mock the JioSaavn SDK's search_albums call
    mock_albums = [
        {
            "album_id": "alb_123",
            "title": "Vikram",
            "artists": "Anirudh Ravichander",
            "track_count": 5,
            "thumbnails": {"quality": {"500x500": "https://images.xyz/vikram_500.jpg"}},
        }
    ]

    with patch.object(
        provider._client, "search_albums", return_value=mock_albums
    ) as mock_search:
        albums = await provider.get_soundtrack("Vikram", 2022)
        assert len(albums) == 1
        assert albums[0].source == "jiosaavn"
        assert albums[0].source_id == "alb_123"
        assert albums[0].title == "Vikram"
        assert albums[0].artist == "Anirudh Ravichander"
        assert albums[0].cover_url == "https://images.xyz/vikram_500.jpg"
        mock_search.assert_called_once_with("Vikram 2022", limit=8)


@pytest.mark.asyncio
async def test_jiosaavn_get_tracks():
    await db.run_migrations()
    provider = JioSaavnProvider()

    # Mock the JioSaavn SDK's album_info call
    mock_info = {
        "album_id": "alb_123",
        "title": "Vikram",
        "tracks": [
            {
                "track_id": "trk_999",
                "title": "Pathala Pathala",
                "primary_artists": "Anirudh Ravichander, Kamal Haasan",
                "duration": 210,
                "stream_urls": {
                    "very_high_quality": "https://stream.xyz/pathala_320.mp3",
                    "low_quality": "https://stream.xyz/pathala_96.mp3",
                },
            }
        ],
    }

    with patch.object(
        provider._client, "album_info", return_value=mock_info
    ) as mock_info_call:
        tracks = await provider.get_tracks("alb_123")
        assert len(tracks) == 1
        assert tracks[0].source == "jiosaavn"
        assert tracks[0].source_id == "trk_999"
        assert tracks[0].title == "Pathala Pathala"
        assert tracks[0].artist == "Anirudh Ravichander, Kamal Haasan"
        assert tracks[0].duration_ms == 210000
        assert tracks[0].download_url == "https://stream.xyz/pathala_320.mp3"
        mock_info_call.assert_called_once_with("alb_123")
```

---

### File: `services/MovieSongDownloader/tests/test_job_queue.py`
- **Path:** `services/MovieSongDownloader/tests/test_job_queue.py`
- **Estimated Tokens:** 453
- **mtime:** 1780861886.644

```python
import pytest
from MovieSongDownloader.core.database import db
from MovieSongDownloader.core.job_queue import job_queue


@pytest.mark.asyncio
async def test_job_queue_state_transitions():
    await db.run_migrations()

    conn = await db.get_connection()
    try:
        # Seed a dummy movie, album, and track to satisfy foreign keys
        await conn.execute(
            (
                "INSERT OR REPLACE INTO movies (id, tmdb_id, title) "
                "VALUES (99, 999, 'Test Movie')"
            )
        )
        await conn.execute(
            (
                "INSERT OR REPLACE INTO albums (id, movie_id, spotify_id, title) "
                "VALUES (99, 99, 'album_99', 'Test Album')"
            )
        )
        await conn.execute(
            (
                "INSERT OR REPLACE INTO tracks (id, album_id, spotify_id, title, track_number) "
                "VALUES (99, 99, 'track_99', 'Test Track', 1)"
            )
        )
        await conn.commit()
    finally:
        await conn.close()

    # Enqueue a job
    job_id = await job_queue.enqueue(track_id=99, format="mp3")
    assert job_id > 0

    # Dequeue the job
    job = await job_queue.dequeue()
    assert job is not None
    assert job.id == job_id
    assert job.status == "queued"

    # Update progress
    await job_queue.update_progress(job_id, 45.0, "downloading")

    # Verify status changed
    jobs = await job_queue.get_all_jobs()
    active_job = [j for j in jobs if j.id == job_id][0]
    assert active_job.status == "downloading"
    assert active_job.progress == 45.0

    # Cancel job
    await job_queue.cancel(job_id)

    # Verify status is cancelled
    jobs = await job_queue.get_all_jobs()
    cancelled_job = [j for j in jobs if j.id == job_id][0]
    assert cancelled_job.status == "cancelled"
```

---

### File: `services/MovieSongDownloader/tests/test_lyrics_waterfall.py`
- **Path:** `services/MovieSongDownloader/tests/test_lyrics_waterfall.py`
- **Estimated Tokens:** 430
- **mtime:** 1780856038.303

```python
import pytest
import asyncio
from MovieSongDownloader.providers.lyrics_provider import LyricsProvider


def test_lyrics_sync_detection():
    provider = LyricsProvider()

    synced_text = (
        "[00:12.34] Synced line one\n"
        "[00:15.50] Synced line two\n"
        "[00:19.00] Synced line three\n"
    )

    plain_text = "This is line one\nThis is line two\nThis is line three\n"

    # Check regex sync detection
    assert provider._is_synced(synced_text) is True
    assert provider._is_synced(plain_text) is False
    assert provider._is_synced("") is False


@pytest.mark.asyncio
async def test_waterfall_priority_fallback(monkeypatch):
    provider = LyricsProvider()

    # Mock settings manager keys
    from MovieSongDownloader.core.settings_manager import settings_manager

    async def mock_get(key):
        return '["lrclib", "genius"]'  # Custom waterfall subset

    monkeypatch.setattr(settings_manager, "get", mock_get)

    calls = []

    # Mock thread executor helper _sync_search_task
    async def mock_thread(func, *args):
        # args[0] is search_query, args[1] is provider
        provider_name = args[1]
        calls.append(provider_name)
        if provider_name == "lrclib":
            return None  # Simulate miss
        elif provider_name == "genius":
            return "Genius plain text lyrics content"  # Simulate hit
        return None

    monkeypatch.setattr(asyncio, "to_thread", mock_thread)

    lyrics, lyrics_type = await provider.fetch("Title", "Artist")

    # Verify both providers were queried in sequence
    assert "lrclib" in calls
    assert "genius" in calls
    assert lyrics == "Genius plain text lyrics content"
    assert lyrics_type == "plain"
```

---

### File: `services/MovieSongDownloader/tests/test_movie_service.py`
- **Path:** `services/MovieSongDownloader/tests/test_movie_service.py`
- **Estimated Tokens:** 1,105
- **mtime:** 1780856038.309

```python
import pytest
import datetime
from unittest.mock import AsyncMock, MagicMock
from MovieSongDownloader.core.database import db
from MovieSongDownloader.core.models import Movie
from MovieSongDownloader.core.settings_manager import settings_manager
from MovieSongDownloader.services.movie_service import MovieService


@pytest.mark.asyncio
async def test_get_today_releases_fresh_fetch():
    # Arrange: Ensure migrations are run and settings/movies are clean
    await db.run_migrations()

    conn = await db.get_connection()
    try:
        await conn.execute("DELETE FROM settings")
        await conn.execute("DELETE FROM movies")
        await conn.commit()
    finally:
        await conn.close()

    await settings_manager.set("last_fetch_date", "2000-01-01")  # Outdated date
    await settings_manager.set(
        "scraping_limit", "0"
    )  # Avoid OMDb enrichment calls for stubs in this test

    mock_movie = Movie(
        tmdb_id=123,
        source="wikipedia",
        source_id="p123",
        title="Test Movie 2026",
        year=datetime.date.today().year,
        poster_url="http://example.com/poster.jpg",
    )

    wiki_mock = MagicMock()
    wiki_mock.get_today_releases = AsyncMock(return_value=[mock_movie])

    service = MovieService(wiki_provider=wiki_mock)

    # Act
    movies = await service.get_today_releases("IN")

    # Assert
    assert len(movies) == 1
    assert movies[0].title == "Test Movie 2026"
    wiki_mock.get_today_releases.assert_called_once_with(region="IN")

    # Check that settings updated the date
    saved_date = await settings_manager.get("last_fetch_date")
    assert saved_date == datetime.date.today().isoformat()


@pytest.mark.asyncio
async def test_get_today_releases_from_cache():
    # Arrange: Populate DB and update last_fetch_date to today
    await db.run_migrations()

    conn = await db.get_connection()
    try:
        await conn.execute("DELETE FROM settings")
        await conn.execute("DELETE FROM movies")
        await conn.commit()
    finally:
        await conn.close()

    current_year = datetime.date.today().year
    current_date_str = datetime.date.today().isoformat()
    await settings_manager.set("last_fetch_date", current_date_str)

    # Seed a cached movie
    service = MovieService()
    cached_movie = Movie(
        tmdb_id=456,
        source="wikipedia",
        source_id="p456",
        title="Cached Movie 2026",
        year=current_year,
        poster_url="http://example.com/cached.jpg",
        release_date=current_date_str,
    )
    await service._db_save_movie_album_tracks(cached_movie, None, [])

    wiki_mock = MagicMock()
    wiki_mock.get_today_releases = AsyncMock()

    service_with_mock = MovieService(wiki_provider=wiki_mock)

    # Act
    movies = await service_with_mock.get_today_releases("IN")

    # Assert: Should load directly from DB cache, meaning wiki_provider is not called
    assert len(movies) == 1
    assert movies[0].title == "Cached Movie 2026"
    wiki_mock.get_today_releases.assert_not_called()


@pytest.mark.asyncio
async def test_get_today_releases_fallback_on_failure():
    # Arrange: Populate DB but set last_fetch_date to outdated
    await db.run_migrations()

    conn = await db.get_connection()
    try:
        await conn.execute("DELETE FROM settings")
        await conn.execute("DELETE FROM movies")
        await conn.commit()
    finally:
        await conn.close()

    current_year = datetime.date.today().year
    await settings_manager.set("last_fetch_date", "2000-01-01")

    # Seed older cached movie
    service = MovieService()
    cached_movie = Movie(
        tmdb_id=789,
        source="wikipedia",
        source_id="p789",
        title="Fallback Movie 2026",
        year=current_year,
        poster_url="http://example.com/fallback.jpg",
        release_date="2026-01-01",
    )
    await service._db_save_movie_album_tracks(cached_movie, None, [])

    # Mock wiki provider to raise an exception
    wiki_mock = MagicMock()
    wiki_mock.get_today_releases = AsyncMock(side_effect=Exception("Network error"))

    service_with_mock = MovieService(wiki_provider=wiki_mock)

    # Act
    movies = await service_with_mock.get_today_releases("IN")

    # Assert: Should gracefully fallback to DB cache
    assert len(movies) == 1
    assert movies[0].title == "Fallback Movie 2026"
    wiki_mock.get_today_releases.assert_called_once()
```

---

### File: `services/MovieSongDownloader/tests/test_musicbrainz_provider.py`
- **Path:** `services/MovieSongDownloader/tests/test_musicbrainz_provider.py`
- **Estimated Tokens:** 524
- **mtime:** 1780856038.31

```python
import pytest
from unittest.mock import patch
from MovieSongDownloader.providers.musicbrainz_provider import MusicBrainzProvider
from MovieSongDownloader.core.models import Album, Track
from MovieSongDownloader.core.database import db


@pytest.mark.asyncio
async def test_musicbrainz_enrich_album():
    await db.run_migrations()
    provider = MusicBrainzProvider()

    # Mock album and tracks
    album = Album(title="Vikram", artist="Anirudh Ravichander")
    tracks = [Track(title="Pathala Pathala"), Track(title="Wasted")]

    # Mock search response
    mock_search = {
        "release-groups": [
            {
                "id": "rg_123",
                "title": "Vikram",
                "artist-credit": [{"artist": {"name": "Anirudh Ravichander"}}],
            }
        ]
    }

    # Mock browse response containing tracks and ISRCs
    mock_browse = {
        "releases": [
            {
                "title": "Vikram",
                "id": "rel_456",
                "media": [
                    {
                        "tracks": [
                            {
                                "title": "Pathala Pathala",
                                "recording": {"isrcs": ["IN-A23-22-00001"]},
                            },
                            {
                                "title": "Wasted",
                                "recording": {"isrcs": ["IN-A23-22-00002"]},
                            },
                        ]
                    }
                ],
            }
        ]
    }

    async def mock_mb_req_handler(url, params):
        if "release-group" in url:
            return mock_search
        elif "release" in url:
            return mock_browse
        return None

    with patch.object(provider, "_mb_request", side_effect=mock_mb_req_handler):
        composer, isrc_map = await provider.enrich_album(album, tracks)
        assert composer == "Anirudh Ravichander"
        assert len(isrc_map) == 2
        assert isrc_map["Pathala Pathala"] == "IN-A23-22-00001"
        assert isrc_map["Wasted"] == "IN-A23-22-00002"
```

---

### File: `services/MovieSongDownloader/tests/test_normalizer.py`
- **Path:** `services/MovieSongDownloader/tests/test_normalizer.py`
- **Estimated Tokens:** 513
- **mtime:** 1780856038.315

```python
from MovieSongDownloader.providers.metadata_normalizer import (
    normalize_title,
    confidence_score,
)


def test_normalize_title():
    # Suffixes should be stripped
    assert normalize_title("Naan Ready (From Leo)") == "Naan Ready"
    assert (
        normalize_title("Inception (Original Motion Picture Soundtrack)") == "Inception"
    )
    assert normalize_title("Song Title (Official Audio)") == "Song Title"
    assert normalize_title("Remastered Track (Remastered 2020)") == "Remastered Track"
    assert normalize_title("Featured Track (feat. Artist Name)") == "Featured Track"

    # Normal title should remain untouched
    assert normalize_title("Stay") == "Stay"


def test_confidence_score_exact():
    source = {
        "title": "Leo Naan Ready",
        "artist": "Anirudh",
        "album": "Leo",
        "duration_ms": 240000,
    }
    target = {
        "title": "Leo Naan Ready",
        "artist": "Anirudh",
        "album": "Leo",
        "duration_ms": 240000,
    }
    # Exact match should score high
    score = confidence_score(source, target)
    assert score == 100


def test_confidence_score_close():
    source = {
        "title": "Naan Ready (From Leo)",
        "artist": "Anirudh Ravichander",
        "album": "Leo",
        "duration_ms": 241000,
    }
    target = {
        "title": "Naan Ready",
        "artist": "Anirudh",
        "album": "Leo",
        "duration_ms": 240000,
    }
    # Close match with cleanable suffix, close artist string, and minor duration delta (1s) should score >= 80
    score = confidence_score(source, target)
    assert score >= 80


def test_confidence_score_different():
    source = {
        "title": "Different Song",
        "artist": "Anirudh",
        "album": "Leo",
        "duration_ms": 180000,
    }
    target = {
        "title": "Naan Ready",
        "artist": "Anirudh",
        "album": "Leo",
        "duration_ms": 240000,
    }
    # Completely different tracks should score low
    score = confidence_score(source, target)
    assert score < 60
```

---

### File: `services/MovieSongDownloader/tests/test_omdb_provider.py`
- **Path:** `services/MovieSongDownloader/tests/test_omdb_provider.py`
- **Estimated Tokens:** 583
- **mtime:** 1780856038.319

```python
import pytest
from unittest.mock import patch, MagicMock
from MovieSongDownloader.core.database import db
from MovieSongDownloader.core.settings_manager import settings_manager
from MovieSongDownloader.core.models import Movie
from MovieSongDownloader.providers.omdb_provider import OMDbProvider


@pytest.mark.asyncio
async def test_omdb_enrich_movie():
    await db.run_migrations()

    # Seed API key setting
    await settings_manager.set("omdb_api_key", "test_key")

    # Mock DB cache clear
    conn = await db.get_connection()
    try:
        await conn.execute("DELETE FROM api_cache")
        await conn.commit()
    finally:
        await conn.close()

    provider = OMDbProvider()

    # Un-enriched movie with empty source_id (should be enriched with imdbID)
    movie = Movie(source="wikipedia", source_id="", title="Vikram", year=2022)

    mock_omdb_resp = {
        "Response": "True",
        "Title": "Vikram",
        "Year": "2022",
        "imdbID": "tt1234567",
        "imdbRating": "8.3",
        "Actors": "Kamal Haasan, Vijay Sethupathi, Fahadh Faasil",
        "Plot": "A special agent investigates a case of serial killings...",
        "Genre": "Action, Thriller",
        "Language": "Tamil",
        "Poster": "https://image.xyz/poster.jpg",
    }

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_omdb_resp

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        enriched = await provider.enrich_movie(movie)
        assert enriched.rating == "8.3"
        assert enriched.cast_info == "Kamal Haasan, Vijay Sethupathi, Fahadh Faasil"
        assert enriched.poster_url == "https://image.xyz/poster.jpg"
        assert "special agent" in enriched.overview
        assert "Action" in enriched.genres
        assert enriched.language == "Tamil"
        # Since source_id was empty, it should be set to imdbID
        assert enriched.source_id == "tt1234567"

    # Test that pre-populated source_id is not overwritten
    movie_with_id = Movie(
        source="wikipedia", source_id="12345", title="Vikram", year=2022
    )
    with patch("httpx.AsyncClient.get", return_value=mock_response):
        enriched_with_id = await provider.enrich_movie(movie_with_id)
        assert enriched_with_id.source_id == "12345"
```

---

### File: `services/MovieSongDownloader/tests/test_spotiflac_provider.py`
- **Path:** `services/MovieSongDownloader/tests/test_spotiflac_provider.py`
- **Estimated Tokens:** 744
- **mtime:** 1780856316.158

```python
import pytest
import os
from unittest.mock import patch, MagicMock, AsyncMock
from MovieSongDownloader.core.models import Track
from MovieSongDownloader.providers.spotiflac_provider import SpotiFLACProvider


@pytest.mark.asyncio
async def test_resolve_spotify_url():
    provider = SpotiFLACProvider()

    # Mock DDG HTML response containing track url
    mock_html = '<html><body><a href="https://open.spotify.com/track/1nHTOlxSEyyrLH6wzzMJTd">Link</a></body></html>'
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = mock_html

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        url = await provider._resolve_spotify_url("Armageddon", "A.R. Rahman")
        assert url == "https://open.spotify.com/track/1nHTOlxSEyyrLH6wzzMJTd"


@pytest.mark.asyncio
async def test_spotiflac_download():
    provider = SpotiFLACProvider()

    track = Track(
        source="spotify",
        source_id="1nHTOlxSEyyrLH6wzzMJTd",
        title="Armageddon",
        artist="A.R. Rahman",
        track_number=1,
    )

    # Mock settings_manager.get
    async def mock_settings_get(key):
        if key == "deezer_arl":
            return "test_arl"
        return None

    # Mock subprocess execution
    mock_process = AsyncMock()
    mock_process.returncode = 0
    mock_process.communicate.return_value = (b"Downloaded successfully", b"")

    # Mock os.walk and file creation
    temp_file_created = None

    def mock_walk(top, topdown=True, onerror=None, followlinks=False):
        nonlocal temp_file_created
        # Create a mock file in the temp subfolder to simulate download
        # Top is output_dir/spotiflac_temp_1nHTOlxSEyyrLH6wzzMJTd
        temp_file_created = os.path.join(top, "track1.flac")
        os.makedirs(top, exist_ok=True)
        with open(temp_file_created, "w") as f:
            f.write("mock audio data")
        return [(top, [], ["track1.flac"])]

    # Mock _transcode_audio to avoid actual ffmpeg running
    async def mock_transcode(input_path, output_path, format_str, bitrate):
        with open(output_path, "w") as f:
            f.write("mock transcoded audio")

    # Mock shutil.move
    def mock_move(src, dst):
        with open(dst, "w") as f:
            f.write("mock final file")

    with (
        patch(
            "MovieSongDownloader.providers.spotiflac_provider.settings_manager.get",
            side_effect=mock_settings_get,
        ),
        patch("asyncio.create_subprocess_exec", return_value=mock_process),
        patch("os.walk", side_effect=mock_walk),
        patch.object(provider, "_transcode_audio", side_effect=mock_transcode),
        patch("shutil.move", side_effect=mock_move),
        patch("shutil.rmtree"),
    ):
        result_path = await provider.download(
            track=track, format="mp3", output_dir="./test_output", filename_template=""
        )

        assert "spotiflac_result_1nHTOlxSEyyrLH6wzzMJTd.mp3" in result_path
```

---

### File: `services/MovieSongDownloader/tests/test_spotify_provider.py`
- **Path:** `services/MovieSongDownloader/tests/test_spotify_provider.py`
- **Estimated Tokens:** 1,301
- **mtime:** 1780861886.644

```python
import pytest
import json
from unittest.mock import patch, MagicMock
from MovieSongDownloader.providers.spotify_provider import SpotifyProvider


@pytest.mark.asyncio
async def test_get_spotify_album():
    provider = SpotifyProvider()

    # Mock embed page HTML response for album
    mock_entity = {
        "type": "album",
        "title": "Ponniyin Selvan - Original Score",
        "subtitle": "A.R. Rahman",
        "id": "7y3bI6blXr4I8l4kKGcBfE",
        "visualIdentity": {
            "image": [
                {
                    "url": "https://image.xyz/cover_small.jpg",
                    "maxHeight": 300,
                    "maxWidth": 300,
                },
                {
                    "url": "https://image.xyz/cover_large.jpg",
                    "maxHeight": 640,
                    "maxWidth": 640,
                },
            ]
        },
        "trackList": [
            {
                "uri": "spotify:track:1nHTOlxSEyyrLH6wzzMJTd",
                "title": "Armageddon",
                "subtitle": "A.R. Rahman",
                "duration": 269000,
                "audioPreview": {"url": "https://preview.xyz/track1.mp3"},
            },
            {
                "uri": "spotify:track:2nHTOlxSEyyrLH6wzzMJTz",
                "title": "Solaikuyil",
                "subtitle": "A.R. Rahman, Shreya Ghoshal",
                "duration": 310000,
                "audioPreview": None,
            },
        ],
    }

    mock_state_data = {
        "props": {"pageProps": {"state": {"data": {"entity": mock_entity}}}}
    }

    mock_html = (
        '<html><body><script id="__NEXT_DATA__" type="application/json">'
        + json.dumps(mock_state_data)
        + "</script></body></html>"
    )

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = mock_html

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        movie, album, tracks = await provider.get_spotify_album_or_track(
            "https://open.spotify.com/album/7y3bI6blXr4I8l4kKGcBfE"
        )

        # Verify Movie
        assert movie.source == "spotify"
        assert movie.source_id == "7y3bI6blXr4I8l4kKGcBfE"
        assert movie.title == "Ponniyin Selvan - Original Score"
        assert movie.poster_url == "https://image.xyz/cover_large.jpg"

        # Verify Album
        assert album.source == "spotify"
        assert album.source_id == "7y3bI6blXr4I8l4kKGcBfE"
        assert album.title == "Ponniyin Selvan - Original Score"
        assert album.artist == "A.R. Rahman"
        assert album.cover_url == "https://image.xyz/cover_large.jpg"
        assert album.total_tracks == 2

        # Verify Tracks
        assert len(tracks) == 2
        assert tracks[0].title == "Armageddon"
        assert tracks[0].artist == "A.R. Rahman"
        assert tracks[0].source_id == "1nHTOlxSEyyrLH6wzzMJTd"
        assert tracks[0].duration_ms == 269000
        assert tracks[0].track_number == 1
        assert tracks[0].preview_url == "https://preview.xyz/track1.mp3"

        assert tracks[1].title == "Solaikuyil"
        assert tracks[1].artist == "A.R. Rahman, Shreya Ghoshal"
        assert tracks[1].source_id == "2nHTOlxSEyyrLH6wzzMJTz"
        assert tracks[1].track_number == 2
        assert tracks[1].preview_url is None


@pytest.mark.asyncio
async def test_get_spotify_track():
    provider = SpotifyProvider()

    # Mock embed page HTML response for track
    mock_entity = {
        "type": "track",
        "title": "Armageddon",
        "name": "Armageddon",
        "id": "1nHTOlxSEyyrLH6wzzMJTd",
        "artists": [{"name": "A.R. Rahman"}],
        "duration": 269000,
        "visualIdentity": {
            "image": [
                {
                    "url": "https://image.xyz/track_large.jpg",
                    "maxHeight": 640,
                    "maxWidth": 640,
                }
            ]
        },
        "audioPreview": {"url": "https://preview.xyz/track1.mp3"},
    }

    mock_state_data = {
        "props": {"pageProps": {"state": {"data": {"entity": mock_entity}}}}
    }

    mock_html = (
        '<html><body><script id="__NEXT_DATA__" type="application/json">'
        + json.dumps(mock_state_data)
        + "</script></body></html>"
    )

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = mock_html

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        movie, album, tracks = await provider.get_spotify_album_or_track(
            "https://open.spotify.com/track/1nHTOlxSEyyrLH6wzzMJTd"
        )

        # Verify single wrapped track
        assert movie.title == "Armageddon"
        assert movie.poster_url == "https://image.xyz/track_large.jpg"

        assert album.title == "Armageddon"
        assert album.artist == "A.R. Rahman"
        assert album.total_tracks == 1

        assert len(tracks) == 1
        assert tracks[0].title == "Armageddon"
        assert tracks[0].artist == "A.R. Rahman"
        assert tracks[0].source_id == "1nHTOlxSEyyrLH6wzzMJTd"
        assert tracks[0].track_number == 1
        assert tracks[0].preview_url == "https://preview.xyz/track1.mp3"
```

---

### File: `services/MovieSongDownloader/tests/test_wikidata_provider.py`
- **Path:** `services/MovieSongDownloader/tests/test_wikidata_provider.py`
- **Estimated Tokens:** 284
- **mtime:** 1780856038.338

```python
import pytest
from unittest.mock import patch
from MovieSongDownloader.providers.wikidata_provider import WikidataProvider
from MovieSongDownloader.core.database import db


@pytest.mark.asyncio
async def test_wikidata_get_posters_batch():
    await db.run_migrations()
    provider = WikidataProvider()

    # Mock response from Wikidata wbgetentities API
    mock_response = {
        "entities": {
            "Q102147287": {
                "sitelinks": {"enwiki": {"title": "Vikram (2022 film)"}},
                "claims": {
                    "P18": [{"mainsnak": {"datavalue": {"value": "Vikram_poster.jpg"}}}]
                },
            }
        }
    }

    with patch.object(
        provider, "_wikidata_request", return_value=mock_response
    ) as mock_req:
        results = await provider.get_posters_batch(["Vikram (2022 film)"], lang="en")
        assert len(results) == 1
        assert "Vikram (2022 film)" in results
        assert (
            results["Vikram (2022 film)"]
            == "https://commons.wikimedia.org/wiki/Special:FilePath/Vikram_poster.jpg"
        )
        mock_req.assert_called_once()
```

---

### File: `services/MovieSongDownloader/tests/test_wikipedia_provider.py`
- **Path:** `services/MovieSongDownloader/tests/test_wikipedia_provider.py`
- **Estimated Tokens:** 596
- **mtime:** 1780861886.648

```python
import pytest
from unittest.mock import patch, MagicMock
from MovieSongDownloader.core.database import db
from MovieSongDownloader.providers.wikipedia_provider import WikipediaProvider


@pytest.mark.asyncio
async def test_wikipedia_search():
    await db.run_migrations()

    # Mock DB cache clear
    conn = await db.get_connection()
    try:
        await conn.execute("DELETE FROM api_cache")
        await conn.commit()
    finally:
        await conn.close()

    provider = WikipediaProvider()

    mock_search_resp = {
        "query": {
            "search": [
                {
                    "title": "Vikram (2022 film)",
                    "snippet": (
                        "Vikram is a 2022 Indian Tamil-language action thriller film "
                        "directed by Lokesh Kanagaraj..."
                    ),
                    "pageid": 12345,
                }
            ]
        }
    }

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_search_resp

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        results = await provider.search("Vikram", year=2022)
        assert len(results) > 0
        assert results[0].title == "Vikram"
        assert results[0].year == 2022
        assert results[0].source == "wikipedia"
        assert results[0].source_id == "12345"


@pytest.mark.asyncio
async def test_wikipedia_get_details():
    await db.run_migrations()
    provider = WikipediaProvider()

    mock_details_resp = {
        "query": {
            "pages": {
                "12345": {
                    "title": "Vikram (2022 film)",
                    "thumbnail": {"source": "https://image.xyz/vikram.jpg"},
                    "extract": (
                        "Vikram is a 2022 action thriller..."
                    ),
                }
            }
        }
    }

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_details_resp

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        movie = await provider.get_movie_details("12345")
        assert movie is not None
        assert movie.title == "Vikram"
        assert movie.year == 2022
        assert movie.poster_url == "https://image.xyz/vikram.jpg"
        assert "action thriller" in movie.overview
```

---

### File: `services/MovieSongDownloader/ui/__init__.py`
- **Path:** `services/MovieSongDownloader/ui/__init__.py`
- **Estimated Tokens:** 202
- **mtime:** 1780856038.251

```python
# UI Module
import os


def resolve_image_src(
    cached_path: str | None, remote_url: str | None, fallback: str = ""
) -> str:
    """Resolve the best image source for display.

    In web mode (FLET_WEB_PORT set), file:// URIs are blocked by browsers.
    Always prefer remote HTTP URLs. Only use local paths in desktop mode.
    """
    is_web_mode = bool(os.environ.get("FLET_WEB_PORT"))

    if is_web_mode:
        # Web mode: remote URL always wins, local paths won't render
        if remote_url:
            return remote_url
        return fallback

    # Desktop mode: prefer cached local file for speed
    if cached_path and os.path.exists(cached_path):
        from pathlib import Path

        return Path(cached_path).as_uri()

    if remote_url:
        return remote_url

    return fallback
```

---

### File: `services/MovieSongDownloader/ui/components/__init__.py`
- **Path:** `services/MovieSongDownloader/ui/components/__init__.py`
- **Estimated Tokens:** 5
- **mtime:** 1780474583.175

```python
# UI Components Module
```

---

### File: `services/MovieSongDownloader/ui/downloads.py`
- **Path:** `services/MovieSongDownloader/ui/downloads.py`
- **Estimated Tokens:** 2,230
- **mtime:** 1780926927.948

```python
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
```

---

### File: `services/MovieSongDownloader/ui/home.py`
- **Path:** `services/MovieSongDownloader/ui/home.py`
- **Estimated Tokens:** 2,200
- **mtime:** 1780928588.346

```python
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

```

---

### File: `services/MovieSongDownloader/ui/search.py`
- **Path:** `services/MovieSongDownloader/ui/search.py`
- **Estimated Tokens:** 1,454
- **mtime:** 1780856038.293

```python
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
```

---

### File: `services/MovieSongDownloader/ui/settings.py`
- **Path:** `services/MovieSongDownloader/ui/settings.py`
- **Estimated Tokens:** 3,355
- **mtime:** 1780861886.635

```python
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
```

---

### File: `services/MovieSongDownloader/ui/songs.py`
- **Path:** `services/MovieSongDownloader/ui/songs.py`
- **Estimated Tokens:** 3,354
- **mtime:** 1780856038.291

```python
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
```

---

### File: `services/MovieSongDownloader/ui/style.py`
- **Path:** `services/MovieSongDownloader/ui/style.py`
- **Estimated Tokens:** 417
- **mtime:** 1780926395.987

```python
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
```

---

### File: `services/aerohub_core/aerohub_config.json`
- **Path:** `services/aerohub_core/aerohub_config.json`
- **Estimated Tokens:** 450
- **mtime:** 1781116305.142

```json
{
  "auto_start": true,
  "restart_delay_sec": 5,
  "processes": [
    {
      "id": "clipboard_manager",
      "name": "Clipboard Manager",
      "icon": "\ud83d\udccb",
      "script": "services/clipboard_manager/clipboard_manager.py",
      "auto_start": true,
      "enabled": true
    },
    {
      "id": "health_app",
      "name": "Health App",
      "icon": "\ud83d\udc41\ufe0f",
      "script": "services/health_app/health_app.py",
      "auto_start": true,
      "enabled": true
    },
    {
      "id": "media_control",
      "name": "Media Control",
      "icon": "\ud83c\udfb5",
      "script": "services/media_control/media_control.py",
      "auto_start": true,
      "enabled": true
    },
    {
      "id": "battery_monitor",
      "name": "Battery Monitor",
      "icon": "\ud83d\udd0b",
      "script": "toggles/battery_monitor/battery_monitor.py",
      "auto_start": true,
      "enabled": true
    },
    {
      "id": "temp_monitor",
      "name": "Temp Monitor",
      "icon": "\ud83c\udf21\ufe0f",
      "script": "toggles/temp_monitor/temp_monitor.py",
      "auto_start": true,
      "enabled": true
    },
    {
      "id": "touch_toggle",
      "name": "Touch Toggle",
      "icon": "\ud83d\udc46",
      "script": "toggles/touch_toggle/touch_toggle.py",
      "auto_start": true,
      "enabled": true
    },
    {
      "id": "tg_fdm_proxy",
      "name": "Telegram FDM Proxy",
      "icon": "\ud83d\udce1",
      "script": "services/tg_fdm_proxy/TgFdmProxy/tg_fdm_proxy.py",
      "auto_start": true,
      "enabled": true
    },
    {
      "id": "taskbar_scroll_controller",
      "name": "Taskbar Scroll Controller",
      "icon": "\ud83d\udd0a",
      "script": "tools/taskbar_scroll/taskbar_scroll.py",
      "auto_start": true,
      "enabled": true
    }
  ]
}
```

---

### File: `services/aerohub_core/remote_control.py`
- **Path:** `services/aerohub_core/remote_control.py`
- **Estimated Tokens:** 659
- **mtime:** 1780923522.094

```python
import json
import logging
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

logger = logging.getLogger("AeroHub.RemoteControl")


class LocalControlHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload, status=200):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _unauthorized(self):
        self._send_json({"error": "Unauthorized"}, status=401)

    def _parse_request(self):
        parsed = urlparse(self.path)
        return parsed.path, parse_qs(parsed.query)

    def _allowed(self):
        token = self.server.control_token
        if not token:
            return True
        header = self.headers.get("X-Local-Token") or self.headers.get("Authorization")
        if header and header.strip() == token:
            return True
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        if params.get("token", [""])[0] == token:
            return True
        return False

    def do_GET(self):
        if not self._allowed():
            return self._unauthorized()

        path, params = self._parse_request()
        core = self.server.core
        if path == "/health":
            return self._send_json(core.get_health())
        if path == "/status":
            return self._send_json(core.get_status())
        if path == "/metrics":
            return self._send_json(core.get_metrics())
        if path == "/control":
            action = params.get("action", [""])[0]
            service_id = params.get("service", [""])[0]
            if action and service_id:
                result = core.control_service(service_id, action)
                return self._send_json(result)
            return self._send_json({"error": "action and service are required"}, status=400)
        if path == "/self-update":
            result = core.perform_self_update()
            status_code = 200 if result.get("status") == "updated" else 500
            return self._send_json(result, status=status_code)
        return self._send_json({"error": "not found"}, status=404)

    def log_message(self, format, *args):
        logger.debug(format % args)


class LocalControlServer(ThreadingHTTPServer):
    def __init__(self, server_address, RequestHandlerClass, core, token=None):
        super().__init__(server_address, RequestHandlerClass)
        self.core = core
        self.control_token = token
```

---

### File: `services/clipboard_manager/ClipboardManager/config.json`
- **Path:** `services/clipboard_manager/ClipboardManager/config.json`
- **Estimated Tokens:** 19
- **mtime:** 1780391350.944

```json
{
    "max_entries": 10000,
    "export_batch": 500,
    "auto_export": true
}
```

---

### File: `services/clipboard_manager/ClipboardManager/tests/test_clipboard_manager.py`
- **Path:** `services/clipboard_manager/ClipboardManager/tests/test_clipboard_manager.py`
- **Estimated Tokens:** 596
- **mtime:** 1780856515.52

```python
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
```

---

### File: `services/health_app/core/__init__.py`
- **Path:** `services/health_app/core/__init__.py`
- **Estimated Tokens:** 6
- **mtime:** 1781114451.516

```python
# HealthApp core package
```

---

### File: `services/health_app/core/audio.py`
- **Path:** `services/health_app/core/audio.py`
- **Estimated Tokens:** 3,051
- **mtime:** 1781116423.527

```python
import os
import math
import struct
import wave
import urllib.request
from core.logger import logger

APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BREATHING_WAV = os.path.join(APP_ROOT, "resources", "breathing_8d.wav")

try:
    import pygame
    # Reinitialize if needed; pygame module level init is fine
    if not pygame.mixer.get_init():
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
    PYGAME_AVAILABLE = True
except Exception:
    PYGAME_AVAILABLE = False


def generate_breathing_sound(duration_sec: int = 65):
    """Generate a stereo WAV with breathing-like tones and 8D panning effect."""
    os.makedirs(os.path.dirname(BREATHING_WAV), exist_ok=True)
    if os.path.exists(BREATHING_WAV):
        return

    logger.info("Generating 8D breathing sound...")
    sample_rate = 44100
    n_samples = sample_rate * duration_sec
    samples = []
    breath_cycle = 4.0
    freq_base = 220
    pan_speed = 0.15

    for i in range(n_samples):
        t = i / sample_rate
        breath_phase = (t % breath_cycle) / breath_cycle

        if breath_phase < 0.5:
            envelope = math.sin(breath_phase * math.pi)
        else:
            envelope = math.sin(breath_phase * math.pi) * 0.6

        envelope = max(0, envelope) * 0.35

        tone = (
            math.sin(2 * math.pi * freq_base * t) * 0.4
            + math.sin(2 * math.pi * freq_base * 1.5 * t) * 0.2
            + math.sin(2 * math.pi * freq_base * 2 * t) * 0.15
            + math.sin(2 * math.pi * freq_base * 0.5 * t) * 0.25
        )

        pan = math.sin(2 * math.pi * pan_speed * t)
        left_vol = math.sqrt(0.5 * (1 + pan))
        right_vol = math.sqrt(0.5 * (1 - pan))

        sample_val = tone * envelope
        left_sample = max(-32767, min(32767, int(sample_val * left_vol * 32767)))
        right_sample = max(-32767, min(32767, int(sample_val * right_vol * 32767)))

        samples.append(left_sample)
        samples.append(right_sample)

    with wave.open(BREATHING_WAV, "w") as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(struct.pack(f"<{len(samples)}h", *samples))

    logger.info(f"8D breathing sound saved: {BREATHING_WAV}")


def ensure_sound_effects():
    """Download sound effects from the web, with local synthesis as a robust fallback."""
    sounds_dir = os.path.join(APP_ROOT, "resources", "sounds")
    os.makedirs(sounds_dir, exist_ok=True)

    sounds = {
        "cyber_alert.wav": "cyber_alert",
        "retro_beep.wav": "retro_beep",
        "zen_bowl.wav": "zen_bowl",
        "echo_ping.wav": "echo_ping",
        "digital_chime.wav": "digital_chime",
        "sci_fi_sweep.wav": "sci_fi_sweep",
        "soft_click.wav": "soft_click",
        "tech_chirp.wav": "tech_chirp",
        "bubble_pop.wav": "bubble_pop",
        "crystal_bell.wav": "crystal_bell",
    }

    # Public domain short WAV files
    sound_urls = {
        "cyber_alert.wav": (
            "https://raw.githubusercontent.com/iondrimba/images-and-sounds/"
            "master/sound-effects/success.wav"
        ),
        "retro_beep.wav": (
            "https://raw.githubusercontent.com/iondrimba/images-and-sounds/"
            "master/sound-effects/click.wav"
        ),
        "zen_bowl.wav": (
            "https://raw.githubusercontent.com/sfiera/wav-samples/master/"
            "input/pcm08m.wav"
        ),
        "echo_ping.wav": (
            "https://raw.githubusercontent.com/nandhaa/AeroHub/main/"
            "BatteryMonitor/sounds/mac_connect.wav"
        ),
    }

    for filename, sound_type in sounds.items():
        filepath = os.path.join(sounds_dir, filename)
        if os.path.exists(filepath):
            continue

        downloaded = False
        url = sound_urls.get(filename)
        if url:
            try:
                logger.info(f"Attempting to download {filename}...")
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
                )
                with urllib.request.urlopen(req, timeout=5) as response:
                    with open(filepath, "wb") as out_file:
                        out_file.write(response.read())
                logger.info(f"Successfully downloaded {filename}")
                downloaded = True
            except Exception as e:
                logger.warning(
                    f"Failed to download {filename}: {e}. Falling back to synthesis."
                )

        if not downloaded:
            try:
                logger.info(f"Synthesizing sound: {filename} ({sound_type})")
                _synthesize_wav(filepath, sound_type)
            except Exception as e:
                logger.error(f"Failed to synthesize {filename}: {e}")


def _synthesize_wav(filepath, sound_type):
    sample_rate = 44100
    channels = 1
    sampwidth = 2
    samples = []

    if sound_type == "cyber_alert":
        duration = 0.4
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            if t < 0.15:
                freq = 880
                val = math.sin(2 * math.pi * freq * t)
                decay = math.exp(-10.0 * t)
            elif 0.15 <= t < 0.20:
                val = 0.0
                decay = 0.0
            else:
                freq = 1760
                val = math.sin(2 * math.pi * freq * (t - 0.20))
                decay = math.exp(-12.0 * (t - 0.20))
            samples.append(int(val * decay * 16384))

    elif sound_type == "retro_beep":
        duration = 0.15
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            val = math.sin(2 * math.pi * 600 * t)
            env = 1.0 if t < 0.12 else (0.15 - t) / 0.03
            samples.append(int(val * env * 12000))

    elif sound_type == "zen_bowl":
        duration = 2.0
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            val = (
                math.sin(2 * math.pi * 150 * t) * 0.5
                + math.sin(2 * math.pi * 300 * t) * 0.3
                + math.sin(2 * math.pi * 450 * t) * 0.2
            )
            decay = math.exp(-2.5 * t)
            samples.append(int(val * decay * 16384))

    elif sound_type == "echo_ping":
        duration = 1.2
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            val1 = math.sin(2 * math.pi * 1000 * t) * math.exp(-8.0 * t)
            val2 = 0.0
            if t > 0.4:
                val2 = (
                    0.4
                    * math.sin(2 * math.pi * 1000 * (t - 0.4))
                    * math.exp(-6.0 * (t - 0.4))
                )
            val = val1 + val2
            samples.append(int(val * 16384))

    elif sound_type == "digital_chime":
        duration = 0.5
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            if t < 0.2:
                val = math.sin(2 * math.pi * 1200 * t) * math.exp(-10.0 * t)
            else:
                val = math.sin(2 * math.pi * 1500 * (t - 0.2)) * math.exp(
                    -10.0 * (t - 0.2)
                )
            samples.append(int(val * 16384))

    elif sound_type == "sci_fi_sweep":
        duration = 0.4
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            freq = 400 + (1200 * (t / duration))
            val = math.sin(2 * math.pi * freq * t)
            env = 1.0
            if t < 0.05:
                env = t / 0.05
            elif t > 0.35:
                env = (duration - t) / 0.05
            samples.append(int(val * env * 14000))

    elif sound_type == "soft_click":
        duration = 0.05
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            val = math.sin(2 * math.pi * 2000 * t)
            decay = math.exp(-100.0 * t)
            samples.append(int(val * decay * 12000))

    elif sound_type == "tech_chirp":
        duration = 0.08
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            freq = 2500 - 1300 * (t / duration)
            val = math.sin(2 * math.pi * freq * t)
            decay = math.exp(-25.0 * t)
            samples.append(int(val * decay * 14000))

    elif sound_type == "bubble_pop":
        duration = 0.15
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            freq = 300 + 1500 * (t / duration)
            val = math.sin(2 * math.pi * freq * t)
            env = math.exp(-15.0 * t)
            samples.append(int(val * env * 16384))

    elif sound_type == "crystal_bell":
        duration = 1.0
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            val = (
                math.sin(2 * math.pi * 2000 * t) * 0.7
                + math.sin(2 * math.pi * 3000 * t) * 0.3
            )
            decay = math.exp(-6.0 * t)
            samples.append(int(val * decay * 16384))

    else:
        duration = 0.2
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            val = math.sin(2 * math.pi * 440 * t)
            samples.append(int(val * 8192))

    with wave.open(filepath, "wb") as w:
        w.setnchannels(channels)
        w.setsampwidth(sampwidth)
        w.setframerate(sample_rate)
        w.writeframes(struct.pack(f"<{len(samples)}h", *samples))


def select_break_audio(settings: dict) -> str:
    """Select the break audio file based on settings."""
    audio_source = settings.get("break_audio_source", "default")
    ambient_dir = os.path.join(APP_ROOT, "resources", "ambient")

    if audio_source == "default":
        return BREATHING_WAV

    if audio_source == "random":
        import random
        if os.path.exists(ambient_dir):
            files = [f for f in os.listdir(ambient_dir) if f.endswith((".mp3", ".wav"))]
            if files:
                return os.path.join(ambient_dir, random.choice(files))
        return BREATHING_WAV

    # Specific track name
    if os.path.exists(ambient_dir):
        for ext in [".mp3", ".wav"]:
            test_path = os.path.join(ambient_dir, f"{audio_source}{ext}")
            if os.path.exists(test_path):
                return test_path

    return BREATHING_WAV


def get_sapi_voices() -> list:
    """Dynamically list SAPI voices description or return default list."""
    try:
        import win32com.client
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        voices = speaker.GetVoices()
        names = []
        for i in range(voices.Count):
            names.append(voices.Item(i).GetDescription())
        return names if names else ["Default"]
    except Exception:
        return ["Default"]


def speak_sapi_async(text: str, voice_name: str = "Default", volume: int = 80, rate: int = 0):
    """Speak SAPI text in a background thread to prevent GUI lockup."""
    import threading

    def target():
        import pythoncom
        import win32com.client
        pythoncom.CoInitialize()
        try:
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            if voice_name and voice_name != "Default":
                voices = speaker.GetVoices()
                for i in range(voices.Count):
                    if voices.Item(i).GetDescription() == voice_name:
                        speaker.Voice = voices.Item(i)
                        break
            speaker.Volume = max(0, min(100, int(volume)))
            speaker.Rate = max(-10, min(10, int(rate)))
            speaker.Speak(text)
        except Exception as e:
            logger.error(f"SAPI voice error: {e}")
        finally:
            pythoncom.CoUninitialize()

    threading.Thread(target=target, daemon=True).start()

```

---

### File: `services/health_app/core/constants.py`
- **Path:** `services/health_app/core/constants.py`
- **Estimated Tokens:** 2,287
- **mtime:** 1781116410.786

```python
# Constants and Configuration defaults for HealthApp

# Theme (Luxury Minimal Dark)
TH = {
    "bg": "#0d0d0f",  # Pure minimalist dark
    "bg2": "#161619",  # Subtle card background
    "bg3": "#212124",  # Active element background
    "accent": "#00df77",  # Mint Green Accent
    "accent_hover": "#32e896",
    "fg": "#f5f5f7",  # Crisp, readable white
    "fg_dim": "#86868b",  # Elegant muted text
    "success": "#34c759",  # Refined green
    "warning": "#ff9f0a",  # Refined orange
    "danger": "#ff453a",  # Refined red
    "border": "#2c2c2e",  # Subtle borders
    "border_glow": "#48484a",  # Soft glow
}

# Media Key Constants
VK_MEDIA_PLAY_PAUSE = 0xB3
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002

# Health Tips
HEALTH_TIPS = {
    "breathing": [
        "Take a slow, deep breath in for 4 seconds, hold for 4, and exhale for 4. 🫁",
        "Deep breathing increases oxygen flow and induces a state of calm. 🧘",
        "Inhale peace, exhale tension. Let your belly rise with each breath. 🌬️",
    ],
    "eye_care": [
        "Look away from the screen! Focus on an object 20 feet away for 20 seconds. 👁️",
        "Blink slowly and deliberately 10 times to rehydrate your eyes. 💧",
        "Gently roll your eyes in circles to relieve strain on the eye muscles. 🌀",
        "Adjust screen brightness so it matches the ambient lighting around you. 💡",
    ],
    "posture": [
        "Sit up straight! Align your ears with your shoulders. 📐",
        "Relax your shoulders away from your ears. Check your spine alignment. 🧘",
        "Make sure your feet are flat on the floor and your knees are at 90 degrees. 🦶",
        "Adjust your chair height so your screen is at eye level. 🖥️",
    ],
    "stretch": [
        "Clasp your hands and stretch them high above your head. 🤸",
        "Rotate your neck slowly to the left, then to the right to release tension. 🔄",
        "Do a gentle torso twist in your chair to stretch your lower back. 🪑",
        "Stand up and stretch your arms and legs. Hold for 15 seconds. 🚶",
    ],
    "hydration": [
        "Time for a sip of water! Stay hydrated to keep your mind sharp. 💧",
        "Drink a glass of water. Proper hydration keeps fatigue at bay. 🥛",
        "Keep a water bottle on your desk and take a sip every few minutes. 🐳",
    ],
    "mental": [
        "Take a 10-second mental pause. Let go of all work thoughts. 🧠",
        "Acknowledge one thing you're grateful for right now. 💖",
        "Smile! Even a forced smile can reduce stress hormones. 😊",
        "Take a deep breath and clear your mind of any clutter. 🧘",
    ],
    "hands_wrists": [
        "Shake out your hands and fingers to relieve typing strain. 🖐️",
        "Stretch your wrists: gently pull your fingers back with your other hand. 🫳",
        "Make gentle fists and rotate your wrists clockwise and counter-clockwise. ✊",
        "Massage the palms of your hands to release muscular tension. 💆",
    ],
}

# Default Settings
DEFAULT_SETTINGS = {
    "short_break_interval_min": 20,
    "short_break_duration_sec": 15,
    "long_break_interval_min": 60,
    "long_break_duration_sec": 60,
    "pre_warning_sec": 30,
    "enable_sound": True,
    "enable_dimming": True,
    "enable_weather_warmth": True,
    "latitude": 13.08,
    "longitude": 80.27,
    "paused": False,
    "night_light_start_hour": 18,
    "night_light_end_hour": 6,
    "run_during_game": True,
    "toast_pos": "Center",
    "toast_custom_x": 100,
    "toast_custom_y": 100,
    "toast_width": 260,
    "toast_height": 60,
    "toast_bg_color": "#252525",
    "toast_fg_color": "#ffffff",
    "toast_accent_color": "#00f0ff",
    "toast_font_size": 11,
    "toast_font_weight": "bold",
    "toast_font_family": "Segoe UI",
    "toast_emoji": "👁️",
    "toast_radius": 16,
    "toast_padding_x": 12,
    "toast_padding_y": 10,
    "toast_anim_style": "Slide",
    "toast_opacity": 0.92,
    "toast_border_width": 0,
    "toast_border_color": "#00f0ff",
    "toast_gradient": False,
    "toast_gradient_end": "#101625",
    "toast_shadow": True,
    "toast_accent_stripe": False,
    "toast_text_align": "left",
    "toast_auto_dismiss": True,
    "toast_click_action": "dismiss",
    "toast_progress_bar": False,
    "toast_enable_sound": True,
    "toast_sound_effect": "mac_connect",
    "toast_volume": 80,
    "toast_border_style": "Solid",
    "toast_stripe_pos": "Left",
    "wellness_points": 0,
    "current_streak": 0,
    "ht_enabled": True,
    "ht_interval_min": 10,
    "ht_duration_sec": 5,
    "ht_cat_breathing": True,
    "ht_cat_eye_care": True,
    "ht_cat_posture": True,
    "ht_cat_stretch": True,
    "ht_cat_hydration": True,
    "ht_cat_mental": True,
    "ht_cat_hands_wrists": True,
    "ht_toast_pos": "Right",
    "ht_toast_custom_x": 100,
    "ht_toast_custom_y": 100,
    "ht_toast_width": 280,
    "ht_toast_height": 70,
    "ht_toast_bg_color": "#252525",
    "ht_toast_fg_color": "#ffffff",
    "ht_toast_accent_color": "#00f0ff",
    "ht_toast_font_size": 11,
    "ht_toast_font_weight": "bold",
    "ht_toast_font_family": "Segoe UI",
    "ht_toast_emoji": "💡",
    "ht_toast_radius": 16,
    "ht_toast_padding_x": 12,
    "ht_toast_padding_y": 10,
    "ht_toast_anim_style": "Slide",
    "ht_toast_opacity": 0.92,
    "ht_toast_border_width": 0,
    "ht_toast_border_color": "#00f0ff",
    "ht_toast_gradient": False,
    "ht_toast_gradient_end": "#101625",
    "ht_toast_shadow": True,
    "ht_toast_accent_stripe": False,
    "ht_toast_text_align": "left",
    "ht_toast_auto_dismiss": True,
    "ht_toast_click_action": "dismiss",
    "ht_toast_progress_bar": False,
    "ht_toast_enable_sound": False,
    "ht_toast_sound_effect": "mac_disconnect",
    "ht_toast_volume": 80,
    "ht_toast_border_style": "Solid",
    "ht_toast_stripe_pos": "Left",
    "bc_enabled": True,
    "bc_start_time": "23:00",
    "bc_end_time": "06:00",
    "bc_target_brightness": 2,
    "bc_duration_minutes": 60,
    "bc_aggressive_target_brightness": 5,
    "bc_aggressive_duration_minutes": 10,
    "bc_safe_brightness": 8,
    "bc_safe_duration_seconds": 30,
    "bc_toast_enable_sound": True,
    "bc_toast_sound_effect": "mac_connect",
    "bc_toast_width": 320,
    "bc_toast_height": 145,
    "bc_toast_bg_color": "#101625",
    "bc_toast_fg_color": "#e2e8f0",
    "bc_toast_accent_color": "#ff2a2a",
    "bc_toast_border_width": 1,
    "bc_toast_border_color": "#7c3aed",
    "bc_toast_radius": 16,
    "bc_toast_gradient": False,
    "bc_toast_gradient_end": "#101625",
    "bc_toast_shadow": True,
    "bc_toast_accent_stripe": False,
    "bc_toast_text_align": "left",
    "bc_toast_progress_bar": False,
    "bc_toast_click_action": "dismiss",
    "bc_toast_border_style": "Solid",
    "bc_toast_stripe_pos": "Left",
    "bc_toast_volume": 80,
    "bc_toast_opacity": 0.95,
    "bc_toast_emoji": "⚠️",
    "bc_toast_padding_x": 12,
    "bc_toast_padding_y": 10,
    "nc_enabled": True,
    "nc_start_time": "23:59",
    "nc_end_time": "06:00",
    "nc_interval_minutes": 5,
    "nc_slogans": (
        "It's late. Your body needs rest. 🌙|"
        "Go to sleep. Tomorrow is a new day. 💤|"
        "Screen time is over. Time for dream time. ✨|"
        "Rest your eyes and your mind. 🛌|"
        "Sleep is the best meditation. 🧘"
    ),
    "nc_toast_width": 300,
    "nc_toast_height": 80,
    "nc_toast_bg_color": "#0d1117",
    "nc_toast_fg_color": "#c9d1d9",
    "nc_toast_accent_color": "#58a6ff",
    "nc_toast_font_size": 12,
    "nc_toast_font_weight": "bold",
    "nc_toast_font_family": "Segoe UI",
    "nc_toast_emoji": "🌙",
    "nc_toast_radius": 12,
    "nc_toast_padding_x": 15,
    "nc_toast_padding_y": 15,
    "nc_toast_anim_style": "Slide",
    "nc_toast_opacity": 0.95,
    "nc_toast_border_width": 2,
    "nc_toast_border_color": "#30363d",
    "nc_toast_enable_sound": True,
    "nc_toast_sound_effect": "mac_connect",
    "nc_toast_gradient": False,
    "nc_toast_gradient_end": "#101625",
    "nc_toast_shadow": True,
    "nc_toast_accent_stripe": False,
    "nc_toast_text_align": "left",
    "nc_toast_progress_bar": False,
    "nc_toast_click_action": "dismiss",
    "nc_toast_border_style": "Solid",
    "nc_toast_stripe_pos": "Left",
    "nc_toast_volume": 80,
    "nl_enabled": True,
    "nl_day_temp": 6500,
    "nl_night_temp": 3500,
    "nl_transition_duration": 20,
    "break_audio_source": "default",
    "voice_prompts_enabled": False,
    "voice_inhale_sec": 4,
    "voice_hold_in_sec": 4,
    "voice_exhale_sec": 4,
    "voice_hold_out_sec": 4,
    "voice_volume": 80,
    "voice_rate": 0,
    "voice_inhale_text": "Breathe in",
    "voice_exhale_text": "Breathe out",
    "voice_hold_in_text": "Hold",
    "voice_hold_out_text": "Hold",
    "voice_break_type": "Both",
    "voice_min_duration_sec": 15,
    "voice_name": "Default",
}

SOUND_EFFECTS = [
    "cyber_alert",
    "retro_beep",
    "zen_bowl",
    "echo_ping",
    "digital_chime",
    "sci_fi_sweep",
    "soft_click",
    "tech_chirp",
    "bubble_pop",
    "crystal_bell",
    "SystemAsterisk",
    "SystemExclamation",
    "SystemHand",
    "SystemQuestion",
    "SystemDefault",
]
```

---

### File: `services/health_app/core/gamma.py`
- **Path:** `services/health_app/core/gamma.py`
- **Estimated Tokens:** 1,084
- **mtime:** 1781114497.088

```python
import ctypes
import ctypes.wintypes
import datetime
import math
import requests
from core.logger import logger
from core.settings import load_settings


def _is_time_between(start_str, end_str):
    try:
        now = datetime.datetime.now().time()
        start_parts = start_str.split(":")
        end_parts = end_str.split(":")
        start = datetime.time(int(start_parts[0]), int(start_parts[1]))
        end = datetime.time(int(end_parts[0]), int(end_parts[1]))
        if start <= end:
            return start <= now <= end
        else:
            return now >= start or now <= end
    except Exception:
        return False


def get_weather_info(lat: float, lon: float) -> dict:
    """Fetch current weather from Open-Meteo API."""
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current_weather=true&daily=sunrise,sunset&timezone=auto"
        )
        resp = requests.get(url, timeout=10)
        data = resp.json()
        return {
            "temperature": data.get("current_weather", {}).get("temperature", 25),
            "is_day": data.get("current_weather", {}).get("is_day", 1),
            "sunrise": data.get("daily", {}).get("sunrise", [""])[0],
            "sunset": data.get("daily", {}).get("sunset", [""])[0],
        }
    except Exception as e:
        logger.error(f"Weather fetch error: {e}")
        settings = load_settings()
        start_hour = settings.get("night_light_start_hour", 18)
        end_hour = settings.get("night_light_end_hour", 6)
        is_day_local = (
            1
            if not _is_night_hour(datetime.datetime.now().hour, start_hour, end_hour)
            else 0
        )
        return {"temperature": 25, "is_day": is_day_local, "sunrise": "", "sunset": ""}


def _is_night_hour(current_hour: int, start_hour: int, end_hour: int) -> bool:
    if start_hour > end_hour:
        return current_hour >= start_hour or current_hour < end_hour
    return start_hour <= current_hour < end_hour


def kelvin_to_rgb(kelvin: int) -> tuple:
    """Convert color temperature (Kelvin) to RGB."""
    temp = kelvin / 100.0

    if temp <= 66:
        red = 255
    else:
        red = max(0, min(255, 329.698727446 * ((temp - 60) ** -0.1332047592)))

    if temp <= 66:
        green = 99.4708025861 * math.log(temp) - 161.1195681661
    else:
        green = 288.1221695283 * ((temp - 60) ** -0.0755148492)
    green = max(0, min(255, green))

    if temp >= 66:
        blue = 255
    elif temp <= 19:
        blue = 0
    else:
        blue = max(0, min(255, 138.5177312231 * math.log(temp - 10) - 305.0447927307))

    return (int(red), int(green), int(blue))


def apply_gamma_ramp(kelvin: int, log_action: bool = True):
    """Apply color temperature via Windows gamma ramp."""
    try:
        r, g, b = kelvin_to_rgb(kelvin)
        rf, gf, bf = r / 255.0, g / 255.0, b / 255.0

        GammaArray = (ctypes.wintypes.WORD * 256 * 3)()
        for i in range(256):
            GammaArray[0][i] = int(min(65535, i * 256 * rf))
            GammaArray[1][i] = int(min(65535, i * 256 * gf))
            GammaArray[2][i] = int(min(65535, i * 256 * bf))

        hdc = ctypes.windll.user32.GetDC(None)

        CurrentGammaArray = (ctypes.wintypes.WORD * 256 * 3)()
        if ctypes.windll.gdi32.GetDeviceGammaRamp(hdc, ctypes.byref(CurrentGammaArray)):
            is_different = False
            for i in range(256):
                if (
                    abs(CurrentGammaArray[0][i] - GammaArray[0][i]) > 10
                    or abs(CurrentGammaArray[1][i] - GammaArray[1][i]) > 10
                    or abs(CurrentGammaArray[2][i] - GammaArray[2][i]) > 10
                ):
                    is_different = True
                    break

            if not is_different:
                ctypes.windll.user32.ReleaseDC(None, hdc)
                return

        ctypes.windll.gdi32.SetDeviceGammaRamp(hdc, ctypes.byref(GammaArray))
        ctypes.windll.user32.ReleaseDC(None, hdc)
        if log_action:
            logger.info(f"Applied color temperature: {kelvin}K")
    except Exception as e:
        if log_action:
            logger.error(f"Gamma ramp error: {e}")


def reset_gamma_ramp():
    """Reset gamma ramp to default (6500K)."""
    apply_gamma_ramp(6500)
```

---

### File: `services/health_app/core/logger.py`
- **Path:** `services/health_app/core/logger.py`
- **Estimated Tokens:** 201
- **mtime:** 1781114467.79

```python
import os
import sys
import logging
import logging.handlers

# Resolve paths relative to app root
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(os.path.dirname(APP_ROOT), "Logs")
LOG_PATH = os.path.join(LOGS_DIR, "health_app.log")

os.makedirs(LOGS_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.handlers.RotatingFileHandler(
            LOG_PATH, maxBytes=2 * 1024 * 1024, backupCount=2, encoding="utf-8"
        ),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("HealthApp")

# Suppress noisy EDID parse warnings from screen_brightness_control
logging.getLogger("screen_brightness_control").setLevel(logging.ERROR)
```

---

### File: `services/health_app/core/media.py`
- **Path:** `services/health_app/core/media.py`
- **Estimated Tokens:** 1,689
- **mtime:** 1781114482.483

```python
import ctypes
import ctypes.wintypes
import threading
import asyncio
import time
from core.logger import logger
from core.constants import (
    VK_MEDIA_PLAY_PAUSE,
    KEYEVENTF_EXTENDEDKEY,
    KEYEVENTF_KEYUP,
)

try:
    from winsdk.windows.media.control import (
        GlobalSystemMediaTransportControlsSessionManager as SessionManager,
    )
    WINSDK_AVAILABLE = True
except ImportError:
    WINSDK_AVAILABLE = False


class MediaController:
    """Manages media pause/resume on a single dedicated COM+async thread.

    Fixes:
    - No more asyncio.run() per call (which creates/destroys event loops)
    - COM is initialized once on the dedicated thread
    - Stale session objects are never reused across calls
    - Each pause/resume fetches fresh sessions from the SessionManager
    - Deduplicates sessions by app_id to prevent flicker
    - Robust error handling per-session so one bad session doesn't crash all
    """

    def __init__(self):
        self._loop = None
        self._thread = None
        self._ready = threading.Event()
        self._paused_app_ids = []
        self._lock = threading.Lock()
        self._start_thread()

    def _start_thread(self):
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        self._ready.wait(timeout=5)

    def _run_loop(self):
        # Initialize COM as MTA once for the lifetime of this thread
        hr = ctypes.windll.ole32.CoInitializeEx(None, 2)
        try:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._ready.set()
            self._loop.run_forever()
        finally:
            if hr in (0, 1):
                ctypes.windll.ole32.CoUninitialize()

    def _run_async(self, coro):
        """Schedule a coroutine on the dedicated loop and wait for result."""
        if not self._loop or not self._loop.is_running():
            return None
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        try:
            return future.result(timeout=10)
        except Exception as e:
            logger.error(f"MediaController async error: {e}")
            return None

    def pause_active_media(self):
        """Pause all currently PLAYING media sessions. Records app_ids to resume later."""
        with self._lock:
            self._paused_app_ids.clear()

        if not WINSDK_AVAILABLE:
            _send_media_key(VK_MEDIA_PLAY_PAUSE)
            return

        paused_ids = self._run_async(self._do_pause())
        if paused_ids is None:
            # Async failed — fall back to global media key
            _send_media_key(VK_MEDIA_PLAY_PAUSE)
            return

        with self._lock:
            self._paused_app_ids = paused_ids

        logger.info(f"Paused {len(paused_ids)} active media sessions via winsdk.")

    def resume_paused_media(self):
        """Resume only the media sessions that were paused before the break."""
        with self._lock:
            ids_to_resume = list(self._paused_app_ids)
            self._paused_app_ids.clear()

        if not WINSDK_AVAILABLE:
            _send_media_key(VK_MEDIA_PLAY_PAUSE)
            return

        if not ids_to_resume:
            return

        count = self._run_async(self._do_resume(ids_to_resume))
        if count is None:
            _send_media_key(VK_MEDIA_PLAY_PAUSE)
            return

        logger.info(f"Resumed {count} media sessions via winsdk.")

    async def _do_pause(self):
        """Fetch fresh sessions and pause all that are Playing (status==4).

        Returns list of app_ids that were successfully paused.
        Deduplicates by app_id so Chrome with 2 tabs only gets paused once.
        """
        paused_ids = []
        seen_app_ids = set()

        try:
            manager = await SessionManager.request_async()
            sessions = manager.get_sessions()

            for session in sessions:
                try:
                    app_id = session.source_app_user_model_id or ""

                    # Deduplicate: only process first session per app
                    if app_id in seen_app_ids:
                        continue
                    seen_app_ids.add(app_id)

                    info = session.get_playback_info()
                    if not info:
                        continue

                    status = info.playback_status
                    if status != 4:  # Not Playing
                        continue

                    result = await session.try_pause_async()
                    if result:
                        paused_ids.append(app_id)
                    else:
                        # try_pause_async returned False — session may not support it
                        paused_ids.append(app_id)

                except Exception as e:
                    logger.debug(f"Error pausing session ({app_id}): {e}")
                    continue

        except Exception as e:
            logger.error(f"SessionManager pause error: {e}")

        return paused_ids

    async def _do_resume(self, app_ids_to_resume):
        """Fetch fresh sessions and resume those whose app_id is in the list.

        Uses fresh session objects (never stale references).
        """
        resumed = 0
        target_ids = set(app_ids_to_resume)

        try:
            manager = await SessionManager.request_async()
            sessions = manager.get_sessions()

            for session in sessions:
                try:
                    app_id = session.source_app_user_model_id or ""
                    if app_id not in target_ids:
                        continue

                    # Remove so we only resume once per app
                    target_ids.discard(app_id)

                    await session.try_play_async()
                    resumed += 1

                except Exception as e:
                    logger.debug(f"Error resuming session ({app_id}): {e}")
                    continue

        except Exception as e:
            logger.error(f"SessionManager resume error: {e}")

        return resumed


def _send_media_key(vk_code: int):
    """Send a media key press/release via keybd_event (global fallback)."""
    try:
        ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_EXTENDEDKEY, 0)
        ctypes.windll.user32.keybd_event(
            vk_code, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0
        )
        time.sleep(0.15)
    except Exception as e:
        logger.error(f"Media key send error: {e}")


# ── Singleton media controller ──
_media_controller = None


def get_media_controller():
    global _media_controller
    if _media_controller is None:
        _media_controller = MediaController()
    return _media_controller
```

---

### File: `services/health_app/core/settings.py`
- **Path:** `services/health_app/core/settings.py`
- **Estimated Tokens:** 219
- **mtime:** 1781114472.45

```python
import os
import json
from core.logger import logger
from core.constants import DEFAULT_SETTINGS

# Resolve path relative to app root
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_PATH = os.path.join(APP_ROOT, "settings.json")

def load_settings() -> dict:
    try:
        if os.path.exists(SETTINGS_PATH):
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                saved = json.load(f)
                return {**DEFAULT_SETTINGS, **saved}
    except Exception as e:
        logger.error(f"Settings load error: {e}")
    return dict(DEFAULT_SETTINGS)


def save_settings(settings: dict):
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)
        logger.info("Settings saved.")
    except Exception as e:
        logger.error(f"Settings save error: {e}")
```

---

### File: `services/health_app/core/utils.py`
- **Path:** `services/health_app/core/utils.py`
- **Estimated Tokens:** 93
- **mtime:** 1781114476.414

```python
import ctypes

def is_workstation_locked() -> bool:
    """Check if the Windows workstation is currently locked."""
    try:
        user32 = ctypes.windll.user32
        hDesktop = user32.OpenInputDesktop(0, False, 0x0100)
        if not hDesktop:
            return True
        user32.CloseDesktop(hDesktop)
        return False
    except Exception:
        return False
```

---

### File: `services/health_app/settings.json`
- **Path:** `services/health_app/settings.json`
- **Estimated Tokens:** 1,276
- **mtime:** 1781115967.151

```json
{
  "short_break_interval_min": 15,
  "short_break_duration_sec": 15,
  "long_break_interval_min": 40,
  "long_break_duration_sec": 40,
  "pre_warning_sec": 30,
  "enable_sound": true,
  "enable_dimming": false,
  "enable_weather_warmth": true,
  "latitude": 13.08,
  "longitude": 80.27,
  "paused": false,
  "night_light_start_hour": 18,
  "night_light_end_hour": 6,
  "run_during_game": true,
  "toast_pos": "Top-Center",
  "toast_custom_x": 100,
  "toast_custom_y": 100,
  "toast_width": 150,
  "toast_height": 50,
  "toast_bg_color": "#00ff40",
  "toast_fg_color": "#000000",
  "toast_accent_color": "#3fb5fc",
  "toast_font_size": 10,
  "toast_font_weight": "normal",
  "toast_font_family": "Segoe UI",
  "toast_emoji": "\u25d5\u203f\u25d5",
  "toast_radius": 8,
  "toast_padding_x": 10,
  "toast_padding_y": 15,
  "toast_anim_style": "Slide",
  "toast_opacity": 1.0,
  "toast_border_width": 1,
  "toast_border_color": "#020202",
  "toast_gradient": false,
  "toast_gradient_end": "#101625",
  "toast_shadow": true,
  "toast_accent_stripe": false,
  "toast_text_align": "left",
  "toast_auto_dismiss": true,
  "toast_click_action": "dismiss",
  "toast_progress_bar": true,
  "toast_enable_sound": true,
  "toast_sound_effect": "bubble_pop",
  "toast_volume": 100,
  "toast_border_style": "Solid",
  "toast_stripe_pos": "Bottom",
  "wellness_points": 520,
  "current_streak": 0,
  "ht_enabled": true,
  "ht_interval_min": 5,
  "ht_duration_sec": 5,
  "ht_cat_breathing": true,
  "ht_cat_eye_care": true,
  "ht_cat_posture": true,
  "ht_cat_stretch": true,
  "ht_cat_hydration": true,
  "ht_cat_mental": true,
  "ht_cat_hands_wrists": true,
  "ht_toast_pos": "Top-Left",
  "ht_toast_custom_x": 100,
  "ht_toast_custom_y": 100,
  "ht_toast_width": 250,
  "ht_toast_height": 70,
  "ht_toast_bg_color": "#ffff04",
  "ht_toast_fg_color": "#000000",
  "ht_toast_accent_color": "#7f7f7f",
  "ht_toast_font_size": 10,
  "ht_toast_font_weight": "normal",
  "ht_toast_font_family": "Segoe UI",
  "ht_toast_emoji": "\u26a1",
  "ht_toast_radius": 18,
  "ht_toast_padding_x": 12,
  "ht_toast_padding_y": 10,
  "ht_toast_anim_style": "Slide",
  "ht_toast_opacity": 0.95,
  "ht_toast_border_width": 1,
  "ht_toast_border_color": "#1a1a2e",
  "ht_toast_gradient": true,
  "ht_toast_gradient_end": "#101625",
  "ht_toast_shadow": true,
  "ht_toast_accent_stripe": false,
  "ht_toast_text_align": "left",
  "ht_toast_auto_dismiss": true,
  "ht_toast_click_action": "dismiss",
  "ht_toast_progress_bar": true,
  "ht_toast_enable_sound": true,
  "ht_toast_sound_effect": "cyber_alert",
  "ht_toast_volume": 80,
  "ht_toast_border_style": "Solid",
  "ht_toast_stripe_pos": "Left",
  "bc_enabled": true,
  "bc_start_time": "23:00",
  "bc_end_time": "06:00",
  "bc_target_brightness": 2,
  "bc_duration_minutes": 60,
  "bc_aggressive_target_brightness": 15,
  "bc_aggressive_duration_minutes": 10,
  "bc_safe_brightness": 8,
  "bc_safe_duration_seconds": 30,
  "bc_toast_enable_sound": true,
  "bc_toast_sound_effect": "cyber_alert",
  "bc_toast_width": 300,
  "bc_toast_height": 122,
  "bc_toast_bg_color": "#ffffff",
  "bc_toast_fg_color": "#008080",
  "bc_toast_accent_color": "#ff2a2a",
  "bc_toast_border_width": 1,
  "bc_toast_border_color": "#7c3aed",
  "bc_toast_radius": 16,
  "bc_toast_gradient": false,
  "bc_toast_gradient_end": "#101625",
  "bc_toast_shadow": true,
  "bc_toast_accent_stripe": false,
  "bc_toast_text_align": "left",
  "bc_toast_progress_bar": false,
  "bc_toast_click_action": "dismiss",
  "bc_toast_border_style": "Solid",
  "bc_toast_stripe_pos": "Left",
  "bc_toast_volume": 80,
  "bc_toast_opacity": 0.95,
  "bc_toast_emoji": "\u26a0\ufe0f",
  "bc_toast_padding_x": 12,
  "bc_toast_padding_y": 10,
  "nc_enabled": true,
  "nc_start_time": "23:59",
  "nc_end_time": "06:00",
  "nc_interval_minutes": 3,
  "nc_slogans": "It's late. Your body needs rest. \ud83c\udf19|Go to sleep. Tomorrow is a new day. \ud83d\udca4|Screen time is over. Time for dream time. \u2728|Rest your eyes and your mind. \ud83d\udecc|Sleep is the best meditation. \ud83e\uddd8",
  "nc_toast_width": 222,
  "nc_toast_height": 60,
  "nc_toast_bg_color": "#000000",
  "nc_toast_fg_color": "#ffffff",
  "nc_toast_accent_color": "#58a6ff",
  "nc_toast_font_size": 12,
  "nc_toast_font_weight": "bold",
  "nc_toast_font_family": "Segoe UI",
  "nc_toast_emoji": "\ud83c\udf19",
  "nc_toast_radius": 12,
  "nc_toast_padding_x": 1,
  "nc_toast_padding_y": 20,
  "nc_toast_anim_style": "Slide",
  "nc_toast_opacity": 0.95,
  "nc_toast_border_width": 2,
  "nc_toast_border_color": "#30363d",
  "nc_toast_enable_sound": true,
  "nc_toast_sound_effect": "echo_ping",
  "nc_toast_gradient": false,
  "nc_toast_gradient_end": "#101625",
  "nc_toast_shadow": true,
  "nc_toast_accent_stripe": false,
  "nc_toast_text_align": "left",
  "nc_toast_progress_bar": true,
  "nc_toast_click_action": "dismiss",
  "nc_toast_border_style": "Solid",
  "nc_toast_stripe_pos": "Left",
  "nc_toast_volume": 80,
  "nl_enabled": true,
  "nl_day_temp": 2500,
  "nl_night_temp": 2900,
  "nl_transition_duration": 25,
  "break_audio_source": "random"
}
```

---

### File: `services/health_app/test_preview.py`
- **Path:** `services/health_app/test_preview.py`
- **Estimated Tokens:** 501
- **mtime:** 1781114625.803

```python
import sys
import tkinter as tk

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.append(SCRIPT_DIR)
from health_app import HealthApp  # noqa: E402
from ui.settings_ui import SettingsWindow  # noqa: E402



def test_preview_window():
    root = tk.Tk()
    root.withdraw()
    try:
        app = HealthApp()
        app.root = root
        sw = SettingsWindow(root, app.settings, lambda x: print("saved", x), app=app)
        sw.show()

        # Test creating SettingsWindow without mainloop blocking
        assert sw is not None
        assert sw.health_preview_scroll_frame is not None
        assert len(sw.health_preview_canvases) > 0
        sw._rebuild_health_toast_previews()
        sw._test_health_preview_sound("breathing")
        sw._show_health_desktop_preview("breathing")

        # Verify triggering desktop previews for each tab to catch any NameErrors/crashes
        sw._show_desktop_preview_for_tab("📅 Schedule") # Should return None gracefully
        sw._show_desktop_preview_for_tab("✨ Toast FX")
        sw._show_desktop_preview_for_tab("💡 Health Toast")
        sw._show_desktop_preview_for_tab("🔆 Brightness Care")
        sw._show_desktop_preview_for_tab("🌙 Night Care")
    finally:
        root.destroy()


if __name__ == "__main__":
    # Interactive manual preview
    root = tk.Tk()
    root.withdraw()
    app = HealthApp()
    app.root = root

    def run_interactive():
        sw = SettingsWindow(root, app.settings, lambda x: print("saved", x))
        sw.entries = {}
        for k in app.settings:
            v = tk.StringVar(value=str(app.settings[k]))
            sw.entries[k] = (
                v,
                True
                if isinstance(app.settings[k], bool)
                else (True if isinstance(app.settings[k], str) else False),
            )
        sw._show_desktop_preview_for_tab("General")
        root.destroy()

    root.after(100, run_interactive)
    root.mainloop()
```

---

### File: `services/health_app/tests/test_health_app.py`
- **Path:** `services/health_app/tests/test_health_app.py`
- **Estimated Tokens:** 2,570
- **mtime:** 1781116938.742

```python
import sys
import os

if "TCL_LIBRARY" not in os.environ:
    local_tcl = os.path.join(
        os.environ.get("LOCALAPPDATA", ""),
        "Programs",
        "Python",
        "Python312",
        "tcl",
        "tcl8.6",
    )
    if os.path.isdir(local_tcl):
        os.environ["TCL_LIBRARY"] = local_tcl

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest  # noqa: E402
import datetime  # noqa: E402
from unittest.mock import patch  # noqa: E402
from core.gamma import kelvin_to_rgb, _is_night_hour  # noqa: E402
from health_app import HealthApp  # noqa: E402


def test_kelvin_to_rgb():
    # Test valid conversions
    r, g, b = kelvin_to_rgb(6500)
    assert r == 255 and g >= 250 and b >= 250

    r, g, b = kelvin_to_rgb(4000)
    assert r == 255 and g > 200 and b < 200  # Roughly warm

    # Test bounds
    r, g, b = kelvin_to_rgb(1000)
    assert r == 255 and g < 100 and b == 0


def test_is_night_hour():
    assert _is_night_hour(20, 18, 6) is True
    assert _is_night_hour(23, 18, 6) is True
    assert _is_night_hour(3, 18, 6) is True
    assert _is_night_hour(5, 18, 6) is True
    assert _is_night_hour(7, 18, 6) is False
    assert _is_night_hour(12, 18, 6) is False


@pytest.fixture
def app():
    with (
        patch(
            "health_app.load_settings",
            return_value={"bc_enabled": True, "nc_enabled": True},
        ),
        patch("health_app.generate_breathing_sound"),
        patch("health_app.get_media_controller"),
        patch(
            "health_app.system_utils.is_system_awake_and_unlocked", return_value=True
        ),
    ):
        # Instantiate safely without launching TK mainloop
        return HealthApp()


def test_is_time_in_range(app):
    # Test time within range overlapping midnight
    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value.time.return_value = datetime.time(23, 30)
        assert app._is_time_in_range("23:00", "06:00") is True

    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value.time.return_value = datetime.time(2, 0)
        assert app._is_time_in_range("23:00", "06:00") is True

    # Test time outside range overlapping midnight
    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value.time.return_value = datetime.time(12, 0)
        assert app._is_time_in_range("23:00", "06:00") is False

    # Test normal range (not overlapping midnight)
    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value.time.return_value = datetime.time(14, 0)
        assert app._is_time_in_range("13:00", "15:00") is True

    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value.time.return_value = datetime.time(16, 0)
        assert app._is_time_in_range("13:00", "15:00") is False

    # Test invalid time format
    assert app._is_time_in_range("invalid", "format") is False


def test_default_settings_keys():
    from health_app import DEFAULT_SETTINGS

    assert DEFAULT_SETTINGS.get("nl_enabled") is True
    assert DEFAULT_SETTINGS.get("nl_day_temp") == 6500
    assert DEFAULT_SETTINGS.get("nl_night_temp") == 3500
    assert DEFAULT_SETTINGS.get("nl_transition_duration") == 20


def test_update_color_temp_disabled(app):
    app.settings["nl_enabled"] = False
    with patch("health_app.apply_gamma_ramp"):
        app._update_color_temp()
        assert app._current_kelvin == 6500
        assert app._target_kelvin_actual == 6500.0


def test_update_color_temp_enabled(app):
    app.settings["nl_enabled"] = True
    app.settings["nl_day_temp"] = 6000
    app.settings["nl_night_temp"] = 3000
    app.settings["enable_weather_warmth"] = False

    with (
        patch("health_app._is_night_hour", return_value=False),
        patch("health_app.apply_gamma_ramp"),
    ):
        app._update_color_temp()
        assert app._current_kelvin == 6000
        assert app._target_kelvin_actual == 6000.0

    with (
        patch("health_app._is_night_hour", return_value=True),
        patch("health_app.apply_gamma_ramp"),
    ):
        app._update_color_temp()
        assert app._current_kelvin == 3000
        assert app._target_kelvin_actual == 3000.0


def test_timer_synchronization(app):
    app.settings["short_break_interval_min"] = 20
    app.settings["long_break_interval_min"] = 60
    # Test settings save synchronization
    app._last_short_break = 100.0
    app._last_long_break = 200.0
    
    with patch("health_app.save_settings"), patch("health_app.apply_gamma_ramp"):
        app._on_settings_saved(dict(app.settings))
        
        # Check that they were reset to the same time
        assert abs(app._last_short_break - app._last_long_break) < 0.01
        assert app._short_warn_shown is False
        assert app._long_warn_shown is False

    # Test lock screen unlock synchronization
    app._last_short_break = 50.0
    app._last_long_break = 150.0
    
    with patch("health_app.is_workstation_locked", side_effect=[True, False]), patch("time.sleep"):
        # Trigger the lock handler
        result = app._handle_lock_screen(12345.0)
        assert result is True
        # Check that they were synchronized to the same time
        assert abs(app._last_short_break - app._last_long_break) < 0.01


def test_box_breathing_overlay_cycle():
    from ui.overlay import BreakOverlay
    import tkinter as tk
    from unittest.mock import MagicMock

    try:
        root = tk.Tk()
        root.withdraw()
    except tk.TclError:
        pytest.skip("Tkinter/Tcl not fully configured on this system")

    settings = {
        "voice_prompts_enabled": True,
        "voice_inhale_sec": 4,
        "voice_hold_in_sec": 2,
        "voice_exhale_sec": 3,
        "voice_hold_out_sec": 1,
        "voice_inhale_text": "Inhale",
        "voice_exhale_text": "Exhale",
        "voice_hold_in_text": "Hold In",
        "voice_hold_out_text": "Hold Out",
        "voice_volume": 80,
        "voice_rate": 0,
        "voice_break_type": "Both",
        "voice_min_duration_sec": 5,
        "voice_name": "Default",
    }

    on_complete = MagicMock()
    overlay = BreakOverlay(root, duration_sec=20, break_type="short", settings=settings, on_complete=on_complete)

    # Initialize Mocks for Tkinter variables and windows
    overlay._countdown_var = MagicMock()
    overlay._breathing_var = MagicMock()
    overlay._breathing_label = MagicMock()
    overlay.window = MagicMock()

    # Test total cycle duration calculation
    T = overlay._inhale_sec + overlay._hold_in_sec + overlay._exhale_sec + overlay._hold_out_sec
    assert T == 10

    # Mock _speak_phase to assert custom text triggers
    overlay._speak_phase = MagicMock()

    # We manually tick the countdown at different remaining times (duration_sec = 20)
    # cycle = (duration_sec - remaining) % T

    # 1. remaining = 20 (cycle = 0): Inhale start
    overlay._remaining = 20
    overlay._tick_countdown()
    overlay._breathing_var.set.assert_called_with("Breathe In... 🌬️")
    overlay._speak_phase.assert_called_with("Inhale")
    overlay._speak_phase.reset_mock()

    # 2. remaining = 18 (cycle = 2): Inhale middle
    overlay._remaining = 18
    overlay._tick_countdown()
    overlay._breathing_var.set.assert_called_with("Breathe In... 🌬️")
    # Should not speak again in middle of phase
    overlay._speak_phase.assert_not_called()

    # 3. remaining = 16 (cycle = 4): Hold In start
    overlay._remaining = 16
    overlay._tick_countdown()
    overlay._breathing_var.set.assert_called_with("Hold... 🛑")
    overlay._speak_phase.assert_called_with("Hold In")
    overlay._speak_phase.reset_mock()

    # 4. remaining = 14 (cycle = 6): Exhale start
    overlay._remaining = 14
    overlay._tick_countdown()
    overlay._breathing_var.set.assert_called_with("Breathe Out... 💨")
    overlay._speak_phase.assert_called_with("Exhale")
    overlay._speak_phase.reset_mock()

    # 5. remaining = 11 (cycle = 9): Hold Out start
    overlay._remaining = 11
    overlay._tick_countdown()
    overlay._breathing_var.set.assert_called_with("Hold... 🛑")
    overlay._speak_phase.assert_called_with("Hold Out")
    overlay._speak_phase.reset_mock()

    root.destroy()


def test_speak_voice_prompts_conditions():
    from ui.overlay import BreakOverlay
    import tkinter as tk
    from unittest.mock import MagicMock

    try:
        root = tk.Tk()
        root.withdraw()
    except tk.TclError:
        pytest.skip("Tkinter/Tcl not fully configured on this system")

    settings = {
        "voice_prompts_enabled": True,
        "voice_inhale_sec": 4,
        "voice_hold_in_sec": 2,
        "voice_exhale_sec": 3,
        "voice_hold_out_sec": 1,
        "voice_break_type": "Long Only",
        "voice_min_duration_sec": 15,
        "voice_name": "Default",
    }

    on_complete = MagicMock()
    
    # Condition: voice_break_type is Long Only but break is Short -> should be False
    overlay_short = BreakOverlay(root, duration_sec=30, break_type="short", settings=settings, on_complete=on_complete)
    assert overlay_short._should_speak_voice() is False

    # Condition: voice_break_type is Long Only, break is Long, duration is 30 -> should be True
    overlay_long = BreakOverlay(root, duration_sec=30, break_type="long", settings=settings, on_complete=on_complete)
    assert overlay_long._should_speak_voice() is True

    # Condition: duration is 10 (less than voice_min_duration_sec = 15) -> should be False
    overlay_long_short_dur = BreakOverlay(root, duration_sec=10, break_type="long", settings=settings, on_complete=on_complete)
    assert overlay_long_short_dur._should_speak_voice() is False

    # Condition: disabled in settings -> should be False
    settings_disabled = dict(settings)
    settings_disabled["voice_prompts_enabled"] = False
    overlay_disabled = BreakOverlay(root, duration_sec=30, break_type="long", settings=settings_disabled, on_complete=on_complete)
    assert overlay_disabled._should_speak_voice() is False

    root.destroy()


def test_get_sapi_voices_fallback():
    from core.audio import get_sapi_voices
    voices = get_sapi_voices()
    assert isinstance(voices, list)
    assert len(voices) >= 1

```

---

### File: `services/health_app/ui/__init__.py`
- **Path:** `services/health_app/ui/__init__.py`
- **Estimated Tokens:** 5
- **mtime:** 1781114456.469

```python
# HealthApp UI package
```

---

### File: `services/health_app/ui/overlay.py`
- **Path:** `services/health_app/ui/overlay.py`
- **Estimated Tokens:** 2,954
- **mtime:** 1781116849.951

```python
import os
import tkinter as tk
from core.logger import logger
from core.constants import TH
from core.media import get_media_controller
from core.audio import select_break_audio, pygame, PYGAME_AVAILABLE
from ui.theme import _add_hover

try:
    import screen_brightness_control as sbc
    SBC_AVAILABLE = True
except ImportError:
    SBC_AVAILABLE = False

# Resolve path relative to HealthApp folder
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BreakOverlay:
    """Full-screen black overlay on all monitors with countdown and breathing text."""

    def __init__(
        self, parent, duration_sec: int, break_type: str, settings: dict, on_complete
    ):
        self.parent = parent
        self.duration = duration_sec
        self.break_type = break_type
        self.settings = settings
        self._remaining = duration_sec
        self._original_brightness = None
        self.status = "completed"
        self.on_complete = on_complete
        self._focus_fail_count = 0
        self._using_windowed_fallback = False

        self._voice_enabled = self.settings.get("voice_prompts_enabled", False)
        self._inhale_sec = int(self.settings.get("voice_inhale_sec", 4))
        self._hold_in_sec = int(self.settings.get("voice_hold_in_sec", 4))
        self._exhale_sec = int(self.settings.get("voice_exhale_sec", 4))
        self._hold_out_sec = int(self.settings.get("voice_hold_out_sec", 4))

    def show(self):
        """Show the overlay (non-blocking call)."""
        try:
            self._dim_screen()
            self._pause_media()
            self._play_break_audio()
            self._create_overlay_window()
            self._start_countdown()
            self._start_focus_keeper()
        except Exception as e:
            logger.error(f"Break overlay error: {e}")
            self._restore()
            if self.on_complete:
                self.on_complete(self.status)

    def _dim_screen(self):
        if SBC_AVAILABLE and self.settings.get("enable_dimming"):
            try:
                self._original_brightness = sbc.get_brightness()
                logger.info("Physical brightness dimming bypassed.")
            except Exception as e:
                logger.error(f"Brightness query error: {e}")

    def _pause_media(self):
        get_media_controller().pause_active_media()
        logger.info("Executed pause for active media sessions.")

    def _play_break_audio(self):
        if not PYGAME_AVAILABLE or not self.settings.get("enable_sound"):
            return
        try:
            sound_file = select_break_audio(self.settings)
            logger.info(f"Loading break sound: {sound_file}")
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play(-1)
        except Exception as e:
            logger.error(f"Audio play error: {e}")

    def _create_overlay_window(self):
        self.window = tk.Toplevel(self.parent)
        self.window.attributes("-fullscreen", True)
        self.window.attributes("-topmost", True)
        self.window.configure(bg="black")
        self.window.overrideredirect(True)

        self.window.protocol("WM_DELETE_WINDOW", lambda: None)
        self.window.bind("<Escape>", lambda e: None)
        self.window.bind("<Alt-F4>", lambda e: None)

        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        self.window.geometry(f"{sw}x{sh}+0+0")
        self.window.grab_set()

        self._build_overlay_ui()

    def _build_overlay_ui(self):
        main_frame = tk.Frame(self.window, bg="black")
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        type_text = "☕ Short Break" if self.break_type == "short" else "🧘 Long Break"
        tk.Label(
            main_frame,
            text=type_text,
            font=("Segoe UI", 20),
            fg=TH["accent"],
            bg="black",
        ).pack(pady=(0, 20))

        self._countdown_var = tk.StringVar(value=str(self.duration))
        tk.Label(
            main_frame,
            textvariable=self._countdown_var,
            font=("Segoe UI Light", 96, "bold"),
            fg="white",
            bg="black",
        ).pack(pady=(0, 20))

        self._breathing_var = tk.StringVar(value="Breathe In...")
        self._breathing_label = tk.Label(
            main_frame,
            textvariable=self._breathing_var,
            font=("Segoe UI", 24),
            fg=TH["fg_dim"],
            bg="black",
        )
        self._breathing_label.pack(pady=(0, 10))

        btn_frame = tk.Frame(main_frame, bg="black")
        btn_frame.pack(pady=10)

        btn_skip = tk.Button(
            btn_frame,
            text="Skip ⏭",
            font=("Segoe UI", 12, "bold"),
            bg="#1a1a2e",
            fg=TH["fg_dim"],
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=TH["bg2"],
            activeforeground="white",
            padx=20,
            pady=8,
            command=self._skip_break,
        )
        btn_skip.pack(side=tk.LEFT, padx=10)

        btn_postpone = tk.Button(
            btn_frame,
            text="Postpone (2m) ⏰",
            font=("Segoe UI", 12, "bold"),
            bg=TH["accent"],
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=TH["accent_hover"],
            activeforeground="white",
            padx=20,
            pady=8,
            command=self._postpone_break,
        )
        btn_postpone.pack(side=tk.LEFT, padx=10)

        _add_hover(btn_skip, "#1a1a2e", TH["bg2"], TH["fg_dim"], "white")
        _add_hover(btn_postpone, TH["accent"], TH["accent_hover"])

        tk.Label(
            main_frame,
            text="Look away from the screen • Focus on something 20ft away",
            font=("Segoe UI", 12),
            fg="#444",
            bg="black",
        ).pack(pady=(20, 0))

    def _skip_break(self):
        self.status = "skipped"
        logger.info("Break skipped by user action.")
        self._cleanup()

    def _postpone_break(self):
        self.status = "postponed"
        logger.info("Break postponed by user action.")
        self._cleanup()

    def _restore(self):
        # Implement restore logic in case of failure or overlay close
        pass

    def _start_countdown(self):
        self._remaining = self.duration
        self._tick_countdown()

    def _tick_countdown(self):
        if self._remaining > 0:
            try:
                self._countdown_var.set(str(self._remaining))

                T = max(1, self._inhale_sec + self._hold_in_sec + self._exhale_sec + self._hold_out_sec)
                cycle = (self.duration - self._remaining) % T

                if cycle < self._inhale_sec:
                    self._breathing_var.set("Breathe In... 🌬️")
                    self._breathing_label.config(fg=TH["success"])
                    if cycle == 0:
                        self._speak_phase(self.settings.get("voice_inhale_text", "Breathe in"))
                elif cycle < self._inhale_sec + self._hold_in_sec:
                    self._breathing_var.set("Hold... 🛑")
                    self._breathing_label.config(fg=TH["warning"])
                    if cycle == self._inhale_sec:
                        self._speak_phase(self.settings.get("voice_hold_in_text", "Hold"))
                elif cycle < self._inhale_sec + self._hold_in_sec + self._exhale_sec:
                    self._breathing_var.set("Breathe Out... 💨")
                    self._breathing_label.config(fg=TH["accent"])
                    if cycle == self._inhale_sec + self._hold_in_sec:
                        self._speak_phase(self.settings.get("voice_exhale_text", "Breathe out"))
                else:
                    self._breathing_var.set("Hold... 🛑")
                    self._breathing_label.config(fg=TH["fg_dim"])
                    if cycle == self._inhale_sec + self._hold_in_sec + self._exhale_sec:
                        self._speak_phase(self.settings.get("voice_hold_out_text", "Hold"))

                self._remaining -= 1
                self.window.after(1000, self._tick_countdown)
            except tk.TclError:
                pass
        else:
            self._cleanup()

    def _should_speak_voice(self) -> bool:
        if not self._voice_enabled:
            return False
        
        # Check break type filter
        vt = self.settings.get("voice_break_type", "Both")
        if vt == "Short Only" and self.break_type != "short":
            return False
        if vt == "Long Only" and self.break_type != "long":
            return False
            
        # Check duration threshold
        min_dur = int(self.settings.get("voice_min_duration_sec", 15))
        if self.duration < min_dur:
            return False
            
        return True

    def _speak_phase(self, text):
        if self._should_speak_voice():
            from core.audio import speak_sapi_async
            voice_name = self.settings.get("voice_name", "Default")
            volume = int(self.settings.get("voice_volume", 80))
            rate = int(self.settings.get("voice_rate", 0))
            speak_sapi_async(text, voice_name, volume, rate)

    def _start_focus_keeper(self):
        self._keep_on_top()

    def _keep_on_top(self):
        if not hasattr(self, "window") or not self.window.winfo_exists():
            return
        try:
            if self.window.state() == "iconic":
                self.window.deiconify()

            self.window.lift()
            self.window.attributes("-topmost", True)

            if self.window.focus_displayof() is None:
                self._focus_fail_count += 1
                if self._focus_fail_count >= 5 and not self._using_windowed_fallback:
                    logger.warning(
                        "Focus repeatedly lost. Applying windowed borderless fallback..."
                    )
                    try:
                        self.window.attributes("-fullscreen", False)
                        self.window.overrideredirect(True)
                        sw = self.window.winfo_screenwidth()
                        sh = self.window.winfo_screenheight()
                        self.window.geometry(f"{sw}x{sh}+0+0")
                        self._using_windowed_fallback = True
                    except Exception as ex:
                        logger.error(f"Failed to apply borderless fallback: {ex}")

                self.window.focus_force()
                try:
                    self.window.grab_set()
                except Exception:
                    pass
            else:
                self._focus_fail_count = 0
        except Exception as e:
            logger.error(f"Keep on top error: {e}")

        self.window.after(500, self._keep_on_top)

    def _cleanup(self):
        """Clean up and restore system state."""
        try:
            if PYGAME_AVAILABLE:
                try:
                    pygame.mixer.music.stop()
                except Exception:
                    pass
            self.window.grab_release()
            self.window.destroy()

            if self.settings.get("enable_sound"):
                try:
                    import winsound

                    sound_path = os.path.join(
                        APP_ROOT, "resources", "on_stop_break.wav"
                    )
                    if os.path.exists(sound_path):
                        winsound.PlaySound(
                            sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC
                        )
                except Exception:
                    pass
            if self.on_complete:
                self.on_complete(self.status)
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
```

---

### File: `services/health_app/ui/theme.py`
- **Path:** `services/health_app/ui/theme.py`
- **Estimated Tokens:** 729
- **mtime:** 1781114542.243

```python
import ctypes
from PIL import Image, ImageDraw
from core.logger import logger

# Theme (Luxury Minimal Dark)
TH = {
    "bg": "#0d0d0f",  # Pure minimalist dark
    "bg2": "#161619",  # Subtle card background
    "bg3": "#212124",  # Active element background
    "accent": "#00df77",  # Mint Green Accent
    "accent_hover": "#32e896",
    "fg": "#f5f5f7",  # Crisp, readable white
    "fg_dim": "#86868b",  # Elegant muted text
    "success": "#34c759",  # Refined green
    "warning": "#ff9f0a",  # Refined orange
    "danger": "#ff453a",  # Refined red
    "border": "#2c2c2e",  # Subtle borders
    "border_glow": "#48484a",  # Soft glow
}


def _add_hover(widget, bg_normal, bg_hover, fg_normal=None, fg_hover=None):
    def on_enter(e):
        widget.config(bg=bg_hover)
        if fg_hover is not None:
            widget.config(fg=fg_hover)

    def on_leave(e):
        widget.config(bg=bg_normal)
        if fg_normal is not None:
            widget.config(fg=fg_normal)

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)


def apply_dwm_rounding(window):
    try:
        window.update_idletasks()
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        if hwnd == 0:
            hwnd = window.winfo_id()
        pref = ctypes.c_int(2)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, 33, ctypes.byref(pref), ctypes.sizeof(pref)
        )
    except Exception as e:
        logger.error(f"DWM rounding error: {e}")


def create_health_icon(paused: bool = False) -> Image.Image:
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Luxury outer ring
    ring_color = (150, 150, 150, 255) if paused else (0, 223, 119, 255)
    draw.ellipse([2, 2, 62, 62], outline=ring_color, width=2)

    # Premium dark glassmorphism inner background
    bg_color = (40, 40, 42, 240) if paused else (22, 22, 25, 240)
    draw.ellipse([4, 4, 60, 60], fill=bg_color)

    # Glowing pulse/heartbeat line in the center
    pulse_color = (150, 150, 150, 255) if paused else (0, 223, 119, 255)
    
    # Heartbeat path coordinates (a sleek pulse wave)
    points = [
        (10, 32),
        (20, 32),
        (25, 20),
        (29, 44),
        (34, 12),
        (39, 52),
        (44, 32),
        (54, 32)
    ]
    
    # Draw glow effect (semi-transparent wider lines behind)
    glow_color = (150, 150, 150, 60) if paused else (0, 223, 119, 60)
    draw.line(points, fill=glow_color, width=6, joint="round")
    draw.line(points, fill=pulse_color, width=3, joint="round")

    # Add a glowing core dot at the peak
    if not paused:
        draw.ellipse([32, 10, 36, 14], fill=(255, 255, 255, 255))
    else:
        # Subtle cross for pause state
        draw.line([26, 26, 38, 38], fill=(255, 69, 58, 255), width=3)
        draw.line([38, 26, 26, 38], fill=(255, 69, 58, 255), width=3)

    return img
```

---

### File: `services/media_control/MediaControl.vbs`
- **Path:** `services/media_control/MediaControl.vbs`
- **Estimated Tokens:** 65
- **mtime:** 1779287728.048

```
Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
batPath = fso.BuildPath(scriptDir, "run_media_control.bat")
WshShell.Run """" & batPath & """", 0, False
```

---

### File: `services/media_control/Volume_Control_Taskbar.vbs`
- **Path:** `services/media_control/Volume_Control_Taskbar.vbs`
- **Estimated Tokens:** 154
- **mtime:** 1779287738.489

```
Set objWMIService = GetObject("winmgmts:\\.\root\cimv2")
Set colProcesses = objWMIService.ExecQuery("Select * from Win32_Process Where Name = 'Volume_Control_Taskbar.exe'")

If colProcesses.Count = 0 Then
    Set WshShell = CreateObject("WScript.Shell")
    Set fso = CreateObject("Scripting.FileSystemObject")
    scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
    parent1 = fso.GetParentFolderName(scriptDir)
    parent2 = fso.GetParentFolderName(parent1)
    exePath = fso.BuildPath(fso.BuildPath(parent2, "legacy"), "Volume_Control_Taskbar.exe")
    WshShell.Run """" & exePath & """", 0, False
End If
```

---

### File: `services/media_control/debug_sessions.py`
- **Path:** `services/media_control/debug_sessions.py`
- **Estimated Tokens:** 628
- **mtime:** 1780861103.716

```python
"""
Quick diagnostic: enumerate all media sessions and print their status.
Run this while playing audio in 2+ apps to see what Windows reports.
"""

import asyncio
import ctypes

from winsdk.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as SessionManager,
)

# Init COM as MTA
ctypes.windll.ole32.CoInitializeEx(None, 2)

STATUS_MAP = {
    0: "Closed",
    1: "Opened",
    2: "Changing",
    3: "Stopped",
    4: "Playing",
    5: "Paused",
}


async def main():
    manager = await SessionManager.request_async()

    print("=" * 60)
    print("CURRENT SESSION:")
    current = manager.get_current_session()
    if current:
        info = current.get_playback_info()
        status = info.playback_status if info else None
        try:
            props = await current.try_get_media_properties_async()
            title = props.title if props else ""
            artist = props.artist if props else ""
        except Exception:
            title = artist = "?"
        app_id = current.source_app_user_model_id
        print(f"  App: {app_id}")
        print(f"  Status: {status} ({STATUS_MAP.get(status, 'Unknown')})")
        print(f"  Title: {title}")
        print(f"  Artist: {artist}")
    else:
        print("  (none)")

    print()
    print("ALL SESSIONS:")
    sessions = manager.get_sessions()
    total = 0
    for i, s in enumerate(sessions):
        total += 1
        try:
            s_info = s.get_playback_info()
            s_status = s_info.playback_status if s_info else None
            try:
                s_props = await s.try_get_media_properties_async()
                s_title = s_props.title if s_props else ""
                s_artist = s_props.artist if s_props else ""
            except Exception:
                s_title = s_artist = "?"
            s_app_id = s.source_app_user_model_id
            print(f"  [{i}] App: {s_app_id}")
            print(f"      Status: {s_status} ({STATUS_MAP.get(s_status, 'Unknown')})")
            print(f"      Title: {s_title}")
            print(f"      Artist: {s_artist}")
        except Exception as e:
            print(f"  [{i}] Error: {e}")

    if total == 0:
        print("  (none)")

    print(f"\nTotal sessions: {total}")
    playing_paused_only = sum(
        1
        for s in sessions
        if s.get_playback_info()
        and s.get_playback_info().playback_status in (4, 5)
    )
    print(f"Playing/Paused only: {playing_paused_only}")
    print("=" * 60)


asyncio.run(main())
```

---

### File: `services/media_control/patch.py`
- **Path:** `services/media_control/patch.py`
- **Estimated Tokens:** 1,215
- **mtime:** 1780860277.104

```python
import re

with open("services/media_control/media_control.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove MediaDashboard class completely
content = re.sub(
    r"class MediaDashboard:.*?# ══════════════════════════════════════════════════════════\n",
    "# ══════════════════════════════════════════════════════════\n",
    content,
    flags=re.DOTALL,
)

# 2. Remove self.root and self.dashboard initialization
init_target = """        # Initialize Tkinter root for dashboard on main thread
        self.root = tk.Tk()
        self.root.withdraw()
        self.dashboard = MediaDashboard(self, self.root)
        """
content = content.replace(init_target, "")

# 3. Clean _handle_window_msg dashboard toggle
handle_msg_target = """                    # Only the Play/Pause button (id=2) opens the dashboard on multi-session
                    if wparam == 2 and count > 1:
                        logger.info("Multi-session detected on Play/Pause click — toggling dashboard...")
                        self.root.after(0, self.dashboard.toggle)
                    else:
                        logger.info("Executing standard media key command...")
                        for ctrl in self.controls:
                            if ctrl["id"] == wparam:
                                ctrl["cmd"]()
                                break"""
handle_msg_replacement = """                    logger.info("Executing standard media key command...")
                    for ctrl in self.controls:
                        if ctrl["id"] == wparam:
                            ctrl["cmd"]()
                            break"""
content = content.replace(handle_msg_target, handle_msg_replacement)

# 4. Clean show_context_menu
menu_target = """        win32gui.AppendMenu(hmenu, win32con.MF_STRING, DASHBOARD_CMD_ID, "Open Dashboard")
        win32gui.AppendMenu(hmenu, win32con.MF_SEPARATOR, 0, "")
        win32gui.AppendMenu(hmenu, win32con.MF_STRING, EXIT_CMD_ID, "Exit")"""
menu_replacement = (
    """        win32gui.AppendMenu(hmenu, win32con.MF_STRING, EXIT_CMD_ID, "Exit")"""
)
content = content.replace(menu_target, menu_replacement)

# 5. Clean WM_COMMAND
cmd_target = """            elif msg == win32con.WM_COMMAND:
                if wparam == EXIT_CMD_ID:
                    self.quit_app()
                elif wparam == DASHBOARD_CMD_ID:
                    self.root.after(0, self.dashboard.show)"""
cmd_replacement = """            elif msg == win32con.WM_COMMAND:
                if wparam == EXIT_CMD_ID:
                    self.quit_app()"""
content = content.replace(cmd_target, cmd_replacement)

# 6. Clean monitor_media dashboard updates
monitor_target = """                if new_count != getattr(self, 'prev_active_count', -1):
                    logger.info(f"Active sessions count changed to: {new_count}")
                    prev_count = getattr(self, 'prev_active_count', -1)
                    # Auto-show dashboard when going from 1 to >1 session, but NOT on startup
                    if prev_count != -1 and new_count > 1 and prev_count <= 1:
                        if not self.dashboard._visible:
                            logger.info("Auto-opening dashboard due to multiple sessions")
                            self.root.after(0, self.dashboard.show)
                    self.prev_active_count = new_count

                # Generate a simple hash of the current session state to avoid unnecessary UI rebuilds
                current_state_hash = str([{
                    "id": d["app_id"],
                    "status": d["status"],
                    "title": d["title"],
                    "artist": d["artist"]
                } for d in active_sessions_list])

                if current_state_hash != getattr(self, 'prev_state_hash', ""):
                    # ALWAYS send data to dashboard so it has a cached copy to display instantly on toggle
                    self.root.after(0, self.dashboard.update_sessions, active_sessions_list)
                    self.prev_state_hash = current_state_hash"""
monitor_replacement = """                if new_count != getattr(self, 'prev_active_count', -1):
                    logger.info(f"Active sessions count changed to: {new_count}")
                    self.prev_active_count = new_count"""
content = content.replace(monitor_target, monitor_replacement)

# 7. Replace run() loop
run_target = """    def run(self):
        self.root.mainloop()"""
run_replacement = """    def run(self):
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.quit_app()"""
content = content.replace(run_target, run_replacement)

with open("services/media_control/media_control.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Patch applied successfully")
```

---

### File: `services/media_control/requirements.txt`
- **Path:** `services/media_control/requirements.txt`
- **Estimated Tokens:** 12
- **mtime:** 1776780628.651

```
customtkinter
pystray
Pillow
pycaw
comtypes
winsdk
```

---

### File: `services/media_control/run_media_control.bat`
- **Path:** `services/media_control/run_media_control.bat`
- **Estimated Tokens:** 15
- **mtime:** 1776794826.76

```
@echo off
cd /d "%~dp0"
start "" pythonw media_control.py
exit
```

---

### File: `services/media_control/test_icon.py`
- **Path:** `services/media_control/test_icon.py`
- **Estimated Tokens:** 307
- **mtime:** 1780856038.257

```python
import win32api
import win32gui
import win32ui
import win32con
from PIL import Image


def get_icon(path):
    ico_x = 32
    ico_y = 32

    large, small = win32gui.ExtractIconEx(path, 0)
    if not large:
        return None

    hicon = large[0]
    win32gui.DestroyIcon(small[0]) if small else None

    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
    hbmp = win32ui.CreateBitmap()
    hbmp.CreateCompatibleBitmap(hdc, ico_x, ico_y)
    hdc_mem = hdc.CreateCompatibleDC()

    hdc_mem.SelectObject(hbmp)

    # Fill background with #1a1a3e
    brush = win32gui.CreateSolidBrush(win32api.RGB(0x1A, 0x1A, 0x3E))
    win32gui.FillRect(hdc_mem.GetSafeHdc(), (0, 0, ico_x, ico_y), brush)
    win32gui.DeleteObject(brush)

    # Draw icon
    win32gui.DrawIconEx(
        hdc_mem.GetSafeHdc(), 0, 0, hicon, ico_x, ico_y, 0, None, win32con.DI_NORMAL
    )

    bmpinfo = hbmp.GetInfo()
    bmpstr = hbmp.GetBitmapBits(True)

    im = Image.frombuffer(
        "RGBA", (bmpinfo["bmWidth"], bmpinfo["bmHeight"]), bmpstr, "raw", "BGRA", 0, 1
    )

    win32gui.DestroyIcon(hicon)
    return im


im = get_icon(r"C:\Program Files\Mozilla Firefox\firefox.exe")
if im:
    im.save("firefox_icon_bg.png")
    print("Icon saved")
```

---

### File: `services/media_control/test_pause.py`
- **Path:** `services/media_control/test_pause.py`
- **Estimated Tokens:** 265
- **mtime:** 1780856038.258

```python
import win32gui
import win32con
import win32process


def pause_app(process_name):
    # Find HWNDs for process
    hwnds = []

    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            hwnds.append((hwnd, pid))
        return True

    win32gui.EnumWindows(callback, hwnds)

    import psutil

    target_pids = [
        p.pid
        for p in psutil.process_iter(["name"])
        if p.info["name"] and p.info["name"].lower() == process_name.lower()
    ]

    for hwnd, pid in hwnds:
        if pid in target_pids:
            print(f"Sending APPCOMMAND_MEDIA_PAUSE to {process_name} (HWND: {hwnd})")
            win32gui.PostMessage(
                hwnd, win32con.WM_APPCOMMAND, 0, win32con.APPCOMMAND_MEDIA_PAUSE << 16
            )
            # or try PLAY_PAUSE
            # win32gui.PostMessage(hwnd, win32con.WM_APPCOMMAND, 0, win32con.APPCOMMAND_MEDIA_PLAY_PAUSE << 16)


if __name__ == "__main__":
    pause_app("vlc.exe")
    pause_app("firefox.exe")
```

---

### File: `services/movie_song_downloader/MovieSongDownloader.py`
- **Path:** `services/movie_song_downloader/MovieSongDownloader.py`
- **Estimated Tokens:** 2,930
- **mtime:** 1780928588.348

```python
# MovieSongDownloader/MovieSongDownloader.py

import reflex as rx
import time

from MovieSongDownloader.ui.state import AppState
from MovieSongDownloader.ui import style
from MovieSongDownloader.ui.home import home_view, watchlist_view
from MovieSongDownloader.ui.search import search_view
from MovieSongDownloader.ui.songs import songs_view
from MovieSongDownloader.ui.downloads import downloads_view
from MovieSongDownloader.ui.settings import settings_view


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
        from MovieSongDownloader.core.job_queue import job_queue

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
    logger = logging.getLogger("MovieSongDownloader.FastAPI")
    try:
        from MovieSongDownloader.core.database import db

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

    logger = logging.getLogger("MovieSongDownloader.FastAPI")
    logger.info("Initializing database migrations via FastAPI startup hook...")
    try:
        from MovieSongDownloader.core.database import db

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
        from MovieSongDownloader.services.download_service import download_service

        logger.info("Starting background download service worker...")
        await download_service.start()
    except Exception as e:
        logger.error(f"Failed to start download service worker: {e}")


@app._api.on_event("shutdown")
async def shutdown_event():
    import logging

    logger = logging.getLogger("MovieSongDownloader.FastAPI")
    logger.info(
        "Stopping background download service worker via FastAPI shutdown hook..."
    )
    try:
        from MovieSongDownloader.services.download_service import download_service

        await download_service.stop()
    except Exception as e:
        logger.error(f"Error stopping download service worker: {e}")
```

---

### File: `services/movie_song_downloader/Unknown.lrc`
- **Path:** `services/movie_song_downloader/Unknown.lrc`
- **Estimated Tokens:** 721
- **mtime:** 1780556746.346

```
[00:00.16] ம்ம், வரியா
[00:09.61] மவனுக்கு காத்தளுக்க
[00:10.89] கஞ்சனுக்கு செஞ்சருக்க
[00:11.87] செய்தோருக்கு செய்கொடுக்க
[00:12.88] நன்னோருக்கு நன்னருக்க
[00:14.17] 
[00:52.57] ஹே, சடாருனு உருமும் வேங்கை இது
[00:54.73] உன் அடாவடி அடக்கும் ஆளு இது
[00:57.02] Boom! படாருனு வெடிக்கும் வேளையில
[00:59.27] பத்த வச்சுகிட்ட வந்து தொலைக்காதே
[01:01.57] ஹே, சடாருனு உருமும் வேங்கை இது
[01:03.75] உன் அடாவடி அடக்கும் ஆளு இது
[01:06.07] Boom! படாருனு வெடிக்கும் வேளையில
[01:08.31] பத்த வச்சுகிட்ட வந்து தொலைக்காதே
[01:10.67] ஹே தப்பு தப்பா கணக்க நீ போட்டே
[01:13.48] சூரியன சுட்டுதள்ள பாத்தே
[01:15.66] வச்சிக்காத உனக்கினி ஆப்பே, ஹே-ஹே,-ஹே-ஹே-ஹே,-ஹே
[01:19.86] ஹே தம்பி போயி gate'ah கொஞ்சம் சாத்தே
[01:22.44] கையி காலு கண்ணு ரெண்டும் பாத்தே
[01:24.75] வீசபோது ராட்சச காத்தே, ஹே-ஹே,-ஹே-ஹே-ஹே,-ஹே
[01:28.70] ம்ம், வரியா
[01:33.38] ம்ம், வரியா
[01:37.95] ம்ம், வரியா
[01:42.39] ம்ம், வரியா
[01:47.04] பரியேறி நின்னவன்தானே உருமாறி வந்துருக்கானே
[01:51.58] பட நூறு பாத்தவன்தானே, பதற விடுவானே
[01:56.01] நரி மொத்தம் வெரட்டிடத்தானே அரிமாவா வந்துருக்கானே
[02:00.57] பகையெல்லாம் எரிச்சிடத்தானே நெருப்பா சிரிப்பானே
[02:05.48] 
[02:25.26] சாத்தான் பணிஞ்சு ஓட்டான் தல வெடிச்சு
[02:27.57] போட்டான் சுளுக்கு பாட்டன்தான் நமக்கு
[02:29.82] காட்டான் அடிச்ச டாட்டாதான் உனக்கு, ஹே
[02:33.95] ரத்த தோட்டா தெறிக்கும் வெட்டா கொரல் ஒலிக்கும்
[02:36.54] கேட்டா அலறும் பாத்தா கொல நடுங்கும்
[02:38.92] छोटा புளிப்பு அவளோதான் உனக்கு, ஹே
[02:43.45] ஹே, சடாருனு உருமும் வேங்கை இது
[02:45.61] உன் அடாவடி அடக்கும் ஆளு இது
[02:47.80] Boom! படாருனு வெடிக்கும் நேரம் இது
[02:50.11] அய்யன் முன்ன நீ வந்து கொறைக்காதே
[02:52.42] ஹே, சடாருனு உருமும் வேங்கை இது
[02:54.64] உன் அடாவடி அடக்கும் ஆளு இது
[02:56.99] Boom! படாருனு வெடிக்கும் நேரம் இது
[02:59.49] சிங்கம் வாயில தல குடுக்காதே
[03:01.58] ஹே, சடாருனு உருமும் வேங்கை இது
[03:03.85] உன் அடாவடி அடக்கும் ஆளு இது
[03:06.11] Boom! படாருனு வெடிக்கும் நேரம் இது
[03:10.03] Crown on fire, he bounces when the night gets cold
[03:12.74] Blade of truth cuttin' through the lies they've told
[03:14.87] King of justice hear the innocent cry his name
[03:17.20] Chills the weak while he sets the dark in flame
[03:19.28] வெரப்பா எலும்ப எண்ணி
[03:22.60] எடைக்கு போடும் எமன் இங்க பார், எமன் இங்க பார்
[03:28.49] மொறச்சா தெறிச்சு நீயும் செதறு silent'ah
[03:37.76] சாத்தான் பணிஞ்சு ஓட்டான் தல வெடிச்சு
[03:39.94] போட்டான் சுளுக்கு பாட்டன்தான் நமக்கு
[03:42.30] காட்டான் அடிச்ச டாட்டாதான் உனக்கு, ஹே
[03:46.60] ரத்த தோட்டா தெறிக்கும் வெட்டா கொரல் ஒலிக்கும்
[03:49.03] கேட்டா அலறும் பாத்தா கொல நடுங்கும்
[03:51.31] छोटा புளிப்பு அவளோதான் உனக்கு, ஹே
[03:58.27] ஹே, சடாருனு உருமும் வேங்கை இது
[04:00.49] உன் அடாவடி அடக்கும் ஆளு இது
[04:02.77] Boom! படாருனு வெடிக்கும் நேரம் இது
[04:04.90] சிங்கம் வாயில தல குடுக்காதே
[04:07.15] ஹே, சடாருனு உருமும் வேங்கை இது
[04:09.40] உன் அடாவடி அடக்கும் ஆளு இது
[04:11.72] Boom! படாருனு வெடிக்கும் நேரம் இது
[04:13.89] கருப்பன் வர்றான் வழிமறிக்காதே
[04:17.11] 
```

---

### File: `services/movie_song_downloader/Unknown.txt`
- **Path:** `services/movie_song_downloader/Unknown.txt`
- **Estimated Tokens:** 46
- **mtime:** 1780556618.382

```
இது God'u mode'u
இது God'u mode'u
இது God'u mode'u ஓசையே நிக்காதே
கர பத்தும் ஜனம் மொத்தோம் பேர கத்தும் கொல சத்தம்
கர பத்தும் ஜனம் மொத்தோம் பேர கத்தும் கொல சத்தம்
கர பத்தும் ஜனம் மொத்தோம்
```

---

### File: `services/movie_song_downloader/__init__.py`
- **Path:** `services/movie_song_downloader/__init__.py`
- **Estimated Tokens:** 549
- **mtime:** 1780856038.253

```python
# MovieSongDownloader Package Init

import os
import sys


# Synchronously bootstrap DoH DNS resolver to bypass ISP block.
# We do this at the very beginning of package import to override the socket resolution.
def _early_bootstrap_dns():
    import sqlite3
    from pathlib import Path

    app_dir = Path(__file__).resolve().parent
    db_path = app_dir / "db.sqlite3"
    doh_enabled = True
    dns_provider = "cloudflare"
    try:
        if db_path.exists():
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute(
                "SELECT key, value FROM settings WHERE key IN ('doh_enabled', 'dns_provider')"
            )
            rows = cursor.fetchall()
            for key, val in rows:
                if key == "doh_enabled":
                    doh_enabled = val == "true"
                elif key == "dns_provider":
                    dns_provider = val
            conn.close()
    except Exception:
        pass

    if doh_enabled:
        try:
            from MovieSongDownloader.core.dns_resolver import bootstrap_dns_sync

            bootstrap_dns_sync(dns_provider)
        except Exception as e:
            print(f"Error early-bootstrapping DoH DNS resolver: {e}", file=sys.stderr)


_early_bootstrap_dns()

# Apply runtime patches for Windows paths / ampersands inside yt-dlp & deezload
import yt_dlp  # noqa: E402

sys.modules["youtube_dl"] = yt_dlp

# Prepend local bin directory to system PATH for FFmpeg binaries
bin_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")

# Patch deezload query string parsing for Windows paths / ampersands
try:
    import deezload.base

    original_extract = deezload.base.extract_video_id

    def patched_extract_video_id(qs: str):
        try:
            qs_decoded = qs.encode("utf-8").decode("unicode-escape")
        except Exception:
            qs_decoded = qs
        qs_decoded = qs_decoded.replace(r"\u0026", "&").replace("\\u0026", "&")
        return original_extract(qs_decoded)

    deezload.base.extract_video_id = patched_extract_video_id
except Exception:
    pass
```

---

### File: `services/movie_song_downloader/build_prod.ps1`
- **Path:** `services/movie_song_downloader/build_prod.ps1`
- **Estimated Tokens:** 248
- **mtime:** 1780923522.093

```powershell
param(
    [int]$port = 8555
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:FLET_WEB_PORT = "$port"
$logdir = Join-Path $root "logs"
if (-not (Test-Path $logdir)) { New-Item -ItemType Directory -Path $logdir | Out-Null }
$timestamp = (Get-Date).ToString('yyyyMMdd-HHmmss')
$logfile = Join-Path $logdir "build_prod_$timestamp.log"

Write-Host "Building MovieSongDownloader production bundle..."
Write-Host "Logs: $logfile"

try {
    python -m pip install --upgrade pip | Out-Null
    python -m pip install -r requirements.txt | Out-Null
    python MovieSongDownloader/main.py --env prod 2>&1 | Tee-Object -FilePath $logfile
    Write-Host "Production run successful. Packaging artifacts..."
    $archive = Join-Path $logdir "MovieSongDownloader-production-$timestamp.zip"
    Compress-Archive -Path "$root\MovieSongDownloader\*" -DestinationPath $archive -Force
    Write-Host "Packaged production artifact: $archive"
} catch {
    Write-Error "Build failed: $_"
    exit 1
}
```

---

### File: `services/movie_song_downloader/build_prod.sh`
- **Path:** `services/movie_song_downloader/build_prod.sh`
- **Estimated Tokens:** 117
- **mtime:** 1780923522.093

```bash
#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
export FLET_WEB_PORT="8555"
echo "Building MovieSongDownloader production bundle..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python "$ROOT_DIR/main.py" --env prod
archive="$ROOT_DIR/../logs/MovieSongDownloader-production-$(date +%Y%m%d%H%M%S).zip"
mkdir -p "$ROOT_DIR/../logs"
zip -r "$archive" "$ROOT_DIR"
echo "Packaged production artifact: $archive"
```

---

### File: `services/movie_song_downloader/config.py`
- **Path:** `services/movie_song_downloader/config.py`
- **Estimated Tokens:** 543
- **mtime:** 1780856038.256

```python
from pathlib import Path

APP_NAME = "MovieSongDownloader"
APP_VERSION = "2.0.0"

APP_DIR = Path(__file__).resolve().parent
DATABASE_DIR = APP_DIR / ".db"
DATABASE_PATH = DATABASE_DIR / "db.sqlite3"
SETTINGS_BACKUP_PATH = DATABASE_DIR / "settings_backup.json"

LOGS_DIR = APP_DIR / ".logs"
CACHE_DIR = APP_DIR / ".cache"
POSTERS_CACHE_DIR = CACHE_DIR / "posters"
COVERS_CACHE_DIR = CACHE_DIR / "covers"

for directory in [
    DATABASE_DIR,
    LOGS_DIR,
    CACHE_DIR,
    POSTERS_CACHE_DIR,
    COVERS_CACHE_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)

APP_LOG_PATH = LOGS_DIR / "app.log"
DOWNLOADS_LOG_PATH = LOGS_DIR / "downloads.log"
PROVIDERS_LOG_PATH = LOGS_DIR / "providers.log"

DEFAULT_DOWNLOAD_DIR = str(Path.home() / "Music" / "MovieSongDownloader")

# Data source URLs
WIKIPEDIA_EN_API = "https://en.wikipedia.org/w/api.php"
WIKIPEDIA_TA_API = "https://ta.wikipedia.org/w/api.php"
OMDB_BASE_URL = "https://www.omdbapi.com/"

DEFAULT_SETTINGS = {
    "omdb_api_key": "",
    "deezer_arl": "",
    "download_provider": "spotiflac",
    "scraping_limit": "5",
    "last_fetch_date": "",
    # Download
    "audio_format": "mp3",
    "bitrate": "320",
    "output_dir": DEFAULT_DOWNLOAD_DIR,
    "filename_format": "{TrackNum} - {Title}",
    "folder_format": "{Year}/{Movie}/Songs",
    "download_mode": "accurate",
    "max_concurrent": "2",
    # Lyrics
    "lyrics_priority": '["lrclib", "syncedlyrics", "musixmatch", "genius"]',
    "save_lrc_file": "true",
    "embed_lyrics": "true",
    # UI
    "theme": "dark",
    "default_tab": "home",
    "language_region": "en-US",
    # Watchlist
    "check_interval_hours": "24",
    "auto_download": "true",
    "notify_on_found": "true",
    # DNS (bypass ISP blocks)
    "doh_enabled": "true",
    "dns_provider": "cloudflare",
}

# Cyberpunk Cyan Design Tokens
COLOR_ACCENT = "#06B6D4"  # Cyan accent
COLOR_ACCENT_LIGHT = "#22D3EE"  # Light cyan for hover/focus
COLOR_TEXT_PRIMARY = "#FFFFFF"  # Crisp white
COLOR_TEXT_MUTED = "#94A3B8"  # Muted cool gray
COLOR_BG_PRIMARY = "#0B0F19"  # Deep dark blue/gray
COLOR_BG_SECONDARY = "#111827"  # Dark gray
COLOR_BORDER = "#1F2937"  # Dark gray border
```

---

### File: `services/movie_song_downloader/core/__init__.py`
- **Path:** `services/movie_song_downloader/core/__init__.py`
- **Estimated Tokens:** 3
- **mtime:** 1780474573.814

```python
# Core Module
```

---

### File: `services/movie_song_downloader/core/cache_manager.py`
- **Path:** `services/movie_song_downloader/core/cache_manager.py`
- **Estimated Tokens:** 1,430
- **mtime:** 1780856038.258

```python
import os
import hashlib
import json
import logging
from datetime import datetime, timedelta
from typing import Optional
import httpx
from MovieSongDownloader.config import POSTERS_CACHE_DIR, COVERS_CACHE_DIR
from MovieSongDownloader.core.database import db

logger = logging.getLogger("MovieSongDownloader.CacheManager")


class DownloadCache:
    @staticmethod
    def generate_hash(artist: str, title: str, album: str, duration_ms: int) -> str:
        raw = f"{artist.lower()}|{title.lower()}|{album.lower()}|{duration_ms}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    async def check(self, track_hash: str) -> Optional[dict]:
        conn = await db.get_connection()
        try:
            async with conn.execute(
                "SELECT file_path, format, downloaded_at FROM download_cache WHERE track_hash = ?",
                (track_hash,),
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    if os.path.exists(row[0]):
                        return {
                            "file_path": row[0],
                            "format": row[1],
                            "downloaded_at": row[2],
                        }
                    await conn.execute(
                        "DELETE FROM download_cache WHERE track_hash = ?", (track_hash,)
                    )
                    await conn.commit()
                    logger.warning(f"Pruned stale cache entry: {track_hash}")
            return None
        finally:
            await conn.close()

    async def add(self, track_hash: str, file_path: str, fmt: str) -> None:
        conn = await db.get_connection()
        try:
            await conn.execute(
                "INSERT OR REPLACE INTO download_cache (track_hash, file_path, format) VALUES (?, ?, ?)",
                (track_hash, file_path, fmt),
            )
            await conn.commit()
        finally:
            await conn.close()


class ImageCache:
    def __init__(self):
        self.poster_dir = POSTERS_CACHE_DIR
        self.cover_dir = COVERS_CACHE_DIR

    async def get_or_download(self, url: str, category: str) -> Optional[str]:
        if not url:
            return None
        target_dir = self.poster_dir if category == "poster" else self.cover_dir
        url_hash = hashlib.md5(url.encode("utf-8")).hexdigest()
        ext = "png"
        clean_url = url.split("?")[0]
        if "." in clean_url:
            potential = clean_url.rsplit(".", 1)[-1].lower()
            if potential in ("jpg", "jpeg", "png", "webp"):
                ext = potential
        local_path = target_dir / f"{url_hash}.{ext}"
        if local_path.exists():
            return str(local_path)
        headers = {
            "User-Agent": "MovieSongDownloader/2.0 (contact: nandha.dev@gmail.com)"
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url, headers=headers)
                if resp.status_code == 200:
                    with open(local_path, "wb") as f:
                        f.write(resp.content)
                    return str(local_path)
                logger.warning(f"Image download HTTP {resp.status_code}: {url}")
        except Exception as e:
            logger.error(f"Image download failed: {e}")
        return None


class APICache:
    async def get(self, cache_key: str) -> Optional[dict]:
        conn = await db.get_connection()
        try:
            async with conn.execute(
                "SELECT json_payload, expires_at FROM api_cache WHERE cache_key = ?",
                (cache_key,),
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    if datetime.now() < datetime.fromisoformat(row[1]):
                        try:
                            return json.loads(row[0])
                        except json.JSONDecodeError:
                            logger.error(f"Corrupt cache key: {cache_key}")
                    else:
                        await conn.execute(
                            "DELETE FROM api_cache WHERE cache_key = ?", (cache_key,)
                        )
                        await conn.commit()
            return None
        finally:
            await conn.close()

    async def set(
        self,
        cache_key: str,
        provider: str,
        payload: dict,
        ttl: int = 86400,
        expires_in_seconds: Optional[int] = None,
    ) -> None:
        if expires_in_seconds is not None:
            ttl = expires_in_seconds
        conn = await db.get_connection()
        try:
            expires_at = (datetime.now() + timedelta(seconds=ttl)).isoformat()
            await conn.execute(
                "INSERT OR REPLACE INTO api_cache (cache_key, provider, json_payload, expires_at) VALUES (?, ?, ?, ?)",
                (cache_key, provider, json.dumps(payload), expires_at),
            )
            await conn.commit()
        finally:
            await conn.close()

    async def verify_scraped_data(
        self, cache_key: str, new_data: dict, fields: list
    ) -> dict:
        """Compare freshly scraped data against cached version.
        Returns merged result preferring cached values for stable fields (IDs)
        and new values for volatile fields (ratings, availability)."""
        cached = await self.get(cache_key)
        if cached is None:
            return new_data

        merged = {**cached}
        for field in fields:
            if field in new_data:
                merged[field] = new_data[field]
        return merged


download_cache = DownloadCache()
image_cache = ImageCache()
api_cache = APICache()
```

---

### File: `services/movie_song_downloader/core/database.py`
- **Path:** `services/movie_song_downloader/core/database.py`
- **Estimated Tokens:** 690
- **mtime:** 1780494706.304

```python
import re
import aiosqlite
import logging
from pathlib import Path
from MovieSongDownloader.config import DATABASE_PATH

logger = logging.getLogger("MovieSongDownloader.Database")


class DatabaseManager:
    def __init__(self, db_path: Path = DATABASE_PATH):
        self.db_path = db_path

    async def get_connection(self) -> aiosqlite.Connection:
        conn = await aiosqlite.connect(self.db_path)
        conn.row_factory = aiosqlite.Row
        await conn.execute("PRAGMA journal_mode=WAL;")
        await conn.execute("PRAGMA synchronous=NORMAL;")
        await conn.execute("PRAGMA foreign_keys=ON;")
        return conn

    async def run_migrations(self, max_version: int = 99) -> None:
        migrations_dir = Path(__file__).resolve().parent / "migrations"
        if not migrations_dir.exists():
            logger.warning("Migrations directory not found, skipping.")
            return

        conn = await self.get_connection()
        try:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version INTEGER PRIMARY KEY,
                    applied_at TEXT DEFAULT (datetime('now'))
                );
            """)
            await conn.commit()

            async with conn.execute("SELECT version FROM schema_migrations") as cursor:
                applied_versions = {row[0] for row in await cursor.fetchall()}

            migration_files = []
            for filepath in migrations_dir.glob("*.sql"):
                match = re.match(r"^(\d+)_(.+)\.sql$", filepath.name)
                if match:
                    version = int(match.group(1))
                    migration_files.append((version, filepath))

            migration_files.sort(key=lambda x: x[0])

            for version, filepath in migration_files:
                if version > max_version:
                    continue
                if version not in applied_versions:
                    logger.info(f"Applying migration v{version}: {filepath.name}")
                    try:
                        sql_content = filepath.read_text(encoding="utf-8")
                        await conn.executescript(sql_content)
                        await conn.execute(
                            "INSERT INTO schema_migrations (version) VALUES (?)",
                            (version,),
                        )
                        await conn.commit()
                        logger.info(f"Migration v{version} applied.")
                    except Exception as e:
                        await conn.rollback()
                        logger.error(f"Migration {filepath.name} failed: {e}")
                        raise
        finally:
            await conn.close()


db = DatabaseManager()
```

---

### File: `services/movie_song_downloader/core/dns_resolver.py`
- **Path:** `services/movie_song_downloader/core/dns_resolver.py`
- **Estimated Tokens:** 2,345
- **mtime:** 1780861103.717

```python
import socket
import logging
import ssl
import json
import urllib.request
import httpx
from typing import Dict, Optional

logger = logging.getLogger("MovieSongDownloader.DnsResolver")

_original_getaddrinfo = socket.getaddrinfo
_dns_overrides: Dict[str, str] = {}
_active_doh_url: str = "https://cloudflare-dns.com/dns-query"

DOH_PROVIDERS = {
    "cloudflare": "https://cloudflare-dns.com/dns-query",
    "google": "https://dns.google/dns-query",
    "quad9": "https://dns.quad9.net:5053/dns-query",
}

DOMAINS_TO_RESOLVE = [
    "www.jiosaavn.com",
    "www.omdbapi.com",
]


def _patched_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    """Intercepts DNS lookups for blocked domains, returns DoH-resolved IPs.
    TLS SNI still uses the original hostname so HTTPS works correctly."""
    if host is None:
        return _original_getaddrinfo(host, port, family, type, proto, flags)

    if isinstance(host, bytes):
        host_str = host.decode("utf-8", errors="ignore")
    elif isinstance(host, str):
        host_str = host
    else:
        host_str = str(host)

    clean_host = host_str.rstrip(".")

    # Fast bypass for numeric IPs, localhost, and local network domains
    is_numeric = False
    try:
        # Check if valid IPv4
        socket.inet_aton(clean_host)
        is_numeric = True
    except Exception:
        pass
    if not is_numeric:
        try:
            # Check if valid IPv6
            socket.inet_pton(socket.AF_INET6, clean_host)
            is_numeric = True
        except Exception:
            pass

    is_local = (
        not clean_host
        or clean_host.lower() in ("localhost", "none", "127.0.0.1", "::1", "0.0.0.0")
        or clean_host.endswith(".local")
        or is_numeric
        or "." not in clean_host
    )

    if is_local:
        return _original_getaddrinfo(clean_host, port, family, type, proto, flags)

    resolved = _dns_overrides.get(clean_host)
    if resolved:
        logger.debug(f"DNS override: {clean_host} -> {resolved}")
        try:
            return _original_getaddrinfo(resolved, port, family, type, proto, flags)
        except Exception as e:
            logger.warning(
                f"DNS override original getaddrinfo failed for {resolved}: {e}. Retrying with AI_NUMERICHOST."
            )
            try:
                f = socket.AF_INET if family in (0, socket.AF_INET) else family
                t = type or socket.SOCK_STREAM
                p = proto or socket.IPPROTO_TCP
                return _original_getaddrinfo(
                    resolved, port, f, t, p, socket.AI_NUMERICHOST
                )
            except Exception as e2:
                logger.error(
                    f"DNS override backup getaddrinfo failed for {resolved}: {e2}. Using manual fallback."
                )
                f = socket.AF_INET if family in (0, socket.AF_INET) else family
                t = type or socket.SOCK_STREAM
                p = proto or socket.IPPROTO_TCP
                return [(f, t, p, "", (resolved, port))]

    # For non-overridden hosts, strip trailing dots and attempt system resolution.
    # If the system resolver fails (e.g. Jio/ISP blocks or DNS poisoning), fall back
    # dynamically to DNS-over-HTTPS in real-time.
    try:
        return _original_getaddrinfo(clean_host, port, family, type, proto, flags)
    except Exception as e:
        # Avoid recursive calls if it's the DoH provider domain itself failing
        if (
            clean_host in _dns_overrides
            or "dns-query" in clean_host
            or "cloudflare-dns.com" in clean_host
            or "dns.google" in clean_host
        ):
            raise e

        logger.warning(
            f"System DNS lookup failed for {clean_host}: {e}. Attempting real-time DoH fallback..."
        )
        resolved = _resolve_via_doh_sync(clean_host, _active_doh_url)
        if resolved:
            _dns_overrides[clean_host] = resolved
            logger.info(
                f"Dynamically resolved {clean_host} -> {resolved} via DoH fallback."
            )
            try:
                return _original_getaddrinfo(resolved, port, family, type, proto, flags)
            except Exception as e2:
                logger.warning(
                    "Dynamic DNS override original getaddrinfo failed for %s: %s. "
                    "Retrying with AI_NUMERICHOST.",
                    resolved,
                    e2,
                )
                try:
                    f = socket.AF_INET if family in (0, socket.AF_INET) else family
                    t = type or socket.SOCK_STREAM
                    p = proto or socket.IPPROTO_TCP
                    return _original_getaddrinfo(
                        resolved, port, f, t, p, socket.AI_NUMERICHOST
                    )
                except Exception as e3:
                    logger.error(
                        f"Dynamic DNS override backup getaddrinfo failed for {resolved}: {e3}. Using manual fallback."
                    )
                    f = socket.AF_INET if family in (0, socket.AF_INET) else family
                    t = type or socket.SOCK_STREAM
                    p = proto or socket.IPPROTO_TCP
                    return [(f, t, p, "", (resolved, port))]

        # If DoH resolution fails too, raise the original getaddrinfo exception
        if clean_host != host:
            try:
                return _original_getaddrinfo(host, port, family, type, proto, flags)
            except Exception:
                raise e
        raise e


async def _resolve_via_doh(hostname: str, doh_url: str) -> Optional[str]:
    """Resolves a hostname to an IPv4 address using DNS-over-HTTPS (RFC 8484 JSON)."""
    params = {"name": hostname, "type": "A"}
    headers = {"Accept": "application/dns-json"}
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(doh_url, params=params, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                for answer in data.get("Answer", []):
                    if answer.get("type") == 1:
                        ip = answer["data"]
                        logger.info(f"DoH resolved {hostname} -> {ip}")
                        return ip
    except Exception as e:
        logger.warning(f"DoH resolution failed for {hostname}: {e}")
    return None


async def bootstrap_dns(provider: str = "cloudflare") -> None:
    """Pre-resolves blocked domains via DoH and patches socket.getaddrinfo.
    Call once at app startup before any API requests."""
    global _active_doh_url
    doh_url = DOH_PROVIDERS.get(provider, DOH_PROVIDERS["cloudflare"])
    _active_doh_url = doh_url
    logger.info(f"Bootstrapping DNS via DoH provider: {provider} ({doh_url})")

    for domain in DOMAINS_TO_RESOLVE:
        ip = await _resolve_via_doh(domain, doh_url)
        if ip:
            _dns_overrides[domain] = ip

    if _dns_overrides:
        socket.getaddrinfo = _patched_getaddrinfo
        logger.info(
            f"DNS overrides active for {len(_dns_overrides)} domain(s): {list(_dns_overrides.keys())}"
        )
    else:
        logger.warning(
            "No DNS overrides resolved. Some providers may be unreachable if ISP blocks DNS."
        )


def _resolve_via_doh_sync(hostname: str, doh_url: str) -> Optional[str]:
    """Resolves a hostname to an IPv4 address synchronously using DNS-over-HTTPS."""
    url = f"{doh_url}?name={hostname}&type=A"
    req = urllib.request.Request(url, headers={"Accept": "application/dns-json"})
    try:
        ctx = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=ctx, timeout=5.0) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                for answer in data.get("Answer", []):
                    if answer.get("type") == 1:
                        ip = answer["data"]
                        logger.info(f"DoH resolved {hostname} -> {ip} (sync)")
                        return ip
    except Exception as e:
        logger.warning(f"DoH resolution failed synchronously for {hostname}: {e}")
    return None


def bootstrap_dns_sync(provider: str = "cloudflare") -> None:
    """Pre-resolves blocked domains synchronously via DoH and patches socket.getaddrinfo.
    Call at early startup before any libraries perform DNS lookups."""
    global _active_doh_url
    doh_url = DOH_PROVIDERS.get(provider, DOH_PROVIDERS["cloudflare"])
    _active_doh_url = doh_url
    logger.info(
        f"Synchronously bootstrapping DNS via DoH provider: {provider} ({doh_url})"
    )

    for domain in DOMAINS_TO_RESOLVE:
        ip = _resolve_via_doh_sync(domain, doh_url)
        if ip:
            _dns_overrides[domain] = ip

    if _dns_overrides:
        socket.getaddrinfo = _patched_getaddrinfo
        logger.info(
            f"DNS overrides active for {len(_dns_overrides)} domain(s): {list(_dns_overrides.keys())}"
        )
    else:
        logger.warning(
            "No DNS overrides resolved. Some providers may be unreachable if ISP blocks DNS."
        )


def clear_dns_overrides() -> None:
    """Restores original DNS resolution."""
    _dns_overrides.clear()
    socket.getaddrinfo = _original_getaddrinfo
    logger.info("DNS overrides cleared, restored system resolver.")
```

---

### File: `services/movie_song_downloader/core/event_bus.py`
- **Path:** `services/movie_song_downloader/core/event_bus.py`
- **Estimated Tokens:** 467
- **mtime:** 1780856038.246

```python
import asyncio
import logging
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Any

logger = logging.getLogger("MovieSongDownloader.EventBus")


@dataclass
class Event:
    type: str
    data: Dict[str, Any] = field(default_factory=dict)


class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._lock = asyncio.Lock()

    async def subscribe(self, event_type: str, callback: Callable) -> None:
        async with self._lock:
            self._subscribers.setdefault(event_type, []).append(callback)

    async def unsubscribe(self, event_type: str, callback: Callable) -> None:
        async with self._lock:
            if event_type in self._subscribers:
                try:
                    self._subscribers[event_type].remove(callback)
                except ValueError:
                    pass

    async def publish(self, event: Event) -> None:
        async with self._lock:
            callbacks = list(self._subscribers.get(event.type, []))
        for cb in callbacks:
            try:
                if asyncio.iscoroutinefunction(cb):
                    await cb(event)
                else:
                    cb(event)
            except Exception as e:
                logger.error(f"Callback error for {event.type}: {e}", exc_info=True)

    def publish_fire_and_forget(self, event: Event) -> None:
        callbacks = list(self._subscribers.get(event.type, []))
        for cb in callbacks:
            try:
                if asyncio.iscoroutinefunction(cb):
                    asyncio.create_task(cb(event))
                else:
                    cb(event)
            except Exception as e:
                logger.error(
                    f"Fire-and-forget error for {event.type}: {e}", exc_info=True
                )


event_bus = EventBus()
```

---

### File: `services/movie_song_downloader/core/job_queue.py`
- **Path:** `services/movie_song_downloader/core/job_queue.py`
- **Estimated Tokens:** 1,943
- **mtime:** 1780861103.717

```python
import asyncio
import logging
from typing import Optional, List, Dict
from MovieSongDownloader.core.database import db
from MovieSongDownloader.core.models import DownloadJob
from MovieSongDownloader.core.event_bus import event_bus, Event
from MovieSongDownloader.config import DOWNLOADS_LOG_PATH

downloads_logger = logging.getLogger("MovieSongDownloader.Downloads")
if not downloads_logger.handlers:
    handler = logging.FileHandler(DOWNLOADS_LOG_PATH, encoding="utf-8")
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    downloads_logger.addHandler(handler)
    downloads_logger.setLevel(logging.INFO)

_JOBS_JOIN_QUERY = """
    SELECT j.id, j.track_id, j.status, j.progress, j.output_path, j.format,
           j.error_message, j.retry_count,
           t.title, t.artist, a.title, m.title, a.cover_cached_path
    FROM download_jobs j
    JOIN tracks t ON j.track_id = t.id
    JOIN albums a ON t.album_id = a.id
    JOIN movies m ON a.movie_id = m.id
"""


def _row_to_job(row) -> DownloadJob:
    return DownloadJob(
        id=row[0],
        track_id=row[1],
        status=row[2],
        progress=row[3],
        output_path=row[4],
        format=row[5],
        error_message=row[6],
        retry_count=row[7],
        track_title=row[8],
        track_artist=row[9],
        album_title=row[10],
        movie_title=row[11],
        cover_cached_path=row[12],
    )


class JobQueue:
    def __init__(self):
        self._active_tasks: Dict[int, asyncio.Task] = {}
        self._lock = asyncio.Lock()

    async def enqueue(self, track_id: int, format: str = "mp3") -> int:
        conn = await db.get_connection()
        try:
            cursor = await conn.execute(
                "INSERT INTO download_jobs (track_id, format, status, progress) VALUES (?, ?, 'queued', 0.0)",
                (track_id, format),
            )
            job_id = cursor.lastrowid
            await conn.commit()
            downloads_logger.info(
                f"Enqueued job {job_id} for track {track_id} ({format})"
            )
            async with conn.execute(
                "SELECT title FROM tracks WHERE id = ?", (track_id,)
            ) as c:
                r = await c.fetchone()
                title = r[0] if r else f"Track {track_id}"
            event_bus.publish_fire_and_forget(
                Event("job.queued", {"job_id": job_id, "track_title": title})
            )
            return job_id
        finally:
            await conn.close()

    async def dequeue(self) -> Optional[DownloadJob]:
        conn = await db.get_connection()
        try:
            query = (
                _JOBS_JOIN_QUERY
                + " WHERE j.status = 'queued' ORDER BY j.created_at ASC LIMIT 1"
            )
            async with conn.execute(query) as cursor:
                row = await cursor.fetchone()
                return _row_to_job(row) if row else None
        finally:
            await conn.close()

    async def update_progress(self, job_id: int, progress: float, status: str) -> None:
        conn = await db.get_connection()
        try:
            await conn.execute(
                "UPDATE download_jobs SET progress=?, status=?, updated_at=datetime('now') WHERE id=?",
                (progress, status, job_id),
            )
            await conn.commit()
            event_bus.publish_fire_and_forget(
                Event(
                    "job.progress",
                    {
                        "job_id": job_id,
                        "progress": progress,
                        "status": status,
                    },
                )
            )
        finally:
            await conn.close()

    async def mark_completed(self, job_id: int, output_path: str) -> None:
        conn = await db.get_connection()
        try:
            await conn.execute(
                "UPDATE download_jobs SET progress=100.0, status='completed', output_path=?, "
                "error_message=NULL, updated_at=datetime('now') WHERE id=?",
                (output_path, job_id),
            )
            await conn.commit()
            downloads_logger.info(f"Job {job_id} completed -> {output_path}")
            event_bus.publish_fire_and_forget(
                Event("job.completed", {"job_id": job_id, "output_path": output_path})
            )
        finally:
            await conn.close()

    async def mark_failed(self, job_id: int, error: str) -> None:
        conn = await db.get_connection()
        try:
            await conn.execute(
                "UPDATE download_jobs SET status='failed', error_message=?, "
                "retry_count=retry_count+1, updated_at=datetime('now') WHERE id=?",
                (error, job_id),
            )
            await conn.commit()
            downloads_logger.error(f"Job {job_id} failed: {error}")
            event_bus.publish_fire_and_forget(
                Event("job.failed", {"job_id": job_id, "error": error})
            )
        finally:
            await conn.close()

    async def pause(self, job_id: int) -> None:
        conn = await db.get_connection()
        try:
            await conn.execute(
                "UPDATE download_jobs SET status='paused', updated_at=datetime('now') WHERE id=? AND status='queued'",
                (job_id,),
            )
            await conn.commit()
            event_bus.publish_fire_and_forget(
                Event(
                    "job.progress",
                    {"job_id": job_id, "progress": 0.0, "status": "paused"},
                )
            )
        finally:
            await conn.close()

    async def resume(self, job_id: int) -> None:
        conn = await db.get_connection()
        try:
            await conn.execute(
                "UPDATE download_jobs SET status='queued', updated_at=datetime('now') "
                "WHERE id=? AND status IN ('paused','failed','cancelled')",
                (job_id,),
            )
            await conn.commit()
            event_bus.publish_fire_and_forget(
                Event(
                    "job.progress",
                    {"job_id": job_id, "progress": 0.0, "status": "queued"},
                )
            )
        finally:
            await conn.close()

    async def cancel(self, job_id: int) -> None:
        conn = await db.get_connection()
        try:
            await conn.execute(
                "UPDATE download_jobs SET status='cancelled', updated_at=datetime('now') WHERE id=?",
                (job_id,),
            )
            await conn.commit()
            downloads_logger.info(f"Cancelled job {job_id}")
            async with self._lock:
                task = self._active_tasks.get(job_id)
            if task and not task.done():
                task.cancel()
            event_bus.publish_fire_and_forget(
                Event(
                    "job.progress",
                    {"job_id": job_id, "progress": 0.0, "status": "cancelled"},
                )
            )
        finally:
            await conn.close()

    async def register_task(self, job_id: int, task: asyncio.Task) -> None:
        async with self._lock:
            self._active_tasks[job_id] = task

    async def unregister_task(self, job_id: int) -> None:
        async with self._lock:
            self._active_tasks.pop(job_id, None)

    async def get_all_jobs(self) -> List[DownloadJob]:
        conn = await db.get_connection()
        try:
            query = _JOBS_JOIN_QUERY + " ORDER BY j.created_at DESC"
            async with conn.execute(query) as cursor:
                return [_row_to_job(row) for row in await cursor.fetchall()]
        finally:
            await conn.close()


job_queue = JobQueue()
```

---

### File: `services/movie_song_downloader/core/migrations/001_initial.sql`
- **Path:** `services/movie_song_downloader/core/migrations/001_initial.sql`
- **Estimated Tokens:** 1,074
- **mtime:** 1780401662.737

```sql
-- Migration: 001_initial
-- Date: 2026-06-02

-- Create schema_migrations tracker
CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY,
    applied_at TEXT DEFAULT (datetime('now'))
);

-- Movies Business Data
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tmdb_id INTEGER UNIQUE NOT NULL,
    title TEXT NOT NULL,
    year INTEGER,
    poster_url TEXT,
    poster_cached_path TEXT,
    overview TEXT,
    language TEXT,
    genres TEXT,          -- JSON Array of string
    ott_providers TEXT,   -- JSON Array of dicts
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_movies_tmdb ON movies(tmdb_id);
CREATE INDEX IF NOT EXISTS idx_movies_year ON movies(year);

-- Albums Business Data
CREATE TABLE IF NOT EXISTS albums (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
    spotify_id TEXT UNIQUE,
    title TEXT NOT NULL,
    artist TEXT,
    cover_url TEXT,
    cover_cached_path TEXT,
    total_tracks INTEGER,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_albums_spotify ON albums(spotify_id);
CREATE INDEX IF NOT EXISTS idx_albums_movie ON albums(movie_id);

-- Tracks Business Data
CREATE TABLE IF NOT EXISTS tracks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    album_id INTEGER REFERENCES albums(id) ON DELETE CASCADE,
    spotify_id TEXT UNIQUE,
    title TEXT NOT NULL,
    artist TEXT,
    duration_ms INTEGER,
    track_number INTEGER,
    preview_url TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_tracks_spotify ON tracks(spotify_id);
CREATE INDEX IF NOT EXISTS idx_tracks_album ON tracks(album_id);

-- Download Job Queue
CREATE TABLE IF NOT EXISTS download_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    track_id INTEGER REFERENCES tracks(id) ON DELETE CASCADE,
    status TEXT NOT NULL DEFAULT 'queued', -- queued, downloading, fetching_lyrics, embedding_cover, embedding_metadata, saving_lrc, generating_playlist, completed, failed, paused, cancelled
    progress REAL DEFAULT 0.0,
    output_path TEXT,
    format TEXT DEFAULT 'mp3',
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON download_jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_track ON download_jobs(track_id);

-- Lyrics Fallback Output Results
CREATE TABLE IF NOT EXISTS lyrics_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    track_id INTEGER REFERENCES tracks(id) ON DELETE CASCADE,
    provider TEXT,        -- lrclib | syncedlyrics | musixmatch | genius
    lyrics_type TEXT,     -- synced | plain | none
    content TEXT,
    confidence REAL,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_lyrics_track ON lyrics_results(track_id);

-- Watchlist tracker
CREATE TABLE IF NOT EXISTS watchlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tmdb_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    expected_release TEXT,
    last_checked TEXT,
    auto_download INTEGER DEFAULT 1,
    status TEXT DEFAULT 'watching', -- watching | found | downloaded | expired
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_watchlist_tmdb ON watchlist(tmdb_id);

-- Settings Key-Value Configuration Store
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    category TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_settings_category ON settings(category);

-- Download Deduplication Cache
CREATE TABLE IF NOT EXISTS download_cache (
    track_hash TEXT PRIMARY KEY, -- SHA256(artist + title + album + duration)
    file_path TEXT NOT NULL,
    format TEXT NOT NULL,
    downloaded_at TEXT DEFAULT (datetime('now'))
);

-- Raw API Response Cache (Metadata cache decoupling)
CREATE TABLE IF NOT EXISTS api_cache (
    cache_key TEXT PRIMARY KEY,
    provider TEXT NOT NULL,
    json_payload TEXT NOT NULL,
    expires_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_api_cache_expires ON api_cache(expires_at);
CREATE INDEX IF NOT EXISTS idx_api_cache_provider ON api_cache(provider);
```

---

### File: `services/movie_song_downloader/core/migrations/002_provider_health.sql`
- **Path:** `services/movie_song_downloader/core/migrations/002_provider_health.sql`
- **Estimated Tokens:** 95
- **mtime:** 1780401669.059

```sql
-- Migration: 002_provider_health
-- Date: 2026-06-02

CREATE TABLE IF NOT EXISTS provider_health (
    provider TEXT NOT NULL,
    category TEXT NOT NULL,      -- movie | soundtrack | lyrics | download
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    total_latency_ms INTEGER DEFAULT 0,
    last_checked TEXT,
    PRIMARY KEY (provider, category)
);
```

---

### File: `services/movie_song_downloader/core/migrations/003_cache.sql`
- **Path:** `services/movie_song_downloader/core/migrations/003_cache.sql`
- **Estimated Tokens:** 75
- **mtime:** 1780401673.784

```sql
-- Migration: 003_cache
-- Date: 2026-06-02

-- Unified search index virtual table (FTS5)
CREATE VIRTUAL TABLE IF NOT EXISTS search_index USING fts5(
    source,        -- tmdb | spotify
    source_id,     -- external ID
    title,
    artist,
    year,
    type           -- movie | album | track
);
```

---

### File: `services/movie_song_downloader/core/migrations/004_scraper_sources.sql`
- **Path:** `services/movie_song_downloader/core/migrations/004_scraper_sources.sql`
- **Estimated Tokens:** 213
- **mtime:** 1780494673.786

```sql
-- Migration: 004_scraper_sources
-- Date: 2026-06-03
-- Adds source tracking columns for Wikipedia/JioSaavn/OMDb migration

-- Movies: add source tracking + enrichment fields
ALTER TABLE movies ADD COLUMN source TEXT DEFAULT 'wikipedia';
ALTER TABLE movies ADD COLUMN source_id TEXT DEFAULT '';
ALTER TABLE movies ADD COLUMN rating TEXT;
ALTER TABLE movies ADD COLUMN cast_info TEXT;

-- Albums: add source tracking
ALTER TABLE albums ADD COLUMN source TEXT DEFAULT 'jiosaavn';
ALTER TABLE albums ADD COLUMN source_id TEXT DEFAULT '';

-- Tracks: add source tracking + direct download URL
ALTER TABLE tracks ADD COLUMN source TEXT DEFAULT 'jiosaavn';
ALTER TABLE tracks ADD COLUMN source_id TEXT DEFAULT '';
ALTER TABLE tracks ADD COLUMN download_url TEXT;

-- Watchlist: add generic source_id
ALTER TABLE watchlist ADD COLUMN source_id TEXT DEFAULT '';
```

---

### File: `services/movie_song_downloader/core/migrations/005_release_date_enrichment.sql`
- **Path:** `services/movie_song_downloader/core/migrations/005_release_date_enrichment.sql`
- **Estimated Tokens:** 67
- **mtime:** 1780513434.911

```sql
-- Migration: 005_release_date_enrichment
-- Date: 2026-06-04
-- Adds release_date to movies, composer to albums, and isrc to tracks

ALTER TABLE movies ADD COLUMN release_date TEXT;
ALTER TABLE albums ADD COLUMN composer TEXT;
ALTER TABLE tracks ADD COLUMN isrc TEXT;
```

---

### File: `services/movie_song_downloader/core/models.py`
- **Path:** `services/movie_song_downloader/core/models.py`
- **Estimated Tokens:** 694
- **mtime:** 1780856038.25

```python
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Movie:
    id: Optional[int] = None
    tmdb_id: int = 0  # Legacy, kept for backward compat
    source: str = "wikipedia"  # "wikipedia" | "omdb" | "tmdb"
    source_id: str = ""  # Wikipedia page ID or OMDb imdbID
    title: str = ""
    year: Optional[int] = None
    poster_url: Optional[str] = None
    poster_cached_path: Optional[str] = None
    overview: Optional[str] = None
    language: Optional[str] = None
    rating: Optional[str] = None  # IMDb rating from OMDb
    cast_info: Optional[str] = None  # Comma-separated top cast
    release_date: Optional[str] = None
    genres: List[str] = field(default_factory=list)
    ott_providers: List[dict] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Album:
    id: Optional[int] = None
    movie_id: Optional[int] = None
    spotify_id: Optional[str] = None  # Legacy
    source: str = "jiosaavn"  # "jiosaavn" | "spotify"
    source_id: str = ""  # JioSaavn album ID
    title: str = ""
    artist: Optional[str] = None
    cover_url: Optional[str] = None
    cover_cached_path: Optional[str] = None
    total_tracks: Optional[int] = None
    composer: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class Track:
    id: Optional[int] = None
    album_id: Optional[int] = None
    spotify_id: Optional[str] = None  # Legacy
    source: str = "jiosaavn"  # "jiosaavn" | "spotify"
    source_id: str = ""  # JioSaavn track ID
    title: str = ""
    artist: Optional[str] = None
    duration_ms: int = 0
    track_number: int = 0
    preview_url: Optional[str] = None
    download_url: Optional[str] = None  # Direct stream URL from JioSaavn
    isrc: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class DownloadJob:
    id: Optional[int] = None
    track_id: int = 0
    status: str = "queued"
    progress: float = 0.0
    output_path: Optional[str] = None
    format: str = "mp3"
    error_message: Optional[str] = None
    retry_count: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    # Joined metadata for UI display
    track_title: Optional[str] = None
    track_artist: Optional[str] = None
    album_title: Optional[str] = None
    movie_title: Optional[str] = None
    cover_cached_path: Optional[str] = None


@dataclass
class WatchlistItem:
    id: Optional[int] = None
    tmdb_id: int = 0  # Legacy, kept for backward compat
    source_id: str = ""
    title: str = ""
    expected_release: Optional[str] = None
    last_checked: Optional[str] = None
    auto_download: bool = True
    status: str = "watching"
    created_at: Optional[str] = None
```

---

### File: `services/movie_song_downloader/core/rate_limiter.py`
- **Path:** `services/movie_song_downloader/core/rate_limiter.py`
- **Estimated Tokens:** 463
- **mtime:** 1780856038.252

```python
import asyncio
import time
import logging
from MovieSongDownloader.config import PROVIDERS_LOG_PATH

providers_logger = logging.getLogger("MovieSongDownloader.Providers")
if not providers_logger.handlers:
    handler = logging.FileHandler(PROVIDERS_LOG_PATH, encoding="utf-8")
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    providers_logger.addHandler(handler)
    providers_logger.setLevel(logging.INFO)


class RateLimiter:
    def __init__(self, rps: float, name: str):
        self.delay = 1.0 / rps if rps > 0 else 0.0
        self.last_called = 0.0
        self.name = name
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        if self.delay <= 0:
            return
        async with self._lock:
            now = time.time()
            wait = self.delay - (now - self.last_called)
            if wait > 0:
                providers_logger.debug(
                    f"provider={self.name} rate_limit sleep_ms={int(wait * 1000)}"
                )
                await asyncio.sleep(wait)
            self.last_called = time.time()


class GlobalRateLimiters:
    def __init__(self):
        self._limiters = {
            "wikipedia": RateLimiter(5.0, "wikipedia"),
            "jiosaavn": RateLimiter(2.0, "jiosaavn"),
            "omdb": RateLimiter(3.0, "omdb"),
            "lyrics": RateLimiter(2.0, "lyrics"),
            "deezspot": RateLimiter(1.0, "deezspot"),
        }
        self._lock = asyncio.Lock()

    async def acquire(self, provider: str) -> None:
        key = provider.lower()
        async with self._lock:
            if key not in self._limiters:
                self._limiters[key] = RateLimiter(2.0, key)
            limiter = self._limiters[key]
        await limiter.acquire()


rate_limiter = GlobalRateLimiters()
```

---

### File: `services/movie_song_downloader/core/settings_manager.py`
- **Path:** `services/movie_song_downloader/core/settings_manager.py`
- **Estimated Tokens:** 1,018
- **mtime:** 1780856038.255

```python
import json
import logging
from pathlib import Path
from MovieSongDownloader.config import SETTINGS_BACKUP_PATH, DEFAULT_SETTINGS
from MovieSongDownloader.core.database import db

logger = logging.getLogger("MovieSongDownloader.SettingsManager")

CATEGORY_MAP = {
    "tmdb_api_key": "api",
    "tmdb_base_url": "api",
    "spotify_client_id": "api",
    "spotify_client_secret": "api",
    "deezer_arl": "api",
    "audio_format": "download",
    "bitrate": "download",
    "output_dir": "download",
    "filename_format": "download",
    "folder_format": "download",
    "download_mode": "download",
    "max_concurrent": "download",
    "lyrics_priority": "lyrics",
    "save_lrc_file": "lyrics",
    "embed_lyrics": "lyrics",
    "theme": "ui",
    "default_tab": "ui",
    "language_region": "ui",
    "check_interval_hours": "watchlist",
    "auto_download": "watchlist",
    "notify_on_found": "watchlist",
    "last_fetch_date": "watchlist",
    "doh_enabled": "network",
    "dns_provider": "network",
}


def _get_category(key: str) -> str:
    return CATEGORY_MAP.get(key, "ui")


class SettingsManager:
    def __init__(self, backup_path: Path = SETTINGS_BACKUP_PATH):
        self.backup_path = backup_path

    async def get_all(self) -> dict:
        conn = await db.get_connection()
        try:
            async with conn.execute("SELECT key, value FROM settings") as cursor:
                rows = await cursor.fetchall()
            if not rows:
                logger.warning("Settings empty. Attempting backup restore...")
                restored = await self.restore_from_backup()
                if not restored:
                    logger.info("Seeding defaults...")
                    await self._seed_defaults(conn)
                    restored = DEFAULT_SETTINGS.copy()
                else:
                    await self._save_many_to_conn(conn, restored)
                return restored
            return {row[0]: row[1] for row in rows}
        finally:
            await conn.close()

    async def get(self, key: str) -> str:
        all_s = await self.get_all()
        return all_s.get(key, DEFAULT_SETTINGS.get(key, ""))

    async def set(self, key: str, value: str) -> None:
        conn = await db.get_connection()
        try:
            await conn.execute(
                "INSERT OR REPLACE INTO settings (key, value, category) VALUES (?, ?, ?)",
                (key, str(value), _get_category(key)),
            )
            await conn.commit()
            updated = await self.get_all()
            await self.export_backup(updated)
        finally:
            await conn.close()

    async def save_many(self, settings_dict: dict) -> None:
        conn = await db.get_connection()
        try:
            await self._save_many_to_conn(conn, settings_dict)
            updated = await self.get_all()
            await self.export_backup(updated)
        finally:
            await conn.close()

    async def _save_many_to_conn(self, conn, data: dict) -> None:
        for k, v in data.items():
            await conn.execute(
                "INSERT OR REPLACE INTO settings (key, value, category) VALUES (?, ?, ?)",
                (k, str(v), _get_category(k)),
            )
        await conn.commit()

    async def _seed_defaults(self, conn) -> None:
        await self._save_many_to_conn(conn, DEFAULT_SETTINGS)
        await self.export_backup(DEFAULT_SETTINGS)

    async def export_backup(self, data: dict) -> None:
        try:
            with open(self.backup_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logger.error(f"Backup export failed: {e}")

    async def restore_from_backup(self) -> dict:
        if not self.backup_path.exists():
            return {}
        try:
            with open(self.backup_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Backup restore failed: {e}")
            return {}


settings_manager = SettingsManager()
```

---

### File: `services/movie_song_downloader/dev_run.ps1`
- **Path:** `services/movie_song_downloader/dev_run.ps1`
- **Estimated Tokens:** 86
- **mtime:** 1780923522.093

```powershell
param(
    [int]$port = 8555
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:FLET_WEB_PORT = "$port"
Write-Host "Starting MovieSongDownloader in DEVELOPMENT mode with hot reload"
Start-Process -NoNewWindow -FilePath python -ArgumentList "MovieSongDownloader/main.py"
Start-Sleep -Seconds 4
Start-Process "http://127.0.0.1:$port"
```

---

### File: `services/movie_song_downloader/main.py`
- **Path:** `services/movie_song_downloader/main.py`
- **Estimated Tokens:** 2,011
- **mtime:** 1781124203.228

```python
# MovieSongDownloader/main.py

import argparse
import importlib
import os
import signal
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path

from importlib.abc import MetaPathFinder

sub_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.dirname(os.path.dirname(sub_dir))
services_dir = os.path.join(workspace_root, "services")

# Remove subdirectory from path to avoid package naming collision
if sub_dir in sys.path:
    sys.path.remove(sub_dir)

# Add workspace root and services directory to path
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)
if services_dir not in sys.path:
    sys.path.insert(0, services_dir)

# Register Redirector so MovieSongDownloader -> movie_song_downloader works seamlessly
class MovieSongDownloaderRedirector(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname.startswith("MovieSongDownloader"):
            real_name = fullname.replace("MovieSongDownloader", "movie_song_downloader", 1)
            mod = importlib.import_module(real_name)
            sys.modules[fullname] = mod
            return mod.__spec__
        return None

sys.meta_path.insert(0, MovieSongDownloaderRedirector())

# Import shared config loader from root
from config.loader import load_config, load_env  # noqa: E402

# Import MovieSongDownloader package first to trigger early DNS override bootstrap inside __init__.py
import MovieSongDownloader  # noqa: F401, E402


class DevConfigWatcher:
    def __init__(self, root_dir: Path, callback):
        self.root_dir = root_dir
        self.callback = callback
        self.files = [self.root_dir.parent / ".env", self.root_dir / "rxconfig.py"]
        self.mod_times = {path: path.stat().st_mtime for path in self.files if path.exists()}
        self.running = True

    def watch(self):
        while self.running:
            for path in self.files:
                if path.exists():
                    mtime = path.stat().st_mtime
                    if self.mod_times.get(path) != mtime:
                        self.mod_times[path] = mtime
                        self.callback(path)
            time.sleep(2)

    def stop(self):
        self.running = False


def apply_env_from_config(root_dir: Path):
    runtime = load_config()
    env_settings = runtime.get("app", {})
    os.environ.setdefault("FLET_WEB_PORT", str(env_settings.get("flet_port", 8555)))
    os.environ.setdefault("ENV", env_settings.get("env", "dev"))
    env_file = root_dir.parent / ".env"
    for key, value in load_env(env_file).items():
        if key not in os.environ:
            os.environ[key] = value


def reload_rxconfig(root_dir: Path):
    try:
        import rxconfig

        importlib.reload(rxconfig)
        print("Reloaded rxconfig.py", flush=True)
    except Exception as exc:
        print(f"Failed to reload rxconfig: {exc}", file=sys.stderr, flush=True)


def is_port_free(port: int) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("0.0.0.0", port))
        return True
    except OSError:
        return False


def find_free_port(start_port: int = 8555, max_port: int = 8600) -> int:
    for port in range(start_port, max_port + 1):
        if is_port_free(port):
            return port
    raise RuntimeError(f"No free ports found between {start_port} and {max_port}")


def get_processes_on_port(port: int) -> list[int]:
    try:
        import psutil
    except ImportError:
        return []

    pids = set()
    for conn in psutil.net_connections(kind="inet"):
        if conn.laddr and conn.laddr.port == port and conn.pid and conn.pid != os.getpid():
            pids.add(conn.pid)
    return sorted(pids)


def kill_process(pid: int) -> bool:
    try:
        import psutil
        proc = psutil.Process(pid)
        proc.terminate()
        proc.wait(timeout=3)
        return True
    except Exception:
        pass

    if sys.platform.startswith("win"):
        try:
            subprocess.run(
                ["taskkill", "/PID", str(pid), "/F", "/T"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except Exception:
            return False

    try:
        os.kill(pid, signal.SIGTERM)
        return True
    except Exception:
        return False


def release_port(port: int) -> bool:
    if is_port_free(port):
        return True

    pids = get_processes_on_port(port)
    if not pids:
        return False

    killed = []
    for pid in pids:
        if kill_process(pid):
            killed.append(pid)

    if killed:
        print(
            f"Stopped existing process(es) {', '.join(str(pid) for pid in killed)} "
            f"using port {port}",
            flush=True,
        )
        time.sleep(1)

    return is_port_free(port)


def main():
    root_dir = Path(__file__).resolve().parent
    repo_root = root_dir.parent
    print(f"Launching Reflex App from workspace root: {repo_root}", flush=True)

    apply_env_from_config(root_dir)
    parser = argparse.ArgumentParser(description="Movie Song Downloader launcher")
    parser.add_argument("--env", choices=["dev", "prod"], default="dev")
    parser.add_argument("--frontend-port", dest="frontend_port", default=os.environ.get("FLET_WEB_PORT"))
    args, extra_args = parser.parse_known_args(sys.argv[1:])

    requested_port = int(args.frontend_port) if args.frontend_port else None
    frontend_port = requested_port
    if requested_port is None:
        configured_port = int(os.environ.get("FLET_WEB_PORT", 8555))
        if is_port_free(configured_port):
            frontend_port = configured_port
        elif release_port(configured_port):
            frontend_port = configured_port
        else:
            fallback_port = find_free_port(configured_port + 1)
            print(
                f"Configured port {configured_port} is unavailable, using fallback port {fallback_port}",
                flush=True,
            )
            frontend_port = fallback_port
    else:
        if not is_port_free(requested_port):
            if release_port(requested_port):
                frontend_port = requested_port
            else:
                fallback_port = find_free_port(requested_port + 1)
                print(
                    f"Requested port {requested_port} is unavailable and could not be released, using fallback port {fallback_port}",
                    flush=True,
                )
                frontend_port = fallback_port

    cmd = ["reflex", "run"]
    if frontend_port:
        cmd.extend(["--frontend-port", str(frontend_port)])
    if args.env == "prod":
        cmd.append("--env")
        cmd.append("prod")
    cmd.extend(extra_args)

    if args.env == "dev":
        def on_config_change(path: Path):
            if path.name == ".env":
                apply_env_from_config(root_dir)
                print("Reloaded .env settings", flush=True)
            elif path.name == "rxconfig.py":
                reload_rxconfig(root_dir)

        watcher = DevConfigWatcher(root_dir, on_config_change)
        watcher_thread = threading.Thread(target=watcher.watch, daemon=True)
        watcher_thread.start()

    print(f"Running command: {' '.join(cmd)}", flush=True)
    try:
        env = os.environ.copy()
        env["PYTHONPATH"] = f"{workspace_root}{os.pathsep}{services_dir}{os.pathsep}{env.get('PYTHONPATH', '')}"
        subprocess.run(cmd, cwd=repo_root, env=env, check=True)
    except KeyboardInterrupt:
        print("\nExiting Reflex Application...", flush=True)
    except subprocess.CalledProcessError as exc:
        print(f"Reflex exited with {exc.returncode}", file=sys.stderr, flush=True)
        sys.exit(exc.returncode)
    finally:
        if args.env == "dev":
            watcher.stop()


if __name__ == "__main__":
    main()
```

---

### File: `services/movie_song_downloader/movie.json`
- **Path:** `services/movie_song_downloader/movie.json`
- **Estimated Tokens:** 214
- **mtime:** 1780556746.662

```json
{
    "tmdb_id": 3574151120,
    "title": "Karuppu",
    "year": 2026,
    "overview": "Karuppu (transl.\u2009Black) is a 2026 Indian Tamil-language fantasy action film directed by RJ Balaji from a screenplay he co-wrote with Rathna Kumar, Ashwin Ravichandran, Rahul Raj, T. S. Gopi Krishnan and Karan Aravind Kumar. Produced by Dream Warrior Pictures, the film stars Suriya, Trisha Krishnan and Balaji, alongside Indrans, Natty Subramaniam, Swasika, Sshivada and Supreeth Reddy. In the film, the guardian deity Vettai Karuppu disguises himself as a lawyer to fight corruption in a court syste",
    "language": "ta",
    "genres": [],
    "ott_providers": [
        {
            "id": 2,
            "name": "Amazon Prime"
        },
        {
            "id": 6,
            "name": "Aha"
        }
    ],
    "exported_at": "2026-06-04T12:35:46.659080"
}
```

---

### File: `services/movie_song_downloader/playlist.m3u`
- **Path:** `services/movie_song_downloader/playlist.m3u`
- **Estimated Tokens:** 19
- **mtime:** 1780556746.673

```
#EXTM3U
#PLAYLIST:Karuppu (Original Motion Picture Soundtrack)

Unknown.mp3
```

---

### File: `services/movie_song_downloader/providers/__init__.py`
- **Path:** `services/movie_song_downloader/providers/__init__.py`
- **Estimated Tokens:** 4
- **mtime:** 1780474576.991

```python
# Providers Module
```

---

### File: `services/movie_song_downloader/providers/base.py`
- **Path:** `services/movie_song_downloader/providers/base.py`
- **Estimated Tokens:** 420
- **mtime:** 1780856038.259

```python
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Callable
from MovieSongDownloader.core.models import Movie, Album, Track


class BaseMovieProvider(ABC):
    @abstractmethod
    async def search(self, query: str, **filters) -> List[Movie]:
        pass

    @abstractmethod
    async def get_today_releases(self, region: str = "IN") -> List[Movie]:
        pass

    @abstractmethod
    async def get_watch_providers(
        self, source_id: str, region: str = "IN"
    ) -> List[dict]:
        pass


class BaseSoundtrackProvider(ABC):
    @abstractmethod
    async def get_soundtrack(
        self, movie_title: str, year: Optional[int] = None
    ) -> List[Album]:
        pass


class BaseDownloadProvider(ABC):
    @abstractmethod
    async def download(
        self,
        track: Track,
        format: str,
        output_dir: str,
        filename_template: str,
        on_progress: Optional[Callable[[float, str], None]] = None,
    ) -> str:
        pass


class BaseLyricsProvider(ABC):
    @abstractmethod
    async def fetch(self, title: str, artist: str) -> Tuple[Optional[str], str]:
        pass


class BaseTaggingProvider(ABC):
    @abstractmethod
    async def embed_cover(self, file_path: str, image_path: str) -> None:
        pass

    @abstractmethod
    async def embed_lyrics(
        self, file_path: str, lyrics_content: str, is_synced: bool = False
    ) -> None:
        pass

    @abstractmethod
    async def embed_metadata(
        self,
        file_path: str,
        title: str,
        artist: str,
        album: str,
        year: Optional[int] = None,
        track_num: int = 1,
    ) -> None:
        pass
```

---

### File: `services/movie_song_downloader/providers/deezspot_provider.py`
- **Path:** `services/movie_song_downloader/providers/deezspot_provider.py`
- **Estimated Tokens:** 1,030
- **mtime:** 1780856038.261

```python
import os
import sys
import httpx
import logging
import asyncio
from typing import Optional, Callable

if "youtube_dl" not in sys.modules:
    import yt_dlp

    sys.modules["youtube_dl"] = yt_dlp

bin_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bin"
)
if bin_dir not in os.environ.get("PATH", ""):
    os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")

import deezload.base  # noqa: E402

if not getattr(deezload.base.extract_video_id, "__patched__", False):
    _orig = deezload.base.extract_video_id

    def _patched(qs: str):
        try:
            qs = qs.encode("utf-8").decode("unicode-escape")
        except Exception:
            pass
        qs = qs.replace(r"\u0026", "&").replace("\\u0026", "&")
        return _orig(qs)

    _patched.__patched__ = True
    deezload.base.extract_video_id = _patched

from MovieSongDownloader.providers.base import BaseDownloadProvider  # noqa: E402
from MovieSongDownloader.core.models import Track  # noqa: E402
from MovieSongDownloader.core.rate_limiter import rate_limiter  # noqa: E402

logger = logging.getLogger("MovieSongDownloader.DeezspotProvider")


class DeezspotProvider(BaseDownloadProvider):
    async def _resolve_deezer_id(self, title: str, artist: str) -> Optional[int]:
        await rate_limiter.acquire("lyrics")
        clean_title = title.replace('"', "").replace("'", "")
        clean_artist = artist.split(",")[0].strip()
        url = "https://api.deezer.com/search"

        for params in [
            {"q": f'track:"{clean_title}" artist:"{clean_artist}"'},
            {"q": f"{clean_artist} {clean_title}"},
        ]:
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.get(url, params=params)
                    if resp.status_code == 200:
                        data = resp.json()
                        if data.get("data"):
                            return data["data"][0]["id"]
            except Exception as e:
                logger.error(f"Deezer search error: {e}")
        return None

    async def download(
        self,
        track: Track,
        format: str,
        output_dir: str,
        filename_template: str,
        on_progress: Optional[Callable[[float, str], None]] = None,
    ) -> str:
        deezer_id = await self._resolve_deezer_id(track.title, track.artist)
        if not deezer_id:
            raise Exception(
                f"Could not resolve '{track.title}' by '{track.artist}' on Deezer."
            )

        deezer_url = f"https://www.deezer.com/track/{deezer_id}"
        await rate_limiter.acquire("deezspot")
        logger.info(f"Downloading Deezer ID {deezer_id} ({format})...")

        def _task():
            from deezload.base import Loader, LoadStatus

            loader = Loader(
                urls=[deezer_url],
                output_dir=output_dir,
                format=format.lower(),
                tree=False,
                slugify=False,
            )
            path = None
            ok = False
            err = None
            for status, t, i, prog in loader.load_gen():
                if on_progress:
                    on_progress(
                        float(int(prog * 100)), f"deezload_{status.name.lower()}"
                    )
                if status in (LoadStatus.FINISHED, LoadStatus.SKIPPED):
                    path = t.path
                    ok = True
                elif status == LoadStatus.FAILED:
                    err = "Track not found on YouTube."
                elif status == LoadStatus.ERROR:
                    err = "deezload internal error."
            if not ok:
                raise Exception(err or "Download failed.")
            return path

        loop = asyncio.get_running_loop()
        local_path = await loop.run_in_executor(None, _task)
        if not local_path or not os.path.exists(local_path):
            raise FileNotFoundError(f"File not found after download: {local_path}")
        logger.info(f"Downloaded -> {local_path}")
        return local_path
```

---

### File: `services/movie_song_downloader/providers/jiosaavn_provider.py`
- **Path:** `services/movie_song_downloader/providers/jiosaavn_provider.py`
- **Estimated Tokens:** 2,497
- **mtime:** 1780856038.265

```python
import logging
import hashlib
from typing import List, Optional
from jiosaavnpy import JioSaavn

from MovieSongDownloader.providers.base import BaseSoundtrackProvider
from MovieSongDownloader.core.models import Album, Track
from MovieSongDownloader.core.rate_limiter import rate_limiter, providers_logger
from MovieSongDownloader.core.cache_manager import api_cache

logger = logging.getLogger("MovieSongDownloader.JioSaavnProvider")


class JioSaavnProvider(BaseSoundtrackProvider):
    def __init__(self):
        self._client = JioSaavn()

    async def get_soundtrack(
        self, movie_title: str, year: Optional[int] = None
    ) -> List[Album]:
        """Search JioSaavn for soundtrack albums matching movie title."""
        query = movie_title
        if year:
            query = f"{movie_title} {year}"

        cache_key = f"jiosaavn:album_search:{hashlib.md5(query.encode()).hexdigest()}"
        cached = await api_cache.get(cache_key)
        if cached is not None:
            return self._parse_cached_albums(cached)

        await rate_limiter.acquire("jiosaavn")
        try:
            results = self._client.search_albums(query, limit=8)
            if not results:
                return []

            albums = []
            for item in results:
                cover = None
                thumbs = item.get("thumbnails", {}).get("quality", {})
                cover = (
                    thumbs.get("500x500")
                    or thumbs.get("150x150")
                    or thumbs.get("50x50")
                )

                album = Album(
                    source="jiosaavn",
                    source_id=item.get("album_id", ""),
                    spotify_id=None,
                    title=item.get("title", ""),
                    artist=item.get("artists", "Unknown"),
                    cover_url=cover,
                    total_tracks=int(item.get("track_count", 0)),
                )
                albums.append(album)

            # Cache raw results
            await api_cache.set(cache_key, "jiosaavn", results, ttl=86400)
            providers_logger.info(
                f"provider=jiosaavn success=True endpoint=search_albums results={len(albums)}"
            )
            return albums

        except Exception as e:
            providers_logger.error(
                f'provider=jiosaavn success=False error="{e}" endpoint=search_albums'
            )
            logger.error(f"JioSaavn album search failed: {e}")
            return []

    async def get_tracks(self, album_id: str) -> List[Track]:
        """Fetch all tracks for a JioSaavn album."""
        cache_key = f"jiosaavn:album_tracks:{album_id}"
        cached = await api_cache.get(cache_key)
        if cached is not None:
            return self._parse_cached_tracks(cached)

        await rate_limiter.acquire("jiosaavn")
        try:
            info = self._client.album_info(album_id)
            if not info or "tracks" not in info:
                return []

            raw_tracks = info["tracks"]
            tracks = []
            for idx, item in enumerate(raw_tracks, start=1):
                # Get best quality stream URL
                streams = item.get("stream_urls", {})
                best_url = (
                    streams.get("very_high_quality")
                    or streams.get("high_quality")
                    or streams.get("medium_quality")
                    or streams.get("low_quality")
                )

                duration_sec = int(item.get("duration", 0))

                tracks.append(
                    Track(
                        source="jiosaavn",
                        source_id=item.get("track_id", ""),
                        spotify_id=None,
                        title=item.get("title", ""),
                        artist=item.get("primary_artists", "Unknown"),
                        duration_ms=duration_sec * 1000,
                        track_number=idx,
                        preview_url=streams.get("low_quality"),
                        download_url=best_url,
                    )
                )

            await api_cache.set(cache_key, "jiosaavn", raw_tracks, ttl=86400)
            providers_logger.info(
                f"provider=jiosaavn success=True endpoint=album_info tracks={len(tracks)}"
            )
            return tracks

        except Exception as e:
            providers_logger.error(
                f'provider=jiosaavn success=False error="{e}" endpoint=album_info'
            )
            logger.error(f"JioSaavn album tracks failed: {e}")
            return []

    async def get_album_details(self, album_id: str) -> Optional[Album]:
        """Fetch album metadata from JioSaavn."""
        cache_key = f"jiosaavn:album_detail:{album_id}"
        cached = await api_cache.get(cache_key)
        if cached is not None and isinstance(cached, dict):
            return self._dict_to_album(cached)

        await rate_limiter.acquire("jiosaavn")
        try:
            info = self._client.album_info(album_id)
            if not info:
                return None

            cover = None
            thumbs = info.get("thumbnails", {}).get("quality", {})
            cover = thumbs.get("500x500") or thumbs.get("150x150")

            album = Album(
                source="jiosaavn",
                source_id=info.get("album_id", album_id),
                title=info.get("title", ""),
                artist=info.get("primary_artists", "Unknown"),
                cover_url=cover,
                total_tracks=len(info.get("tracks", [])),
            )

            await api_cache.set(
                cache_key,
                "jiosaavn",
                {
                    "album_id": album.source_id,
                    "title": album.title,
                    "artist": album.artist,
                    "cover_url": album.cover_url,
                    "total_tracks": album.total_tracks,
                },
                ttl=86400,
            )

            return album

        except Exception as e:
            logger.error(f"JioSaavn album details failed: {e}")
            return None

    async def search_songs(self, query: str, limit: int = 10) -> List[Track]:
        """Direct song search on JioSaavn."""
        cache_key = f"jiosaavn:song_search:{hashlib.md5(query.encode()).hexdigest()}"
        cached = await api_cache.get(cache_key)
        if cached is not None:
            return self._parse_cached_tracks(cached)

        await rate_limiter.acquire("jiosaavn")
        try:
            results = self._client.search_songs(query, limit=limit)
            if not results:
                return []

            tracks = []
            for idx, item in enumerate(results, start=1):
                streams = item.get("stream_urls", {})
                best_url = (
                    streams.get("very_high_quality")
                    or streams.get("high_quality")
                    or streams.get("medium_quality")
                )
                duration_sec = int(item.get("duration", 0))

                tracks.append(
                    Track(
                        source="jiosaavn",
                        source_id=item.get("track_id", ""),
                        title=item.get("title", ""),
                        artist=item.get("primary_artists", "Unknown"),
                        duration_ms=duration_sec * 1000,
                        track_number=idx,
                        preview_url=streams.get("low_quality"),
                        download_url=best_url,
                    )
                )

            await api_cache.set(cache_key, "jiosaavn", results, ttl=86400)
            return tracks

        except Exception as e:
            logger.error(f"JioSaavn song search failed: {e}")
            return []

    def _parse_cached_albums(self, cached_data: list) -> List[Album]:
        """Convert cached raw JioSaavn album dicts back to Album objects."""
        albums = []
        for item in cached_data:
            cover = None
            thumbs = item.get("thumbnails", {}).get("quality", {})
            cover = thumbs.get("500x500") or thumbs.get("150x150")
            albums.append(
                Album(
                    source="jiosaavn",
                    source_id=item.get("album_id", ""),
                    title=item.get("title", ""),
                    artist=item.get("artists", "Unknown"),
                    cover_url=cover,
                    total_tracks=int(item.get("track_count", 0)),
                )
            )
        return albums

    def _parse_cached_tracks(self, cached_data: list) -> List[Track]:
        """Convert cached raw JioSaavn track dicts back to Track objects."""
        tracks = []
        for idx, item in enumerate(cached_data, start=1):
            streams = item.get("stream_urls", {})
            best_url = (
                streams.get("very_high_quality")
                or streams.get("high_quality")
                or streams.get("medium_quality")
            )
            duration_sec = int(item.get("duration", 0))
            tracks.append(
                Track(
                    source="jiosaavn",
                    source_id=item.get("track_id", ""),
                    title=item.get("title", ""),
                    artist=item.get("primary_artists", "Unknown"),
                    duration_ms=duration_sec * 1000,
                    track_number=idx,
                    preview_url=streams.get("low_quality"),
                    download_url=best_url,
                )
            )
        return tracks

    @staticmethod
    def _dict_to_album(d: dict) -> Album:
        return Album(
            source="jiosaavn",
            source_id=d.get("album_id", ""),
            title=d.get("title", ""),
            artist=d.get("artist", "Unknown"),
            cover_url=d.get("cover_url"),
            total_tracks=d.get("total_tracks", 0),
        )
```

---

### File: `services/movie_song_downloader/providers/lyrics_provider.py`
- **Path:** `services/movie_song_downloader/providers/lyrics_provider.py`
- **Estimated Tokens:** 591
- **mtime:** 1780856038.287

```python
import asyncio
import re
import logging
import time
import json
from typing import Tuple, Optional
import syncedlyrics
from MovieSongDownloader.providers.base import BaseLyricsProvider
from MovieSongDownloader.core.settings_manager import settings_manager
from MovieSongDownloader.core.rate_limiter import rate_limiter, providers_logger

logger = logging.getLogger("MovieSongDownloader.LyricsProvider")


class LyricsProvider(BaseLyricsProvider):
    def __init__(self):
        self._lrc_re = re.compile(r"\[\d{2,}:\d{2}(?:\.\d{1,3})?\]")

    def _is_synced(self, text: str) -> bool:
        return bool(text) and len(self._lrc_re.findall(text)) >= 3

    @staticmethod
    def _search(query: str, provider: str) -> Optional[str]:
        try:
            return syncedlyrics.search(query, providers=[provider])
        except Exception:
            return None

    async def fetch(self, title: str, artist: str) -> Tuple[Optional[str], str]:
        raw = await settings_manager.get("lyrics_priority")
        try:
            providers = json.loads(raw)
        except Exception:
            providers = ["lrclib", "syncedlyrics", "musixmatch", "genius"]

        query = f"{title} {artist}"
        for prov in providers:
            await rate_limiter.acquire("lyrics")
            t0 = time.time()
            try:
                target = prov.lower()
                if target == "syncedlyrics":
                    result = await asyncio.to_thread(syncedlyrics.search, query)
                else:
                    result = await asyncio.to_thread(self._search, query, target)
                ms = int((time.time() - t0) * 1000)
                if result:
                    providers_logger.info(
                        f"provider=lyrics_{prov} latency={ms}ms success=True response_size={len(result)}"
                    )
                    ltype = "synced" if self._is_synced(result) else "plain"
                    return result, ltype
                providers_logger.info(
                    f"provider=lyrics_{prov} latency={ms}ms success=False response_size=0"
                )
            except Exception as e:
                ms = int((time.time() - t0) * 1000)
                providers_logger.error(
                    f'provider=lyrics_{prov} latency={ms}ms success=False error="{e}"'
                )
        return None, "none"
```

---

### File: `services/movie_song_downloader/providers/metadata_normalizer.py`
- **Path:** `services/movie_song_downloader/providers/metadata_normalizer.py`
- **Estimated Tokens:** 362
- **mtime:** 1780856038.289

```python
import re
from rapidfuzz import fuzz

NOISE_PATTERNS = [
    r"\(From\s+.*?\)",
    r"\(Remastered\s*\d*\)",
    r"\(Official\s+Audio\)",
    r"\[Extended\s+Version\]",
    r"\(Deluxe\s*Edition?\)",
    r"\(feat\.\s+.*?\)",
    r'\(From\s+"[^"]*"\)',
    r"\(Original\s+Motion\s+Picture\s+Soundtrack\)",
]


def normalize_title(title: str) -> str:
    # Strip Wikipedia parenthetical suffixes (e.g. "(film)", "(2026 film)", "(soundtrack)")
    title = re.sub(
        r"\s*\((?:film|\d{4}(?:\s+film)?|soundtrack|tamil\s+film|original\s+motion\s+picture\s+soundtrack|album)\)",
        "",
        title,
        flags=re.IGNORECASE,
    )

    for p in NOISE_PATTERNS:
        title = re.sub(p, "", title, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", title).strip()


def confidence_score(source: dict, target: dict) -> int:
    src_t = normalize_title(source.get("title", "")).lower()
    tgt_t = normalize_title(target.get("title", "")).lower()
    score = int(fuzz.ratio(src_t, tgt_t) * 0.50)
    score += int(
        fuzz.ratio(source.get("artist", "").lower(), target.get("artist", "").lower())
        * 0.30
    )
    sa, ta = source.get("album", "").lower(), target.get("album", "").lower()
    score += int(fuzz.ratio(sa, ta) * 0.10) if sa and ta else 10
    dur = abs(source.get("duration_ms", 0) - target.get("duration_ms", 0))
    score += 10 if dur <= 3000 else (5 if dur <= 5000 else (2 if dur <= 10000 else 0))
    return score
```

---

### File: `services/movie_song_downloader/providers/musicbrainz_provider.py`
- **Path:** `services/movie_song_downloader/providers/musicbrainz_provider.py`
- **Estimated Tokens:** 1,641
- **mtime:** 1780856038.294

```python
import logging
import httpx
import hashlib
import time
from typing import List, Dict, Optional, Tuple
from MovieSongDownloader.core.rate_limiter import rate_limiter, providers_logger
from MovieSongDownloader.core.cache_manager import api_cache
from MovieSongDownloader.core.models import Album, Track

logger = logging.getLogger("MovieSongDownloader.MusicBrainzProvider")

USER_AGENT = "MovieSongDownloader/2.0 (contact: nandha.dev@gmail.com)"


class MusicBrainzProvider:
    async def _mb_request(
        self, url: str, params: dict, cache_ttl: int = 2592000
    ) -> Optional[dict]:
        """Make a request to MusicBrainz API with caching and strict 1 req/sec rate limit."""
        params["fmt"] = "json"
        param_str = "".join(f"{k}={params[k]}" for k in sorted(params))
        cache_key = f"musicbrainz:{hashlib.md5((url + param_str).encode()).hexdigest()}"

        cached = await api_cache.get(cache_key)
        if cached is not None:
            return cached

        # MusicBrainz guidelines mandate strict rate limits (1 req/sec)
        await rate_limiter.acquire("musicbrainz")
        t0 = time.time()
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.get(
                    url, params=params, headers={"User-Agent": USER_AGENT}
                )
                ms = int((time.time() - t0) * 1000)
                if resp.status_code == 200:
                    data = resp.json()
                    providers_logger.info(
                        f"provider=musicbrainz latency={ms}ms success=True"
                    )
                    await api_cache.set(cache_key, "musicbrainz", data, cache_ttl)
                    return data
                providers_logger.error(
                    f"provider=musicbrainz latency={ms}ms success=False status={resp.status_code}"
                )
        except Exception as e:
            ms = int((time.time() - t0) * 1000)
            providers_logger.error(
                f'provider=musicbrainz latency={ms}ms success=False error="{e}"'
            )
            logger.error(f"MusicBrainz API request failed: {e}")
        return None

    async def enrich_album(
        self, album: Album, tracks: List[Track]
    ) -> Tuple[Optional[str], Dict[str, str]]:
        """
        Enrich Album with composer info and Tracks with ISRC codes from MusicBrainz.
        Returns: (composer_name, {track_title: isrc_code})
        """
        composer = None
        isrc_map = {}

        # 1. Search release groups
        query = f'release-group:"{album.title}" AND type:soundtrack'
        if album.artist and album.artist != "Unknown":
            # Add artist if known to narrow down
            query += f' AND artist:"{album.artist}"'

        search_data = await self._mb_request(
            "https://musicbrainz.org/ws/2/release-group/", {"query": query}
        )

        if not search_data or not search_data.get("release-groups"):
            # Try a broader search without soundtrack filter
            query_broad = f'release-group:"{album.title}"'
            search_data = await self._mb_request(
                "https://musicbrainz.org/ws/2/release-group/", {"query": query_broad}
            )
            if not search_data or not search_data.get("release-groups"):
                return None, {}

        rg = search_data["release-groups"][0]
        rg_id = rg["id"]

        # If artist-credit lists the composer, capture it
        artist_credit = rg.get("artist-credit", [])
        if artist_credit:
            composer = artist_credit[0].get("artist", {}).get("name")

        # 2. Browse releases for this release group to find tracks/recordings and relations
        browse_data = await self._mb_request(
            "https://musicbrainz.org/ws/2/release",
            {
                "release-group": rg_id,
                "inc": "recordings+artist-rels+work-rels+isrcs+work-level-rels",
            },
        )

        if not browse_data or not browse_data.get("releases"):
            return composer, {}

        # Look through releases
        for rel in browse_data["releases"]:
            # Check release relations for composer if not resolved
            if not composer:
                for rel_item in rel.get("relations", []):
                    if rel_item.get("type") == "composer" and rel_item.get("artist"):
                        composer = rel_item["artist"].get("name")
                        break

            # Collect recordings and ISRCs
            media_list = rel.get("media", [])
            for media in media_list:
                for mb_track in media.get("tracks", []):
                    title = mb_track.get("title", "")
                    recording = mb_track.get("recording", {})
                    isrcs = recording.get("isrcs", [])

                    if isrcs:
                        isrc_map[title.lower().strip()] = isrcs[0]

                    # Check recording level relations for composer if still not found
                    if not composer:
                        for rec_rel in recording.get("relations", []):
                            if rec_rel.get("type") == "composer" and rec_rel.get(
                                "artist"
                            ):
                                composer = rec_rel["artist"].get("name")
                                break

        # Match ISRCs back to JioSaavn tracks by title matching
        final_isrcs = {}
        for t in tracks:
            t_title_clean = t.title.lower().strip()
            # Try exact match first
            if t_title_clean in isrc_map:
                final_isrcs[t.title] = isrc_map[t_title_clean]
            else:
                # Try partial match (e.g. "Song Name (From film)" vs "Song Name")
                matched = False
                for mb_title, isrc in isrc_map.items():
                    if mb_title in t_title_clean or t_title_clean in mb_title:
                        final_isrcs[t.title] = isrc
                        matched = True
                        break
                if not matched:
                    # Try cleaning common suffixes
                    clean_jio = t_title_clean.split("(")[0].strip()
                    for mb_title, isrc in isrc_map.items():
                        clean_mb = mb_title.split("(")[0].strip()
                        if clean_jio == clean_mb:
                            final_isrcs[t.title] = isrc
                            break

        return composer, final_isrcs
```

---

### File: `services/movie_song_downloader/providers/omdb_provider.py`
- **Path:** `services/movie_song_downloader/providers/omdb_provider.py`
- **Estimated Tokens:** 1,309
- **mtime:** 1780856038.303

```python
import time
import httpx
import logging
import hashlib
from typing import List, Optional

from MovieSongDownloader.core.models import Movie
from MovieSongDownloader.core.settings_manager import settings_manager
from MovieSongDownloader.core.rate_limiter import rate_limiter, providers_logger
from MovieSongDownloader.core.cache_manager import api_cache
from MovieSongDownloader.config import OMDB_BASE_URL

logger = logging.getLogger("MovieSongDownloader.OMDbProvider")


class OMDbProvider:
    """Optional fallback provider for movie ratings, cast, and plot via OMDb API."""

    async def _request(self, params: dict, cache_ttl: int = 2592000) -> Optional[dict]:
        """Make OMDb API request with caching. TTL default 30 days."""
        api_key = await settings_manager.get("omdb_api_key")
        if not api_key:
            logger.debug("OMDb API key not configured.")
            return None

        full_params = {**params, "apikey": api_key}
        param_str = "".join(f"{k}={params[k]}" for k in sorted(params))
        cache_key = f"omdb:{hashlib.md5(param_str.encode()).hexdigest()}"

        cached = await api_cache.get(cache_key)
        if cached is not None:
            return cached

        await rate_limiter.acquire("omdb")
        t0 = time.time()
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                resp = await client.get(OMDB_BASE_URL, params=full_params)
                ms = int((time.time() - t0) * 1000)
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("Response") == "True":
                        providers_logger.info(
                            f"provider=omdb latency={ms}ms success=True"
                        )
                        await api_cache.set(cache_key, "omdb", data, cache_ttl)
                        return data
                    providers_logger.warning(
                        f'provider=omdb latency={ms}ms response=False error="{data.get("Error")}"'
                    )
                else:
                    providers_logger.error(
                        f"provider=omdb latency={ms}ms success=False status={resp.status_code}"
                    )
        except Exception as e:
            ms = int((time.time() - t0) * 1000)
            providers_logger.error(
                f'provider=omdb latency={ms}ms success=False error="{e}"'
            )
            logger.error(f"OMDb request failed: {e}")
        return None

    async def search(self, query: str, year: Optional[int] = None) -> List[Movie]:
        """Search OMDb for movies."""
        params = {"s": query, "type": "movie"}
        if year:
            params["y"] = str(year)

        data = await self._request(params, cache_ttl=86400)
        if not data or "Search" not in data:
            return []

        movies = []
        for item in data["Search"]:
            yr = None
            try:
                yr = int(item.get("Year", "0").split("–")[0])
            except (ValueError, IndexError):
                pass

            movies.append(
                Movie(
                    source="omdb",
                    source_id=item.get("imdbID", ""),
                    title=item.get("Title", ""),
                    year=yr,
                    poster_url=item.get("Poster")
                    if item.get("Poster") != "N/A"
                    else None,
                )
            )
        return movies

    async def get_details(self, imdb_id: str) -> Optional[dict]:
        """Fetch full movie details from OMDb by IMDb ID."""
        params = {"i": imdb_id, "plot": "short"}
        return await self._request(params, cache_ttl=2592000)

    async def enrich_movie(self, movie: Movie) -> Movie:
        """Enrich a Movie object with OMDb data (rating, cast, poster, overview).
        Tries by title+year if no imdb_id available."""
        data = None

        # If we have an IMDb ID, use it directly
        if movie.source == "omdb" and movie.source_id:
            data = await self.get_details(movie.source_id)

        # Otherwise search by title
        if not data:
            params = {"t": movie.title, "type": "movie"}
            if movie.year:
                params["y"] = str(movie.year)
            data = await self._request(params, cache_ttl=2592000)

        if not data:
            return movie

        # Enrich fields
        if not movie.poster_url or movie.poster_url == "N/A":
            poster = data.get("Poster")
            if poster and poster != "N/A":
                movie.poster_url = poster

        movie.rating = data.get("imdbRating")
        movie.cast_info = data.get("Actors")

        if not movie.overview:
            movie.overview = data.get("Plot")

        if not movie.genres:
            genres_str = data.get("Genre", "")
            if genres_str and genres_str != "N/A":
                movie.genres = [g.strip() for g in genres_str.split(",")]

        if not movie.language:
            movie.language = data.get("Language")

        # Store IMDb ID for future lookups
        if data.get("imdbID") and not movie.source_id:
            movie.source_id = data["imdbID"]

        return movie
```

---

### File: `services/movie_song_downloader/providers/spotiflac_provider.py`
- **Path:** `services/movie_song_downloader/providers/spotiflac_provider.py`
- **Estimated Tokens:** 2,481
- **mtime:** 1781123459.224

```python
import os
import httpx
import re
import logging
import asyncio
import shutil
from typing import Optional, Callable
from urllib.parse import quote_plus

from MovieSongDownloader.providers.base import BaseDownloadProvider
from MovieSongDownloader.core.models import Track
from MovieSongDownloader.core.settings_manager import settings_manager

logger = logging.getLogger("MovieSongDownloader.SpotiFLACProvider")


class SpotiFLACProvider(BaseDownloadProvider):
    def _get_subprocess_env(self) -> dict:
        """
        Prepares environment variables for subprocesses, ensuring ffmpeg is in PATH
        and preventing UnicodeEncodeError in python CLI tools.
        """
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUTF8"] = "1"
        
        # Add local bin directory to PATH
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        bin_dir = os.path.join(base_dir, "bin")
        if os.path.exists(bin_dir):
            env["PATH"] = bin_dir + os.pathsep + env.get("PATH", "")
            
        return env

    async def _resolve_spotify_url(self, title: str, artist: str) -> str:
        """
        Queries DuckDuckGo HTML search to resolve a song's title & artist to a Spotify track URL.
        """
        clean_title = title.replace('"', "").replace("'", "")
        clean_artist = artist.split(",")[0].strip()
        query = f'site:open.spotify.com/track "{clean_artist}" "{clean_title}"'
        url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36"
            )
        }

        logger.info(
            f"Resolving Spotify track URL for '{title}' by '{artist}' via DDG..."
        )

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url, headers=headers)
                if resp.status_code == 200:
                    matches = re.findall(
                        r"open\.spotify\.com/track/([a-zA-Z0-9]+)", resp.text
                    )
                    if matches:
                        spotify_id = matches[0]
                        resolved_url = f"https://open.spotify.com/track/{spotify_id}"
                        logger.info(f"Resolved track successfully to: {resolved_url}")
                        return resolved_url
        except Exception as e:
            logger.error(f"DDG Spotify resolution request failed: {e}")

        # Fallback to a broader search query if exact match failed
        query_broad = f"site:open.spotify.com/track {clean_artist} {clean_title}"
        url_broad = f"https://html.duckduckgo.com/html/?q={quote_plus(query_broad)}"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url_broad, headers=headers)
                if resp.status_code == 200:
                    matches = re.findall(
                        r"open\.spotify\.com/track/([a-zA-Z0-9]+)", resp.text
                    )
                    if matches:
                        spotify_id = matches[0]
                        resolved_url = f"https://open.spotify.com/track/{spotify_id}"
                        logger.info(
                            f"Resolved track via broad query to: {resolved_url}"
                        )
                        return resolved_url
        except Exception as e:
            logger.error(f"DDG Spotify broad resolution request failed: {e}")

        raise Exception(
            f"Could not resolve a Spotify track URL for '{title}' by '{artist}'."
        )

    async def _transcode_audio(
        self, input_path: str, output_path: str, format_str: str, bitrate: str = "320"
    ) -> None:
        """
        Transcodes the input audio file to the target format using ffmpeg.
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ffmpeg_path = os.path.join(base_dir, "bin", "ffmpeg.exe")
        if not os.path.exists(ffmpeg_path):
            ffmpeg_path = "ffmpeg"  # fallback to path

        format_str = format_str.lower()
        cmd = [ffmpeg_path, "-y", "-i", input_path, "-vn"]

        if format_str == "mp3":
            cmd.extend(["-ar", "44100", "-ac", "2", "-b:a", f"{bitrate}k", output_path])
        elif format_str == "flac":
            cmd.extend([output_path])
        elif format_str in ("m4a", "aac"):
            cmd.extend(["-c:a", "copy", output_path])
        else:
            cmd.extend([output_path])

        logger.info(f"SpotiFLAC Transcode: {' '.join(cmd)}")
        env = self._get_subprocess_env()
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, env=env
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            err_msg = stderr.decode(errors="ignore")
            logger.error(f"ffmpeg transcoding failed: {err_msg}")
            raise Exception(f"Transcoding failed: {err_msg}")

    async def download(
        self,
        track: Track,
        format: str,
        output_dir: str,
        filename_template: str,
        on_progress: Optional[Callable[[float, str], None]] = None,
    ) -> str:
        """
        Downloads a track using spotiflac globally installed CLI command.
        """
        # Resolve Spotify track URL
        if track.source == "spotify" and track.source_id:
            spotify_url = f"https://open.spotify.com/track/{track.source_id}"
        else:
            spotify_url = await self._resolve_spotify_url(track.title, track.artist)

        # We will download the track into a temporary subfolder to identify the generated file
        temp_subfolder = os.path.join(
            output_dir, f"spotiflac_temp_{track.source_id or 'unknown'}"
        )
        if os.path.exists(temp_subfolder):
            shutil.rmtree(temp_subfolder, ignore_errors=True)
        os.makedirs(temp_subfolder, exist_ok=True)

        if on_progress:
            on_progress(20.0, "spotiflac_starting")

        cmd = ["spotiflac", spotify_url, temp_subfolder]

        # Check settings for Deezer ARL or other service prioritization (optional parameter)
        deezer_arl = await settings_manager.get("deezer_arl")
        # We can specify service priority or other custom flags if desired
        # e.g., --service deezer
        services = []
        if deezer_arl:
            # If Deezer ARL is configured, we prioritize deezer download
            services.append("deezer")

        # Default priority: tidal, qobuz, deezer, amazon
        # We can pass them as args if spotiflac CLI supports --service flag
        if services:
            cmd.extend(["--service"] + services)

        logger.info(f"Executing SpotiFLAC Command: {' '.join(cmd)}")

        if on_progress:
            on_progress(40.0, "spotiflac_downloading")

        try:
            env = self._get_subprocess_env()
            process = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, env=env
            )
            stdout, stderr = await process.communicate()

            stdout_str = stdout.decode(errors="ignore")
            stderr_str = stderr.decode(errors="ignore")

            logger.info(f"spotiflac stdout: {stdout_str}")
            if process.returncode != 0:
                logger.error(f"spotiflac stderr: {stderr_str}")
                raise Exception(
                    f"SpotiFLAC download failed with exit code {process.returncode}: {stderr_str}"
                )

        except Exception as e:
            shutil.rmtree(temp_subfolder, ignore_errors=True)
            raise e

        if on_progress:
            on_progress(80.0, "spotiflac_postprocessing")

        # Scan for the downloaded audio file
        audio_extensions = (".flac", ".mp3", ".m4a", ".aac", ".ogg", ".wav")
        downloaded_file = None
        for root, _, files in os.walk(temp_subfolder):
            for file in files:
                if file.lower().endswith(audio_extensions):
                    downloaded_file = os.path.join(root, file)
                    break
            if downloaded_file:
                break

        if not downloaded_file or not os.path.exists(downloaded_file):
            shutil.rmtree(temp_subfolder, ignore_errors=True)
            raise Exception(
                "SpotiFLAC executed successfully, but no audio file was generated in the output directory."
            )

        # Resolve target path in output_dir
        file_ext = os.path.splitext(downloaded_file)[1].lower()
        target_ext = f".{format.lower()}"

        # Check if we need transcoding (e.g. SpotiFLAC downloaded FLAC but format is MP3)
        if file_ext != target_ext:
            logger.info(
                f"Transcoding SpotiFLAC output {file_ext} to target {target_ext}..."
            )
            bitrate = await settings_manager.get("bitrate") or "320"
            temp_transcoded = os.path.join(temp_subfolder, f"transcoded{target_ext}")
            await self._transcode_audio(
                downloaded_file, temp_transcoded, format, bitrate
            )
            downloaded_file = temp_transcoded

        # Copy the file to the parent output_dir (or return its path so download_service moves it)
        final_temp_path = os.path.join(
            output_dir, f"spotiflac_result_{track.source_id}{target_ext}"
        )
        if os.path.exists(final_temp_path):
            os.remove(final_temp_path)

        shutil.move(downloaded_file, final_temp_path)
        shutil.rmtree(temp_subfolder, ignore_errors=True)

        return final_temp_path
```

---

### File: `services/movie_song_downloader/providers/spotify_provider.py`
- **Path:** `services/movie_song_downloader/providers/spotify_provider.py`
- **Estimated Tokens:** 1,557
- **mtime:** 1780861103.721

```python
import httpx
import re
import json
import logging
from typing import Tuple, List, Optional
from MovieSongDownloader.core.models import Movie, Album, Track

logger = logging.getLogger("MovieSongDownloader.SpotifyProvider")


class SpotifyProvider:
    def __init__(self):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36"
            )
        }

    def _get_cover_url(self, vi: dict) -> Optional[str]:
        if not vi or "image" not in vi:
            return None
        images = vi["image"]
        if not images:
            return None
        # Sort images by maxWidth/maxHeight descending to get the best quality
        sorted_imgs = sorted(
            images,
            key=lambda x: (x.get("maxWidth", 0) or 0) * (x.get("maxHeight", 0) or 0),
            reverse=True,
        )
        return sorted_imgs[0].get("url")

    async def get_spotify_album_or_track(
        self, spotify_url_or_id: str
    ) -> Tuple[Movie, Album, List[Track]]:
        """
        Parses the Spotify URL or ID to scrape the public embed metadata.
        Returns:
            Tuple[Movie, Album, List[Track]]
        """
        # Detect ID and Type
        match = re.search(r"(album|track)/([a-zA-Z0-9]+)", spotify_url_or_id)
        if match:
            item_type = match.group(1)
            item_id = match.group(2)
        else:
            # Assume it's a raw ID, default to album
            item_type = "album"
            item_id = spotify_url_or_id

        embed_url = f"https://open.spotify.com/embed/{item_type}/{item_id}"

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(embed_url, headers=self.headers)
            if resp.status_code != 200:
                raise Exception(
                    f"Failed to fetch Spotify embed page: status {resp.status_code}"
                )

        html = resp.text
        json_match = re.search(
            r'<script id="__NEXT_DATA__"[^>]* type="application/json">(.*?)</script>',
            html,
            re.DOTALL,
        )
        if not json_match:
            raise Exception(
                "Failed to extract metadata from Spotify embed page: __NEXT_DATA__ not found."
            )

        try:
            data = json.loads(json_match.group(1))
        except Exception as e:
            raise Exception(f"Failed to parse Spotify embed JSON metadata: {e}")

        state_data = (
            data.get("props", {}).get("pageProps", {}).get("state", {}).get("data", {})
        )
        entity = state_data.get("entity", {})
        if not entity:
            raise Exception("Invalid Spotify embed JSON structure: 'entity' not found.")

        # Check for error status
        if data.get("props", {}).get("pageProps", {}).get("status") == 404:
            raise Exception("Spotify item not found (404). Check the URL/ID.")

        title = entity.get("title") or entity.get("name") or "Unknown"
        cover_url = self._get_cover_url(entity.get("visualIdentity", {}))

        if item_type == "album":
            artist_name = entity.get("subtitle") or "Unknown Artist"
            movie = Movie(
                source="spotify",
                source_id=item_id,
                title=title,
                poster_url=cover_url,
                overview=f"Spotify Album: {title} by {artist_name}",
            )
            album = Album(
                source="spotify",
                source_id=item_id,
                spotify_id=item_id,
                title=title,
                artist=artist_name,
                cover_url=cover_url,
                total_tracks=len(entity.get("trackList", [])),
            )

            tracks = []
            for idx, t in enumerate(entity.get("trackList", []), start=1):
                t_uri = t.get("uri", "")
                t_id = t_uri.split(":")[-1] if ":" in t_uri else t.get("uid", "")

                # Extract preview URL if available
                preview_url = (
                    t.get("audioPreview", {}).get("url")
                    if t.get("audioPreview")
                    else None
                )

                tracks.append(
                    Track(
                        source="spotify",
                        source_id=t_id,
                        spotify_id=t_id,
                        title=t.get("title", "Unknown Track"),
                        artist=t.get("subtitle") or artist_name,
                        duration_ms=t.get("duration", 0),
                        track_number=idx,
                        preview_url=preview_url,
                    )
                )
            return movie, album, tracks

        else:  # track
            artists_list = entity.get("artists", [])
            artist_name = (
                ", ".join([a.get("name", "") for a in artists_list])
                if artists_list
                else "Unknown Artist"
            )

            # For a single track, wrap it in a dummy album of size 1
            movie = Movie(
                source="spotify",
                source_id=item_id,
                title=title,
                poster_url=cover_url,
                overview=f"Spotify Track: {title} by {artist_name}",
            )
            album = Album(
                source="spotify",
                source_id=item_id,
                spotify_id=item_id,
                title=title,
                artist=artist_name,
                cover_url=cover_url,
                total_tracks=1,
            )

            preview_url = (
                entity.get("audioPreview", {}).get("url")
                if entity.get("audioPreview")
                else None
            )

            track = Track(
                source="spotify",
                source_id=item_id,
                spotify_id=item_id,
                title=title,
                artist=artist_name,
                duration_ms=entity.get("duration", 0),
                track_number=1,
                preview_url=preview_url,
            )
            return movie, album, [track]
```

---

### File: `services/movie_song_downloader/providers/tagging_provider.py`
- **Path:** `services/movie_song_downloader/providers/tagging_provider.py`
- **Estimated Tokens:** 913
- **mtime:** 1780856038.315

```python
import os
import logging
from typing import Optional
from MovieSongDownloader.providers.base import BaseTaggingProvider
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, USLT, TIT2, TPE1, TALB, TYER, TRCK, ID3NoHeaderError
from mutagen.flac import FLAC, Picture

logger = logging.getLogger("MovieSongDownloader.TaggingProvider")


class TaggingProvider(BaseTaggingProvider):
    async def embed_cover(self, file_path: str, image_path: str) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio not found: {file_path}")
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        with open(image_path, "rb") as f:
            img_data = f.read()
        mime = "image/png" if image_path.lower().endswith(".png") else "image/jpeg"
        ext = file_path.rsplit(".", 1)[-1].lower()

        if ext == "mp3":
            audio = self._get_mp3(file_path)
            for k in [k for k in audio.tags.keys() if k.startswith("APIC")]:
                audio.tags.pop(k)
            audio.tags.add(
                APIC(encoding=3, mime=mime, type=3, desc="Front Cover", data=img_data)
            )
            audio.save()
        elif ext == "flac":
            audio = FLAC(file_path)
            audio.clear_pictures()
            pic = Picture()
            pic.data, pic.type, pic.mime, pic.desc = img_data, 3, mime, "Front Cover"
            audio.add_picture(pic)
            audio.save()

    async def embed_lyrics(
        self, file_path: str, lyrics_content: str, is_synced: bool = False
    ) -> None:
        if not os.path.exists(file_path) or not lyrics_content:
            return
        ext = file_path.rsplit(".", 1)[-1].lower()
        if ext == "mp3":
            audio = self._get_mp3(file_path)
            for k in [k for k in audio.tags.keys() if k.startswith("USLT")]:
                audio.tags.pop(k)
            audio.tags.add(
                USLT(encoding=3, lang="eng", desc="Lyrics", text=lyrics_content)
            )
            audio.save()
        elif ext == "flac":
            audio = FLAC(file_path)
            audio["lyrics"] = lyrics_content
            audio["unsyncedlyrics"] = lyrics_content
            audio.save()

    async def embed_metadata(
        self,
        file_path: str,
        title: str,
        artist: str,
        album: str,
        year: Optional[int] = None,
        track_num: int = 1,
    ) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio not found: {file_path}")
        ext = file_path.rsplit(".", 1)[-1].lower()
        if ext == "mp3":
            audio = self._get_mp3(file_path)
            audio.tags.add(TIT2(encoding=3, text=title))
            audio.tags.add(TPE1(encoding=3, text=artist))
            audio.tags.add(TALB(encoding=3, text=album))
            audio.tags.add(TRCK(encoding=3, text=str(track_num)))
            if year:
                audio.tags.add(TYER(encoding=3, text=str(year)))
            audio.save()
        elif ext == "flac":
            audio = FLAC(file_path)
            audio["title"] = title
            audio["artist"] = artist
            audio["album"] = album
            audio["tracknumber"] = str(track_num)
            if year:
                audio["date"] = str(year)
            audio.save()

    @staticmethod
    def _get_mp3(path: str) -> MP3:
        try:
            audio = MP3(path, ID3=ID3)
        except ID3NoHeaderError:
            audio = MP3(path)
            audio.add_tags()
        if audio.tags is None:
            audio.add_tags()
        return audio
```

---

### File: `services/movie_song_downloader/providers/wikidata_provider.py`
- **Path:** `services/movie_song_downloader/providers/wikidata_provider.py`
- **Estimated Tokens:** 1,060
- **mtime:** 1780856515.522

```python
import logging
import httpx
import hashlib
import time
from typing import List, Dict, Optional
from MovieSongDownloader.core.rate_limiter import rate_limiter, providers_logger
from MovieSongDownloader.core.cache_manager import api_cache

logger = logging.getLogger("MovieSongDownloader.WikidataProvider")

USER_AGENT = "MovieSongDownloader/2.0 (contact: nandha.dev@gmail.com)"


class WikidataProvider:
    async def _wikidata_request(
        self, params: dict, cache_ttl: int = 604800
    ) -> Optional[dict]:
        """Make a request to Wikidata API with caching and rate limiting."""
        params["format"] = "json"
        param_str = "".join(f"{k}={params[k]}" for k in sorted(params))
        cache_key = f"wikidata:{hashlib.md5(param_str.encode()).hexdigest()}"

        cached = await api_cache.get(cache_key)
        if cached is not None:
            return cached

        await rate_limiter.acquire("wikidata")
        t0 = time.time()
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.get(
                    "https://www.wikidata.org/w/api.php",
                    params=params,
                    headers={"User-Agent": USER_AGENT},
                )
                ms = int((time.time() - t0) * 1000)
                if resp.status_code == 200:
                    data = resp.json()
                    providers_logger.info(
                        f"provider=wikidata latency={ms}ms success=True"
                    )
                    await api_cache.set(cache_key, "wikidata", data, cache_ttl)
                    return data
                providers_logger.error(
                    f"provider=wikidata latency={ms}ms success=False status={resp.status_code}"
                )
        except Exception as e:
            ms = int((time.time() - t0) * 1000)
            providers_logger.error(
                f'provider=wikidata latency={ms}ms success=False error="{e}"'
            )
            logger.error(f"Wikidata API request failed: {e}")
        return None

    async def get_posters_batch(
        self, wikipedia_titles: List[str], lang: str = "en"
    ) -> Dict[str, str]:
        """
        Query Wikidata API in batches to resolve P18 (image) property for Wikipedia page titles.
        Returns a dictionary mapping {wikipedia_title: poster_url}.
        """
        if not wikipedia_titles:
            return {}

        results = {}
        site = "enwiki" if lang == "en" else "tawiki"

        # Wikipedia allows batching up to 50 items
        batch_size = 40
        for i in range(0, len(wikipedia_titles), batch_size):
            batch = wikipedia_titles[i:i+batch_size]
            params = {
                "action": "wbgetentities",
                "sites": site,
                "titles": "|".join(batch),
                "props": "claims|sitelinks",
            }

            data = await self._wikidata_request(params, cache_ttl=86400 * 7)
            if not data or "entities" not in data:
                continue

            entities = data["entities"]
            for entity_id, entity_data in entities.items():
                if entity_id == "-1":
                    continue

                # Retrieve the original title from sitelinks to map correctly
                sitelinks = entity_data.get("sitelinks", {})
                wiki_site = sitelinks.get(site, {})
                title = wiki_site.get("title")
                if not title:
                    continue

                claims = entity_data.get("claims", {})
                p18_claims = claims.get("P18", [])
                if p18_claims:
                    # Get filename from the claim
                    mainsnak = p18_claims[0].get("mainsnak", {})
                    datavalue = mainsnak.get("datavalue", {})
                    filename = datavalue.get("value")
                    if filename:
                        # Construct Wikimedia Commons Special:FilePath URL
                        # Special:FilePath redirects directly to the raw media URL
                        url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{filename}"
                        results[title] = url

        return results
```

---

### File: `services/movie_song_downloader/requirements.txt`
- **Path:** `services/movie_song_downloader/requirements.txt`
- **Estimated Tokens:** 42
- **mtime:** 1780574049.314

```
reflex>=0.5.0
httpx>=0.27.0
yt-dlp>=2024.0.0
deezload>=0.2.0
mutagen>=1.47.0
aiosqlite>=0.20.0
syncedlyrics>=1.0.0
jiosaavnpy>=0.1.3
beautifulsoup4>=4.12.0
lxml>=5.0.0
```

---

### File: `services/movie_song_downloader/scripts/run_migrations.py`
- **Path:** `services/movie_song_downloader/scripts/run_migrations.py`
- **Estimated Tokens:** 100
- **mtime:** 1780924764.321

```python
import asyncio
import traceback

from MovieSongDownloader.core.database import db

async def main():
    try:
        print('Running migrations...', flush=True)
        await db.run_migrations()
        print('Migrations applied successfully', flush=True)
    except Exception as e:
        print('Migration failed:', e)
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(main())
```

---

### File: `services/movie_song_downloader/services/__init__.py`
- **Path:** `services/movie_song_downloader/services/__init__.py`
- **Estimated Tokens:** 4
- **mtime:** 1780474579.015

```python
# Services Module
```

---

### File: `services/movie_song_downloader/services/download_service.py`
- **Path:** `services/movie_song_downloader/services/download_service.py`
- **Estimated Tokens:** 4,107
- **mtime:** 1780861103.744

```python
import os
import shutil
import asyncio
import logging
import json
from typing import Optional
from pathlib import Path
import httpx

from MovieSongDownloader.core.database import db
from MovieSongDownloader.core.models import DownloadJob, Movie, Album, Track
from MovieSongDownloader.core.job_queue import job_queue
from MovieSongDownloader.core.cache_manager import download_cache, image_cache
from MovieSongDownloader.core.settings_manager import settings_manager
from MovieSongDownloader.providers.deezspot_provider import DeezspotProvider
from MovieSongDownloader.providers.spotiflac_provider import SpotiFLACProvider
from MovieSongDownloader.providers.lyrics_provider import LyricsProvider
from MovieSongDownloader.providers.tagging_provider import TaggingProvider
from MovieSongDownloader.services.folder_service import FolderService

logger = logging.getLogger("MovieSongDownloader.DownloadService")


class DownloadService:
    def __init__(self):
        self.download_provider = DeezspotProvider()
        self.lyrics_provider = LyricsProvider()
        self.tagging_provider = TaggingProvider()
        self.folder_service = FolderService()
        self._worker_task: Optional[asyncio.Task] = None
        self._running = False

    async def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._worker_task = asyncio.create_task(self._worker())
        logger.info("Download worker started.")

    async def stop(self) -> None:
        self._running = False
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass
        logger.info("Download worker stopped.")

    async def _worker(self) -> None:
        while self._running:
            try:
                job = await job_queue.dequeue()
                if job:
                    task = asyncio.create_task(self._process(job))
                    await job_queue.register_task(job.id, task)
                    try:
                        await task
                    except asyncio.CancelledError:
                        await self._cleanup(job)
                    finally:
                        await job_queue.unregister_task(job.id)
                else:
                    await asyncio.sleep(2.0)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Worker error: {e}", exc_info=True)
                await asyncio.sleep(5.0)

    async def _transcode_audio(
        self, input_path: str, output_path: str, format: str, bitrate: str = "320"
    ) -> None:
        # Locate local ffmpeg binary
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ffmpeg_path = os.path.join(base_dir, "bin", "ffmpeg.exe")
        if not os.path.exists(ffmpeg_path):
            ffmpeg_path = "ffmpeg"  # fallback to system PATH

        format = format.lower()
        cmd = [ffmpeg_path, "-y", "-i", input_path, "-vn"]

        if format == "mp3":
            cmd.extend(["-ar", "44100", "-ac", "2", "-b:a", f"{bitrate}k", output_path])
        elif format == "flac":
            cmd.extend([output_path])
        elif format in ("m4a", "aac"):
            cmd.extend(["-c:a", "copy", output_path])
        else:
            cmd.extend([output_path])

        logger.info(f"Running transcode: {' '.join(cmd)}")

        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            err_msg = stderr.decode(errors="ignore")
            logger.error(f"ffmpeg transcoding failed: {err_msg}")
            raise Exception(f"Transcoding failed: {err_msg}")

    async def _process(self, job: DownloadJob) -> None:
        conn = await db.get_connection()
        try:
            async with conn.execute(
                "SELECT m.tmdb_id, m.title, m.year, m.poster_url, m.poster_cached_path, m.overview, "
                "m.language, m.genres, m.ott_providers, m.source, m.source_id, m.rating, m.cast_info "
                "FROM movies m JOIN albums a ON a.movie_id=m.id JOIN tracks t ON t.album_id=a.id "
                "WHERE t.id=?",
                (job.track_id,),
            ) as c:
                r = await c.fetchone()
                if not r:
                    await job_queue.mark_failed(job.id, "Movie/Album metadata missing.")
                    return
                movie = Movie(
                    tmdb_id=r[0],
                    title=r[1],
                    year=r[2],
                    poster_url=r[3],
                    poster_cached_path=r[4],
                    overview=r[5],
                    language=r[6],
                    genres=json.loads(r[7]) if r[7] else [],
                    ott_providers=json.loads(r[8]) if r[8] else [],
                    source=r[9],
                    source_id=r[10],
                    rating=r[11],
                    cast_info=r[12],
                )
            async with conn.execute(
                "SELECT a.id, a.spotify_id, a.title, a.artist, a.cover_url, a.cover_cached_path, "
                "a.total_tracks, a.source, a.source_id "
                "FROM albums a JOIN tracks t ON t.album_id=a.id WHERE t.id=?",
                (job.track_id,),
            ) as c:
                r = await c.fetchone()
                album = Album(
                    id=r[0],
                    spotify_id=r[1],
                    title=r[2],
                    artist=r[3],
                    cover_url=r[4],
                    cover_cached_path=r[5],
                    total_tracks=r[6],
                    source=r[7],
                    source_id=r[8],
                )
            async with conn.execute(
                "SELECT id, spotify_id, title, artist, duration_ms, track_number, preview_url, "
                "source, source_id, download_url FROM tracks WHERE id=?",
                (job.track_id,),
            ) as c:
                r = await c.fetchone()
                track = Track(
                    id=r[0],
                    spotify_id=r[1],
                    title=r[2],
                    artist=r[3],
                    duration_ms=r[4],
                    track_number=r[5],
                    preview_url=r[6],
                    source=r[7],
                    source_id=r[8],
                    download_url=r[9],
                )
        finally:
            await conn.close()

        # Cache dedup check
        track_hash = download_cache.generate_hash(
            track.artist, track.title, album.title, track.duration_ms
        )
        target_dir, abs_path = await self.folder_service.get_target_path(
            movie, album, track, job.format
        )
        hit = await download_cache.check(track_hash)

        if hit:
            await job_queue.update_progress(job.id, 50.0, "copying_from_cache")
            try:
                os.makedirs(target_dir, exist_ok=True)
                shutil.copy2(hit["file_path"], abs_path)
                await self.folder_service.write_movie_metadata(movie, target_dir)
                await self.folder_service.generate_m3u_playlist(target_dir, album.title)
                await job_queue.mark_completed(job.id, abs_path)
                return
            except Exception as e:
                logger.error(f"Cache copy failed: {e}")

        # Download
        temp_dir = os.path.join(Path(__file__).resolve().parent.parent, "cache", "temp")
        os.makedirs(temp_dir, exist_ok=True)
        await job_queue.update_progress(job.id, 10.0, "downloading")

        temp_path = None
        for attempt in range(3):
            temp_raw_path = None
            try:
                provider_setting = (
                    await settings_manager.get("download_provider") or "spotiflac"
                )
                use_cdn = (
                    track.download_url
                    and provider_setting != "spotiflac"
                    and job.format.lower() != "flac"
                )

                if use_cdn:
                    logger.info(
                        f"Downloading directly from JioSaavn CDN: {track.download_url}"
                    )
                    temp_raw_path = os.path.join(temp_dir, f"temp_{job.id}_raw.mp4")

                    async with httpx.AsyncClient(timeout=30.0) as client:
                        async with client.stream("GET", track.download_url) as resp:
                            if resp.status_code != 200:
                                raise Exception(
                                    f"Failed to fetch saavncdn URL: status {resp.status_code}"
                                )
                            total_bytes = int(resp.headers.get("content-length", 0))
                            downloaded_bytes = 0
                            with open(temp_raw_path, "wb") as f:
                                async for chunk in resp.iter_bytes(chunk_size=65536):
                                    f.write(chunk)
                                    downloaded_bytes += len(chunk)
                                    if total_bytes > 0:
                                        pct = (downloaded_bytes / total_bytes) * 100.0
                                        # Scale progress from 10% to 50% of the overall download pipeline
                                        scaled_prog = 10.0 + (pct / 100.0) * 40.0
                                        await job_queue.update_progress(
                                            job.id, scaled_prog, "downloading"
                                        )

                    bitrate = await settings_manager.get("bitrate") or "320"
                    dest_ext = job.format.lower()
                    temp_dest_path = os.path.join(temp_dir, f"temp_{job.id}.{dest_ext}")

                    await self._transcode_audio(
                        temp_raw_path, temp_dest_path, job.format, bitrate
                    )

                    if os.path.exists(temp_raw_path):
                        os.remove(temp_raw_path)

                    temp_path = temp_dest_path
                else:
                    if provider_setting == "spotiflac":
                        logger.info("Using SpotiFLAC download provider.")
                        provider = SpotiFLACProvider()
                    else:
                        logger.info("Using Deezspot download provider.")
                        provider = self.download_provider

                    loop = asyncio.get_running_loop()

                    async def provider_progress(prog_pct: float, status_str: str):
                        # Scale progress from 10% to 50%
                        scaled_prog = 10.0 + (prog_pct / 100.0) * 40.0
                        await job_queue.update_progress(
                            job.id, scaled_prog, "downloading"
                        )

                    def sync_progress(prog_pct: float, status_str: str):
                        asyncio.run_coroutine_threadsafe(
                            provider_progress(prog_pct, status_str), loop
                        )

                    temp_path = await provider.download(
                        track=track,
                        format=job.format,
                        output_dir=temp_dir,
                        filename_template="",
                        on_progress=sync_progress,
                    )

                if await self._verify(temp_path, job.format):
                    break
                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)
                temp_path = None
            except Exception as e:
                logger.error(f"Download attempt {attempt + 1} failed: {e}")
                if temp_raw_path and os.path.exists(temp_raw_path):
                    try:
                        os.remove(temp_raw_path)
                    except Exception:
                        pass
                if temp_path and os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except Exception:
                        pass
                temp_path = None
            await asyncio.sleep(2.0)

        if not temp_path:
            await job_queue.mark_failed(
                job.id, "Download integrity failed after 3 retries."
            )
            return

        # Lyrics
        await job_queue.update_progress(job.id, 60.0, "fetching_lyrics")
        lyrics, ltype = await self.lyrics_provider.fetch(track.title, track.artist)
        if lyrics:
            conn = await db.get_connection()
            try:
                await conn.execute(
                    "INSERT INTO lyrics_results (track_id, provider, lyrics_type, content) "
                    "VALUES (?, 'waterfall', ?, ?)",
                    (track.id, ltype, lyrics),
                )
                await conn.commit()
            finally:
                await conn.close()

        # Cover art
        await job_queue.update_progress(job.id, 75.0, "embedding_cover")
        cover = None
        if album.cover_url:
            cover = await image_cache.get_or_download(album.cover_url, "cover")
        if not cover and movie.poster_url:
            cover = await image_cache.get_or_download(movie.poster_url, "poster")
        if cover:
            try:
                await self.tagging_provider.embed_cover(temp_path, cover)
            except Exception as e:
                logger.error(f"Cover embed failed: {e}")

        # Metadata + lyrics tags
        await job_queue.update_progress(job.id, 85.0, "embedding_metadata")
        if lyrics and await settings_manager.get("embed_lyrics") == "true":
            try:
                await self.tagging_provider.embed_lyrics(
                    temp_path, lyrics, ltype == "synced"
                )
            except Exception as e:
                logger.error(f"Lyrics embed failed: {e}")
        try:
            await self.tagging_provider.embed_metadata(
                temp_path,
                track.title,
                track.artist,
                album.title,
                movie.year,
                track.track_number,
            )
        except Exception as e:
            logger.error(f"Metadata embed failed: {e}")

        # Move to destination
        await job_queue.update_progress(job.id, 95.0, "copying_to_destination")
        try:
            os.makedirs(target_dir, exist_ok=True)
            shutil.move(temp_path, abs_path)
            if lyrics and await settings_manager.get("save_lrc_file") == "true":
                ext = "lrc" if ltype == "synced" else "txt"
                with open(
                    abs_path.rsplit(".", 1)[0] + f".{ext}", "w", encoding="utf-8"
                ) as f:
                    f.write(lyrics)
            await download_cache.add(track_hash, abs_path, job.format)
            await self.folder_service.write_movie_metadata(movie, target_dir)
            await self.folder_service.generate_m3u_playlist(target_dir, album.title)
            await job_queue.mark_completed(job.id, abs_path)
        except Exception as e:
            await job_queue.mark_failed(job.id, f"Save error: {e}")

    async def _verify(self, path: str, fmt: str) -> bool:
        if not path or not os.path.exists(path):
            return False
        sz = os.path.getsize(path)
        if sz < (500 * 1024 if fmt.lower() == "mp3" else 2 * 1024 * 1024):
            return False
        if fmt.lower() == "flac":
            try:
                from mutagen.flac import FLAC

                FLAC(path)
            except Exception:
                return False
        return True

    async def _cleanup(self, job: DownloadJob) -> None:
        temp_dir = os.path.join(Path(__file__).resolve().parent.parent, "cache", "temp")
        if os.path.exists(temp_dir):
            for f in os.listdir(temp_dir):
                try:
                    fp = os.path.join(temp_dir, f)
                    if os.path.isfile(fp):
                        os.remove(fp)
                except Exception:
                    pass


download_service = DownloadService()
```

---

### File: `services/movie_song_downloader/services/folder_service.py`
- **Path:** `services/movie_song_downloader/services/folder_service.py`
- **Estimated Tokens:** 835
- **mtime:** 1780856038.246

```python
import os
import re
import json
import logging
from datetime import datetime
from typing import Tuple
from pathlib import Path
from MovieSongDownloader.core.models import Movie, Album, Track
from MovieSongDownloader.core.settings_manager import settings_manager

logger = logging.getLogger("MovieSongDownloader.FolderService")


class FolderService:
    @staticmethod
    def sanitize_name(name: str) -> str:
        if not name:
            return "Unknown"
        s = re.sub(r'[\\/:*?"<>|]', "-", name)
        return re.sub(r"\s+", " ", s).strip() or "Unknown"

    async def get_target_path(
        self, movie: Movie, album: Album, track: Track, fmt: str = "mp3"
    ) -> Tuple[str, str]:
        output_dir = await settings_manager.get("output_dir")
        folder_tpl = await settings_manager.get("folder_format")
        file_tpl = await settings_manager.get("filename_format")

        tokens = {
            "{Year}": str(movie.year) if movie.year else "Unknown",
            "{Movie}": self.sanitize_name(movie.title),
            "{Artist}": self.sanitize_name(track.artist),
            "{Album}": self.sanitize_name(album.title),
            "{TrackNum}": f"{track.track_number:02d}",
            "{Title}": self.sanitize_name(track.title),
        }

        resolved_folder = folder_tpl
        resolved_file = file_tpl
        for k, v in tokens.items():
            resolved_folder = resolved_folder.replace(k, v)
            resolved_file = resolved_file.replace(k, v)

        parts = [self.sanitize_name(p) for p in resolved_folder.split("/") if p.strip()]
        target_dir = Path(output_dir) / Path(*parts)
        filename = f"{self.sanitize_name(resolved_file)}.{fmt.lower()}"
        return str(target_dir), str(target_dir / filename)

    async def write_movie_metadata(self, movie: Movie, target_dir: str) -> None:
        os.makedirs(target_dir, exist_ok=True)
        path = os.path.join(target_dir, "movie.json")
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "tmdb_id": movie.tmdb_id,
                        "title": movie.title,
                        "year": movie.year,
                        "overview": movie.overview,
                        "language": movie.language,
                        "genres": movie.genres,
                        "ott_providers": movie.ott_providers,
                        "exported_at": datetime.now().isoformat(),
                    },
                    f,
                    indent=4,
                )
        except Exception as e:
            logger.error(f"movie.json write failed: {e}")

    async def generate_m3u_playlist(self, target_dir: str, album_title: str) -> None:
        if not os.path.exists(target_dir):
            return
        files = sorted(
            f for f in os.listdir(target_dir) if f.lower().endswith((".mp3", ".flac"))
        )
        if not files:
            return
        try:
            with open(
                os.path.join(target_dir, "playlist.m3u"), "w", encoding="utf-8"
            ) as f:
                f.write(f"#EXTM3U\n#PLAYLIST:{album_title}\n\n")
                for name in files:
                    f.write(f"{name}\n")
        except Exception as e:
            logger.error(f"playlist.m3u failed: {e}")
```

---

### File: `services/movie_song_downloader/services/soundtrack_service.py`
- **Path:** `services/movie_song_downloader/services/soundtrack_service.py`
- **Estimated Tokens:** 1,599
- **mtime:** 1780861103.721

```python
import logging
from typing import List, Optional
from MovieSongDownloader.providers.jiosaavn_provider import JioSaavnProvider
from MovieSongDownloader.core.models import Album, Track
from MovieSongDownloader.providers.metadata_normalizer import normalize_title
from MovieSongDownloader.core.database import db

logger = logging.getLogger("MovieSongDownloader.SoundtrackService")


class SoundtrackService:
    def __init__(self, provider: Optional[JioSaavnProvider] = None):
        self.provider = provider or JioSaavnProvider()

    async def find_soundtracks(
        self,
        movie_title: str,
        movie_year: Optional[int] = None,
        movie_id: Optional[int] = None,
    ) -> List[Album]:
        """Search JioSaavn for soundtrack albums matching the movie, with DB cache support."""
        if movie_id:
            conn = await db.get_connection()
            db_albums = []
            try:
                async with conn.execute(
                    (
                        "SELECT id, movie_id, spotify_id, title, artist, cover_url, "
                        "cover_cached_path, total_tracks, source, source_id FROM albums "
                        "WHERE movie_id = ?"
                    ),
                    (movie_id,),
                ) as c:
                    rows = await c.fetchall()
                    for r in rows:
                        db_albums.append(
                            Album(
                                id=r[0],
                                movie_id=r[1],
                                spotify_id=r[2],
                                title=r[3],
                                artist=r[4],
                                cover_url=r[5],
                                cover_cached_path=r[6],
                                total_tracks=r[7],
                                source=r[8],
                                source_id=r[9],
                            )
                        )
            except Exception as e:
                logger.error(f"Error loading albums from DB: {e}")
            finally:
                await conn.close()
            if db_albums:
                logger.info(
                    f"Loaded {len(db_albums)} albums from local database cache for movie ID {movie_id}."
                )
                return db_albums

        if not movie_title:
            return []
        cleaned = normalize_title(movie_title)
        albums = await self.provider.get_soundtrack(cleaned, year=movie_year)
        if not albums and movie_year:
            # Retry without year filter
            albums = await self.provider.get_soundtrack(cleaned, year=None)
        return albums

    async def get_tracks_for_album(
        self, album_id: str, db_album_id: Optional[int] = None
    ) -> List[Track]:
        """Get all tracks for a JioSaavn or Spotify album, with DB cache support."""
        if db_album_id:
            conn = await db.get_connection()
            db_tracks = []
            try:
                async with conn.execute(
                    (
                        "SELECT id, album_id, spotify_id, title, artist, duration_ms, "
                        "track_number, preview_url, source, source_id, download_url "
                        "FROM tracks WHERE album_id = ?"
                    ),
                    (db_album_id,),
                ) as c:
                    rows = await c.fetchall()
                    for r in rows:
                        db_tracks.append(
                            Track(
                                id=r[0],
                                album_id=r[1],
                                spotify_id=r[2],
                                title=r[3],
                                artist=r[4],
                                duration_ms=r[5],
                                track_number=r[6],
                                preview_url=r[7],
                                source=r[8],
                                source_id=r[9],
                                download_url=r[10],
                            )
                        )
            except Exception as e:
                logger.error(f"Error loading tracks from DB: {e}")
            finally:
                await conn.close()
            if db_tracks:
                logger.info(
                    f"Loaded {len(db_tracks)} tracks from local database cache for album ID {db_album_id}."
                )
                return db_tracks

        if not album_id:
            return []

        # Check album source from DB if db_album_id is provided
        source = "jiosaavn"
        spotify_url = None
        if db_album_id:
            conn = await db.get_connection()
            try:
                async with conn.execute(
                    "SELECT source, source_id FROM albums WHERE id = ?", (db_album_id,)
                ) as c:
                    row = await c.fetchone()
                    if row:
                        source = row[0]
                        if source == "spotify":
                            spotify_url = row[1]
            except Exception as e:
                logger.error(f"Error checking album source: {e}")
            finally:
                await conn.close()

        # Route to SpotifyProvider if source is Spotify
        if source == "spotify" or "spotify.com" in album_id or len(album_id) == 22:
            from MovieSongDownloader.providers.spotify_provider import SpotifyProvider

            spotify_prov = SpotifyProvider()
            url_or_id = spotify_url or album_id
            try:
                _, _, tracks = await spotify_prov.get_spotify_album_or_track(url_or_id)
                return tracks
            except Exception as e:
                logger.error(f"Failed to fetch Spotify tracks for {url_or_id}: {e}")
                return []

        tracks = await self.provider.get_tracks(album_id)
        for t in tracks:
            t.title = normalize_title(t.title)
        return tracks

    async def get_album_details(self, album_id: str) -> Optional[Album]:
        """Get album metadata from JioSaavn."""
        return await self.provider.get_album_details(album_id)

    async def search_songs(self, query: str, limit: int = 10) -> List[Track]:
        """Direct song search on JioSaavn."""
        return await self.provider.search_songs(query, limit=limit)
```

---

### File: `services/movie_song_downloader/services/watchlist_service.py`
- **Path:** `services/movie_song_downloader/services/watchlist_service.py`
- **Estimated Tokens:** 1,862
- **mtime:** 1780861103.721

```python
import logging
from datetime import datetime
from typing import List
from MovieSongDownloader.core.database import db
from MovieSongDownloader.core.models import WatchlistItem, Movie, Album, Track
from MovieSongDownloader.providers.wikipedia_provider import WikipediaProvider
from MovieSongDownloader.services.soundtrack_service import SoundtrackService
from MovieSongDownloader.core.job_queue import job_queue

logger = logging.getLogger("MovieSongDownloader.WatchlistService")


class WatchlistService:
    def __init__(self, wiki=None, soundtrack=None):
        self.wiki = wiki or WikipediaProvider()
        self.soundtrack = soundtrack or SoundtrackService()

    async def add_to_watchlist(self, movie: Movie, auto_download: bool = True) -> int:
        conn = await db.get_connection()
        try:
            c = await conn.execute(
                (
                    "INSERT INTO watchlist (tmdb_id, source_id, title, expected_release, "
                    "auto_download, status, last_checked) "
                    "VALUES (?, ?, ?, ?, ?, 'watching', datetime('now'))"
                ),
                (
                    movie.tmdb_id,
                    movie.source_id,
                    movie.title,
                    movie.year,
                    1 if auto_download else 0,
                ),
            )
            await conn.commit()
            return c.lastrowid
        finally:
            await conn.close()

    async def get_watchlist(self) -> List[WatchlistItem]:
        conn = await db.get_connection()
        try:
            async with conn.execute(
                (
                    "SELECT id, tmdb_id, title, expected_release, last_checked, "
                    "auto_download, status, created_at FROM watchlist"
                )
            ) as c:
                return [
                    WatchlistItem(
                        id=r[0],
                        tmdb_id=r[1],
                        title=r[2],
                        expected_release=r[3],
                        last_checked=r[4],
                        auto_download=bool(r[5]),
                        status=r[6],
                        created_at=r[7],
                    )
                    for r in await c.fetchall()
                ]
        finally:
            await conn.close()

    async def check_releases_and_trigger(self) -> None:
        items = await self.get_watchlist()
        conn = await db.get_connection()
        try:
            for item in items:
                if item.status != "watching":
                    continue
                try:
                    results = await self.wiki.search(item.title)
                    target = next(
                        (m for m in results if m.title.lower() == item.title.lower()),
                        None,
                    )
                    if not target:
                        continue
                    await conn.execute(
                        "UPDATE watchlist SET last_checked=datetime('now') WHERE id=?",
                        (item.id,),
                    )
                    await conn.commit()
                    if target.year and target.year <= datetime.now().year:
                        status = "found"
                        if item.auto_download:
                            albums = await self.soundtrack.find_soundtracks(
                                item.title, movie_year=target.year
                            )
                            if albums:
                                best = albums[0]
                                tracks = await self.soundtrack.get_tracks_for_album(
                                    best.source_id
                                )
                                mid = await self._ensure_movie(conn, target)
                                aid = await self._ensure_album(conn, mid, best)
                                for t in tracks:
                                    tid = await self._ensure_track(conn, aid, t)
                                    await job_queue.enqueue(tid)
                                status = "downloaded"
                        await conn.execute(
                            "UPDATE watchlist SET status=? WHERE id=?",
                            (status, item.id),
                        )
                        await conn.commit()
                except Exception as e:
                    logger.error(f"Watchlist check error for {item.title}: {e}")
        finally:
            await conn.close()

    async def _ensure_movie(self, conn, m: Movie) -> int:
        async with conn.execute(
            "SELECT id FROM movies WHERE source_id=? AND source=?",
            (m.source_id, m.source),
        ) as c:
            r = await c.fetchone()
            if r:
                return r[0]
        # Fallback: check by title+year
        async with conn.execute(
            "SELECT id FROM movies WHERE title=? AND year=?", (m.title, m.year)
        ) as c:
            r = await c.fetchone()
            if r:
                return r[0]
        c = await conn.execute(
            (
                "INSERT INTO movies (tmdb_id, source, source_id, title, year, poster_url, "
                "overview, language, rating, cast_info) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)"
            ),
            (
                m.tmdb_id,
                m.source,
                m.source_id,
                m.title,
                m.year,
                m.poster_url,
                m.overview,
                m.language,
                m.rating,
                m.cast_info,
            ),
        )
        return c.lastrowid

    async def _ensure_album(self, conn, movie_id: int, a: Album) -> int:
        async with conn.execute(
            "SELECT id FROM albums WHERE source_id=? AND source=?",
            (a.source_id, a.source),
        ) as c:
            r = await c.fetchone()
            if r:
                return r[0]
        c = await conn.execute(
            (
                "INSERT INTO albums (movie_id, spotify_id, source, source_id, title, artist, "
                "cover_url, total_tracks) VALUES (?,?,?,?,?,?,?,?)"
            ),
            (
                movie_id,
                a.spotify_id,
                a.source,
                a.source_id,
                a.title,
                a.artist,
                a.cover_url,
                a.total_tracks,
            ),
        )
        return c.lastrowid

    async def _ensure_track(self, conn, album_id: int, t: Track) -> int:
        async with conn.execute(
            "SELECT id FROM tracks WHERE source_id=? AND source=?",
            (t.source_id, t.source),
        ) as c:
            r = await c.fetchone()
            if r:
                return r[0]
        c = await conn.execute(
            (
                "INSERT INTO tracks (album_id, spotify_id, source, source_id, title, artist, "
                "duration_ms, track_number, preview_url, download_url) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)"
            ),
            (
                album_id,
                t.spotify_id,
                t.source,
                t.source_id,
                t.title,
                t.artist,
                t.duration_ms,
                t.track_number,
                t.preview_url,
                t.download_url,
            ),
        )
        return c.lastrowid
```

---

### File: `services/movie_song_downloader/settings_backup.json`
- **Path:** `services/movie_song_downloader/settings_backup.json`
- **Estimated Tokens:** 17
- **mtime:** 1780590896.318

```json
{
    "last_fetch_date": "2000-01-01",
    "omdb_api_key": "test_key"
}
```

---

### File: `services/movie_song_downloader/test_output/spotiflac_result_1nHTOlxSEyyrLH6wzzMJTd.mp3`
- **Path:** `services/movie_song_downloader/test_output/spotiflac_result_1nHTOlxSEyyrLH6wzzMJTd.mp3`
- **Estimated Tokens:** 3
- **mtime:** 1781123079.716

```
mock final file
```

---

### File: `services/movie_song_downloader/test_output/spotiflac_temp_1nHTOlxSEyyrLH6wzzMJTd/track1.flac`
- **Path:** `services/movie_song_downloader/test_output/spotiflac_temp_1nHTOlxSEyyrLH6wzzMJTd/track1.flac`
- **Estimated Tokens:** 3
- **mtime:** 1781123079.711

```
mock audio data
```

---

### File: `services/movie_song_downloader/test_output/spotiflac_temp_1nHTOlxSEyyrLH6wzzMJTd/transcoded.mp3`
- **Path:** `services/movie_song_downloader/test_output/spotiflac_temp_1nHTOlxSEyyrLH6wzzMJTd/transcoded.mp3`
- **Estimated Tokens:** 5
- **mtime:** 1781123079.712

```
mock transcoded audio
```

---

### File: `services/movie_song_downloader/tests/__init__.py`
- **Path:** `services/movie_song_downloader/tests/__init__.py`
- **Estimated Tokens:** 3
- **mtime:** 1780474585.197

```python
# Tests Module
```

---

### File: `services/movie_song_downloader/tests/conftest.py`
- **Path:** `services/movie_song_downloader/tests/conftest.py`
- **Estimated Tokens:** 468
- **mtime:** 1781117033.179

```python
# ruff: noqa: E402
import os
import sys
import importlib
from importlib.abc import MetaPathFinder

# Add workspace root and services directory to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
services_dir = os.path.join(workspace_root, "services")

if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)
if services_dir not in sys.path:
    sys.path.insert(0, services_dir)

# Register Redirector so MovieSongDownloader -> movie_song_downloader works seamlessly
class MovieSongDownloaderRedirector(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname.startswith("MovieSongDownloader"):
            real_name = fullname.replace("MovieSongDownloader", "movie_song_downloader", 1)
            mod = importlib.import_module(real_name)
            sys.modules[fullname] = mod
            return mod.__spec__
        return None

# Only insert if not already present
if not any(isinstance(finder, MovieSongDownloaderRedirector) for finder in sys.meta_path):
    sys.meta_path.insert(0, MovieSongDownloaderRedirector())

import pytest
import MovieSongDownloader.config
from MovieSongDownloader.core.database import db


@pytest.fixture(scope="session", autouse=True)
def use_test_database(tmp_path_factory):
    # Redirect DATABASE_PATH to a temporary test database file
    test_db_dir = tmp_path_factory.mktemp("test_db_dir")
    test_db_path = test_db_dir / "test_db.sqlite3"

    # Patch the configuration path and the instantiated database manager path
    MovieSongDownloader.config.DATABASE_PATH = test_db_path
    db.db_path = test_db_path

    yield

    # Cleanup after the test session finishes
    if test_db_path.exists():
        try:
            os.remove(test_db_path)
        except Exception:
            pass
```

---

### File: `services/movie_song_downloader/tests/test_cache.py`
- **Path:** `services/movie_song_downloader/tests/test_cache.py`
- **Estimated Tokens:** 277
- **mtime:** 1780856038.263

```python
import pytest
from MovieSongDownloader.core.database import db
from MovieSongDownloader.core.cache_manager import download_cache, api_cache


@pytest.mark.asyncio
async def test_api_cache_operations():
    # Force initialization first
    await db.run_migrations()

    key = "test_spotify_endpoint"
    payload = {"data": [1, 2, 3]}

    # Check cache miss
    miss = await api_cache.get(key)
    assert miss is None

    # Save cache with 5 seconds expiry
    await api_cache.set(key, "spotify", payload, expires_in_seconds=5)

    # Check cache hit
    hit = await api_cache.get(key)
    assert hit == payload

    # Save cache with -1 seconds expiry (expired)
    await api_cache.set(key, "spotify", payload, expires_in_seconds=-1)

    # Check cache expired (should return None)
    expired = await api_cache.get(key)
    assert expired is None


@pytest.mark.asyncio
async def test_download_cache_hash():
    h1 = download_cache.generate_hash("Artist", "Song", "Album", 200000)
    h2 = download_cache.generate_hash("artist", "song", "album", 200000)

    # Check case-insensitivity
    assert h1 == h2
```

---

### File: `services/movie_song_downloader/tests/test_cache_verification.py`
- **Path:** `services/movie_song_downloader/tests/test_cache_verification.py`
- **Estimated Tokens:** 328
- **mtime:** 1780856038.264

```python
import pytest
from MovieSongDownloader.core.database import db
from MovieSongDownloader.core.cache_manager import api_cache


@pytest.mark.asyncio
async def test_cache_verification_logic():
    await db.run_migrations()

    # Mock DB cache clear
    conn = await db.get_connection()
    try:
        await conn.execute("DELETE FROM api_cache")
        await conn.commit()
    finally:
        await conn.close()

    cache_key = "test_verification_key"
    cached_data = {
        "id": "123",
        "title": "Old Title",
        "rating": "7.5",
        "cast": "Old Cast",
    }

    # Verify when cache is empty, returns new data directly
    result = await api_cache.verify_scraped_data(
        cache_key, cached_data, ["rating", "cast"]
    )
    assert result == cached_data

    # Set initial cache
    await api_cache.set(cache_key, "test", cached_data)

    new_data = {"id": "456", "title": "New Title", "rating": "8.5", "cast": "New Cast"}

    # Verify fields (volatile fields rating/cast are updated, but id/title are kept from cached_data)
    result = await api_cache.verify_scraped_data(
        cache_key, new_data, ["rating", "cast"]
    )
    assert result["id"] == "123"
    assert result["title"] == "Old Title"
    assert result["rating"] == "8.5"
    assert result["cast"] == "New Cast"
```

---

### File: `services/movie_song_downloader/tests/test_event_bus.py`
- **Path:** `services/movie_song_downloader/tests/test_event_bus.py`
- **Estimated Tokens:** 174
- **mtime:** 1780856038.272

```python
import pytest
from MovieSongDownloader.core.event_bus import EventBus, Event


@pytest.mark.asyncio
async def test_event_bus_pub_sub():
    bus = EventBus()
    received_data = []

    async def callback(event: Event):
        received_data.append(event.data)

    # Subscribe callback to event
    await bus.subscribe("test.event", callback)

    # Publish event
    await bus.publish(Event("test.event", {"val": 42}))

    assert len(received_data) == 1
    assert received_data[0]["val"] == 42

    # Unsubscribe
    await bus.unsubscribe("test.event", callback)
    await bus.publish(Event("test.event", {"val": 100}))

    # Received list should not change
    assert len(received_data) == 1
```

---

### File: `services/movie_song_downloader/tests/test_folder_service.py`
- **Path:** `services/movie_song_downloader/tests/test_folder_service.py`
- **Estimated Tokens:** 375
- **mtime:** 1780856038.29

```python
import pytest
from MovieSongDownloader.services.folder_service import FolderService
from MovieSongDownloader.core.models import Movie, Album, Track


def test_sanitize_name():
    # Remove Windows invalid characters
    assert (
        FolderService.sanitize_name("Leo: Naan Ready? *FLAC*")
        == "Leo- Naan Ready- -FLAC-"
    )
    assert FolderService.sanitize_name("Artist / Title") == "Artist - Title"
    assert FolderService.sanitize_name("") == "Unknown"


@pytest.mark.asyncio
async def test_target_path_generation(monkeypatch):
    service = FolderService()

    # Mock settings manager keys
    from MovieSongDownloader.core.settings_manager import settings_manager

    async def mock_get(key):
        if key == "output_dir":
            return "C:/Downloads"
        elif key == "folder_format":
            return "{Year}/{Movie}/Songs"
        elif key == "filename_format":
            return "{TrackNum} - {Title}"
        return ""

    monkeypatch.setattr(settings_manager, "get", mock_get)

    movie = Movie(title="Inception", year=2010)
    album = Album(title="Inception OST")
    track = Track(title="Time", track_number=5, artist="Hans Zimmer")

    target_dir, file_path = await service.get_target_path(movie, album, track, "mp3")

    # Verify proper replacements and path construction
    assert (
        "C:\\Downloads\\2010\\Inception\\Songs" in target_dir
        or "C:/Downloads/2010/Inception/Songs" in target_dir
    )
    assert "05 - Time.mp3" in file_path
```

---

### File: `services/movie_song_downloader/tests/test_jiosaavn_provider.py`
- **Path:** `services/movie_song_downloader/tests/test_jiosaavn_provider.py`
- **Estimated Tokens:** 666
- **mtime:** 1780856038.293

```python
import pytest
from unittest.mock import patch
from MovieSongDownloader.core.database import db
from MovieSongDownloader.providers.jiosaavn_provider import JioSaavnProvider


@pytest.mark.asyncio
async def test_jiosaavn_search_album():
    await db.run_migrations()

    # Mock DB cache clear
    conn = await db.get_connection()
    try:
        await conn.execute("DELETE FROM api_cache")
        await conn.commit()
    finally:
        await conn.close()

    provider = JioSaavnProvider()

    # Mock the JioSaavn SDK's search_albums call
    mock_albums = [
        {
            "album_id": "alb_123",
            "title": "Vikram",
            "artists": "Anirudh Ravichander",
            "track_count": 5,
            "thumbnails": {"quality": {"500x500": "https://images.xyz/vikram_500.jpg"}},
        }
    ]

    with patch.object(
        provider._client, "search_albums", return_value=mock_albums
    ) as mock_search:
        albums = await provider.get_soundtrack("Vikram", 2022)
        assert len(albums) == 1
        assert albums[0].source == "jiosaavn"
        assert albums[0].source_id == "alb_123"
        assert albums[0].title == "Vikram"
        assert albums[0].artist == "Anirudh Ravichander"
        assert albums[0].cover_url == "https://images.xyz/vikram_500.jpg"
        mock_search.assert_called_once_with("Vikram 2022", limit=8)


@pytest.mark.asyncio
async def test_jiosaavn_get_tracks():
    await db.run_migrations()
    provider = JioSaavnProvider()

    # Mock the JioSaavn SDK's album_info call
    mock_info = {
        "album_id": "alb_123",
        "title": "Vikram",
        "tracks": [
            {
                "track_id": "trk_999",
                "title": "Pathala Pathala",
                "primary_artists": "Anirudh Ravichander, Kamal Haasan",
                "duration": 210,
                "stream_urls": {
                    "very_high_quality": "https://stream.xyz/pathala_320.mp3",
                    "low_quality": "https://stream.xyz/pathala_96.mp3",
                },
            }
        ],
    }

    with patch.object(
        provider._client, "album_info", return_value=mock_info
    ) as mock_info_call:
        tracks = await provider.get_tracks("alb_123")
        assert len(tracks) == 1
        assert tracks[0].source == "jiosaavn"
        assert tracks[0].source_id == "trk_999"
        assert tracks[0].title == "Pathala Pathala"
        assert tracks[0].artist == "Anirudh Ravichander, Kamal Haasan"
        assert tracks[0].duration_ms == 210000
        assert tracks[0].download_url == "https://stream.xyz/pathala_320.mp3"
        mock_info_call.assert_called_once_with("alb_123")
```

---

### File: `services/movie_song_downloader/tests/test_job_queue.py`
- **Path:** `services/movie_song_downloader/tests/test_job_queue.py`
- **Estimated Tokens:** 453
- **mtime:** 1780861886.644

```python
import pytest
from MovieSongDownloader.core.database import db
from MovieSongDownloader.core.job_queue import job_queue


@pytest.mark.asyncio
async def test_job_queue_state_transitions():
    await db.run_migrations()

    conn = await db.get_connection()
    try:
        # Seed a dummy movie, album, and track to satisfy foreign keys
        await conn.execute(
            (
                "INSERT OR REPLACE INTO movies (id, tmdb_id, title) "
                "VALUES (99, 999, 'Test Movie')"
            )
        )
        await conn.execute(
            (
                "INSERT OR REPLACE INTO albums (id, movie_id, spotify_id, title) "
                "VALUES (99, 99, 'album_99', 'Test Album')"
            )
        )
        await conn.execute(
            (
                "INSERT OR REPLACE INTO tracks (id, album_id, spotify_id, title, track_number) "
                "VALUES (99, 99, 'track_99', 'Test Track', 1)"
            )
        )
        await conn.commit()
    finally:
        await conn.close()

    # Enqueue a job
    job_id = await job_queue.enqueue(track_id=99, format="mp3")
    assert job_id > 0

    # Dequeue the job
    job = await job_queue.dequeue()
    assert job is not None
    assert job.id == job_id
    assert job.status == "queued"

    # Update progress
    await job_queue.update_progress(job_id, 45.0, "downloading")

    # Verify status changed
    jobs = await job_queue.get_all_jobs()
    active_job = [j for j in jobs if j.id == job_id][0]
    assert active_job.status == "downloading"
    assert active_job.progress == 45.0

    # Cancel job
    await job_queue.cancel(job_id)

    # Verify status is cancelled
    jobs = await job_queue.get_all_jobs()
    cancelled_job = [j for j in jobs if j.id == job_id][0]
    assert cancelled_job.status == "cancelled"
```

---

### File: `services/movie_song_downloader/tests/test_lyrics_waterfall.py`
- **Path:** `services/movie_song_downloader/tests/test_lyrics_waterfall.py`
- **Estimated Tokens:** 430
- **mtime:** 1780856038.303

```python
import pytest
import asyncio
from MovieSongDownloader.providers.lyrics_provider import LyricsProvider


def test_lyrics_sync_detection():
    provider = LyricsProvider()

    synced_text = (
        "[00:12.34] Synced line one\n"
        "[00:15.50] Synced line two\n"
        "[00:19.00] Synced line three\n"
    )

    plain_text = "This is line one\nThis is line two\nThis is line three\n"

    # Check regex sync detection
    assert provider._is_synced(synced_text) is True
    assert provider._is_synced(plain_text) is False
    assert provider._is_synced("") is False


@pytest.mark.asyncio
async def test_waterfall_priority_fallback(monkeypatch):
    provider = LyricsProvider()

    # Mock settings manager keys
    from MovieSongDownloader.core.settings_manager import settings_manager

    async def mock_get(key):
        return '["lrclib", "genius"]'  # Custom waterfall subset

    monkeypatch.setattr(settings_manager, "get", mock_get)

    calls = []

    # Mock thread executor helper _sync_search_task
    async def mock_thread(func, *args):
        # args[0] is search_query, args[1] is provider
        provider_name = args[1]
        calls.append(provider_name)
        if provider_name == "lrclib":
            return None  # Simulate miss
        elif provider_name == "genius":
            return "Genius plain text lyrics content"  # Simulate hit
        return None

    monkeypatch.setattr(asyncio, "to_thread", mock_thread)

    lyrics, lyrics_type = await provider.fetch("Title", "Artist")

    # Verify both providers were queried in sequence
    assert "lrclib" in calls
    assert "genius" in calls
    assert lyrics == "Genius plain text lyrics content"
    assert lyrics_type == "plain"
```

---

### File: `services/movie_song_downloader/tests/test_movie_service.py`
- **Path:** `services/movie_song_downloader/tests/test_movie_service.py`
- **Estimated Tokens:** 1,105
- **mtime:** 1780856038.309

```python
import pytest
import datetime
from unittest.mock import AsyncMock, MagicMock
from MovieSongDownloader.core.database import db
from MovieSongDownloader.core.models import Movie
from MovieSongDownloader.core.settings_manager import settings_manager
from MovieSongDownloader.services.movie_service import MovieService


@pytest.mark.asyncio
async def test_get_today_releases_fresh_fetch():
    # Arrange: Ensure migrations are run and settings/movies are clean
    await db.run_migrations()

    conn = await db.get_connection()
    try:
        await conn.execute("DELETE FROM settings")
        await conn.execute("DELETE FROM movies")
        await conn.commit()
    finally:
        await conn.close()

    await settings_manager.set("last_fetch_date", "2000-01-01")  # Outdated date
    await settings_manager.set(
        "scraping_limit", "0"
    )  # Avoid OMDb enrichment calls for stubs in this test

    mock_movie = Movie(
        tmdb_id=123,
        source="wikipedia",
        source_id="p123",
        title="Test Movie 2026",
        year=datetime.date.today().year,
        poster_url="http://example.com/poster.jpg",
    )

    wiki_mock = MagicMock()
    wiki_mock.get_today_releases = AsyncMock(return_value=[mock_movie])

    service = MovieService(wiki_provider=wiki_mock)

    # Act
    movies = await service.get_today_releases("IN")

    # Assert
    assert len(movies) == 1
    assert movies[0].title == "Test Movie 2026"
    wiki_mock.get_today_releases.assert_called_once_with(region="IN")

    # Check that settings updated the date
    saved_date = await settings_manager.get("last_fetch_date")
    assert saved_date == datetime.date.today().isoformat()


@pytest.mark.asyncio
async def test_get_today_releases_from_cache():
    # Arrange: Populate DB and update last_fetch_date to today
    await db.run_migrations()

    conn = await db.get_connection()
    try:
        await conn.execute("DELETE FROM settings")
        await conn.execute("DELETE FROM movies")
        await conn.commit()
    finally:
        await conn.close()

    current_year = datetime.date.today().year
    current_date_str = datetime.date.today().isoformat()
    await settings_manager.set("last_fetch_date", current_date_str)

    # Seed a cached movie
    service = MovieService()
    cached_movie = Movie(
        tmdb_id=456,
        source="wikipedia",
        source_id="p456",
        title="Cached Movie 2026",
        year=current_year,
        poster_url="http://example.com/cached.jpg",
        release_date=current_date_str,
    )
    await service._db_save_movie_album_tracks(cached_movie, None, [])

    wiki_mock = MagicMock()
    wiki_mock.get_today_releases = AsyncMock()

    service_with_mock = MovieService(wiki_provider=wiki_mock)

    # Act
    movies = await service_with_mock.get_today_releases("IN")

    # Assert: Should load directly from DB cache, meaning wiki_provider is not called
    assert len(movies) == 1
    assert movies[0].title == "Cached Movie 2026"
    wiki_mock.get_today_releases.assert_not_called()


@pytest.mark.asyncio
async def test_get_today_releases_fallback_on_failure():
    # Arrange: Populate DB but set last_fetch_date to outdated
    await db.run_migrations()

    conn = await db.get_connection()
    try:
        await conn.execute("DELETE FROM settings")
        await conn.execute("DELETE FROM movies")
        await conn.commit()
    finally:
        await conn.close()

    current_year = datetime.date.today().year
    await settings_manager.set("last_fetch_date", "2000-01-01")

    # Seed older cached movie
    service = MovieService()
    cached_movie = Movie(
        tmdb_id=789,
        source="wikipedia",
        source_id="p789",
        title="Fallback Movie 2026",
        year=current_year,
        poster_url="http://example.com/fallback.jpg",
        release_date="2026-01-01",
    )
    await service._db_save_movie_album_tracks(cached_movie, None, [])

    # Mock wiki provider to raise an exception
    wiki_mock = MagicMock()
    wiki_mock.get_today_releases = AsyncMock(side_effect=Exception("Network error"))

    service_with_mock = MovieService(wiki_provider=wiki_mock)

    # Act
    movies = await service_with_mock.get_today_releases("IN")

    # Assert: Should gracefully fallback to DB cache
    assert len(movies) == 1
    assert movies[0].title == "Fallback Movie 2026"
    wiki_mock.get_today_releases.assert_called_once()
```

---

### File: `services/movie_song_downloader/tests/test_musicbrainz_provider.py`
- **Path:** `services/movie_song_downloader/tests/test_musicbrainz_provider.py`
- **Estimated Tokens:** 524
- **mtime:** 1780856038.31

```python
import pytest
from unittest.mock import patch
from MovieSongDownloader.providers.musicbrainz_provider import MusicBrainzProvider
from MovieSongDownloader.core.models import Album, Track
from MovieSongDownloader.core.database import db


@pytest.mark.asyncio
async def test_musicbrainz_enrich_album():
    await db.run_migrations()
    provider = MusicBrainzProvider()

    # Mock album and tracks
    album = Album(title="Vikram", artist="Anirudh Ravichander")
    tracks = [Track(title="Pathala Pathala"), Track(title="Wasted")]

    # Mock search response
    mock_search = {
        "release-groups": [
            {
                "id": "rg_123",
                "title": "Vikram",
                "artist-credit": [{"artist": {"name": "Anirudh Ravichander"}}],
            }
        ]
    }

    # Mock browse response containing tracks and ISRCs
    mock_browse = {
        "releases": [
            {
                "title": "Vikram",
                "id": "rel_456",
                "media": [
                    {
                        "tracks": [
                            {
                                "title": "Pathala Pathala",
                                "recording": {"isrcs": ["IN-A23-22-00001"]},
                            },
                            {
                                "title": "Wasted",
                                "recording": {"isrcs": ["IN-A23-22-00002"]},
                            },
                        ]
                    }
                ],
            }
        ]
    }

    async def mock_mb_req_handler(url, params):
        if "release-group" in url:
            return mock_search
        elif "release" in url:
            return mock_browse
        return None

    with patch.object(provider, "_mb_request", side_effect=mock_mb_req_handler):
        composer, isrc_map = await provider.enrich_album(album, tracks)
        assert composer == "Anirudh Ravichander"
        assert len(isrc_map) == 2
        assert isrc_map["Pathala Pathala"] == "IN-A23-22-00001"
        assert isrc_map["Wasted"] == "IN-A23-22-00002"
```

---

### File: `services/movie_song_downloader/tests/test_normalizer.py`
- **Path:** `services/movie_song_downloader/tests/test_normalizer.py`
- **Estimated Tokens:** 513
- **mtime:** 1780856038.315

```python
from MovieSongDownloader.providers.metadata_normalizer import (
    normalize_title,
    confidence_score,
)


def test_normalize_title():
    # Suffixes should be stripped
    assert normalize_title("Naan Ready (From Leo)") == "Naan Ready"
    assert (
        normalize_title("Inception (Original Motion Picture Soundtrack)") == "Inception"
    )
    assert normalize_title("Song Title (Official Audio)") == "Song Title"
    assert normalize_title("Remastered Track (Remastered 2020)") == "Remastered Track"
    assert normalize_title("Featured Track (feat. Artist Name)") == "Featured Track"

    # Normal title should remain untouched
    assert normalize_title("Stay") == "Stay"


def test_confidence_score_exact():
    source = {
        "title": "Leo Naan Ready",
        "artist": "Anirudh",
        "album": "Leo",
        "duration_ms": 240000,
    }
    target = {
        "title": "Leo Naan Ready",
        "artist": "Anirudh",
        "album": "Leo",
        "duration_ms": 240000,
    }
    # Exact match should score high
    score = confidence_score(source, target)
    assert score == 100


def test_confidence_score_close():
    source = {
        "title": "Naan Ready (From Leo)",
        "artist": "Anirudh Ravichander",
        "album": "Leo",
        "duration_ms": 241000,
    }
    target = {
        "title": "Naan Ready",
        "artist": "Anirudh",
        "album": "Leo",
        "duration_ms": 240000,
    }
    # Close match with cleanable suffix, close artist string, and minor duration delta (1s) should score >= 80
    score = confidence_score(source, target)
    assert score >= 80


def test_confidence_score_different():
    source = {
        "title": "Different Song",
        "artist": "Anirudh",
        "album": "Leo",
        "duration_ms": 180000,
    }
    target = {
        "title": "Naan Ready",
        "artist": "Anirudh",
        "album": "Leo",
        "duration_ms": 240000,
    }
    # Completely different tracks should score low
    score = confidence_score(source, target)
    assert score < 60
```

---

### File: `services/movie_song_downloader/tests/test_omdb_provider.py`
- **Path:** `services/movie_song_downloader/tests/test_omdb_provider.py`
- **Estimated Tokens:** 583
- **mtime:** 1780856038.319

```python
import pytest
from unittest.mock import patch, MagicMock
from MovieSongDownloader.core.database import db
from MovieSongDownloader.core.settings_manager import settings_manager
from MovieSongDownloader.core.models import Movie
from MovieSongDownloader.providers.omdb_provider import OMDbProvider


@pytest.mark.asyncio
async def test_omdb_enrich_movie():
    await db.run_migrations()

    # Seed API key setting
    await settings_manager.set("omdb_api_key", "test_key")

    # Mock DB cache clear
    conn = await db.get_connection()
    try:
        await conn.execute("DELETE FROM api_cache")
        await conn.commit()
    finally:
        await conn.close()

    provider = OMDbProvider()

    # Un-enriched movie with empty source_id (should be enriched with imdbID)
    movie = Movie(source="wikipedia", source_id="", title="Vikram", year=2022)

    mock_omdb_resp = {
        "Response": "True",
        "Title": "Vikram",
        "Year": "2022",
        "imdbID": "tt1234567",
        "imdbRating": "8.3",
        "Actors": "Kamal Haasan, Vijay Sethupathi, Fahadh Faasil",
        "Plot": "A special agent investigates a case of serial killings...",
        "Genre": "Action, Thriller",
        "Language": "Tamil",
        "Poster": "https://image.xyz/poster.jpg",
    }

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_omdb_resp

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        enriched = await provider.enrich_movie(movie)
        assert enriched.rating == "8.3"
        assert enriched.cast_info == "Kamal Haasan, Vijay Sethupathi, Fahadh Faasil"
        assert enriched.poster_url == "https://image.xyz/poster.jpg"
        assert "special agent" in enriched.overview
        assert "Action" in enriched.genres
        assert enriched.language == "Tamil"
        # Since source_id was empty, it should be set to imdbID
        assert enriched.source_id == "tt1234567"

    # Test that pre-populated source_id is not overwritten
    movie_with_id = Movie(
        source="wikipedia", source_id="12345", title="Vikram", year=2022
    )
    with patch("httpx.AsyncClient.get", return_value=mock_response):
        enriched_with_id = await provider.enrich_movie(movie_with_id)
        assert enriched_with_id.source_id == "12345"
```

---

### File: `services/movie_song_downloader/tests/test_spotiflac_provider.py`
- **Path:** `services/movie_song_downloader/tests/test_spotiflac_provider.py`
- **Estimated Tokens:** 744
- **mtime:** 1780856316.158

```python
import pytest
import os
from unittest.mock import patch, MagicMock, AsyncMock
from MovieSongDownloader.core.models import Track
from MovieSongDownloader.providers.spotiflac_provider import SpotiFLACProvider


@pytest.mark.asyncio
async def test_resolve_spotify_url():
    provider = SpotiFLACProvider()

    # Mock DDG HTML response containing track url
    mock_html = '<html><body><a href="https://open.spotify.com/track/1nHTOlxSEyyrLH6wzzMJTd">Link</a></body></html>'
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = mock_html

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        url = await provider._resolve_spotify_url("Armageddon", "A.R. Rahman")
        assert url == "https://open.spotify.com/track/1nHTOlxSEyyrLH6wzzMJTd"


@pytest.mark.asyncio
async def test_spotiflac_download():
    provider = SpotiFLACProvider()

    track = Track(
        source="spotify",
        source_id="1nHTOlxSEyyrLH6wzzMJTd",
        title="Armageddon",
        artist="A.R. Rahman",
        track_number=1,
    )

    # Mock settings_manager.get
    async def mock_settings_get(key):
        if key == "deezer_arl":
            return "test_arl"
        return None

    # Mock subprocess execution
    mock_process = AsyncMock()
    mock_process.returncode = 0
    mock_process.communicate.return_value = (b"Downloaded successfully", b"")

    # Mock os.walk and file creation
    temp_file_created = None

    def mock_walk(top, topdown=True, onerror=None, followlinks=False):
        nonlocal temp_file_created
        # Create a mock file in the temp subfolder to simulate download
        # Top is output_dir/spotiflac_temp_1nHTOlxSEyyrLH6wzzMJTd
        temp_file_created = os.path.join(top, "track1.flac")
        os.makedirs(top, exist_ok=True)
        with open(temp_file_created, "w") as f:
            f.write("mock audio data")
        return [(top, [], ["track1.flac"])]

    # Mock _transcode_audio to avoid actual ffmpeg running
    async def mock_transcode(input_path, output_path, format_str, bitrate):
        with open(output_path, "w") as f:
            f.write("mock transcoded audio")

    # Mock shutil.move
    def mock_move(src, dst):
        with open(dst, "w") as f:
            f.write("mock final file")

    with (
        patch(
            "MovieSongDownloader.providers.spotiflac_provider.settings_manager.get",
            side_effect=mock_settings_get,
        ),
        patch("asyncio.create_subprocess_exec", return_value=mock_process),
        patch("os.walk", side_effect=mock_walk),
        patch.object(provider, "_transcode_audio", side_effect=mock_transcode),
        patch("shutil.move", side_effect=mock_move),
        patch("shutil.rmtree"),
    ):
        result_path = await provider.download(
            track=track, format="mp3", output_dir="./test_output", filename_template=""
        )

        assert "spotiflac_result_1nHTOlxSEyyrLH6wzzMJTd.mp3" in result_path
```

---

### File: `services/movie_song_downloader/tests/test_spotify_provider.py`
- **Path:** `services/movie_song_downloader/tests/test_spotify_provider.py`
- **Estimated Tokens:** 1,301
- **mtime:** 1780861886.644

```python
import pytest
import json
from unittest.mock import patch, MagicMock
from MovieSongDownloader.providers.spotify_provider import SpotifyProvider


@pytest.mark.asyncio
async def test_get_spotify_album():
    provider = SpotifyProvider()

    # Mock embed page HTML response for album
    mock_entity = {
        "type": "album",
        "title": "Ponniyin Selvan - Original Score",
        "subtitle": "A.R. Rahman",
        "id": "7y3bI6blXr4I8l4kKGcBfE",
        "visualIdentity": {
            "image": [
                {
                    "url": "https://image.xyz/cover_small.jpg",
                    "maxHeight": 300,
                    "maxWidth": 300,
                },
                {
                    "url": "https://image.xyz/cover_large.jpg",
                    "maxHeight": 640,
                    "maxWidth": 640,
                },
            ]
        },
        "trackList": [
            {
                "uri": "spotify:track:1nHTOlxSEyyrLH6wzzMJTd",
                "title": "Armageddon",
                "subtitle": "A.R. Rahman",
                "duration": 269000,
                "audioPreview": {"url": "https://preview.xyz/track1.mp3"},
            },
            {
                "uri": "spotify:track:2nHTOlxSEyyrLH6wzzMJTz",
                "title": "Solaikuyil",
                "subtitle": "A.R. Rahman, Shreya Ghoshal",
                "duration": 310000,
                "audioPreview": None,
            },
        ],
    }

    mock_state_data = {
        "props": {"pageProps": {"state": {"data": {"entity": mock_entity}}}}
    }

    mock_html = (
        '<html><body><script id="__NEXT_DATA__" type="application/json">'
        + json.dumps(mock_state_data)
        + "</script></body></html>"
    )

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = mock_html

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        movie, album, tracks = await provider.get_spotify_album_or_track(
            "https://open.spotify.com/album/7y3bI6blXr4I8l4kKGcBfE"
        )

        # Verify Movie
        assert movie.source == "spotify"
        assert movie.source_id == "7y3bI6blXr4I8l4kKGcBfE"
        assert movie.title == "Ponniyin Selvan - Original Score"
        assert movie.poster_url == "https://image.xyz/cover_large.jpg"

        # Verify Album
        assert album.source == "spotify"
        assert album.source_id == "7y3bI6blXr4I8l4kKGcBfE"
        assert album.title == "Ponniyin Selvan - Original Score"
        assert album.artist == "A.R. Rahman"
        assert album.cover_url == "https://image.xyz/cover_large.jpg"
        assert album.total_tracks == 2

        # Verify Tracks
        assert len(tracks) == 2
        assert tracks[0].title == "Armageddon"
        assert tracks[0].artist == "A.R. Rahman"
        assert tracks[0].source_id == "1nHTOlxSEyyrLH6wzzMJTd"
        assert tracks[0].duration_ms == 269000
        assert tracks[0].track_number == 1
        assert tracks[0].preview_url == "https://preview.xyz/track1.mp3"

        assert tracks[1].title == "Solaikuyil"
        assert tracks[1].artist == "A.R. Rahman, Shreya Ghoshal"
        assert tracks[1].source_id == "2nHTOlxSEyyrLH6wzzMJTz"
        assert tracks[1].track_number == 2
        assert tracks[1].preview_url is None


@pytest.mark.asyncio
async def test_get_spotify_track():
    provider = SpotifyProvider()

    # Mock embed page HTML response for track
    mock_entity = {
        "type": "track",
        "title": "Armageddon",
        "name": "Armageddon",
        "id": "1nHTOlxSEyyrLH6wzzMJTd",
        "artists": [{"name": "A.R. Rahman"}],
        "duration": 269000,
        "visualIdentity": {
            "image": [
                {
                    "url": "https://image.xyz/track_large.jpg",
                    "maxHeight": 640,
                    "maxWidth": 640,
                }
            ]
        },
        "audioPreview": {"url": "https://preview.xyz/track1.mp3"},
    }

    mock_state_data = {
        "props": {"pageProps": {"state": {"data": {"entity": mock_entity}}}}
    }

    mock_html = (
        '<html><body><script id="__NEXT_DATA__" type="application/json">'
        + json.dumps(mock_state_data)
        + "</script></body></html>"
    )

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = mock_html

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        movie, album, tracks = await provider.get_spotify_album_or_track(
            "https://open.spotify.com/track/1nHTOlxSEyyrLH6wzzMJTd"
        )

        # Verify single wrapped track
        assert movie.title == "Armageddon"
        assert movie.poster_url == "https://image.xyz/track_large.jpg"

        assert album.title == "Armageddon"
        assert album.artist == "A.R. Rahman"
        assert album.total_tracks == 1

        assert len(tracks) == 1
        assert tracks[0].title == "Armageddon"
        assert tracks[0].artist == "A.R. Rahman"
        assert tracks[0].source_id == "1nHTOlxSEyyrLH6wzzMJTd"
        assert tracks[0].track_number == 1
        assert tracks[0].preview_url == "https://preview.xyz/track1.mp3"
```

---

### File: `services/movie_song_downloader/tests/test_wikidata_provider.py`
- **Path:** `services/movie_song_downloader/tests/test_wikidata_provider.py`
- **Estimated Tokens:** 284
- **mtime:** 1780856038.338

```python
import pytest
from unittest.mock import patch
from MovieSongDownloader.providers.wikidata_provider import WikidataProvider
from MovieSongDownloader.core.database import db


@pytest.mark.asyncio
async def test_wikidata_get_posters_batch():
    await db.run_migrations()
    provider = WikidataProvider()

    # Mock response from Wikidata wbgetentities API
    mock_response = {
        "entities": {
            "Q102147287": {
                "sitelinks": {"enwiki": {"title": "Vikram (2022 film)"}},
                "claims": {
                    "P18": [{"mainsnak": {"datavalue": {"value": "Vikram_poster.jpg"}}}]
                },
            }
        }
    }

    with patch.object(
        provider, "_wikidata_request", return_value=mock_response
    ) as mock_req:
        results = await provider.get_posters_batch(["Vikram (2022 film)"], lang="en")
        assert len(results) == 1
        assert "Vikram (2022 film)" in results
        assert (
            results["Vikram (2022 film)"]
            == "https://commons.wikimedia.org/wiki/Special:FilePath/Vikram_poster.jpg"
        )
        mock_req.assert_called_once()
```

---

### File: `services/movie_song_downloader/tests/test_wikipedia_provider.py`
- **Path:** `services/movie_song_downloader/tests/test_wikipedia_provider.py`
- **Estimated Tokens:** 596
- **mtime:** 1780861886.648

```python
import pytest
from unittest.mock import patch, MagicMock
from MovieSongDownloader.core.database import db
from MovieSongDownloader.providers.wikipedia_provider import WikipediaProvider


@pytest.mark.asyncio
async def test_wikipedia_search():
    await db.run_migrations()

    # Mock DB cache clear
    conn = await db.get_connection()
    try:
        await conn.execute("DELETE FROM api_cache")
        await conn.commit()
    finally:
        await conn.close()

    provider = WikipediaProvider()

    mock_search_resp = {
        "query": {
            "search": [
                {
                    "title": "Vikram (2022 film)",
                    "snippet": (
                        "Vikram is a 2022 Indian Tamil-language action thriller film "
                        "directed by Lokesh Kanagaraj..."
                    ),
                    "pageid": 12345,
                }
            ]
        }
    }

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_search_resp

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        results = await provider.search("Vikram", year=2022)
        assert len(results) > 0
        assert results[0].title == "Vikram"
        assert results[0].year == 2022
        assert results[0].source == "wikipedia"
        assert results[0].source_id == "12345"


@pytest.mark.asyncio
async def test_wikipedia_get_details():
    await db.run_migrations()
    provider = WikipediaProvider()

    mock_details_resp = {
        "query": {
            "pages": {
                "12345": {
                    "title": "Vikram (2022 film)",
                    "thumbnail": {"source": "https://image.xyz/vikram.jpg"},
                    "extract": (
                        "Vikram is a 2022 action thriller..."
                    ),
                }
            }
        }
    }

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_details_resp

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        movie = await provider.get_movie_details("12345")
        assert movie is not None
        assert movie.title == "Vikram"
        assert movie.year == 2022
        assert movie.poster_url == "https://image.xyz/vikram.jpg"
        assert "action thriller" in movie.overview
```

---

### File: `services/movie_song_downloader/ui/__init__.py`
- **Path:** `services/movie_song_downloader/ui/__init__.py`
- **Estimated Tokens:** 202
- **mtime:** 1780856038.251

```python
# UI Module
import os


def resolve_image_src(
    cached_path: str | None, remote_url: str | None, fallback: str = ""
) -> str:
    """Resolve the best image source for display.

    In web mode (FLET_WEB_PORT set), file:// URIs are blocked by browsers.
    Always prefer remote HTTP URLs. Only use local paths in desktop mode.
    """
    is_web_mode = bool(os.environ.get("FLET_WEB_PORT"))

    if is_web_mode:
        # Web mode: remote URL always wins, local paths won't render
        if remote_url:
            return remote_url
        return fallback

    # Desktop mode: prefer cached local file for speed
    if cached_path and os.path.exists(cached_path):
        from pathlib import Path

        return Path(cached_path).as_uri()

    if remote_url:
        return remote_url

    return fallback
```

---

### File: `services/movie_song_downloader/ui/components/__init__.py`
- **Path:** `services/movie_song_downloader/ui/components/__init__.py`
- **Estimated Tokens:** 5
- **mtime:** 1780474583.175

```python
# UI Components Module
```

---

### File: `services/movie_song_downloader/ui/downloads.py`
- **Path:** `services/movie_song_downloader/ui/downloads.py`
- **Estimated Tokens:** 2,230
- **mtime:** 1780926927.948

```python
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
```

---

### File: `services/movie_song_downloader/ui/home.py`
- **Path:** `services/movie_song_downloader/ui/home.py`
- **Estimated Tokens:** 2,200
- **mtime:** 1780928588.346

```python
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

```

---

### File: `services/movie_song_downloader/ui/search.py`
- **Path:** `services/movie_song_downloader/ui/search.py`
- **Estimated Tokens:** 1,454
- **mtime:** 1780856038.293

```python
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
```

---

### File: `services/movie_song_downloader/ui/settings.py`
- **Path:** `services/movie_song_downloader/ui/settings.py`
- **Estimated Tokens:** 3,355
- **mtime:** 1780861886.635

```python
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
```

---

### File: `services/movie_song_downloader/ui/songs.py`
- **Path:** `services/movie_song_downloader/ui/songs.py`
- **Estimated Tokens:** 3,354
- **mtime:** 1780856038.291

```python
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
```

---

### File: `services/movie_song_downloader/ui/style.py`
- **Path:** `services/movie_song_downloader/ui/style.py`
- **Estimated Tokens:** 417
- **mtime:** 1780926395.987

```python
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
```

---

### File: `services/reflex.lock/package.json`
- **Path:** `services/reflex.lock/package.json`
- **Estimated Tokens:** 235
- **mtime:** 1781125153.597

```json
{
  "name": "reflex",
  "type": "module",
  "scripts": {
    "dev": "react-router dev --host",
    "export": "react-router build"
  },
  "dependencies": {
    "@radix-ui/react-form": "0.1.8",
    "@radix-ui/themes": "3.3.0",
    "@react-router/node": "7.15.0",
    "isbot": "5.1.40",
    "lucide-react": "1.14.0",
    "react": "19.2.6",
    "react-debounce-input": "3.3.0",
    "react-dom": "19.2.6",
    "react-error-boundary": "6.1.1",
    "react-helmet": "6.1.0",
    "react-player": "3.4.0",
    "react-router": "7.15.0",
    "react-router-dom": "7.15.0",
    "socket.io-client": "4.8.3",
    "sonner": "2.0.7",
    "universal-cookie": "7.2.2"
  },
  "devDependencies": {
    "@emotion/react": "11.14.0",
    "@react-router/dev": "7.15.0",
    "@react-router/fs-routes": "7.15.0",
    "autoprefixer": "10.5.0",
    "postcss": "8.5.14",
    "postcss-import": "16.1.1",
    "vite": "8.0.14"
  },
  "overrides": {
    "cookie": "1.1.1"
  }
}
```

---

### File: `services/requirements.txt`
- **Path:** `services/requirements.txt`
- **Estimated Tokens:** 3
- **mtime:** 1781124219.382

```

reflex==0.9.4
```

---

### File: `services/rxconfig.py`
- **Path:** `services/rxconfig.py`
- **Estimated Tokens:** 44
- **mtime:** 1780862784.996

```python
import reflex as rx

config = rx.Config(
    app_name="MovieSongDownloader",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.RadixThemesPlugin(),
    ],
)
```

---

### File: `services/tg_fdm_proxy/TgFdmProxy/.env.example`
- **Path:** `services/tg_fdm_proxy/TgFdmProxy/.env.example`
- **Estimated Tokens:** 59
- **mtime:** 1780923522.093

```
# Example environment variables for TgFdmProxy
# Do not commit real credentials. Use OS secret storage or CI/Docker secrets.
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
FDM_PROXY_PORT=8080
TELEMETRY_ENABLED=false
```

---

### File: `services/tg_fdm_proxy/TgFdmProxy/Dockerfile`
- **Path:** `services/tg_fdm_proxy/TgFdmProxy/Dockerfile`
- **Estimated Tokens:** 146
- **mtime:** 1775593973.598

```dockerfile
# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port (will be set dynamically)
EXPOSE 8000-9000

# Run the application
CMD ["python", "tg_fdm_proxy.py"]
```

---

### File: `services/tg_fdm_proxy/TgFdmProxy/docker-compose.yml`
- **Path:** `services/tg_fdm_proxy/TgFdmProxy/docker-compose.yml`
- **Estimated Tokens:** 100
- **mtime:** 1775593973.594

```yaml
version: '3.8'

services:
  tg-fdm-proxy:
    build: .
    ports:
      - "8080:8080"  # Adjust port as needed
    volumes:
      - ./.env:/app/.env:ro
      - ./logs:/app/logs
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
    # Optional: Mount session files if you want persistence
    # volumes:
    #   - ./fdm_proxy_bot_session.session:/app/fdm_proxy_bot_session.session
```

---

### File: `services/tg_fdm_proxy/TgFdmProxy/download_analytics.json`
- **Path:** `services/tg_fdm_proxy/TgFdmProxy/download_analytics.json`
- **Estimated Tokens:** 193
- **mtime:** 1775833102.211

```json
{
  "downloads": [
    {
      "timestamp": "2026-04-10T20:18:39.302244",
      "file_name": "Paruthiveeran 2007 Tamil HQ HDRip - 1080p - x264 - (DD5.1 - .mkv",
      "file_size_mb": 2881.6003246307373,
      "status": "created_link"
    },
    {
      "timestamp": "2026-04-10T20:24:11.188103",
      "file_name": "Paruthiveeran 2007 Tamil HQ HDRip - 1080p - x264 - (DD5.1 - .mkv",
      "file_size_mb": 2881.6003246307373,
      "status": "created_link"
    },
    {
      "timestamp": "2026-04-10T20:28:22.205913",
      "file_name": "Paruthiveeran 2007 Tamil HQ HDRip - 1080p - x264 - (DD5.1 - .mkv",
      "file_size_mb": 2881.6003246307373,
      "status": "created_link"
    }
  ],
  "stats": {
    "total_downloads": 3,
    "total_size_mb": 8644.800973892212
  }
}
```

---

### File: `services/tg_fdm_proxy/TgFdmProxy/install_startup.py`
- **Path:** `services/tg_fdm_proxy/TgFdmProxy/install_startup.py`
- **Estimated Tokens:** 101
- **mtime:** 1780856038.29

```python
import os
import shutil

# Paths
source = r"c:\Scripts\tg_fdm_proxy\launch_proxy.vbs"
startup_folder = os.path.join(
    os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs\Startup"
)
destination = os.path.join(startup_folder, "TG_FDM_Proxy.vbs")

try:
    shutil.copy2(source, destination)
    print(f"Successfully installed to: {destination}")
except Exception as e:
    print(f"Error: {e}")
```

---

### File: `services/tg_fdm_proxy/TgFdmProxy/watchdog.bat`
- **Path:** `services/tg_fdm_proxy/TgFdmProxy/watchdog.bat`
- **Estimated Tokens:** 131
- **mtime:** 1780159099.955

```
@echo off
title TG-FDM Proxy Watchdog
echo ============================================
echo  Telegram FDM Proxy - Watchdog Active
echo  Press Ctrl+C to stop permanently.
echo ============================================

:loop
echo [%date% %time%] Starting proxy...
python tg_fdm_proxy.py
echo [%date% %time%] Proxy exited (code %ERRORLEVEL%). Restarting in 3 s... >> "c:\Users\NANDHA A\Desktop\UTILITIES\Logs\watchdog.log"
echo [%date% %time%] Proxy exited. Restarting in 3 seconds...
timeout /t 3 /nobreak > nul
goto loop
```

---

### File: `system_utils.py`
- **Path:** `system_utils.py`
- **Estimated Tokens:** 651
- **mtime:** 1781117231.331

```python
import ctypes
import os


def is_system_awake_and_unlocked():
    """
    Returns True if the workstation is unlocked and active.
    If the system is locked, asleep, or the display is off in a secure way,
    OpenInputDesktop will typically fail.
    """
    if os.name != "nt":
        return True

    try:
        user32 = ctypes.windll.user32
        # 0x0100 = DESKTOP_READOBJECTS
        h_desktop = user32.OpenInputDesktop(0, False, 0x0100)
        if h_desktop:
            user32.CloseDesktop(h_desktop)
            return True
        return False
    except Exception:
        return False


def monitor_parent_process(quit_callback, check_interval_sec=5):
    """
    Spawns a background daemon thread that monitors the parent process.
    If the parent process was AeroHub and it exits/terminates, runs quit_callback.
    """
    import threading
    import time
    import sys
    import psutil
    import logging

    logger = logging.getLogger("AeroHub.ParentMonitor")
    
    parent_pid = os.getppid()
    parent_is_hub = False
    parent_create_time = None

    try:
        parent_proc = psutil.Process(parent_pid)
        parent_cmd = parent_proc.cmdline()
        parent_name = parent_proc.name().lower()
        if any("aerohub.py" in arg.lower() for arg in parent_cmd) or "pythonw_aerohub.exe" in parent_name:
            parent_is_hub = True
            parent_create_time = parent_proc.create_time()
            logger.info(f"Parent process is AeroHub (PID {parent_pid}, created at {parent_create_time})")
    except Exception as e:
        logger.warning(f"Failed to inspect parent process: {e}")

    if not parent_is_hub:
        logger.info("Parent process is not AeroHub. Running in standalone mode.")
        return

    def _monitor():
        while True:
            try:
                parent_proc = psutil.Process(parent_pid)
                if not parent_proc.is_running() or parent_proc.create_time() != parent_create_time or parent_proc.status() == psutil.STATUS_ZOMBIE:
                    logger.warning("Parent AeroHub process has terminated. Initiating shutdown.")
                    quit_callback()
                    break
            except psutil.NoSuchProcess:
                logger.warning("Parent AeroHub process has terminated (no such process). Initiating shutdown.")
                quit_callback()
                break
            except Exception as e:
                logger.error(f"Error checking parent process: {e}")
            time.sleep(check_interval_sec)

    thread = threading.Thread(target=_monitor, daemon=True)
    thread.start()

```

---

### File: `task.md`
- **Path:** `task.md`
- **Estimated Tokens:** 632
- **mtime:** 1781116491.843

```markdown
# Reflex UI Migration Progress

## Reflex Environment Setup & Configuration
- [x] Add `reflex>=0.5.0` to `MovieSongDownloader/requirements.txt`
- [x] Initialize Reflex config in `rxconfig.py`
- [x] Forward `FLET_WEB_PORT` environment variables to `--frontend-port` in `MovieSongDownloader/main.py`
- [x] Support forwarding all launcher arguments to `reflex run` in `MovieSongDownloader/main.py`

## State & Layout Migration
- [x] Set up Cyberpunk design tokens in `ui/style.py`
- [x] Implement central state management in `ui/state.py`
- [x] Migrate dashboard home view to React/Next.js components in `ui/home.py`
- [x] Migrate soundtrack search and JioSaavn link resolution in `ui/search.py`
- [x] Migrate album tracks grid, checkboxes, and local browser-compatible directory explorer in `ui/songs.py`
- [x] Migrate downloads queue with progress indicators in `ui/downloads.py`
- [x] Migrate credentials and format template settings in `ui/settings.py`

## Tasks: Restructure UTILITIES
- [x] Create category directories (services/, toggles/, tools/, tests/)
- [x] Move utility directories to new structured paths and rename to lowercase
- [x] Move root tests to tests/
- [x] Delete root screenshots and temporary files
- [x] Move root logs to Logs/
- [x] Move aerohub_config.json from aerohub/ to services/aerohub_core/ and delete aerohub/
- [x] Update imports and path depth resolution in moved utility python scripts
- [x] Update paths in launchers and runners (run_utility.ps1, run.ps1, dev_run.ps1, etc.)
- [x] Run verification tests and compile checks

## Bug Fixes & Refactoring
- [x] Remove old Flet UI views and clean up imports
- [x] Wrap search input controls in `rx.form` to support Enter key submissions across browsers
- [x] Fix `TypeError: async_generator can't be used in 'await' expression` by implementing proper `async for` generator delegation in state handler chaining
- [x] Fix `TypeError: Returned events of types <class 'coroutine'>` by returning class references for event handoff in state router
- [x] Replace invalid `rx.format` calls with Python f-strings in page rendering elements
- [x] Optimize downloads polling from `rx.moment.interval` to `@rx.event(background=True)` native background loop

## Launch Scripts & Verification
- [x] Create easy-to-use launch scripts `run_app.bat` and `run_app.ps1` supporting prod/dev run environments
- [x] Run full pytest suite (`23 passed`) to verify backend database and provider services
- [x] Verify server starts successfully and frontend loads correctly
```

---

### File: `test_output/spotiflac_result_1nHTOlxSEyyrLH6wzzMJTd.mp3`
- **Path:** `test_output/spotiflac_result_1nHTOlxSEyyrLH6wzzMJTd.mp3`
- **Estimated Tokens:** 3
- **mtime:** 1781123837.936

```
mock final file
```

---

### File: `test_output/spotiflac_temp_1nHTOlxSEyyrLH6wzzMJTd/track1.flac`
- **Path:** `test_output/spotiflac_temp_1nHTOlxSEyyrLH6wzzMJTd/track1.flac`
- **Estimated Tokens:** 3
- **mtime:** 1781123837.93

```
mock audio data
```

---

### File: `test_output/spotiflac_temp_1nHTOlxSEyyrLH6wzzMJTd/transcoded.mp3`
- **Path:** `test_output/spotiflac_temp_1nHTOlxSEyyrLH6wzzMJTd/transcoded.mp3`
- **Estimated Tokens:** 5
- **mtime:** 1781123837.932

```
mock transcoded audio
```

---

### File: `tests/test_health_toast.py`
- **Path:** `tests/test_health_toast.py`
- **Estimated Tokens:** 444
- **mtime:** 1781116196.453

```python
import tkinter as tk
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from toast_utils import BaseToast  # noqa: E402


def test():
    root = tk.Tk()
    root.withdraw()
    settings = {
        "ht_toast_pos": "Right",
        "ht_toast_custom_x": 100,
        "ht_toast_custom_y": 100,
        "ht_toast_width": 280,
        "ht_toast_height": 70,
        "ht_toast_bg_color": "#101625",
        "ht_toast_fg_color": "#e2e8f0",
        "ht_toast_accent_color": "#00f0ff",
        "ht_toast_font_size": 10,
        "ht_toast_font_weight": "normal",
        "ht_toast_font_family": "Segoe UI",
        "ht_toast_emoji": "\u26a1",
        "ht_toast_radius": 18,
        "ht_toast_padding_x": 12,
        "ht_toast_padding_y": 10,
        "ht_toast_anim_style": "Slide",
        "ht_toast_opacity": 0.95,
        "ht_toast_border_width": 1,
        "ht_toast_border_color": "#1e293b",
        "ht_toast_gradient": False,
        "ht_toast_gradient_end": "#101625",
        "ht_toast_shadow": True,
        "ht_toast_accent_stripe": False,
        "ht_toast_text_align": "left",
        "ht_toast_auto_dismiss": True,
        "ht_toast_click_action": "dismiss",
        "ht_toast_progress_bar": False,
        "ht_toast_enable_sound": False,
    }
    toast = BaseToast(
        root,
        "Health Tip",
        "Sit up straight! Align your ears with your shoulders. 📐",
        settings,
        is_health_tip=True,
    )
    try:
        toast._create_toast()
        print("Success")
    except Exception as e:
        print(f"Error: {e}")
    root.after(3000, root.destroy)
    root.mainloop()


if __name__ == "__main__":
    test()
```

---

### File: `tests/test_toast.py`
- **Path:** `tests/test_toast.py`
- **Estimated Tokens:** 130
- **mtime:** 1781116177.829

```python
import tkinter as tk
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from toast_utils import BaseToast  # noqa: E402


def test():
    root = tk.Tk()
    root.withdraw()
    settings = {"toast_pos": "Center"}
    toast = BaseToast(root, "Test", "This is a test", settings)
    toast.show()
    root.after(3000, root.destroy)
    root.mainloop()


if __name__ == "__main__":
    test()
```

---

### File: `tests/test_toast_queue.py`
- **Path:** `tests/test_toast_queue.py`
- **Estimated Tokens:** 580
- **mtime:** 1781116184.309

```python
import sys
import os
import pytest

# Ensure Tcl/Tk can find its init.tcl in some Python installs where the
# embedded tcl folder isn't discovered automatically. Use LOCALAPPDATA
# Python install path as a sensible default on Windows.
if "TCL_LIBRARY" not in os.environ:
    local_tcl = os.path.join(
        os.environ.get("LOCALAPPDATA", ""),
        "Programs",
        "Python",
        "Python312",
        "tcl",
        "tcl8.6",
    )
    if os.path.isdir(local_tcl):
        os.environ["TCL_LIBRARY"] = local_tcl

import tkinter as tk

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from toast_utils import BaseToast  # noqa: E402


def test():
    try:
        root = tk.Tk()
        root.withdraw()
    except tk.TclError:
        pytest.skip("Tcl/Tk not available on this system; skipping GUI test")
    settings = {
        "ht_toast_pos": "Right",
        "ht_toast_custom_x": 100,
        "ht_toast_custom_y": 100,
        "ht_toast_width": 280,
        "ht_toast_height": 70,
        "ht_toast_bg_color": "#101625",
        "ht_toast_fg_color": "#e2e8f0",
        "ht_toast_accent_color": "#00f0ff",
        "ht_toast_font_size": 10,
        "ht_toast_font_weight": "normal",
        "ht_toast_font_family": "Segoe UI",
        "ht_toast_emoji": "\u26a1",
        "ht_toast_radius": 18,
        "ht_toast_padding_x": 12,
        "ht_toast_padding_y": 10,
        "ht_toast_anim_style": "Slide",
        "ht_toast_opacity": 0.95,
        "ht_toast_border_width": 1,
        "ht_toast_border_color": "#1e293b",
        "ht_toast_gradient": False,
        "ht_toast_gradient_end": "#101625",
        "ht_toast_shadow": True,
        "ht_toast_accent_stripe": False,
        "ht_toast_text_align": "left",
        "ht_toast_auto_dismiss": True,
        "ht_duration_sec": 2,
        "toast_enable_sound": False,
    }

    # Send multiple toasts
    toast1 = BaseToast(
        root, "Health Tip", "First toast! ⚡", settings, is_health_tip=True
    )
    toast1.show()

    toast2 = BaseToast(
        root, "Health Tip", "Second toast! 💧", settings, is_health_tip=True
    )
    toast2.show()

    root.after(10000, root.destroy)
    root.mainloop()


if __name__ == "__main__":
    test()
```

---

### File: `tests/test_ui.py`
- **Path:** `tests/test_ui.py`
- **Estimated Tokens:** 139
- **mtime:** 1781116190.526

```python
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "services", "health_app"))
from health_app import HealthApp  # noqa: E402


def main():
    import time

    app = HealthApp()
    app._on_settings(None, None)

    # We don't have a main Tk loop because HealthApp relies on the tray icon
    # for its main loop. But for this test, we can just start a simple blocking loop.
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
```

---

### File: `toast_status.json`
- **Path:** `toast_status.json`
- **Estimated Tokens:** 68
- **mtime:** 1781123845.133

```json
{
  "active_toast_pid": null,
  "active_toast_end_time": 0.0,
  "break_warning_active": false,
  "break_warning_pid": null,
  "break_warning_end_time": 0.0,
  "break_active": false,
  "break_pid": null,
  "break_end_time": 0.0,
  "last_break_end_time": 1781115386.4198272
}
```

---

### File: `toggles/battery_monitor/settings.json`
- **Path:** `toggles/battery_monitor/settings.json`
- **Estimated Tokens:** 298
- **mtime:** 1780753463.655

```json
{
    "enable_sounds": true,
    "low_threshold": 30,
    "full_threshold": 95,
    "toast_pos": "Top-Center",
    "toast_custom_x": 120,
    "toast_custom_y": 120,
    "toast_width": 200,
    "toast_height": 55,
    "toast_bg_color": "#000000",
    "toast_fg_color": "#ffffff",
    "toast_accent_color": "#28c840",
    "toast_font_size": 11,
    "toast_font_weight": "bold",
    "toast_font_family": "Segoe UI",
    "toast_emoji": "\ud83d\udd0b",
    "toast_radius": 18,
    "toast_padding_x": 18,
    "toast_padding_y": 18,
    "toast_anim_style": "Slide",
    "toast_opacity": 0.92,
    "toast_border_width": 0,
    "toast_border_color": "#010301",
    "toast_gradient": true,
    "toast_gradient_end": "#101625",
    "toast_shadow": true,
    "toast_accent_stripe": false,
    "toast_text_align": "center",
    "toast_auto_dismiss": true,
    "toast_click_action": "dismiss",
    "toast_progress_bar": true,
    "toast_enable_sound": true,
    "toast_sound_effect": "mac_connect",
    "toast_duration": 3,
    "sound_charger_connect": "mac_connect",
    "sound_charger_disconnect": "mac_disconnect",
    "sound_battery_full": "SystemDefault",
    "sound_battery_low": "SystemExclamation"
}
```

---

### File: `toggles/battery_monitor/test_battery_monitor.py`
- **Path:** `toggles/battery_monitor/test_battery_monitor.py`
- **Estimated Tokens:** 826
- **mtime:** 1780856515.52

```python
import os
import sys

# Add current dir to path to import battery_monitor
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import unittest  # noqa: E402
from unittest.mock import patch, MagicMock  # noqa: E402

import battery_monitor  # noqa: E402
from PIL import Image  # noqa: E402


class TestBatteryMonitor(unittest.TestCase):
    def test_get_system_theme_default(self):
        """Test theme defaults to dark if registry fails"""
        with patch("winreg.OpenKey", side_effect=Exception("Mock Registry Error")):
            theme = battery_monitor.get_system_theme()
            self.assertEqual(theme, "dark")

    def test_get_system_theme_light(self):
        """Test registry returns light theme"""
        with (
            patch("winreg.OpenKey", return_value=MagicMock()),
            patch("winreg.QueryValueEx", return_value=(1, 4)),
            patch("winreg.CloseKey"),
        ):
            theme = battery_monitor.get_system_theme()
            self.assertEqual(theme, "light")

    def test_create_battery_icon_full(self):
        """Test drawing battery icon at 100%"""
        img = battery_monitor.create_battery_icon(
            100, plugged=True, low=False, theme="dark"
        )
        self.assertIsInstance(img, Image.Image)
        self.assertEqual(img.size, (64, 64))

    def test_create_battery_icon_low(self):
        """Test drawing low battery icon"""
        img = battery_monitor.create_battery_icon(
            15, plugged=False, low=True, theme="light"
        )
        self.assertIsInstance(img, Image.Image)
        self.assertEqual(img.size, (64, 64))

    def test_battery_info_mocked(self):
        """Test battery info extraction"""
        app = battery_monitor.BatteryMonitorApp()

        mock_bat = MagicMock()
        mock_bat.percent = 85.5
        mock_bat.power_plugged = True

        with patch("psutil.sensors_battery", return_value=mock_bat):
            percent, plugged, has_battery = app._get_battery_info()
            self.assertEqual(percent, 85)
            self.assertTrue(plugged)
            self.assertTrue(has_battery)

    def test_battery_info_no_battery(self):
        """Test fallback when no battery is found"""
        app = battery_monitor.BatteryMonitorApp()

        with patch("psutil.sensors_battery", return_value=None):
            percent, plugged, has_battery = app._get_battery_info()
            self.assertEqual(percent, 100)
            self.assertTrue(plugged)
            self.assertFalse(has_battery)

    def test_play_sound_system_alias(self):
        """Test play_sound plays system aliases correctly via winsound"""
        settings = {"enable_sounds": True}
        with patch("winsound.PlaySound") as mock_play:
            battery_monitor.play_sound("SystemAsterisk", settings)
            import winsound

            mock_play.assert_called_once_with(
                "SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC
            )

    def test_play_sound_none(self):
        """Test play_sound does not play if set to None"""
        settings = {"enable_sounds": True}
        with patch("winsound.PlaySound") as mock_play:
            battery_monitor.play_sound("None", settings)
            mock_play.assert_not_called()


if __name__ == "__main__":
    unittest.main()
```

---

### File: `toggles/temp_monitor/settings.json`
- **Path:** `toggles/temp_monitor/settings.json`
- **Estimated Tokens:** 220
- **mtime:** 1780569786.725

```json
{
    "warning_temp": 65,
    "critical_temp": 70,
    "toast_pos": "Bottom-Center",
    "toast_custom_x": 100,
    "toast_custom_y": 100,
    "toast_width": 200,
    "toast_height": 50,
    "toast_bg_color": "#ffffff",
    "toast_fg_color": "#950000",
    "toast_accent_color": "#000000",
    "toast_font_size": 10,
    "toast_font_weight": "bold",
    "toast_font_family": "Arial",
    "toast_emoji": "\ud83d\udd25",
    "toast_radius": 18,
    "toast_padding_x": 18,
    "toast_padding_y": 18,
    "toast_anim_style": "Slide",
    "toast_opacity": 0.92,
    "toast_border_width": 0,
    "toast_border_color": "#060606",
    "toast_gradient": true,
    "toast_gradient_end": "#40090a",
    "toast_shadow": true,
    "toast_accent_stripe": false,
    "toast_text_align": "right",
    "toast_auto_dismiss": true,
    "toast_click_action": "dismiss",
    "toast_progress_bar": false
}
```

---

### File: `toggles/temp_monitor/temp_settings_ui.py`
- **Path:** `toggles/temp_monitor/temp_settings_ui.py`
- **Estimated Tokens:** 3,934
- **mtime:** 1781116112.297

```python
import tkinter as tk
from tkinter import ttk, colorchooser
import sys
import os

# AeroHub Theme
TH = {
    "bg": "#0a0a1a",
    "bg2": "#12122a",
    "bg3": "#1e1e3f",
    "accent": "#ff3366",  # Red/pink accent for temp
    "accent_hover": "#ff6688",
    "fg": "#f0f0f0",
    "fg_dim": "#a0a0b0",
    "border": "#2d2d5e",
}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(SCRIPT_DIR))
if root_dir not in sys.path:
    sys.path.append(root_dir)

try:
    from toast_utils import BaseToast, EmojiPickerPanel
except ImportError:
    pass


class SettingsWindow:
    def __init__(self, root, current_settings, on_save_callback):
        self.parent = root
        self.settings = current_settings
        self.on_save = on_save_callback

        self.entries = {}
        self.window = tk.Toplevel(root)
        self.window.title("Temperature Monitor Settings")
        self.window.geometry("800x600")
        self.window.configure(bg=TH["bg"])

        # Apply rounded corners
        try:
            import ctypes

            DWMWA_WINDOW_CORNER_PREFERENCE = 33
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                int(self.window.wm_frame(), 16),
                DWMWA_WINDOW_CORNER_PREFERENCE,
                ctypes.byref(ctypes.c_int(2)),
                ctypes.sizeof(ctypes.c_int),
            )
        except Exception:
            pass

        self._build_ui()

    def _build_ui(self):
        main_container = tk.Frame(self.window, bg=TH["bg"])
        main_container.pack(fill=tk.BOTH, expand=True)

        self.sidebar = tk.Frame(main_container, bg=TH["bg2"], width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="TEMP.SYS",
            font=("Consolas", 18, "bold"),
            bg=TH["bg2"],
            fg=TH["accent"],
        ).pack(pady=(30, 40))

        self.content_area = tk.Frame(main_container, bg=TH["bg"])
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        f_general = tk.Frame(self.content_area, bg=TH["bg"])
        f_toast = tk.Frame(self.content_area, bg=TH["bg"])

        self.frames = {"General": f_general, "Toast FX": f_toast}

        self._build_general_tab(f_general)
        self._build_toast_tab(f_toast)

        self.current_frame = None
        self.nav_buttons = {}

        def switch_tab(name):
            if self.current_frame:
                self.current_frame.pack_forget()
                self.nav_buttons[self.current_frame_name].config(
                    bg=TH["bg2"], fg=TH["fg_dim"]
                )
            self.current_frame = self.frames[name]
            self.current_frame_name = name
            self.current_frame.pack(fill=tk.BOTH, expand=True, padx=32, pady=24)
            self.nav_buttons[name].config(bg=TH["bg3"], fg=TH["accent"])

        for name in ["General", "Toast FX"]:
            btn = tk.Button(
                self.sidebar,
                text=f"■ {name.upper()}",
                font=("Consolas", 11, "bold"),
                bg=TH["bg2"],
                fg=TH["fg_dim"],
                activebackground=TH["bg3"],
                activeforeground=TH["accent"],
                relief=tk.FLAT,
                cursor="hand2",
                anchor="w",
                padx=24,
                pady=12,
                command=lambda n=name: switch_tab(n),
            )
            btn.pack(fill=tk.X, pady=4)
            self.nav_buttons[name] = btn

        tk.Button(
            self.sidebar,
            text="[ SAVE_CFG ]",
            font=("Consolas", 12, "bold"),
            bg=TH["accent"],
            fg="white",
            activebackground=TH["accent_hover"],
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            pady=12,
            command=self._save,
        ).pack(side=tk.BOTTOM, fill=tk.X, padx=16, pady=24)

        switch_tab("General")

    def _add_field(self, parent_frame, label, key, row, is_str=False):
        tk.Label(
            parent_frame,
            text=label.upper(),
            font=("Consolas", 9),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).grid(row=row, column=0, sticky=tk.W, pady=8)
        var = tk.StringVar(value=str(self.settings.get(key, "")))
        tk.Entry(
            parent_frame,
            textvariable=var,
            font=("Consolas", 10),
            bg=TH["bg"],
            fg=TH["fg"],
            insertbackground=TH["accent"],
            relief=tk.FLAT,
            highlightthickness=1,
            highlightcolor=TH["accent"],
            highlightbackground=TH["border"],
            width=14,
        ).grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))
        self.entries[key] = (var, is_str)
        if key.startswith("toast_"):
            var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_combo(self, parent_frame, label, key, row, values):
        tk.Label(
            parent_frame,
            text=label.upper(),
            font=("Consolas", 9),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).grid(row=row, column=0, sticky=tk.W, pady=8)
        var = tk.StringVar(value=str(self.settings.get(key, values[0])))
        ttk.Combobox(
            parent_frame,
            textvariable=var,
            values=values,
            font=("Consolas", 10),
            state="readonly",
            width=12,
        ).grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))
        self.entries[key] = (var, True)
        if key.startswith("toast_"):
            var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_color_field(self, parent_frame, label, key, row):
        tk.Label(
            parent_frame,
            text=label.upper(),
            font=("Consolas", 9),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).grid(row=row, column=0, sticky=tk.W, pady=8)
        var = tk.StringVar(value=str(self.settings.get(key, "")))

        def choose_color(v=var):
            c = colorchooser.askcolor(initialcolor=v.get())[1]
            if c:
                v.set(c)
                btn.config(bg=c)

        btn = tk.Button(
            parent_frame,
            bg=var.get(),
            width=10,
            relief=tk.FLAT,
            cursor="hand2",
            command=choose_color,
        )
        btn.grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))
        self.entries[key] = (var, True)
        if key.startswith("toast_"):
            var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_grid_chk(self, parent_frame, label, key, row):
        var = tk.BooleanVar(value=self.settings.get(key, True))
        tk.Checkbutton(
            parent_frame,
            text=label.upper(),
            variable=var,
            font=("Consolas", 9),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            selectcolor=TH["bg2"],
            activebackground=TH["bg"],
            activeforeground=TH["accent"],
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=8)
        self.entries[key] = (var, "bool")
        if key.startswith("toast_"):
            var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_emoji_picker(self, parent_frame, label, key, row):
        tk.Label(
            parent_frame,
            text=label.upper(),
            font=("Consolas", 9),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).grid(row=row, column=0, sticky=tk.W, pady=8)
        var = tk.StringVar(value=str(self.settings.get(key, "🔥")))
        f = tk.Frame(parent_frame, bg=TH["bg"])
        f.grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))
        lbl = tk.Label(
            f, textvariable=var, font=("Segoe UI Emoji", 12), bg=TH["bg"], fg=TH["fg"]
        )
        lbl.pack(side=tk.LEFT, padx=(0, 5))

        def _on_select(emoji):
            var.set(emoji)
            if key.startswith("toast_"):
                self._schedule_preview()

        def _open_picker():
            EmojiPickerPanel(self.window, _on_select)

        btn = tk.Button(
            f,
            text="Pick",
            font=("Consolas", 8),
            bg=TH["bg2"],
            fg=TH["accent"],
            relief=tk.FLAT,
            cursor="hand2",
            command=_open_picker,
        )
        btn.pack(side=tk.LEFT)
        self.entries[key] = (var, True)

    def _build_general_tab(self, tab):
        tk.Label(
            tab,
            text="THERMAL THRESHOLDS",
            font=("Consolas", 14, "bold"),
            bg=TH["bg"],
            fg=TH["fg"],
        ).pack(anchor=tk.W, pady=(0, 20))
        f1 = tk.Frame(tab, bg=TH["bg"])
        f1.pack(fill=tk.X)
        self._add_field(f1, "Warning Temp (°C):", "warning_temp", 0)
        self._add_field(f1, "Critical Temp (°C):", "critical_temp", 1)

    def _build_toast_tab(self, tab):
        tk.Label(
            tab,
            text="UI / UX CONFIG",
            font=("Consolas", 14, "bold"),
            bg=TH["bg"],
            fg=TH["fg"],
        ).pack(anchor=tk.W, pady=(0, 10))
        canvas = tk.Canvas(tab, bg=TH["bg"], highlightthickness=0)
        scrollable_frame = tk.Frame(canvas, bg=TH["bg"])
        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.pack(side="left", fill="both", expand=True)

        def _on_mousewheel(event):
            try:
                w = event.widget.winfo_containing(event.x_root, event.y_root)
                while w:
                    if isinstance(w, tk.Canvas):
                        w.yview_scroll(int(-1 * (event.delta / 120)), "units")
                        break
                    w = w.master
            except Exception:
                pass

        tab.winfo_toplevel().bind_all("<MouseWheel>", _on_mousewheel)

        f_top = tk.Frame(scrollable_frame, bg=TH["bg"])
        f_top.pack(fill=tk.BOTH, expand=True)
        f2_left = tk.Frame(f_top, bg=TH["bg"])
        f2_left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        f2_right = tk.Frame(f_top, bg=TH["bg"])
        f2_right.pack(side=tk.LEFT, fill=tk.Y)

        positions = [
            "Top-Left",
            "Top-Center",
            "Top-Right",
            "Bottom-Left",
            "Bottom-Center",
            "Bottom-Right",
            "Middle-Left",
            "Middle-Right",
            "Custom",
        ]
        animations = ["Slide", "Fade", "Bounce", "Scale", "Typewriter", "Glow", "Drop"]
        fonts = ["Segoe UI", "Consolas", "Cascadia Code", "Arial", "Verdana"]
        actions = ["dismiss", "snooze", "settings"]

        self._add_combo(f2_left, "Position:", "toast_pos", 0, positions)
        self._add_combo(f2_left, "Animation:", "toast_anim_style", 1, animations)
        self._add_field(f2_left, "Width (px):", "toast_width", 2)
        self._add_field(f2_left, "Height (px):", "toast_height", 3)
        self._add_field(f2_left, "Custom X (if custom):", "toast_custom_x", 4)
        self._add_field(f2_left, "Custom Y (if custom):", "toast_custom_y", 5)
        self._add_color_field(f2_left, "Background Color:", "toast_bg_color", 6)
        self._add_color_field(f2_left, "Text Color:", "toast_fg_color", 7)
        self._add_color_field(f2_left, "Accent Color:", "toast_accent_color", 8)
        self._add_combo(f2_left, "Font Family:", "toast_font_family", 9, fonts)
        self._add_field(f2_left, "Font Size:", "toast_font_size", 10)
        self._add_combo(
            f2_left, "Font Weight:", "toast_font_weight", 11, ["normal", "bold"]
        )
        self._add_combo(
            f2_left, "Text Align:", "toast_text_align", 12, ["left", "center", "right"]
        )

        self._add_emoji_picker(f2_right, "Emoji Icon:", "toast_emoji", 0)
        self._add_field(f2_right, "Border Radius (px):", "toast_radius", 1)
        self._add_field(f2_right, "Padding X (px):", "toast_padding_x", 2)
        self._add_field(f2_right, "Padding Y (px):", "toast_padding_y", 3)
        self._add_field(f2_right, "Opacity (0.1 - 1.0):", "toast_opacity", 4)
        self._add_field(f2_right, "Border Width (px):", "toast_border_width", 5)
        self._add_color_field(f2_right, "Border Color:", "toast_border_color", 6)
        self._add_color_field(f2_right, "Gradient End Color:", "toast_gradient_end", 7)
        self._add_combo(f2_right, "Click Action:", "toast_click_action", 8, actions)
        self._add_field(f2_right, "Duration (sec):", "toast_duration", 9)

        f3 = tk.Frame(scrollable_frame, bg=TH["bg"])
        f3.pack(fill=tk.X, pady=(15, 0))

        self._add_grid_chk(f3, "Enable Shadow/Glow", "toast_shadow", 0)
        self._add_grid_chk(f3, "Enable Gradient BG", "toast_gradient", 1)
        self._add_grid_chk(f3, "Enable Accent Stripe", "toast_accent_stripe", 2)
        self._add_grid_chk(f3, "Show Progress Bar", "toast_progress_bar", 3)
        self._add_grid_chk(f3, "Auto-Dismiss", "toast_auto_dismiss", 4)

        btn_frame = tk.Frame(scrollable_frame, bg=TH["bg"])
        btn_frame.pack(fill=tk.X, pady=20)
        tk.Button(
            btn_frame,
            text="[ PREVIEW_UI ]",
            font=("Consolas", 10, "bold"),
            bg=TH["bg2"],
            fg=TH["accent"],
            activebackground=TH["bg3"],
            activeforeground=TH["accent"],
            relief=tk.FLAT,
            cursor="hand2",
            command=self._preview_toast,
            padx=20,
            pady=8,
        ).pack(side=tk.RIGHT)

    def _schedule_preview(self):
        if hasattr(self, "_preview_timer") and self._preview_timer:
            try:
                self.window.after_cancel(self._preview_timer)
            except Exception:
                pass
        self._preview_timer = self.window.after(400, self._preview_toast)

    def _preview_toast(self):
        if hasattr(self, "preview_instance") and getattr(
            self.preview_instance, "force_close", None
        ):
            self.preview_instance.force_close()

        temp_settings = dict(self.settings)
        for key, (var, var_type) in self.entries.items():
            val = var.get()
            try:
                if var_type == "bool":
                    temp_settings[key] = val == "1" or val == "True" or val is True
                elif key in ("toast_opacity",):
                    temp_settings[key] = float(val)
                elif var_type is False:
                    temp_settings[key] = int(val)
                else:
                    temp_settings[key] = val
            except ValueError:
                pass

        self.preview_instance = BaseToast(
            self.window, "THERMAL PREVIEW", "Warning: 80°C reached", temp_settings
        )
        self.preview_instance.show()

    def _save(self):
        for key, (var, var_type) in self.entries.items():
            val = var.get()
            try:
                if var_type == "bool":
                    self.settings[key] = val == "1" or val == "True" or val is True
                elif key in ("toast_opacity",):
                    self.settings[key] = float(val)
                elif var_type is False:
                    self.settings[key] = int(val)
                else:
                    self.settings[key] = val
            except ValueError:
                pass
        self.on_save(self.settings)
        self.window.destroy()
```

---

### File: `toggles/touch_toggle/TouchToggle.ps1`
- **Path:** `toggles/touch_toggle/TouchToggle.ps1`
- **Estimated Tokens:** 323
- **mtime:** 1780159086.273

```powershell
#Requires -RunAsAdministrator
$ErrorActionPreference = 'Stop'

$logPath = "c:\Users\NANDHA A\Desktop\UTILITIES\Logs\touch_toggle_run.log"
"--- Run at $(Get-Date) ---" | Out-File $logPath -Append

try {
    $device = Get-PnpDevice -Class 'HIDClass' | Where-Object { $_.FriendlyName -match 'touch screen' } | Select-Object -First 1
    if (-not $device) {
        "  [ERROR] No HID-compliant touch screen device found!" | Out-File $logPath -Append
        exit 1
    }

    $instanceId = $device.InstanceId
    $currentStatus = $device.Status

    "Device: $($device.FriendlyName)" | Out-File $logPath -Append
    "ID: $instanceId" | Out-File $logPath -Append
    "Status: $currentStatus" | Out-File $logPath -Append

    if ($currentStatus -eq 'OK') {
        "Attempting to disable..." | Out-File $logPath -Append
        Disable-PnpDevice -InstanceId "$instanceId" -Confirm:$false
        "Disabled successfully." | Out-File $logPath -Append
    } else {
        "Attempting to enable..." | Out-File $logPath -Append
        Enable-PnpDevice -InstanceId "$instanceId" -Confirm:$false
        "Enabled successfully." | Out-File $logPath -Append
    }
} catch {
    "ERROR: $_" | Out-File $logPath -Append
    "ScriptStackTrace: $($_.ScriptStackTrace)" | Out-File $logPath -Append
    exit 1
}

```

---

### File: `toggles/touch_toggle/install_touch_toggle_service.ps1`
- **Path:** `toggles/touch_toggle/install_touch_toggle_service.ps1`
- **Estimated Tokens:** 202
- **mtime:** 1780923522.142

```powershell
param(
    [string]$TaskName = "TouchToggle Service"
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$scriptPath = Join-Path $root "TouchToggle.ps1"
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`""
$trigger = New-ScheduledTaskTrigger -AtLogOn
$principal = New-ScheduledTaskPrincipal -UserId "NT AUTHORITY\SYSTEM" -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

try {
    Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force
    Write-Host "Installed scheduled task: $TaskName"
} catch {
    Write-Error "Failed to install TouchToggle service: $_"
    exit 1
}
```

---

### File: `toggles/touch_toggle/run_hidden.vbs`
- **Path:** `toggles/touch_toggle/run_hidden.vbs`
- **Estimated Tokens:** 39
- **mtime:** 1779500918.984

```
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "powershell.exe -NoProfile -ExecutionPolicy Bypass -File """ & WScript.Arguments(0) & """", 0, True
```

---

### File: `toggles/touch_toggle/touch_settings.json`
- **Path:** `toggles/touch_toggle/touch_settings.json`
- **Estimated Tokens:** 219
- **mtime:** 1780554567.289

```json
{
    "toast_pos": "Bottom-Center",
    "toast_custom_x": 100,
    "toast_custom_y": 100,
    "toast_width": 200,
    "toast_height": 55,
    "toast_bg_color": "#000000",
    "toast_fg_color": "#FFFFFF",
    "toast_accent_color": "#ff8800",
    "toast_font_size": 10,
    "toast_font_weight": "normal",
    "toast_font_family": "Segoe UI",
    "toast_emoji": "\ud83d\udd90\ufe0f",
    "toast_radius": 18,
    "toast_padding_x": 12,
    "toast_padding_y": 10,
    "toast_anim_style": "Slide",
    "toast_opacity": 1.0,
    "toast_border_width": 0,
    "toast_border_color": "#000000",
    "toast_gradient": false,
    "toast_gradient_end": "#0a0a0a",
    "toast_shadow": true,
    "toast_accent_stripe": false,
    "toast_text_align": "left",
    "toast_auto_dismiss": true,
    "toast_click_action": "dismiss",
    "toast_progress_bar": false,
    "toast_enable_sound": false
}
```

---

### File: `toggles/touch_toggle/uninstall_touch_toggle_service.ps1`
- **Path:** `toggles/touch_toggle/uninstall_touch_toggle_service.ps1`
- **Estimated Tokens:** 108
- **mtime:** 1780923522.142

```powershell
param(
    [string]$TaskName = "TouchToggle Service"
)

try {
    if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
        Write-Host "Uninstalled scheduled task: $TaskName"
    } else {
        Write-Warning "Scheduled task '$TaskName' not found."
    }
} catch {
    Write-Error "Failed to uninstall TouchToggle service: $_"
    exit 1
}
```

---

### File: `tools/taskbar_scroll/settings.json`
- **Path:** `tools/taskbar_scroll/settings.json`
- **Estimated Tokens:** 14
- **mtime:** 1780159774.655

```json
{
    "invert_scroll": false,
    "step_multiplier": 1
}
```

---

### File: `tools/taskbar_scroll/taskbar_scroll.py`
- **Path:** `tools/taskbar_scroll/taskbar_scroll.py`
- **Estimated Tokens:** 2,031
- **mtime:** 1781123586.584

```python
import os
import sys
import json
import ctypes
import ctypes.wintypes
import threading
import win32gui
from pynput import mouse
import pystray
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import ttk

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.join(SCRIPT_DIR, "settings.json")

# Ensure workspace root is in sys.path to import system_utils
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)
import system_utils

# AeroHub Theme
TH = {
    "bg": "#0a0a1a",
    "bg2": "#12122a",
    "accent": "#7c3aed",
    "fg": "#f0f0f0",
    "border": "#2d2d5e",
}

try:
    ctypes.windll.user32.SetProcessDPIAware()
except Exception:
    pass


class TaskbarScrollApp:
    def __init__(self):
        self.settings = self.load_settings()
        self.mouse_listener = None
        self.icon = None
        self.root = None
        self.settings_window = None

    def load_settings(self):
        if os.path.exists(SETTINGS_PATH):
            try:
                with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"invert_scroll": False, "step_multiplier": 1}

    def save_settings(self):
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)

    def create_tray_icon_image(self):
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Draw a simple speaker/scroll icon
        draw.polygon(
            [(16, 24), (16, 40), (26, 40), (40, 52), (40, 12), (26, 24)],
            fill=TH["accent"],
        )
        draw.arc((30, 20, 50, 44), -45, 45, fill=TH["accent"], width=4)
        draw.arc((20, 10, 60, 54), -45, 45, fill=TH["accent"], width=4)
        return img

    def on_quit(self, icon, item):
        icon.stop()
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.root:
            self.root.quit()
        os._exit(0)

    def _apply_dwm_rounding(self, hwnd):
        try:
            DWMWA_WINDOW_CORNER_PREFERENCE = 33
            DWMWCP_ROUND = 2
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_WINDOW_CORNER_PREFERENCE,
                ctypes.byref(ctypes.c_int(DWMWCP_ROUND)),
                ctypes.sizeof(ctypes.c_int),
            )
        except Exception:
            pass

    def show_settings_window(self, event=None):
        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.lift()
            return

        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Taskbar Scroll Settings")
        self.settings_window.configure(bg=TH["bg"])
        self.settings_window.resizable(False, False)

        self.settings_window.geometry("320x250")
        try:
            self._apply_dwm_rounding(int(self.settings_window.wm_frame(), 16))
        except Exception:
            pass

        tk.Label(
            self.settings_window,
            text="🔊 Taskbar Scroll",
            font=("Segoe UI", 16, "bold"),
            bg=TH["bg"],
            fg=TH["accent"],
        ).pack(pady=(20, 10))

        frame = tk.Frame(self.settings_window, bg=TH["bg"])
        frame.pack(fill=tk.BOTH, expand=True, padx=20)

        # Invert Scroll
        inv_var = tk.BooleanVar(value=self.settings.get("invert_scroll", False))
        tk.Checkbutton(
            frame,
            text="Invert Scroll Direction",
            variable=inv_var,
            font=("Segoe UI", 10),
            bg=TH["bg"],
            fg=TH["fg"],
            selectcolor=TH["bg2"],
            activebackground=TH["bg"],
        ).pack(anchor=tk.W, pady=10)

        # Step Multiplier
        tk.Label(
            frame,
            text="Volume Step Multiplier:",
            font=("Segoe UI", 10),
            bg=TH["bg"],
            fg=TH["fg"],
        ).pack(anchor=tk.W)

        step_var = tk.StringVar(value=str(self.settings.get("step_multiplier", 1)))
        cbox = ttk.Combobox(
            frame,
            textvariable=step_var,
            values=["1", "2", "3", "4", "5"],
            state="readonly",
            font=("Segoe UI", 10),
            width=10,
        )
        cbox.pack(anchor=tk.W, pady=5)

        def save():
            self.settings["invert_scroll"] = inv_var.get()
            try:
                self.settings["step_multiplier"] = int(step_var.get())
            except Exception:
                pass
            self.save_settings()
            self.settings_window.destroy()

        tk.Button(
            self.settings_window,
            text="💾 Save",
            font=("Segoe UI", 10, "bold"),
            bg=TH["accent"],
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=save,
            padx=20,
            pady=5,
        ).pack(pady=20)

    def on_scroll(self, x, y, dx, dy):
        try:
            # Ensure perfect coordinate matching regardless of DPI scaling
            try:
                import win32api

                cx, cy = win32api.GetCursorPos()
            except Exception:
                cx, cy = int(x), int(y)

            hwnd = win32gui.WindowFromPoint((cx, cy))
            try:
                class_name = win32gui.GetClassName(hwnd)
                root_hwnd = ctypes.windll.user32.GetAncestor(hwnd, 2)  # GA_ROOT
                root_class = win32gui.GetClassName(root_hwnd) if root_hwnd else ""
            except Exception:
                class_name = ""
                root_class = ""

            valid_classes = ("Shell_TrayWnd", "Shell_SecondaryTrayWnd")
            if class_name in valid_classes or root_class in valid_classes:
                multiplier = int(self.settings.get("step_multiplier", 1))
                invert = bool(self.settings.get("invert_scroll", False))

                # dy is positive for scroll up, negative for scroll down
                delta = dy
                if invert:
                    delta = -delta

                VK_VOLUME_UP = 0xAF
                VK_VOLUME_DOWN = 0xAE
                vk_code = VK_VOLUME_UP if delta > 0 else VK_VOLUME_DOWN

                for _ in range(multiplier):
                    ctypes.windll.user32.keybd_event(vk_code, 0, 0, 0)
                    ctypes.windll.user32.keybd_event(vk_code, 0, 2, 0)

        except Exception:
            pass

    def open_settings(self, icon, item):
        if hasattr(self, "ui_queue"):
            self.ui_queue.put("open_settings")

    def _poll_queue(self):
        try:
            while not self.ui_queue.empty():
                cmd = self.ui_queue.get_nowait()
                if cmd == "open_settings":
                    self.show_settings_window()
        except Exception:
            pass
        if self.root:
            self.root.after(100, self._poll_queue)

    def run(self):
        self.ui_queue = __import__("queue").Queue()

        self.mouse_listener = mouse.Listener(on_scroll=self.on_scroll)
        self.mouse_listener.start()

        # Start parent process monitoring
        system_utils.monitor_parent_process(lambda: self.on_quit(self.icon, None))

        menu = pystray.Menu(
            pystray.MenuItem("Settings", self.open_settings, default=True),
            pystray.MenuItem("Quit", self.on_quit),
        )
        self.icon = pystray.Icon(
            "TaskbarScroll", self.create_tray_icon_image(), "Taskbar Scroll", menu
        )

        icon_thread = threading.Thread(target=self.icon.run, daemon=True)
        icon_thread.start()

        self.root = tk.Tk()
        self.root.withdraw()
        self.root.after(100, self._poll_queue)
        self.root.mainloop()


if __name__ == "__main__":
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "TaskbarScrollApp_Mutex")
    if ctypes.windll.kernel32.GetLastError() == 183:
        sys.exit(0)

    app = TaskbarScrollApp()
    app.run()
```

---

