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
from encoder import Encoder


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

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
image = Image.new("RGB", (disp.height, disp.width))
    

#Standard runtime
def runTime():
    
    #Standard runtime initialisation
    splashFlag = True
    splashTimer = 50
    TimerCnt = 0
    menuFlag = False
    mainScreenFlag = False
    connectionScreenFlag = False
    e1 = Encoder(18, 17, callback=valueChanged)
    print(e1)
    
    while True:
    
        if splashFlag == True:
            #The splash screen 
            splashScreen(TimerCnt)
            if splashTimer < TimerCnt:
                splashFlag = False
                mainScreenFlag = True
            TimerCnt += 1
            
        if menuFlag == True:
            #The menu screen
            menuFlag = False
            
        if mainScreenFlag == True:
            #The main display
            if (TimerCnt % 100) == 0:
                mainScreen()
            TimerCnt += 1
            
        #cycle timer
        if TimerCnt > 1000:
            TimerCnt = 0
            exit()

        #check inputs

        time.sleep(0.01)

#Splash screen logo
def splashScreen(splashTimerCnt):

    if splashTimerCnt == 0:
        #image should be in the 320x240 px format
        logo = Image.open("logo.png")
    
        # Display image
        disp.image(logo)


#Main screen
def mainScreen():
    #draw the backgorund of the main menu
    padding = 2
    connectedFlag = True

    titleText = "Material: Aluminium"
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, disp.height, disp.width), outline=0, fill=(255,255,255))
    draw.rectangle((0, 0, disp.height-1, 36), outline=(255,255,255), fill=(100,100,100))
    draw.text(((disp.height-font.getsize(titleText)[0])/2, 4), titleText , font=font, fill="#FFFFFF")

    if connectedFlag == True:
        draw.text((padding, 4+36), "Material:" , font=font, fill=0)
        draw.text((padding, 4+2*36), "Thickness:" , font=font, fill=0)
        draw.text((padding, 4+3*36), "Rate:" , font=font, fill=0)
        draw.text((padding, 4+4*36), "Xtal:" , font=font, fill=0)
        
    disp.image(image)


#encoder
def valueChanged(value):
    # Or do something useful with the value here!
    print("Hi")


#Start the runtime
runTime()
