"""
TempMonitor settings GUI — pywebview window with live thermal sparklines and sensor monitor.

Usage:
    from TempMonitor.settings_gui import open_settings
    open_settings(settings, all_temps, temp_history, on_save_callback)
"""

import json
import os
import sys
import webview

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.settings import save_settings
from common.tray import get_theme

_SETTINGS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.json")


class SettingsAPI:
    def __init__(self, settings, all_temps, temp_history, on_save=None):
        self.settings = settings
        self.all_temps = all_temps
        self.temp_history = temp_history
        self.on_save = on_save

    def get_settings(self):
        return self.settings

    def save_settings(self, new_settings):
        self.settings.update(new_settings)
        save_settings(_SETTINGS_PATH, self.settings)
        if self.on_save:
            self.on_save(self.settings)
        return {"status": "ok"}

    def get_autostart_status(self):
        try:
            from TempMonitor.temp_monitor import is_autostart_enabled
            return is_autostart_enabled()
        except Exception:
            return False

    def set_autostart(self, enabled):
        try:
            from TempMonitor.temp_monitor import set_autostart
            return set_autostart(enabled)
        except Exception:
            return False

    def get_live_data(self):
        # Format history into arrays
        history_dict = {k: list(v) for k, v in self.temp_history.items()}
        return {
            "temps": self.all_temps,
            "history": history_dict,
        }

    def get_theme(self):
        return get_theme()


