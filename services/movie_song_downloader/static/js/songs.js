/* MovieSongDownloader/static/js/songs.js */

let movieData = {};
let albumData = {};
let tracksList = [];
let selectedTrackIds = [];
let currentPlayingUrl = "";
let explorerCurrentPath = "";
let explorerParentPath = "";

document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    loadAlbumAndTracks(params);
    setupBackButton();
    setupSelectAll();
    setupDownloadButton();
    setupModalButtons();
});

function setupBackButton() {
    document.getElementById("back-btn").addEventListener("click", () => {
        if (document.referrer && document.referrer.includes("/search")) {
            window.location.href = "/search";
        } else {
            window.location.href = "/";
        }
    });
}

async function loadAlbumAndTracks(params) {
    const loader = document.getElementById("tracks-loader");
    const emptyState = document.getElementById("empty-tracks-state");
    const albumCard = document.getElementById("album-header-card");
    const subControls = document.getElementById("sub-controls-row");
    const tracksListDiv = document.getElementById("tracks-list");
    
    const movieId = params.get("movie_id");
    const source = params.get("source") || "wikipedia";
    const sourceId = params.get("source_id") || "";
    const title = params.get("title") || "";
    const year = params.get("year") || "";
    const albumSourceId = params.get("album_source_id") || "";
    
    try {
        const queryParams = new URLSearchParams({
            movie_id: movieId || "",
            source: source,
            source_id: sourceId,
            title: title,
            year: year,
            album_source_id: albumSourceId
        });
        
        const res = await fetch(`/api/movies/browse?${queryParams}`);
        if (res.ok) {
            const data = await res.json();
            movieData = data.movie;
            albumData = data.album;
            tracksList = data.tracks;
            
            // Initial selection is Select All
            selectedTrackIds = tracksList.map(t => t.db_id);
            
            renderAlbumHeader();
            renderTracks();
            
            loader.style.display = "none";
            albumCard.style.display = "flex";
            subControls.style.display = "flex";
            tracksListDiv.style.display = "flex";
        } else {
            loader.style.display = "none";
            emptyState.style.display = "flex";
        }
    } catch (e) {
        console.error("Failed to load tracks:", e);
        loader.style.display = "none";
        emptyState.style.display = "flex";
    }
}

function renderAlbumHeader() {
    document.getElementById("album-title").textContent = albumData.title || "Unknown Album";
    const coverUrl = albumData.cover_url || "https://via.placeholder.com/120?text=No+Cover";
    document.getElementById("album-cover").src = coverUrl;
    
    const yearText = movieData.year ? `(${movieData.year})` : "";
    document.getElementById("movie-info").textContent = `Movie: ${movieData.title} ${yearText}`;
    document.getElementById("album-artists").textContent = `Artists: ${albumData.artist || 'Various Artists'}`;
}

function renderTracks() {
    const listDiv = document.getElementById("tracks-list");
    const emptyState = document.getElementById("empty-tracks-state");
    
    listDiv.innerHTML = "";
    if (!tracksList || tracksList.length === 0) {
        listDiv.style.display = "none";
        emptyState.style.display = "flex";
        return;
    }
    
    emptyState.style.display = "none";
    listDiv.style.display = "flex";
    
    tracksList.forEach((track) => {
        const row = document.createElement("div");
        row.className = "track-row";
        
        // Duration MM:SS
        const durationSec = Math.floor((track.duration_ms || 0) / 1000);
        const minutes = Math.floor(durationSec / 60);
        const seconds = durationSec % 60;
        const secondsStr = seconds < 10 ? `0${seconds}` : seconds;
        const durationStr = `${minutes}:${secondsStr}`;
        
        const isChecked = selectedTrackIds.includes(track.db_id) ? "checked" : "";
        const playBtnHtml = track.preview_url ? `
            <button class="btn-icon play-preview-btn" data-url="${track.preview_url}" title="Play Preview">
                <i class="fa-solid fa-play"></i>
            </button>
        ` : "";
        
        row.innerHTML = `
            <input type="checkbox" class="track-checkbox" data-id="${track.db_id}" style="cursor: pointer; width: 16px; height: 16px; accent-color: var(--color-accent);" ${isChecked}>
            <span class="track-num">${track.track_number || ''}</span>
            <div class="track-title-info">
                <span class="track-title">${track.title}</span>
                <span class="track-artist">${track.artist || ''}</span>
            </div>
            <span class="spacer"></span>
            <span class="track-duration">${durationStr}</span>
            ${playBtnHtml}
        `;
        
        // Toggle single checkbox
        row.querySelector(".track-checkbox").addEventListener("change", (e) => {
            const trackId = track.db_id;
            if (e.target.checked) {
                if (!selectedTrackIds.includes(trackId)) {
                    selectedTrackIds.push(trackId);
                }
            } else {
                selectedTrackIds = selectedTrackIds.filter(id => id !== trackId);
            }
            updateSelectAllCheckboxState();
        });
        
        // Setup play preview button
        if (track.preview_url) {
            const playBtn = row.querySelector(".play-preview-btn");
            playBtn.addEventListener("click", () => {
                playPreview(track.preview_url, playBtn);
            });
        }
        
        listDiv.appendChild(row);
    });
}

