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

#Standard runtime
def runTime():
    
    #Standard runtime initialisation
    splashFlag = True
    splashTimer = 50
    splashTimerCnt = 0
    menuFlag = False
    mainScreenFlag = False
    connectionScreenFlag = False

    while True:
    
        if splashFlag == True:
            #The splash screen 
            splashScreen()
            if splashTimer < splashTimerCnt:
                splashFlag = False
                mainScreenFlag = True
            splashTimerCnt += 1

            
        if menuFlag == True:
            #The menu screen
            menuFlag = False
            
        if mainScreenFlag == True:
            #The main display
            mainScreen()
            if splashTimer*2 < splashTimerCnt:
                exit()
            splashTimerCnt += 1
            
        #cycle timer
        
        time.sleep(0.1)

#Splash screen logo
def splashScreen():

    #image should be in the 320x240 px format
    image = Image.open("logo.png")
    
    # Display image
    disp.image(image)


#Main screen
def mainScreen():

    image = Image.new("RGB", (disp.height, disp.width))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, disp.height, disp.width), outline=0, fill=(255,255,255))
    draw.rectangle((0, 0, disp.width, 20), outline=0, fill=0)
    disp.image(image)


#Start the runtime
runTime()
