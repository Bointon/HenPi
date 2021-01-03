"""
This will show some Linux Statistics on the attached display. Be sure to adjust
to the display you have connected. Be sure to check the learn guides for more
usage information.

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!
"""

#standard imports
import time
import subprocess
import digitalio
import board
import RPi.GPIO as GPIO 
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

#encoder setup

    
#flags
state = 0
stagFlag = False
checkEncoder = False
encoderValue = 0
oldencoderValue = 0

#Standard runtime
def runTime():
    
    #Standard runtime initialisation
    global state
    global stateFlag
    global encoderValue
    global oldencoderValue
    global TimerCnt
    global checkEncoder
    splashTimer = 500
    TimerCnt = 0

    #setup buttons encoder on pins 17,18, buttons are on 4 and 16
    e1 = Encoder(18, 17, callback=encoderChanged)
    GPIO.setup(4, GPIO.IN)  
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
    GPIO.add_event_detect(4, GPIO.FALLING, callback=encoderButton, bouncetime=300)  
    GPIO.add_event_detect(16, GPIO.FALLING, callback=clearButton, bouncetime=300)  

    #Encoder values for each state machine
    menuRange = [[0,0],[0,0],[0,4]]

    
    while True:
        #The splash screen 
        if state == 0:
            splashScreen(TimerCnt)
            if splashTimer < TimerCnt:
                state = 1
            TimerCnt += 1
            
        #The main display
        if state == 1:
            if (TimerCnt % 100) == 0:
                mainScreen()
            TimerCnt += 1

        if state == 2:
            #The menu screen
            if stateFlag == True:
                oldencoderValue = encoderValue
                stateFlag = False

            selector = oldencoderValue-encoderValue
            if selector < menuRange[state][0]:
                oldencoderValue = encoderValue
                selector = menuRange[state][0]
            elif selector > menuRange[state][1]:
                oldencoderValue = encoderValue
                selector = menuRange[state][1]

            if (TimerCnt % 100) == 0:
                 menuScreen()
                 print(oldencoderValue - encoderValue)
            TimerCnt += 1
           
        #check encoder if it has been changed
        if checkEncoder == True:
            encoderValue = e1.value
            print(encoderValue)
            checkEncoder = False

            
        #cycle timer
        if TimerCnt > 10000:
            TimerCnt = 0
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


    titleText = "Material: Aluminium"
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, disp.height, disp.width), outline=0, fill=(255,255,255))
    draw.rectangle((0, 0, disp.height-1, 36), outline=(255,255,255), fill=(100,100,100))
    draw.text(((disp.height-font.getsize(titleText)[0])/2, 4), titleText , font=font, fill="#FFFFFF")


    draw.text((padding, 4+36), "Material:" , font=font, fill=0)
    draw.text((padding, 4+2*36), "Thickness:" , font=font, fill=0)
    draw.text((padding, 4+3*36), "Rate:" , font=font, fill=0)
    draw.text((padding, 4+4*36), "Xtal:" , font=font, fill=0)
        
    disp.image(image)

#Main screen
def menuScreen(Selector):
    #draw the backgorund of the main menu
    padding = 2
    menuSelect = 2

    
    titleText = "Menu"      
    
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, disp.height, disp.width), outline=0, fill=(255,255,255))
    draw.rectangle((0, 0, disp.height-1, 36), outline=(255,255,255), fill=(100,100,100))

    #draw selected menu cursor
    draw.rectangle((padding,menuSelect * 36 , disp.height-padding, (menuSelect+1)*36), outline=(0,0,0), fill=(255,255,255))  

    draw.text(((disp.height-font.getsize(titleText)[0])/2, 4), titleText , font=font, fill="#FFFFFF")

    draw.text((2*padding, 4+36), "Materials" , font=font, fill=0)
    draw.text((2*padding, 4+2*36), "Connection" , font=font, fill=0)
    draw.text((2*padding, 4+3*36), "Settings" , font=font, fill=0)
    draw.text((2*padding, 4+4*36), "About" , font=font, fill=0)

    
    disp.image(image)


#encoder changed
def encoderChanged(value):
    global checkEncoder
    checkEncoder = True

#encoder button
def encoderButton(value):
    global state
    global stateFlag
    #if on main screen and button is pressed enable menu
    if state == 1:
        state = 2
        stateFlag = True
   
    elif state > 1:
        state = 1
        stateFlag = True

#clear button
def clearButton(value):
    print("Clear button pressed")
    exit()

#Start the runtime
runTime()
