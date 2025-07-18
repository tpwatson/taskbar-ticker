import requests
import pystray
from PIL import Image, ImageDraw
import time
import threading
import json
import os
from tkinter import Tk, simpledialog

last_update_time = 0  # Global to track last successful update time

# Default config if no file
DEFAULT_CONFIG = {
    "coin_id": "bitcoin",
    "symbol": "BTC",
    "vs_currency": "usd"
}

# Load config from file if exists
config_file = 'config.json'
config = DEFAULT_CONFIG.copy()
if os.path.exists(config_file):
    try:
        with open(config_file, 'r') as f:
            config.update(json.load(f))
    except:
        pass  # Use default on error

def get_price(coin_id, vs_currency):
    try:
        response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={vs_currency}")
        return response.json()[coin_id][vs_currency]
    except:
        return "Error"

def create_icon(text):
    image = Image.new('RGB', (64, 64), color=(0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), text, fill=(255, 255, 255))
    return image

def update_price(icon, force=False):
    global last_update_time
    current_time = time.time()
    if force and (current_time - last_update_time < 60):
        return  # Skip if less than 1 minute since last update
    price = get_price(config['coin_id'], config['vs_currency'])
    if price != "Error":
        last_update_time = current_time
    display_text = f"{config['symbol']}: ${price}"
    icon.icon = create_icon(display_text)
    icon.title = f"{config['symbol']} Price: ${price}"

def auto_update_loop(icon):
    while True:
        update_price(icon)
        time.sleep(600)  # 10 minutes

def on_refresh(icon, item):
    update_price(icon, force=True)

def on_settings(icon, item):
    root = Tk()
    root.withdraw()  # Hide the main window
    new_coin_id = simpledialog.askstring("Settings", "Enter new CoinGecko coin ID (e.g., bitcoin):", initialvalue=config['coin_id'])
    if new_coin_id:
        config['coin_id'] = new_coin_id.strip().lower()  # Normalize
        new_symbol = simpledialog.askstring("Settings", "Enter new symbol (e.g., BTC):", initialvalue=config['symbol'])
        if new_symbol:
            config['symbol'] = new_symbol.strip().upper()  # Normalize
        # Save to file
        with open(config_file, 'w') as f:
            json.dump(config, f)
        # Update icon immediately
        update_price(icon, force=True)

def on_quit(icon, item):
    icon.stop()

# Create menu with Refresh, Settings, and Quit
menu = pystray.Menu(
    pystray.MenuItem('Refresh', on_refresh),
    pystray.MenuItem('Settings', on_settings),
    pystray.MenuItem('Quit', on_quit)
)

icon = pystray.Icon('taskbar_ticker', create_icon('Loading'), 'Crypto Ticker', menu)

# Start auto-update thread
threading.Thread(target=auto_update_loop, args=(icon,), daemon=True).start()

# Initial update
update_price(icon)

icon.run()