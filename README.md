# 🚀 AeroHub: The Ultimate Windows Automation & Wellness Suite

![AeroHub Banner](https://img.shields.io/badge/AeroHub-Windows%20Automation-cyan?style=for-the-badge)
![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![PowerShell](https://img.shields.io/badge/PowerShell-Automated-19366B?style=for-the-badge&logo=powershell)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

Welcome to the **AeroHub** repository! 

AeroHub is not just a collection of scripts—it is a highly modular, lightweight, and unified suite of Windows desktop tools, background daemons, and productivity toggles. Designed with performance, stability, and seamless UI/UX in mind, everything is flawlessly orchestrated through a central headless System Tray Hub.

---

## 🌟 Core Architecture & Modules

AeroHub is strictly organized into distinct, sandboxed domains to keep the codebase clean, scalable, and maintainable.

### 🧠 1. The Hub (`/hub`)
The nerve center of the entire suite. A lightweight, headless orchestrator that runs completely silently in the background.
- **Unified System Tray:** Access all your toggles, settings, and services from a single Windows tray icon. Say goodbye to a cluttered taskbar.
- **UDP IPC Architecture:** Background daemons communicate with interactive UI components (like crash toasts, notifications, and dashboards) over a robust UDP-based Inter-Process Communication (IPC) system. This ensures the background process never hangs, even if the UI threads freeze.
- **Lifecycle Manager:** Automatically detects system crashes, monitors child processes, and automatically resurrects services that fail.

### ⚙️ 2. Background Services (`/services`)
Persistent, low-overhead daemons that dramatically improve your daily desktop experience.
- 📋 **Clipboard Manager:** 
  - A robust, cross-platform clipboard manager.
  - Unlimited history with ultra-fast SQLite persistence.
  - Dynamic GUI built with `CustomTkinter` that instantly adapts to Windows Light/Dark mode.
  - Graceful fallbacks for missing assets to prevent crashing (`PIL` Truncated Image support).
- 👁️ **SafeEyes for Windows:** 
  - Your premium desktop wellness companion.
  - **Late-Night Dimming:** Automatically and smoothly reduces screen brightness to 1-2% during late hours to protect your circadian rhythm.
  - **Dynamic Display Temperatures:** Analyzes real-time weather data to dynamically adjust your screen's Kelvin color temperature.
  - **Wellness Voiceovers:** Immersive 8D spatial audio prompts for guided breathing and posture correction.
- 🤖 **Telegram FDM Proxy (`tg_fdm_proxy`):** 
  - A seamless Telethon-based Telegram bot proxy.
  - Bridges your Telegram messages and download requests directly to Free Download Manager (FDM), automating bulk downloads effortlessly.
- 🎵 **Media Control:** 
  - System-wide media orchestration running seamlessly in your taskbar.

### ⚡ 3. Quick Toggles (`/toggles`)
Frictionless, instant-execution scripts designed to give you direct hardware control.
- 🔊 **Volume Control:** A scroll-wheel friendly volume manager with a dedicated system tray icon and visual popup.
- 🖱️ **Touchpad Toggle:** A robust `.vbs` and PowerShell wrapper that instantly enables or disables your laptop's trackpad without digging through Windows settings.

### 📊 4. System Monitoring (`/monitoring`)
Real-time hardware monitors that consume virtually zero CPU.
- 🌡️ **Temperature Monitor:** Keeps an eye on your system thermals to ensure safe operating conditions.
- 🔋 **MacChargerMonitor:** Beautiful, refined power-state monitoring that perfectly replicates the macOS charging notification visual style on your Windows desktop.

---

## 🛠️ Installation & Setup

We have created an elegant, interactive PowerShell setup script to fully automate your environment configuration. No manual dependency hunting required.

### **Prerequisites**
- **Python 3.10+** (Ensure it is added to your System PATH)
- **Windows 10 / Windows 11**
- **Git** (For downloading and updating)

### **1-Minute Setup Guide**
1. Clone this repository and open a PowerShell window.
2. Navigate to the repository root:
   ```powershell
   cd AeroHub
   ```
3. Run the automated setup script:
   ```powershell
   .\Setup.ps1
   ```
*(If you encounter an ExecutionPolicy error, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)*

### **What the Setup Script Does Automatically:**
- ✅ Validates your Python version and System PATH.
- ✅ Installs all dependencies via `requirements.txt` (`pystray`, `Pillow`, `aiohttp`, `customtkinter`, etc.) using a beautiful, color-coded CLI interface.
- ✅ Creates a silent shortcut and configures your Windows Startup folder to automatically launch `Run_Service_Hub.vbs` on boot.

---

## 🎨 Design Philosophy & UX

AeroHub strictly adheres to modern premium UI/UX guidelines:

- **Frictionless UI:** No sudden layout shifts. Hover states exist for all interactive elements. Click targets are generously padded.
- **Context-Aware Theming:** Fully supports Windows 11 dynamic Light and Dark modes seamlessly across all GUI elements.
- **Non-Intrusive by Default:** Background services are built to be entirely headless. They do not spawn annoying command prompt windows or steal focus unless explicitly requested by the user.
- **Terminal Aesthetics:** Even our setup scripts use specific ANSI Foreground Colors (Cyan for primary steps, Green for success, Red for errors) for optimal terminal readability.

---

Enjoy your ultimate Windows workspace! 🎉
