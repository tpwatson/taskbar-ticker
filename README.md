# Taskbar Ticker

[![GitHub Repo stars](https://img.shields.io/github/stars/tpwatson/taskbar-ticker?style=social)](https://github.com/tpwatson/taskbar-ticker/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/tpwatson/taskbar-ticker?style=social)](https://github.com/tpwatson/taskbar-ticker/network/members)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

A lightweight, customizable system tray ticker that displays real-time crypto prices right on your Windows taskbar. 🚀 Perfect for staying glued to your favorite token's ATH during hype threads on X—without switching apps or refreshing browsers!

Inspired by viral taskbar gadgets like RunCat365, this tool pulls prices from CoinGecko's API, auto-updates every 10 minutes, and lets you refresh on demand or tweak settings via a simple menu. Whether you're tracking BTC, ETH, or the next moonshot, it's your discreet desktop companion for crypto enthusiasm.

## Demo

![Taskbar Ticker in Action](docs/demo.gif)  
*(GIF showing the tray icon updating with a crypto price, right-click menu for refresh/settings/quit, and a dialog for changing the coin ID/symbol.)*

## Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Building the Executable](#building-the-executable)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)

## About the Project

In the fast-paced world of crypto, prices can skyrocket (or dip) in minutes—especially during those viral X threads where everyone's buzzing about a token's breakout. Taskbar Ticker solves the hassle of constant tab-switching by putting live USD prices directly in your system tray.

Why this tool?
- **Simple & Fun**: Like a running cat but for crypto prices—minimalist, non-intrusive, and oddly satisfying.
- **Customizable**: Switch coins on the fly (e.g., from Bitcoin to XRP) without restarting.
- **Open-Source**: Fork it, extend it for alerts or multi-coins, and share with your community.
- **Viral-Ready**: Post it in #CryptoTwitter threads: "Tracking $TOKEN's ATH? Here's a free taskbar ticker I built! ⭐"

This project started as a quick hack for XRP enthusiasts but evolved into a general crypto ticker. It's lightweight (<100 lines of core code) and easy to run or package.

## Features

- 📈 **Live Price Updates**: Fetches from CoinGecko API every 10 minutes (or manually refresh with a click).
- ⚡ **On-Demand Refresh**: Right-click > Refresh, with a 1-minute cooldown to avoid API abuse.
- ⚙️ **Easy Settings**: Right-click > Settings to change the CoinGecko ID (e.g., "ripple" for XRP) and symbol via simple dialogs.
- 💾 **Persistent Config**: Saves your preferences to a `config.json` file.
- 🖥️ **System Tray Integration**: Works seamlessly on Windows (with notes for macOS/Linux compatibility).
- 🔒 **Rate-Limited**: Respects API limits for reliable performance.
- 📦 **Portable Executable**: Download a one-click .exe for non-devs—no Python needed!

## Built With

- [Python](https://www.python.org/) - Core language.
- [pystray](https://github.com/moses-palmer/pystray) - For system tray icons.
- [requests](https://requests.readthedocs.io/) - API calls to CoinGecko.
- [Pillow](https://pillow.readthedocs.io/) - Dynamic icon generation.
- [tkinter](https://docs.python.org/3/library/tkinter.html) - Simple dialogs for settings.

## Getting Started

Follow these steps to get Taskbar Ticker running locally.

### Prerequisites

- Python 3.8 or higher (download from [python.org](https://www.python.org/downloads/)).
- Windows OS (primary support; macOS/Linux may require tweaks for tray behavior).

### Installation

1. Clone the repo:
   ```
   git clone https://github.com/tpwatson/taskbar-ticker.git
   cd taskbar-ticker
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
   *(requirements.txt: requests, pystray, pillow)*

For a pre-built executable (no Python needed):
- Download the latest .exe from [Releases](https://github.com/tpwatson/taskbar-ticker/releases).

## Usage

Run the script:
```
python main.py
```
- The icon appears in your taskbar with the default (BTC) price.
- Right-click the icon for menu: Refresh, Settings, Quit.
- In Settings: Enter a new CoinGecko coin ID (e.g., "ethereum") and symbol (e.g., "ETH").

Example: Tracking XRP during an ATH hype thread? Set coin_id to "ripple" and symbol to "XRP"—boom, instant updates!

## Configuration

Preferences are stored in `config.json` (created on first settings change). Example:
```json
{
  "coin_id": "bitcoin",
  "symbol": "BTC",
  "vs_currency": "usd"
}
```
Edit manually or via the in-app dialog. Future updates could add more options like currency or multi-coin cycling.

## Building the Executable

Want to distribute a standalone .exe?
1. Install PyInstaller: `pip install pyinstaller`.
2. Run: `pyinstaller --onefile --windowed main.py`.
3. Find `dist/main.exe`—share it with friends!

(Note: For signed executables to avoid Windows warnings, get a code signing cert from a CA like DigiCert.)

## Contributing

Contributions make the open-source community awesome! 🌟

1. Fork the Project.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

See `CONTRIBUTING.md` for details. Ideas: Add price alerts, multi-coin support, or theme colors for up/down trends.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Terence Watson - [@BuildItTerence](https://x.com/BuildItTerence)

Project Link: [https://github.com/tpwatson/taskbar-ticker](https://github.com/tpwatson/taskbar-ticker)

## Acknowledgments

- Inspired by [RunCat365](https://github.com/Kyome22/RunCat365) for fun taskbar vibes.
- Powered by [CoinGecko API](https://www.coingecko.com/en/api) (free & reliable!).
- Template based on best practices from [othneildrew/Best-README-Template](https://github.com/othneildrew/Best-README-Template).
- Shoutout to the #CryptoCommunity on X for the motivation!

*Back to top* ⬆️