# 🚀 AeroHub: The Ultimate Windows Automation & Wellness Suite

![AeroHub Banner](https://img.shields.io/badge/AeroHub-Windows%20Automation-cyan?style=for-the-badge)
![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![PowerShell](https://img.shields.io/badge/PowerShell-Automated-19366B?style=for-the-badge&logo=powershell)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

Welcome to the **AeroHub** repository! 

AeroHub is not just a collection of scripts—it is a highly modular, lightweight, and unified suite of Windows desktop tools, background daemons, and productivity toggles. Designed with performance, stability, and seamless UI/UX in mind, everything is flawlessly orchestrated through a central headless System Tray Hub.

---

## 🌟 Core Architecture & Modules

AeroHub is organized as a unified, flat suite of Windows desktop tools, background daemons, and productivity toggles.

### 🧠 1. The Core Orchestrator (`/aerohub`)
The nerve center of the entire suite. A lightweight orchestrator that runs in the background.
- **Floating Dashboard & Tray:** Access and monitor the status of all your toggles, settings, and services from a sleek floating widget or a custom tray icon.
- **AeroEco Game Mode:** Native Win32 game and fullscreen detection that optimizes resources:
  - Pauses the **Temperature Monitor** completely when playing or in fullscreen.
  - Automatically restricts the **Health App** process priority to IDLE, disabling heavy UI/audio calls and auto-postponing breaks during gameplay.
- **Lifecycle Manager:** Automatically detects process crashes and restarts them.

### ⚙️ 2. Background Services
Persistent, low-overhead daemons that dramatically improve your daily desktop experience.
- 📋 **Clipboard Manager (`/clipboard_manager`):** 
  - A robust clipboard manager.
  - Unlimited history with SQLite database persistence.
  - Dynamic GUI built with `CustomTkinter` that adapts to Windows Light/Dark mode.
- 👁️ **Health App (`/health_app`):** 
  - Your premium desktop wellness companion (SafeEyes eye break reminder).
  - **Late-Night Dimming:** Gradually reduces screen brightness during late hours.
  - **Dynamic Display Temperatures:** Weather API integration dynamically adjusts your screen's color temperature (Kelvin).
  - **8D Audio Breathing Guidance:** Spatial audio breathing prompts.
- 🤖 **Telegram FDM Proxy (`/tg_fdm_proxy`):** 
  - Bridges your Telegram messages and download requests directly to Free Download Manager (FDM).
- 🎵 **Media Control (`/media_control`):** 
  - System-wide media orchestration running in the taskbar.

### ⚡ 3. Quick Toggles & Monitors
Frictionless, instant-execution scripts designed to give you direct hardware control.
- 🔊 **Taskbar Scroll Controller (`Taskbar Scroll Controller.exe`):** A scroll-wheel friendly volume manager.
- 🖱️ **Touchpad Toggle (`/touch_toggle`):** Instantly enables or disables your laptop's trackpad with a custom status tooltip popup.
- 🌡️ **Temperature Monitor (`/temp_monitor`):** Keeps track of system thermals.
- 🔋 **Battery Monitor (`/battery_monitor`):** Refined power-state monitoring mimicking macOS charging notifications.

---

## 🛠️ Installation & Setup

We have provided automated scripts to set up the environment and configure silent startup.

### **Prerequisites**
- **Python 3.10+** (Ensure it is added to your System PATH)
- **Windows 10 / Windows 11**

### **Installation Guide**
1. Install Python dependencies and initialize folders by running:
   ```cmd
   install.bat
   ```
2. Launch the orchestrator dashboard:
   ```cmd
   run_aerohub.bat
   ```
3. To configure AeroHub to start automatically and silently as Administrator on system logon (bypassing UAC prompts):
   - Right-click `install_elevated_startup.bat` and select **"Run as administrator"**.

---

## 🎨 Design Philosophy & UX

AeroHub strictly adheres to modern premium UI/UX guidelines:

- **Frictionless UI:** No sudden layout shifts. Hover states exist for all interactive elements. Click targets are generously padded.
- **Context-Aware Theming:** Fully supports Windows 11 dynamic Light and Dark modes seamlessly across all GUI elements.
- **Non-Intrusive by Default:** Background services are built to be entirely headless. They do not spawn annoying command prompt windows or steal focus unless explicitly requested by the user.
- **Terminal Aesthetics:** Even our setup scripts use specific ANSI Foreground Colors (Cyan for primary steps, Green for success, Red for errors) for optimal terminal readability.

---

Enjoy your ultimate Windows workspace! 🎉
