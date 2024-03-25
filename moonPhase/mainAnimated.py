# Accurate Moon Phase display for Cosmic Unicorn!
# 2024 By Patrick Hennessey

# This version includes an animation feature! Press the A button to animate the moon phases
# and press again to stop the animation. Moon will return to its current phase afterwards.

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
import machine
from secrets import WIFI_SSID, WIFI_PASSWORD
from cosmic import CosmicUnicorn
from picographics import PicoGraphics, DISPLAY_COSMIC_UNICORN as DISPLAY
from pngdec import PNG

cu = CosmicUnicorn()
cu.set_brightness(1) # 1 = max brightness, can be set to any value between 0 and 1
display = PicoGraphics(DISPLAY)
png = PNG(display)

imgCount = 32 # should match moon image file count
ANIMATE = False # launch without animation
CHECK_TIME = True # launch with a time-check requirement

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

try:
    ntptime.settime()
    startTime = time.time()
except OSError:
    machine.reset()
    
def calc_phase():
    return round( ((time.time() - 583084) / 2551443) % 1 * imgCount ) % imgCount

def draw_moon(n):
    png.open_file(f'img/{n}.png')
    png.decode()

def change_mode(pin):
    global ANIMATE
    ANIMATE = not ANIMATE
    
# Using the IRQ method to detect button presses 
# to prevent multiple firings if the button is held.
mode_button = machine.Pin(cu.SWITCH_A, machine.Pin.IN, machine.Pin.PULL_UP)
mode_button.irq(trigger=machine.Pin.IRQ_FALLING, handler=change_mode)


while True:
    
    if (time.time() - startTime) % 1200 == 0 and not ANIMATE: # Updates every 20 minutes
        if CHECK_TIME:
            n = currentPhase = calc_phase()
            CHECK_TIME = not CHECK_TIME
    else:
        CHECK_TIME = True
        
    if ANIMATE:
        draw_moon(n)
        n += 1
        if n == imgCount: n = 0
    else:
        if n != currentPhase:
            draw_moon(n)
            n += 1
            if n == imgCount: n = 0
        else:
            draw_moon(currentPhase)
            
    cu.update(display)            
    time.sleep(0.02) # Set this value to higher or lower depending on your desired animation speed
