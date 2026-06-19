/* MovieSongDownloader/static/js/home.js */

document.addEventListener("DOMContentLoaded", () => {
    loadCachedMovies();
    triggerBackgroundUpdates();
    setupRefreshButton();
});

let currentMoviesList = [];

async function loadCachedMovies() {
    const loader = document.getElementById("releases-loader");
    const grid = document.getElementById("releases-grid");
    const emptyState = document.getElementById("empty-releases-state");
    
    try {
        const res = await fetch("/api/movies/cached");
        if (res.ok) {
            const movies = await res.json();
            currentMoviesList = movies;
            renderMovieGrid(movies);
        } else {
            loader.style.display = "none";
            emptyState.style.display = "flex";
        }
    } catch (e) {
        console.error("Failed to load cached movies:", e);
        loader.style.display = "none";
        emptyState.style.display = "flex";
    }
}

function renderMovieGrid(movies) {
    const loader = document.getElementById("releases-loader");
    const grid = document.getElementById("releases-grid");
    const emptyState = document.getElementById("empty-releases-state");
    
    loader.style.display = "none";
    grid.innerHTML = "";
    
    if (!movies || movies.length === 0) {
        grid.style.display = "none";
        emptyState.style.display = "flex";
        return;
    }
    
    emptyState.style.display = "none";
    grid.style.display = "grid";
    
    movies.forEach(movie => {
        const card = document.createElement("div");
        card.className = "movie-card";
        
        const posterUrl = movie.poster_url || "https://via.placeholder.com/150x220?text=No+Poster";
        const ratingHtml = movie.rating ? `<span class="movie-rating">★ ${movie.rating}</span>` : "";
        const yearVal = movie.year || "N/A";
        
        card.innerHTML = `
            <div class="poster-container">
                <img src="${posterUrl}" class="movie-poster" alt="${movie.title}">
            </div>
            <div class="movie-info">
                <span class="movie-title" title="${movie.title}">${movie.title}</span>
                <div class="movie-meta">
                    <span class="movie-year">${yearVal}</span>
                    ${ratingHtml}
                </div>
            </div>
            <div class="card-actions">
                <button class="btn btn-ghost browse-btn">Browse</button>
                <button class="btn-icon add-watchlist-btn" title="Add to Watchlist"><i class="fa-solid fa-plus"></i></button>
            </div>
        `;
        
        // Setup card actions
        card.querySelector(".browse-btn").addEventListener("click", (e) => {
            e.stopPropagation();
            // Redirect to songs.html with query parameters
            window.location.href = `/songs?movie_id=${movie.id}&title=${encodeURIComponent(movie.title)}&year=${movie.year}`;
        });
        
        // Clicking card itself opens the metadata modal
        card.addEventListener("click", () => {
            window.showMovieDetailModal(movie);
        });
        
        card.querySelector(".add-watchlist-btn").addEventListener("click", async (e) => {
            e.stopPropagation();
            const btn = e.currentTarget;
            btn.disabled = true;
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
                    btn.innerHTML = `<i class="fa-solid fa-check" style="color: var(--color-success);"></i>`;
                } else {
                    const data = await addRes.json();
                    window.showToast("Failed to add to watchlist: " + (data.error || "error"), "error");
                    btn.disabled = false;
                }
            } catch (err) {
                console.error("Watchlist error:", err);
                window.showToast("Network error adding to watchlist", "error");
                btn.disabled = false;
            }
        });
        
        grid.appendChild(card);
    });
}

function triggerBackgroundUpdates() {
    const statusPanel = document.getElementById("update-status-panel");
    const statusText = document.getElementById("update-status-text");
    
    // Kickoff post request to start background updates
    fetch("/api/movies/fetch-updates", { method: "POST" })
        .then(res => {
            if (res.ok) {
                // Connect to SSE for progress
                const eventSource = new EventSource("/api/movies/fetch-progress");
                statusPanel.style.display = "flex";
                
                eventSource.onmessage = (event) => {
                    const data = JSON.parse(event.data);
                    if (data.is_fetching) {
                        statusPanel.style.display = "flex";
                        statusText.textContent = data.status || `Scraping... (${Math.round(data.progress)}%)`;
                    }
                    
                    if (data.has_new_movies) {
                        document.getElementById("refresh-dashboard-btn").style.display = "inline-flex";
                    }
                    
                    if (!data.is_fetching && data.progress >= 100) {
                        statusPanel.style.display = "none";
                        eventSource.close();
                    }
                };
                
                eventSource.onerror = (err) => {
                    console.error("SSE connection error:", err);
                    statusPanel.style.display = "none";
                    eventSource.close();
                };
            }
        })
        .catch(err => {
            console.error("Failed to start background updates:", err);
        });
}

function setupRefreshButton() {
    const refreshBtn = document.getElementById("refresh-dashboard-btn");
    
    refreshBtn.addEventListener("click", async () => {
        refreshBtn.disabled = true;
        try {
            const res = await fetch("/api/movies/apply-updates", { method: "POST" });
            if (res.ok) {
                refreshBtn.style.display = "none";
                refreshBtn.disabled = false;
                window.showToast("Dashboard refreshed with new releases!", "success");
                loadCachedMovies();
            } else {
                refreshBtn.disabled = false;
            }
        } catch (e) {
            console.error("Failed to apply updates:", e);
            refreshBtn.disabled = false;
        }
    });
}
