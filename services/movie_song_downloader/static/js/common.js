/* MovieSongDownloader/static/js/common.js */

document.addEventListener("DOMContentLoaded", () => {
    renderSidebar();
    initializeToastsContainer();
    checkSetupWizardStatus();
});

function toggleSidebar() {
    const sidebar = document.querySelector(".sidebar");
    const container = document.querySelector(".app-container");
    const toggleBtnIcon = document.querySelector(".sidebar-toggle-btn i");
    
    if (!sidebar || !container) return;
    
    const isCollapsed = sidebar.classList.contains("collapsed");
    
    if (isCollapsed) {
        sidebar.classList.remove("collapsed");
        container.classList.remove("collapsed-sidebar");
        localStorage.setItem("sidebar-collapsed", "false");
        if (toggleBtnIcon) {
            toggleBtnIcon.className = "fa-solid fa-chevron-left";
        }
    } else {
        sidebar.classList.add("collapsed");
        container.classList.add("collapsed-sidebar");
        localStorage.setItem("sidebar-collapsed", "true");
        if (toggleBtnIcon) {
            toggleBtnIcon.className = "fa-solid fa-chevron-right";
        }
    }
}

function renderSidebar() {
    const container = document.getElementById("sidebar-container");
    if (!container) return;
    
    const isCollapsed = localStorage.getItem("sidebar-collapsed") === "true";
    const currentPath = window.location.pathname;
    
    const links = [
        { name: "Home", path: "/", icon: "fa-house" },
        { name: "Search", path: "/search", icon: "fa-magnifying-glass" },
        { name: "Watchlist", path: "/watchlist", icon: "fa-bookmark" },
        { name: "Downloads", path: "/downloads", icon: "fa-download" },
        { name: "Settings", path: "/settings", icon: "fa-gear" }
    ];
    
    // Also apply collapsed-sidebar to app-container immediately if collapsed
    const appContainer = document.querySelector(".app-container");
    if (appContainer) {
        if (isCollapsed) {
            appContainer.classList.add("collapsed-sidebar");
        } else {
            appContainer.classList.remove("collapsed-sidebar");
        }
    }
    
    let html = `
    <div class="sidebar ${isCollapsed ? 'collapsed' : ''}">
        <div class="sidebar-header">
            <div class="brand-section">
                <div class="brand-title-row">
                    <span class="brand-icon"><i class="fa-solid fa-music"></i></span>
                    <span class="brand-name">AeroHub Sync</span>
                </div>
                <span class="brand-subtitle">Song Downloader v2.0</span>
            </div>
            <button id="sidebar-toggle" class="sidebar-toggle-btn" title="Toggle Sidebar">
                <i class="fa-solid ${isCollapsed ? 'fa-chevron-right' : 'fa-chevron-left'}"></i>
            </button>
        </div>
        <nav class="nav-menu">
    `;
    
    links.forEach(link => {
        const isActive = (link.path === "/" && (currentPath === "/" || currentPath === "/index.html")) || 
                         (link.path !== "/" && (currentPath === link.path || currentPath.startsWith(link.path + "/") || currentPath.startsWith(link.path + ".html")));
        const activeClass = isActive ? "active" : "";
        html += `
            <a href="${link.path}" class="nav-link ${activeClass}" title="${link.name}">
                <i class="fa-solid ${link.icon}"></i>
                <span>${link.name}</span>
            </a>
        `;
    });
    
    html += `
        </nav>
    </div>
    `;
    
    container.innerHTML = html;
    
    // Attach event listener
    const toggleBtn = document.getElementById("sidebar-toggle");
    if (toggleBtn) {
        toggleBtn.addEventListener("click", toggleSidebar);
    }
}

function initializeToastsContainer() {
    if (!document.getElementById("toast-container")) {
        const container = document.createElement("div");
        container.id = "toast-container";
        container.className = "toast-container";
        document.body.appendChild(container);
    }
}

