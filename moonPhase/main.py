# Accurate Moon Phase display for Cosmic Unicorn!
# 2024 By Patrick Hennessey

# Connects to your WiFi network to get Unix time in order to generate correct moon phase
# Formula adapted from post: https://community.facer.io/t/moon-phase-formula-updated/35691/8

# Formula starts at 0 and advances to 1, which is a full cycle
# 0 = new moon, 0.5 = full moon, etc.
# Image 0.png should be a new moon image, middle image should be a full moon, etc.

# Very acccurate moon images adapted from NASA's Scientific Visualization Studio
# https://svs.gsfc.nasa.gov/5187

# You'll need to create a "secrets.py" file with your wifi name and password, formatted as follows:

# WIFI_SSID = "WIFI NAME"
# WIFI_PASSWORD = "WIFI PASSWORD"

import time
import network
import ntptime
from secrets import WIFI_SSID, WIFI_PASSWORD
from cosmic import CosmicUnicorn
from picographics import PicoGraphics, DISPLAY_COSMIC_UNICORN as DISPLAY
from pngdec import PNG

cu = CosmicUnicorn()
cu.set_brightness(1) # 1 = max brightness, can be set to any value between 0 and 1
display = PicoGraphics(DISPLAY)
png = PNG(display)

imgCount = 32 # should match moon image file count

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

try:
    ntptime.settime()
except OSError:
    machine.reset()

def draw_moon():
    currentPhase = ((time.time() - 583084) / 2551443) % 1
    phaseImg = round(currentPhase * imgCount ) % imgCount
    png.open_file(f'img/{phaseImg}.png')
    png.decode()
    
while True:
    draw_moon()
    cu.update(display)
    time.sleep(1200) # Updates every 20 minutes