function updateSelectAllCheckboxState() {
    const selectAllCheck = document.getElementById("select-all-checkbox");
    selectAllCheck.checked = selectedTrackIds.length === tracksList.length;
}

function setupSelectAll() {
    const selectAllCheck = document.getElementById("select-all-checkbox");
    selectAllCheck.addEventListener("change", (e) => {
        const isChecked = e.target.checked;
        const trackChecks = document.querySelectorAll(".track-checkbox");
        
        if (isChecked) {
            selectedTrackIds = tracksList.map(t => t.db_id);
            trackChecks.forEach(ch => ch.checked = true);
        } else {
            selectedTrackIds = [];
            trackChecks.forEach(ch => ch.checked = false);
        }
    });
}

function playPreview(url, btnElement) {
    const audio = document.getElementById("audio-preview-element");
    const allPlayBtns = document.querySelectorAll(".play-preview-btn");
    
    if (currentPlayingUrl === url) {
        // Stop currently playing
        audio.pause();
        audio.src = "";
        currentPlayingUrl = "";
        btnElement.innerHTML = `<i class="fa-solid fa-play"></i>`;
        btnElement.title = "Play Preview";
    } else {
        // Reset other buttons
        allPlayBtns.forEach(btn => {
            btn.innerHTML = `<i class="fa-solid fa-play"></i>`;
            btn.title = "Play Preview";
        });
        
        audio.src = url;
        audio.play().then(() => {
            currentPlayingUrl = url;
            btnElement.innerHTML = `<i class="fa-solid fa-square"></i>`;
            btnElement.title = "Stop Preview";
        }).catch(err => {
            console.error("Audio playback error:", err);
            window.showToast("Failed to play preview clip", "error");
        });
        
        // Reset when ended
        audio.onended = () => {
            btnElement.innerHTML = `<i class="fa-solid fa-play"></i>`;
            btnElement.title = "Play Preview";
            currentPlayingUrl = "";
        };
    }
}

function setupDownloadButton() {
    const downloadBtn = document.getElementById("download-selected-btn");
    
    downloadBtn.addEventListener("click", async () => {
        if (selectedTrackIds.length === 0) {
            window.showToast("Please select at least one track to download", "warn");
            return;
        }
        
        downloadBtn.disabled = true;
        downloadBtn.innerHTML = `<div class="spinner"></div> Checking Path...`;
        
        try {
            const res = await fetch("/api/settings");
            if (res.ok) {
                const settings = await res.json();
                if (!settings.output_dir || settings.output_dir.trim() === "") {
                    // Show warning dialog
                    document.getElementById("missing-dir-dialog").classList.add("open");
                    downloadBtn.disabled = false;
                    downloadBtn.innerHTML = `<i class="fa-solid fa-cloud-arrow-down"></i> Download Selected`;
                } else {
                    enqueueDownloads(selectedTrackIds);
                }
            } else {
                window.showToast("Error checking settings", "error");
                downloadBtn.disabled = false;
                downloadBtn.innerHTML = `<i class="fa-solid fa-cloud-arrow-down"></i> Download Selected`;
            }
        } catch (e) {
            console.error("Download path error:", e);
            window.showToast("Connection error checking path", "error");
            downloadBtn.disabled = false;
            downloadBtn.innerHTML = `<i class="fa-solid fa-cloud-arrow-down"></i> Download Selected`;
        }
    });
}

async function enqueueDownloads(trackIds) {
    const downloadBtn = document.getElementById("download-selected-btn");
    downloadBtn.disabled = true;
    downloadBtn.innerHTML = `<div class="spinner"></div> Queuing...`;
    
    try {
        const res = await fetch("/api/downloads/enqueue", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ track_ids: trackIds })
        });
        
        if (res.ok) {
            window.showToast(`Queued ${trackIds.length} soundtracks for download!`, "success");
            setTimeout(() => {
                window.location.href = "/downloads";
            }, 1000);
        } else {
            const data = await res.json();
            window.showToast("Failed to queue downloads: " + (data.error || "error"), "error");
            downloadBtn.disabled = false;
            downloadBtn.innerHTML = `<i class="fa-solid fa-cloud-arrow-down"></i> Download Selected`;
        }
    } catch (e) {
        console.error("Queue downloads error:", e);
        window.showToast("Connection error queuing downloads", "error");
        downloadBtn.disabled = false;
        downloadBtn.innerHTML = `<i class="fa-solid fa-cloud-arrow-down"></i> Download Selected`;
    }
}

