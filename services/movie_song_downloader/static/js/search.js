/* MovieSongDownloader/static/js/search.js */

document.addEventListener("DOMContentLoaded", () => {
    setupSearchForm();
});

function setupSearchForm() {
    const form = document.getElementById("search-form");
    const queryInput = document.getElementById("search-query");
    const yearInput = document.getElementById("search-year");
    const loader = document.getElementById("search-loader");
    const grid = document.getElementById("search-grid");
    const emptyState = document.getElementById("empty-search-state");
    const submitBtn = document.getElementById("search-submit-btn");
    
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const q = queryInput.value.trim();
        const year = yearInput.value.trim();
        
        if (!q) return;
        
        // Hide previous views & show loader
        grid.style.display = "none";
        emptyState.style.display = "none";
        loader.style.display = "flex";
        submitBtn.disabled = true;
        
        try {
            const url = `/api/movies/search?q=${encodeURIComponent(q)}&year=${year}`;
            const res = await fetch(url, { method: "POST" });
            
            if (res.ok) {
                const data = await res.json();
                
                if (data.type === "redirect") {
                    // It resolved a Spotify/JioSaavn link directly
                    window.showToast("Link resolved successfully!", "success");
                    // Redirect to songs.html with the direct album/movie reference
                    const movie = data.movie;
                    const album = data.album;
                    window.location.href = `/songs?movie_id=${movie.id || ''}&source=${movie.source}&source_id=${movie.source_id}&title=${encodeURIComponent(movie.title)}&year=${movie.year || ''}&album_source_id=${album.source_id}`;
                } else {
                    renderSearchResults(data.results);
                }
            } else {
                const errData = await res.json();
                window.showToast("Search failed: " + (errData.detail || "error"), "error");
                loader.style.display = "none";
                emptyState.style.display = "flex";
            }
        } catch (err) {
            console.error("Search error:", err);
            window.showToast("Network error executing search", "error");
            loader.style.display = "none";
            emptyState.style.display = "flex";
        } finally {
            submitBtn.disabled = false;
        }
    });
}

function renderSearchResults(results) {
    const loader = document.getElementById("search-loader");
    const grid = document.getElementById("search-grid");
    const emptyState = document.getElementById("empty-search-state");
    
    loader.style.display = "none";
    grid.innerHTML = "";
    
    if (!results || results.length === 0) {
        grid.style.display = "none";
        emptyState.innerHTML = `
            <i class="fa-solid fa-magnifying-glass"></i>
            <p>No results found matching your query.</p>
        `;
        emptyState.style.display = "flex";
        return;
    }
    
    emptyState.style.display = "none";
    grid.style.display = "grid";
    
    results.forEach(movie => {
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
        `;
        
        card.addEventListener("click", () => {
            window.showMovieDetailModal(movie);
        });
        
        grid.appendChild(card);
    });
}