def _build_html():
    return """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>TempMonitor Settings</title>
<style>
:root {
    --bg: #0f172a; --surface: #1e293b; --border: rgba(255,255,255,0.1);
    --text: #f8fafc; --text-dim: #94a3b8; --accent: #3b82f6;
    --accent-hover: #2563eb; --radius: 10px;
    --success: #10b981; --warning: #f59e0b; --danger: #ef4444;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'Segoe UI', system-ui, sans-serif; background: var(--bg);
    color: var(--text); padding: 20px; user-select: none;
}
h1 { font-size: 18px; margin-bottom: 16px; font-weight: 600; display: flex; align-items: center; gap: 8px; }
.tabs { display: flex; gap: 8px; margin-bottom: 16px; border-bottom: 1px solid var(--border); padding-bottom: 8px; }
.tab {
    padding: 6px 14px; cursor: pointer; font-size: 12px; border-radius: 6px;
    color: var(--text-dim); transition: all 0.2s;
}
.tab:hover { color: var(--text); background: rgba(255,255,255,0.05); }
.tab.active { color: #fff; background: var(--accent); }
.panel { display: none; }
.panel.active { display: block; }

/* Sparkline Card */
.sparkline-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 14px; margin-bottom: 16px;
}
.sparkline-header { display: flex; justify-content: space-between; font-size: 13px; font-weight: 600; margin-bottom: 8px; }
canvas { width: 100%; height: 80px; background: rgba(0,0,0,0.2); border-radius: 6px; }

/* Sensors List */
.sensors-list { display: flex; flex-direction: column; gap: 6px; max-height: 180px; overflow-y: auto; margin-bottom: 16px; }
.sensor-row {
    display: flex; justify-content: space-between; align-items: center;
    background: rgba(0,0,0,0.2); padding: 8px 12px; border-radius: 6px; border: 1px solid var(--border);
    font-size: 12px;
}
.sensor-val { font-weight: 600; }

.field {
    display: flex; justify-content: space-between; align-items: center;
    padding: 10px 0; border-bottom: 1px solid var(--border);
}
.field-label { font-size: 13px; }
.field-desc { font-size: 11px; color: var(--text-dim); }
input[type="number"] {
    width: 80px; padding: 5px 8px; border: 1px solid var(--border);
    border-radius: 6px; background: rgba(0,0,0,0.2);
    color: var(--text); font-size: 12px; text-align: center;
}
.switch { position: relative; display: inline-block; width: 40px; height: 22px; }
.switch input { opacity: 0; width: 0; height: 0; }
.slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background: rgba(255,255,255,0.15); transition: .3s; border-radius: 22px; }
.slider:before { position: absolute; content: ""; height: 16px; width: 16px; left: 3px; bottom: 3px; background: white; transition: .3s; border-radius: 50%; }
input:checked + .slider { background: var(--accent); }
input:checked + .slider:before { transform: translateX(18px); }
.actions { margin-top: 20px; display: flex; gap: 10px; justify-content: flex-end; }
.btn {
    padding: 6px 18px; border: none; border-radius: 6px;
    font-size: 12px; cursor: pointer; font-weight: 500;
}
.btn-primary { background: var(--accent); color: white; }
.btn-secondary { background: rgba(255,255,255,0.08); color: var(--text); border: 1px solid var(--border); }
.saved-msg { color: var(--success); font-size: 12px; opacity: 0; transition: opacity 0.3s; align-self: center; }
.saved-msg.show { opacity: 1; }
</style>
</head>
<body>
<h1>🌡 TempMonitor Live Dashboard</h1>

<div class="tabs">
    <div class="tab active" onclick="switchTab('live')">Live Thermals</div>
    <div class="tab" onclick="switchTab('thresholds')">Settings & Alerts</div>
</div>

<div id="tab-live" class="panel active">
    <div class="sparkline-card">
        <div class="sparkline-header">
            <span>Real-time Thermal Trend</span>
            <span id="peak-temp" style="color: #60a5fa;">Peak: --°C</span>
        </div>
        <canvas id="sparklineCanvas"></canvas>
    </div>
    <div class="sensors-list" id="sensor-table"></div>
</div>

<div id="tab-thresholds" class="panel">
    <div class="field">
        <div><div class="field-label">Launch on Startup</div><div class="field-desc">Start TempMonitor automatically on system boot</div></div>
        <label class="switch"><input type="checkbox" id="autostart" onchange="toggleAutostart(this.checked)"><span class="slider"></span></label>
    </div>
    <div class="field">
        <div><div class="field-label">Adaptive Power Efficiency</div><div class="field-desc">Scale sensor query frequency dynamically with load, thermal slope & battery state</div></div>
        <label class="switch"><input type="checkbox" id="adaptive_polling"><span class="slider"></span></label>
    </div>
    <div class="field">
        <div><div class="field-label">Warning temperature (°C)</div><div class="field-desc">Show warning toast above this temp</div></div>
        <input type="number" id="warning_temp" min="40" max="100">
    </div>
    <div class="field">
        <div><div class="field-label">Critical temperature (°C)</div><div class="field-desc">Show critical alert above this temp</div></div>
        <input type="number" id="critical_temp" min="50" max="110">
    </div>
    <div class="field">
        <div><div class="field-label">Poll interval (seconds)</div><div class="field-desc">Sensor query frequency</div></div>
        <input type="number" id="poll_interval_sec" min="1" max="30">
    </div>
    <div class="field">
        <div><div class="field-label">Alert cooldown (seconds)</div><div class="field-desc">Minimum delay between notifications</div></div>
        <input type="number" id="alert_cooldown_sec" min="10" max="600">
    </div>
</div>

<div class="actions">
    <span class="saved-msg" id="saved-msg">✓ Saved</span>
    <button class="btn btn-secondary" onclick="pywebview.api.get_settings().then(load)">Reset</button>
    <button class="btn btn-primary" onclick="saveAll()">Save</button>
</div>

<script>
function switchTab(name) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    event.target.classList.add('active');
    document.getElementById('tab-' + name).classList.add('active');
}

function load(s) {
    ['warning_temp','critical_temp','poll_interval_sec','alert_cooldown_sec'].forEach(f => {
        const el = document.getElementById(f);
        if (el && s[f] !== undefined) el.value = s[f];
    });
    const adaptEl = document.getElementById('adaptive_polling');
    if (adaptEl && s.adaptive_polling !== undefined) {
        adaptEl.checked = Boolean(s.adaptive_polling);
    }
}

function drawSparkline(historyMap) {
    const canvas = document.getElementById('sparklineCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    let maxVal = 0;
    const keys = Object.keys(historyMap);
    if (keys.length === 0) return;

    // Pick first or hottest history
    const pts = historyMap[keys[0]] || [];
    if (pts.length < 2) return;

    pts.forEach(p => { if (p > maxVal) maxVal = p; });
    document.getElementById('peak-temp').textContent = `Peak: ${maxVal.toFixed(0)}°C`;

    ctx.beginPath();
    ctx.strokeStyle = maxVal >= 80 ? '#ef4444' : (maxVal >= 70 ? '#f59e0b' : '#3b82f6');
    ctx.lineWidth = 2;

    const step = canvas.width / (pts.length - 1);
    const minScale = 30;
    const maxScale = 100;

    pts.forEach((p, i) => {
        const x = i * step;
        const normalized = (p - minScale) / (maxScale - minScale);
        const y = canvas.height - (normalized * (canvas.height - 10)) - 5;
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    });
    ctx.stroke();
}

async function updateLive() {
    const data = await pywebview.api.get_live_data();
    drawSparkline(data.history);

    const container = document.getElementById('sensor-table');
    container.innerHTML = Object.entries(data.temps).map(([name, val]) => {
        const col = val >= 85 ? '#ef4444' : (val >= 75 ? '#f59e0b' : '#10b981');
        return `<div class="sensor-row">
            <span>${name}</span>
            <span class="sensor-val" style="color: ${col}">${val.toFixed(1)}°C</span>
        </div>`;
    }).join('');
}

async function saveAll() {
    const adaptEl = document.getElementById('adaptive_polling');
    await pywebview.api.save_settings({
        warning_temp: parseInt(document.getElementById('warning_temp').value),
        critical_temp: parseInt(document.getElementById('critical_temp').value),
        poll_interval_sec: parseInt(document.getElementById('poll_interval_sec').value),
        alert_cooldown_sec: parseInt(document.getElementById('alert_cooldown_sec').value),
        adaptive_polling: adaptEl ? adaptEl.checked : true,
    });
    const msg = document.getElementById('saved-msg');
    msg.classList.add('show');
    setTimeout(() => msg.classList.remove('show'), 2000);
}

async function toggleAutostart(enabled) {
    await pywebview.api.set_autostart(enabled);
}

window.addEventListener('pywebviewready', async () => {
    const s = await pywebview.api.get_settings();
    load(s);
    try {
        const autostart = await pywebview.api.get_autostart_status();
        const autoEl = document.getElementById('autostart');
        if (autoEl) autoEl.checked = autostart;
    } catch (e) {
        console.error("Failed to query autostart status:", e);
    }
    updateLive();
    setInterval(updateLive, 2500);
});
</script>
</body>
</html>
"""


def _run_gui_standalone():
    """Run TempMonitor settings GUI on main thread."""
    from common.settings import load_settings
    current_settings = load_settings(_SETTINGS_PATH, {})
    from TempMonitor.temp_monitor import _read_temps
    live_temps = _read_temps()
    history = {k: [v] for k, v in live_temps.items()}
    api = SettingsAPI(current_settings, live_temps, history)

    webview.create_window(
        "TempMonitor Settings & Thermals", html=_build_html(), js_api=api,
        width=520, height=540, resizable=True,
    )
    gui_engine = 'qt' if sys.platform != "win32" else None
    webview.start(gui=gui_engine)


def open_settings(_settings=None, _all_temps=None, _temp_history=None, _on_save=None):
    """Open TempMonitor settings in a dedicated subprocess."""
    import subprocess
    subprocess.Popen([sys.executable, "-B", os.path.abspath(__file__)])


if __name__ == "__main__":
    _run_gui_standalone()

