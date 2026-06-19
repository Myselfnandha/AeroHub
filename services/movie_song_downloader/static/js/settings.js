/* MovieSongDownloader/static/js/settings.js */

let explorerCurrentPath = "";
let explorerParentPath = "";

document.addEventListener("DOMContentLoaded", () => {
    loadSettings();
    setupDropdownToggles();
    setupFolderPicker();
    setupSaveSettings();
});

async function loadSettings() {
    try {
        const res = await fetch("/api/settings");
        if (res.ok) {
            const data = await res.json();
            
            document.getElementById("omdb-api-key").value = data.omdb_api_key || "";
            document.getElementById("deezer-arl").value = data.deezer_arl || "";
            document.getElementById("output-dir").value = data.output_dir || "";
            
            // Handle folder format presets
            const folderVal = data.folder_format || "";
            const folderDropdown = document.getElementById("folder-format-dropdown");
            const folderCustomInput = document.getElementById("folder-format-custom");
            
            const folderPresets = ["{Year}/{Movie}/Songs", "{Movie}", "{Artist}/{Album}", "{Movie}/{Songs}"];
            if (folderPresets.includes(folderVal)) {
                folderDropdown.value = folderVal;
                folderCustomInput.style.display = "none";
            } else {
                folderDropdown.value = "Custom...";
                folderCustomInput.value = folderVal;
                folderCustomInput.style.display = "block";
            }
            
            // Handle filename format presets
            const filenameVal = data.filename_format || "";
            const filenameDropdown = document.getElementById("filename-format-dropdown");
            const filenameCustomInput = document.getElementById("filename-format-custom");
            
            const filenamePresets = ["{TrackNum} - {Title}", "{Title}", "{Artist} - {Title}", "{TrackNum}. {Title}"];
            if (filenamePresets.includes(filenameVal)) {
                filenameDropdown.value = filenameVal;
                filenameCustomInput.style.display = "none";
            } else {
                filenameDropdown.value = "Custom...";
                filenameCustomInput.value = filenameVal;
                filenameCustomInput.style.display = "block";
            }
            
            document.getElementById("audio-format").value = data.audio_format || "mp3";
            document.getElementById("audio-bitrate").value = data.bitrate || "320";
            document.getElementById("download-provider").value = data.download_provider || "spotiflac";
            
            document.getElementById("save-lrc-file").checked = data.save_lrc_file === true || data.save_lrc_file === "true";
            document.getElementById("embed-lyrics").checked = data.embed_lyrics === true || data.embed_lyrics === "true";
            document.getElementById("auto-download").checked = data.auto_download === true || data.auto_download === "true";
        } else {
            window.showToast("Failed to load settings data", "error");
        }
    } catch (e) {
        console.error("Settings load error:", e);
        window.showToast("Connection error loading settings", "error");
    }
}

function setupDropdownToggles() {
    const folderDropdown = document.getElementById("folder-format-dropdown");
    const folderCustom = document.getElementById("folder-format-custom");
    folderDropdown.addEventListener("change", (e) => {
        if (e.target.value === "Custom...") {
            folderCustom.style.display = "block";
            folderCustom.focus();
        } else {
            folderCustom.style.display = "none";
        }
    });
    
    const filenameDropdown = document.getElementById("filename-format-dropdown");
    const filenameCustom = document.getElementById("filename-format-custom");
    filenameDropdown.addEventListener("change", (e) => {
        if (e.target.value === "Custom...") {
            filenameCustom.style.display = "block";
            filenameCustom.focus();
        } else {
            filenameCustom.style.display = "none";
        }
    });
}

function setupFolderPicker() {
    const browseBtn = document.getElementById("browse-dir-btn");
    const explorerModal = document.getElementById("dir-explorer-modal");
    const cancelBtn = document.getElementById("cancel-explorer-btn");
    const selectBtn = document.getElementById("select-folder-btn");
    const parentBtn = document.getElementById("parent-dir-btn");
    
    browseBtn.addEventListener("click", () => {
        explorerModal.classList.add("open");
        const currentPathVal = document.getElementById("output-dir").value.trim();
        loadExplorerPath(currentPathVal);
    });
    
    cancelBtn.addEventListener("click", () => {
        explorerModal.classList.remove("open");
    });
    
    parentBtn.addEventListener("click", () => {
        if (explorerParentPath) {
            loadExplorerPath(explorerParentPath);
        }
    });
    
    selectBtn.addEventListener("click", () => {
        document.getElementById("output-dir").value = explorerCurrentPath;
        explorerModal.classList.remove("open");
        window.showToast("Folder selected!", "info");
    });
}

async function loadExplorerPath(path) {
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
                    const separator = explorerCurrentPath.includes("\\") ? "\\" : "/";
                    const newPath = explorerCurrentPath.endsWith(separator) ? 
                                    `${explorerCurrentPath}${folder}` : 
                                    `${explorerCurrentPath}${separator}${folder}`;
                    loadExplorerPath(newPath);
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

function setupSaveSettings() {
    const saveBtn = document.getElementById("save-settings-btn");
    const statusMsg = document.getElementById("settings-status-msg");
    
    saveBtn.addEventListener("click", async () => {
        statusMsg.textContent = "Saving...";
        statusMsg.style.color = "#F59E0B";
        saveBtn.disabled = true;
        
        // Resolve templates values
        const folderDropdown = document.getElementById("folder-format-dropdown").value;
        const folderCustom = document.getElementById("folder-format-custom").value.trim();
        const folderFormat = folderDropdown === "Custom..." ? folderCustom : folderDropdown;
        
        const filenameDropdown = document.getElementById("filename-format-dropdown").value;
        const filenameCustom = document.getElementById("filename-format-custom").value.trim();
        const filenameFormat = filenameDropdown === "Custom..." ? filenameCustom : filenameDropdown;
        
        const payload = {
            omdb_api_key: document.getElementById("omdb-api-key").value.trim(),
            deezer_arl: document.getElementById("deezer-arl").value.trim(),
            output_dir: document.getElementById("output-dir").value.trim(),
            folder_format: folderFormat || "{Year}/{Movie}/Songs",
            filename_format: filenameFormat || "{TrackNum} - {Title}",
            audio_format: document.getElementById("audio-format").value,
            bitrate: document.getElementById("audio-bitrate").value,
            download_provider: document.getElementById("download-provider").value,
            save_lrc_file: document.getElementById("save-lrc-file").checked,
            embed_lyrics: document.getElementById("embed-lyrics").checked,
            auto_download: document.getElementById("auto-download").checked
        };
        
        try {
            const res = await fetch("/api/settings", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            
            if (res.ok) {
                statusMsg.textContent = "Settings Saved Successfully!";
                statusMsg.style.color = "#22C55E";
                window.showToast("Settings saved successfully!", "success");
            } else {
                const data = await res.json();
                statusMsg.textContent = "Failed to save: " + (data.error || "error");
                statusMsg.style.color = "#EF4444";
                window.showToast("Failed to save settings", "error");
            }
        } catch (e) {
            console.error("Save settings error:", e);
            statusMsg.textContent = "Connection error saving settings";
            statusMsg.style.color = "#EF4444";
            window.showToast("Connection error saving settings", "error");
        } finally {
            saveBtn.disabled = false;
        }
    });
}
