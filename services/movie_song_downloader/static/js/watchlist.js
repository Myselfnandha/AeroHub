/* MovieSongDownloader/static/js/watchlist.js */

document.addEventListener("DOMContentLoaded", () => {
    loadWatchlist();
    setupCheckButton();
});

async function loadWatchlist() {
    const loader = document.getElementById("watchlist-loader");
    const emptyState = document.getElementById("empty-watchlist-state");
    const listContainer = document.getElementById("watchlist-list");
    
    try {
        const res = await fetch("/api/watchlist");
        if (res.ok) {
            const items = await res.json();
            renderWatchlist(items);
        } else {
            loader.style.display = "none";
            emptyState.style.display = "flex";
        }
    } catch (e) {
        console.error("Watchlist load error:", e);
        loader.style.display = "none";
        emptyState.style.display = "flex";
    }
}

function renderWatchlist(items) {
    const loader = document.getElementById("watchlist-loader");
    const emptyState = document.getElementById("empty-watchlist-state");
    const listContainer = document.getElementById("watchlist-list");
    
    loader.style.display = "none";
    listContainer.innerHTML = "";
    
    if (!items || items.length === 0) {
        listContainer.style.display = "none";
        emptyState.style.display = "flex";
        return;
    }
    
    emptyState.style.display = "none";
    listContainer.style.display = "flex";
    
    items.forEach(item => {
        const row = document.createElement("div");
        row.className = "watchlist-row";
        
        const lastCheckedStr = item.last_checked ? `Last checked: ${item.last_checked}` : "Last checked: N/A";
        const autoDownloadStr = item.auto_download ? "Auto-DL" : "Manual";
        
        // Match status to badge class
        let badgeClass = "badge-watching";
        if (item.status === "found") badgeClass = "badge-found";
        else if (item.status === "downloaded") badgeClass = "badge-downloaded";
        else if (item.status === "expired") badgeClass = "badge-expired";
        
        row.innerHTML = `
            <span class="row-icon"><i class="fa-solid fa-tv"></i></span>
            <div class="row-details">
                <span class="row-title">${item.title}</span>
                <span class="row-subtitle">${lastCheckedStr}</span>
            </div>
            <span class="spacer"></span>
            <span class="row-meta" style="margin-right: 16px;">${autoDownloadStr}</span>
            <span class="badge ${badgeClass}" style="margin-right: 16px;">${item.status}</span>
            <button class="btn-icon btn-icon-danger delete-btn" title="Remove Movie"><i class="fa-solid fa-trash-2"></i></button>
        `;
        
        // Remove item event
        row.querySelector(".delete-btn").addEventListener("click", async () => {
            if (confirm(`Are you sure you want to remove "${item.title}" from your watchlist?`)) {
                try {
                    const delRes = await fetch(`/api/watchlist/${item.id}`, { method: "DELETE" });
                    if (delRes.ok) {
                        window.showToast(`"${item.title}" removed!`, "success");
                        loadWatchlist();
                    } else {
                        window.showToast("Failed to remove item", "error");
                    }
                } catch (e) {
                    console.error("Watchlist delete error:", e);
                    window.showToast("Connection error removing item", "error");
                }
            }
        });
        
        listContainer.appendChild(row);
    });
}

function setupCheckButton() {
    const checkBtn = document.getElementById("check-watchlist-btn");
    
    checkBtn.addEventListener("click", async () => {
        checkBtn.disabled = true;
        checkBtn.innerHTML = `<div class="spinner"></div> Checking...`;
        
        try {
            const res = await fetch("/api/watchlist/check", { method: "POST" });
            if (res.ok) {
                window.showToast("Watchlist check completed successfully!", "success");
                loadWatchlist();
            } else {
                const data = await res.json();
                window.showToast("Watchlist check failed: " + (data.error || "error"), "error");
            }
        } catch (e) {
            console.error("Watchlist check error:", e);
            window.showToast("Connection error running watchlist check", "error");
        } finally {
            checkBtn.disabled = false;
            checkBtn.innerHTML = `<i class="fa-solid fa-arrows-spin"></i> Check Watchlist`;
        }
    });
}
