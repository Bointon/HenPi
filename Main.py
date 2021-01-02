"""
This will show some Linux Statistics on the attached display. Be sure to adjust
to the display you have connected. Be sure to check the learn guides for more
usage information.

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!
"""

import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ili9341 as ili9341

#Initialise the LCD screen
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

BAUDRATE = 24000000

spi = board.SPI()

disp = ili9341.ILI9341(
    spi,
    rotation=90,  # 2.2", 2.4", 2.8", 3.2" ILI9341
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height

image = Image.new("RGB", (width, height))


#Standard runtime
def runTime():
    
    #Standard runtime initialisation
    splashFlag = True
    splashTimer = 5
    splashTimerCnt = 0
    menuFlag = False
    mainScreenFlag = False

    while True:
    
        if splashFlag == True:
            #The splash screen 
            splashScreen()
            if splashTimer < splashTimerCnt:
                splashFlag = False
                mainScreenFlag = True
            splashTimerCnt += 1
            print("Splash")
        if menuFlag == True:
            #The menu screen
            menuFlag = False
        if mainScreenFlag == True:
            #The main display
            mainScreen()
            print("Main")
        #cycle timer
        time.sleep(1)

#Splash screen logo
def splashScreen():
    
    image = Image.open("logo.png")

    # Crop and center the image
    x = (disp.width - image.width) // 2
    y = (disp.height - image.height) // 2
    image = image.crop((x, y, x + image.width, y + image.height))

    # Display image.
    disp.image(image)

#Main screen
def mainScreen():
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=(0, 0, 0))
    disp.image(image)
    #close program once the main has run once
    exit()
#Start the runtime
runTime()
