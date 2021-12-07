import RPi.GPIO as GPIO
import time
import hashlib
from urllib.request import urlopen, Request

GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN)
GPIO.setup(21, GPIO.OUT)

# flashing lights that will be seen when the program is being ended
def flash_reset():
    for x in range(5):
        GPIO.output(21, GPIO.HIGH)
        time.sleep(.5)
        GPIO.output(21, GPIO.LOW)
        time.sleep(.5)

# website url that will be monitored
# url = Request('https://sdsucirclek.org/',headers={'User-Agent': 'Mozilla/5.0'})
url = Request('https://leetcode.com/',headers={'User-Agent': 'Mozilla/5.0'})
response = urlopen(url).read()
# hash the webpage to take in the initial information
prevHash = hashlib.sha224(response).hexdigest()
print("running")

# intial variables
count = 0

while count < 10:
    response = urlopen(url).read()
    currentHash = hashlib.sha224(response).hexdigest()
    if currentHash != prevHash:
        changed = True
        print("Site has been updated...")
    else:
        changed = False
    prevHash = currentHash
    
    if changed:
        GPIO.output(21, GPIO.HIGH)
        changed = False
        
    if GPIO.input(20):
        GPIO.output(21, GPIO.LOW)
        count += 1
    else:
        count = 0
    time.sleep(.1)
    print(count)
flash_reset()
GPIO.cleanup()
