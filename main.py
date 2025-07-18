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

def get_coin_data(coin_id, vs_currency):
    try:
        # Get both price and coin details including image
        price_response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={vs_currency}")
        price = price_response.json()[coin_id][vs_currency]
        
        # Get coin details for image
        details_response = requests.get(f"https://api.coingecko.com/api/v3/coins/{coin_id}")
        details = details_response.json()
        image_url = details['image']['large']  # Get the large image URL
        
        return price, image_url
    except:
        return "Error", None

def download_coin_image(image_url):
    """Download and process coin logo image"""
    try:
        import io
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Open the downloaded image
        coin_image = Image.open(io.BytesIO(response.content))
        
        # Convert to RGBA if needed
        if coin_image.mode != 'RGBA':
            coin_image = coin_image.convert('RGBA')
        
        # Resize to fit nicely in taskbar (slightly smaller for padding)
        coin_image = coin_image.resize((56, 56), Image.Resampling.LANCZOS)
        
        # Create a 64x64 transparent canvas
        icon_image = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))
        
        # Center the coin image on the canvas
        icon_image.paste(coin_image, (4, 4), coin_image)
        
        return icon_image
    except:
        return None

def create_icon(symbol, image_url=None):
    """Create icon using coin logo or fallback to text"""
    
    # Try to use the coin's actual logo first
    if image_url:
        coin_icon = download_coin_image(image_url)
        if coin_icon:
            return coin_icon
    
    # Fallback to text-based icon if image fails
    image = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))  # Transparent background
    draw = ImageDraw.Draw(image)
    
    # Try to use the largest possible font for the symbol
    try:
        from PIL import ImageFont
        # Start with a large font and find the biggest that fits
        font_size = 32  # Start bigger
        font = ImageFont.truetype("arial.ttf", font_size)
        
        # Check if text fits, if not reduce font size
        bbox = draw.textbbox((0, 0), symbol, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Reduce font size if text is too big for the icon
        while (text_width > 58 or text_height > 58) and font_size > 12:
            font_size -= 2
            font = ImageFont.truetype("arial.ttf", font_size)
            bbox = draw.textbbox((0, 0), symbol, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
    except:
        # Fallback to default font if system font not available
        try:
            font = ImageFont.load_default()
            bbox = draw.textbbox((0, 0), symbol, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except:
            font = None
            text_width = len(symbol) * 8  # Rough estimate
            text_height = 12
    
    # Calculate position to center the text
    x = (64 - text_width) // 2
    y = (64 - text_height) // 2
    
    # Draw the symbol centered with high contrast
    draw.text((x, y), symbol, fill=(255, 255, 255, 255), font=font)  # Pure white for max contrast
    
    return image

def update_price(icon, force=False):
    global last_update_time
    current_time = time.time()
    # Only check rate limit if NOT forced
    if not force and (current_time - last_update_time < 60):
        return  # Skip if less than 1 minute since last update and not forced
    price, image_url = get_coin_data(config['coin_id'], config['vs_currency'])
    if price != "Error":
        last_update_time = current_time
    # Icon shows the coin logo (or symbol as fallback)
    icon.icon = create_icon(config['symbol'], image_url)
    # Tooltip shows just the price
    icon.title = f"${price}"

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

icon = pystray.Icon('taskbar_ticker', create_icon('...'), 'Loading...', menu)

# Start auto-update thread
threading.Thread(target=auto_update_loop, args=(icon,), daemon=True).start()

# Initial update
update_price(icon)

icon.run()