window.showToast = function(message, type = "info") {
    const container = document.getElementById("toast-container");
    if (!container) return;
    
    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    
    let icon = "fa-circle-info";
    if (type === "success") icon = "fa-circle-check";
    else if (type === "error") icon = "fa-circle-xmark";
    else if (type === "warn") icon = "fa-circle-exclamation";
    
    toast.innerHTML = `
        <i class="fa-solid ${icon}"></i>
        <span>${message}</span>
    `;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = "0";
        setTimeout(() => {
            toast.remove();
        }, 200);
    }, 4000);
};

// Check if OMDb Key is missing to prompt setup wizard modal
async function checkSetupWizardStatus() {
    try {
        const res = await fetch("/api/settings");
        if (res.ok) {
            const settings = await res.json();
            if (!settings.omdb_api_key) {
                showSetupWizardModal();
            }
        }
    } catch (e) {
        console.error("Failed to check setup wizard status:", e);
    }
}

function showSetupWizardModal() {
    // Create setup wizard elements if not present
    if (document.getElementById("setup-wizard-modal")) return;
    
    const overlay = document.createElement("div");
    overlay.id = "setup-wizard-modal";
    overlay.className = "modal-overlay open";
    
    overlay.innerHTML = `
        <div class="modal-content">
            <h2 class="modal-title">Welcome! Quick Setup</h2>
            <p class="modal-description">
                Movie details come from Wikipedia & JioSaavn automatically. 
                For ratings, cast info, and high-quality Deezer files, 
                configure key credentials below.
            </p>
            <div class="modal-body">
                <div class="form-group">
                    <label class="form-label">OMDb API Key (Required for ratings & cast)</label>
                    <input type="password" id="wizard-omdb-key" class="input-field" placeholder="Get a free key from omdbapi.com">
                </div>
                <div class="form-group" style="margin-top: 12px;">
                    <label class="form-label">Deezer ARL Token (Optional for 320kbps MP3s)</label>
                    <input type="password" id="wizard-deezer-arl" class="input-field" placeholder="Paste your Deezer ARL cookie">
                </div>
                <div id="wizard-error-msg" style="color: var(--color-error); font-size: 0.8rem; margin-top: 8px; display: none;"></div>
            </div>
            <div class="modal-footer">
                <button id="wizard-save-btn" class="btn btn-primary" style="width: 100%; margin-top: 12px;">Save and Continue</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(overlay);
    
    document.getElementById("wizard-save-btn").addEventListener("click", async () => {
        const omdbKey = document.getElementById("wizard-omdb-key").value.trim();
        const deezerArl = document.getElementById("wizard-deezer-arl").value.trim();
        const errorDiv = document.getElementById("wizard-error-msg");
        
        if (!omdbKey) {
            errorDiv.textContent = "OMDb API Key is required! Get a free key from omdbapi.com";
            errorDiv.style.display = "block";
            return;
        }
        
        try {
            // Save settings via API
            const getRes = await fetch("/api/settings");
            let settings = {};
            if (getRes.ok) {
                settings = await getRes.json();
            }
            
            settings.omdb_api_key = omdbKey;
            if (deezerArl) {
                settings.deezer_arl = deezerArl;
            }
            
            const saveRes = await fetch("/api/settings", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(settings)
            });
            
            if (saveRes.ok) {
                overlay.classList.remove("open");
                setTimeout(() => overlay.remove(), 200);
                window.showToast("Setup completed successfully!", "success");
                // Trigger refresh if we are on settings page
                if (window.location.pathname.startsWith("/settings")) {
                    window.location.reload();
                }
            } else {
                const data = await saveRes.json();
                errorDiv.textContent = "Error saving keys: " + (data.error || "Unknown error");
                errorDiv.style.display = "block";
            }
        } catch (e) {
            errorDiv.textContent = "Error saving keys: " + e.message;
            errorDiv.style.display = "block";
        }
    });
}

window.showMovieDetailModal = function(movie) {
    let overlay = document.getElementById("movie-detail-modal");
    if (!overlay) {
        overlay = document.createElement("div");
        overlay.id = "movie-detail-modal";
        overlay.className = "modal-overlay";
        document.body.appendChild(overlay);
    }
    
    const posterUrl = movie.poster_url || "https://via.placeholder.com/150x220?text=No+Poster";
    const ratingVal = movie.rating || "N/A";
    const yearVal = movie.year || "N/A";
    const castInfo = movie.cast_info || "Cast details not available.";
    const overview = movie.overview || "No overview description available for this release.";
    
    // Create detailed modal content
    overlay.innerHTML = `
        <div class="modal-content movie-detail-content">
            <button id="modal-close-btn" class="modal-close-btn" title="Close"><i class="fa-solid fa-xmark"></i></button>
            <div class="movie-detail-grid">
                <div class="movie-detail-poster-wrapper">
                    <img id="modal-poster" src="${posterUrl}" alt="${movie.title}" class="modal-poster">
                </div>
                <div class="movie-detail-info">
                    <div class="movie-detail-header">
                        <h2 id="modal-title" class="movie-detail-title">${movie.title}</h2>
                        <div class="movie-detail-meta">
                            <span id="modal-year" class="movie-detail-year">${yearVal}</span>
                            <span id="modal-rating" class="movie-rating-badge">
                                <i class="fa-solid fa-star"></i> <span id="modal-rating-val">${ratingVal}</span>
                            </span>
                        </div>
                    </div>
                    
                    <div class="movie-detail-section">
                        <span class="movie-detail-section-title">Cast</span>
                        <p id="modal-cast" class="movie-detail-cast">${castInfo}</p>
                    </div>
                    
                    <div class="movie-detail-section">
                        <span class="movie-detail-section-title">Overview</span>
                        <p id="modal-overview" class="movie-detail-overview">${overview}</p>
                    </div>
                    
                    <div class="movie-detail-actions">
                        <button id="modal-browse-btn" class="btn btn-primary"><i class="fa-solid fa-music"></i> Browse Tracks</button>
                        <button id="modal-watchlist-btn" class="btn btn-secondary"><i class="fa-solid fa-plus"></i> Add to Watchlist</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Trigger open transition
    requestAnimationFrame(() => {
        overlay.classList.add("open");
    });
    
    // Close handler
    const closeBtn = overlay.querySelector("#modal-close-btn");
    const closeModal = () => {
        overlay.classList.remove("open");
    };
    closeBtn.addEventListener("click", closeModal);
    overlay.addEventListener("click", (e) => {
        if (e.target === overlay) closeModal();
    });
    
    // Browse handler
    overlay.querySelector("#modal-browse-btn").addEventListener("click", () => {
        closeModal();
        window.location.href = `/songs?movie_id=${movie.id || ''}&source=${movie.source || 'wikipedia'}&source_id=${movie.source_id || ''}&title=${encodeURIComponent(movie.title)}&year=${movie.year || ''}`;
    });
    
    // Watchlist handler
    const watchlistBtn = overlay.querySelector("#modal-watchlist-btn");
    watchlistBtn.addEventListener("click", async () => {
        watchlistBtn.disabled = true;
        try {
            const addRes = await fetch("/api/watchlist", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    title: movie.title,
                    source: movie.source || "wikipedia",
                    source_id: movie.source_id || "",
                    auto_download: true
                })
            });
            
            if (addRes.ok) {
                window.showToast(`"${movie.title}" added to watchlist!`, "success");
                watchlistBtn.innerHTML = `<i class="fa-solid fa-check" style="color: var(--color-success);"></i> Added`;
            } else {
                const data = await addRes.json();
                window.showToast("Failed to add to watchlist: " + (data.error || "error"), "error");
                watchlistBtn.disabled = false;
            }
        } catch (err) {
            console.error("Watchlist error:", err);
            window.showToast("Network error adding to watchlist", "error");
            watchlistBtn.disabled = false;
        }
    });
};
