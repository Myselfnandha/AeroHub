/* MovieSongDownloader/static/js/downloads.js */

let pollIntervalId = null;

document.addEventListener("DOMContentLoaded", () => {
    loadDownloadJobs(true);
    setupRefreshButton();
    startPolling();
});

// Clear interval when navigating away
window.addEventListener("beforeunload", () => {
    if (pollIntervalId) {
        clearInterval(pollIntervalId);
    }
});

async function loadDownloadJobs(showLoader = false) {
    const loader = document.getElementById("downloads-loader");
    const emptyState = document.getElementById("empty-downloads-state");
    const listContainer = document.getElementById("downloads-list");
    
    if (showLoader) {
        loader.style.display = "flex";
        listContainer.style.display = "none";
        emptyState.style.display = "none";
    }
    
    try {
        const res = await fetch("/api/downloads");
        if (res.ok) {
            const jobs = await res.json();
            renderDownloadJobs(jobs);
        } else {
            if (showLoader) {
                loader.style.display = "none";
                emptyState.style.display = "flex";
            }
        }
    } catch (e) {
        console.error("Failed to load download jobs:", e);
        if (showLoader) {
            loader.style.display = "none";
            emptyState.style.display = "flex";
        }
    }
}

function renderDownloadJobs(jobs) {
    const loader = document.getElementById("downloads-loader");
    const emptyState = document.getElementById("empty-downloads-state");
    const listContainer = document.getElementById("downloads-list");
    
    loader.style.display = "none";
    listContainer.innerHTML = "";
    
    if (!jobs || jobs.length === 0) {
        listContainer.style.display = "none";
        emptyState.style.display = "flex";
        return;
    }
    
    emptyState.style.display = "none";
    listContainer.style.display = "flex";
    
    jobs.forEach(job => {
        const card = document.createElement("div");
        card.className = "job-card";
        
        const status = (job.status || "queued").toLowerCase();
        
        // Active status check
        const isFinished = status === "completed" || status === "failed" || status === "cancelled" || status === "paused";
        const isActive = !isFinished;
        
        const progressPercent = isActive ? (job.progress || 0) : (status === "completed" ? 100 : 0);
        
        // Setup status badge classes
        let badgeStyle = `background-color: var(--color-dim); color: var(--color-text-primary);`;
        if (status === "queued") badgeStyle = `background-color: var(--color-warn); color: var(--color-bg-primary);`;
        else if (status === "downloading" || status === "fetching_lyrics" || status === "embedding_cover" || status === "embedding_metadata") {
            badgeStyle = `background-color: var(--color-info); color: white;`;
        }
        else if (status === "copying_to_destination") badgeStyle = `background-color: var(--color-warn); color: var(--color-bg-primary);`;
        else if (status === "completed") badgeStyle = `background-color: var(--color-success); color: var(--color-bg-primary);`;
        else if (status === "failed") badgeStyle = `background-color: var(--color-error); color: white;`;
        
        // Set action button based on state
        let actionBtnHtml = "";
        if (isActive) {
            actionBtnHtml = `
                <button class="btn-icon btn-icon-danger cancel-job-btn" title="Cancel Download"><i class="fa-solid fa-square"></i></button>
            `;
        } else if (status === "paused") {
            actionBtnHtml = `
                <button class="btn-icon resume-job-btn" title="Resume Download"><i class="fa-solid fa-play"></i></button>
            `;
        } else if (status === "failed" || status === "cancelled") {
            actionBtnHtml = `
                <button class="btn-icon retry-job-btn" title="Retry Download"><i class="fa-solid fa-rotate-right"></i></button>
            `;
        }
        
        const errorHtml = job.error_message ? `
            <div class="job-error">
                <span>${job.error_message}</span>
            </div>
        ` : "";
        
        const outPath = job.output_path || "Output path pending";
        const fmt = job.format || "mp3";
        
        card.innerHTML = `
            <div class="job-header">
                <div class="job-titles">
                    <span class="job-track">${job.track_title}</span>
                    <span class="job-album">${job.track_artist} • ${job.album_title}</span>
                </div>
                <span class="badge" style="${badgeStyle}">${status}</span>
            </div>
            
            <div class="progress-row">
                <div class="progress-bar-container">
                    <div class="progress-bar-fill" style="width: ${progressPercent}%;"></div>
                </div>
                <span class="progress-text">${progressPercent}%</span>
            </div>
            
            <div class="job-meta-row">
                <span>Format: ${fmt}</span>
                <span style="max-width: 75%; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${outPath}">${outPath}</span>
            </div>
            
            ${errorHtml}
            
            <div class="job-actions">
                ${actionBtnHtml}
            </div>
        `;
        
        // Attach action events
        if (isActive) {
            card.querySelector(".cancel-job-btn").addEventListener("click", () => controlJob(job.id, "cancel"));
        } else if (status === "paused") {
            card.querySelector(".resume-job-btn").addEventListener("click", () => controlJob(job.id, "resume"));
        } else if (status === "failed" || status === "cancelled") {
            card.querySelector(".retry-job-btn").addEventListener("click", () => controlJob(job.id, "retry"));
        }
        
        listContainer.appendChild(card);
    });
}

async function controlJob(id, action) {
    try {
        const res = await fetch(`/api/downloads/${action}/${id}`, { method: "POST" });
        if (res.ok) {
            window.showToast(`Job ${action} command sent!`, "success");
            loadDownloadJobs();
        } else {
            window.showToast(`Failed to ${action} job`, "error");
        }
    } catch (e) {
        console.error(`Error controlling job:`, e);
        window.showToast("Connection error executing command", "error");
    }
}

function setupRefreshButton() {
    const refreshBtn = document.getElementById("refresh-queue-btn");
    refreshBtn.addEventListener("click", () => {
        loadDownloadJobs(true);
    });
}

function startPolling() {
    if (pollIntervalId) clearInterval(pollIntervalId);
    
    pollIntervalId = setInterval(() => {
        loadDownloadJobs(false);
    }, 2000);
}
