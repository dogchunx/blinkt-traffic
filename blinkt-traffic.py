import time
import json
import requests
import blinkt

from sys import exit

ORIGIN_ADDRESS = "" # start destination
DESTINATION_ADDRESS = "" # end destination
API_KEY = "" # Google API Key
UNITS = "imperial" # metric or imperial
BRIGHTNESS = 0.1 # a value between 0.1 and 1.0 (10 is BRIGHT!)
LONG_DURATION = 2400 # in seconds, the value for a "long" drive to your destination
MEDIUM_DURATION = 1800 # in seconds, the value for a "medium" drive to your destination

blinkt.set_clear_on_exit() # make sure Blinkt! is cleared when exiting the app

def lights(red, green, blue):
    blinkt.set_all(red, green, blue, BRIGHTNESS)
    blinkt.show()

def trafficCheck():
    req = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?units=%s&origins=%s&destinations=%s&travel_mode=driving&key=%s&departure_time=now" % (UNITS, ORIGIN_ADDRESS, DESTINATION_ADDRESS, API_KEY), timeout=2)
    data = json.loads(req.text)
    durationValue = data["rows"][0]["elements"][0]["duration_in_traffic"]["value"]
    
    if durationValue >= LONG_DURATION: # red light
        lights(255, 0, 0)
    elif durationValue >= MEDIUM_DURATION: # orange light
        lights(255, 165, 0)
    else:
        lights(0, 255, 0) # green light

try:
    while True:
        trafficCheck()
        time.sleep(30) # run every 30 seconds
except KeyboardInterrupt:
    print(" exiting...")