function setupModalButtons() {
    // Missing directory warning modal buttons
    const missingDialog = document.getElementById("missing-dir-dialog");
    const defaultBtn = document.getElementById("default-downloads-btn");
    const triggerPickerBtn = document.getElementById("trigger-picker-btn");
    
    defaultBtn.addEventListener("click", async () => {
        missingDialog.classList.remove("open");
        try {
            // Set output_dir to default downloads folder
            const res = await fetch("/api/settings/set-default-dir", { method: "POST" });
            if (res.ok) {
                enqueueDownloads(selectedTrackIds);
            } else {
                window.showToast("Failed to set default downloads path", "error");
            }
        } catch (e) {
            window.showToast("Connection error setting path", "error");
        }
    });
    
    triggerPickerBtn.addEventListener("click", () => {
        missingDialog.classList.remove("open");
        openDirectoryExplorer();
    });
    
    // Directory explorer modal buttons
    const explorerModal = document.getElementById("dir-explorer-modal");
    const cancelExplorerBtn = document.getElementById("cancel-explorer-btn");
    const selectFolderBtn = document.getElementById("select-folder-btn");
    const parentDirBtn = document.getElementById("parent-dir-btn");
    
    cancelExplorerBtn.addEventListener("click", () => {
        explorerModal.classList.remove("open");
    });
    
    parentDirBtn.addEventListener("click", () => {
        if (explorerParentPath) {
            loadDirectoryPath(explorerParentPath);
        }
    });
    
    selectFolderBtn.addEventListener("click", async () => {
        try {
            // Save folder via API
            const getRes = await fetch("/api/settings");
            let settings = {};
            if (getRes.ok) {
                settings = await getRes.json();
            }
            settings.output_dir = explorerCurrentPath;
            
            const saveRes = await fetch("/api/settings", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(settings)
            });
            
            if (saveRes.ok) {
                explorerModal.classList.remove("open");
                window.showToast("Output directory configured successfully!", "success");
                enqueueDownloads(selectedTrackIds);
            } else {
                window.showToast("Failed to save output directory", "error");
            }
        } catch (e) {
            window.showToast("Connection error saving path", "error");
        }
    });
}

function openDirectoryExplorer() {
    document.getElementById("dir-explorer-modal").classList.add("open");
    loadDirectoryPath("");
}

async function loadDirectoryPath(path) {
    const errorDiv = document.getElementById("explorer-error-msg");
    const itemsContainer = document.getElementById("explorer-items-container");
    const pathText = document.getElementById("current-explorer-path");
    
    errorDiv.style.display = "none";
    itemsContainer.innerHTML = `<div class="spinner" style="margin: 12px auto;"></div>`;
    
    try {
        const queryParams = new URLSearchParams({ path: path });
        const res = await fetch(`/api/utils/dir-explorer?${queryParams}`);
        if (res.ok) {
            const data = await res.json();
            explorerCurrentPath = data.current_path;
            explorerParentPath = data.parent_path;
            pathText.textContent = data.current_path;
            
            itemsContainer.innerHTML = "";
            if (!data.subdirectories || data.subdirectories.length === 0) {
                itemsContainer.innerHTML = `<span style="color: var(--color-text-muted); font-size: 0.85rem; padding: 12px; text-align: center;">No subdirectories found.</span>`;
                return;
            }
            
            data.subdirectories.forEach(folder => {
                const btn = document.createElement("button");
                btn.className = "explorer-item";
                btn.innerHTML = `<i class="fa-solid fa-folder"></i> <span>${folder}</span>`;
                
                btn.addEventListener("click", () => {
                    // Navigate down
                    // Concatenate path correctly based on OS
                    const separator = explorerCurrentPath.includes("\\") ? "\\" : "/";
                    const newPath = explorerCurrentPath.endsWith(separator) ? 
                                    `${explorerCurrentPath}${folder}` : 
                                    `${explorerCurrentPath}${separator}${folder}`;
                    loadDirectoryPath(newPath);
                });
                
                itemsContainer.appendChild(btn);
            });
        } else {
            const err = await res.json();
            itemsContainer.innerHTML = "";
            errorDiv.textContent = "Error reading folder: " + (err.error || "error");
            errorDiv.style.display = "block";
        }
    } catch (e) {
        itemsContainer.innerHTML = "";
        errorDiv.textContent = "Connection error reading directory: " + e.message;
        errorDiv.style.display = "block";
    }
}
