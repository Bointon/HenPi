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
stateFlag = False
checkEncoder = False
encoderValue = 0
oldencoderValue = 0
encoderButtonPressed = False


#Standard runtime
def runTime():
    
    #Standard runtime initialisation
    global state
    global stateFlag
    global encoderValue
    global oldencoderValue
    global TimerCnt
    global checkEncoder
    global encoderButtonPressed

    splashTimer = 500
    TimerCnt = 0

    #setup buttons encoder on pins 17,18, buttons are on 4 and 16
    e1 = Encoder(18, 17, callback=encoderChanged)
    GPIO.setup(4, GPIO.IN)  
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
    GPIO.add_event_detect(4, GPIO.FALLING, callback=encoderButton, bouncetime=300)  
    GPIO.add_event_detect(16, GPIO.FALLING, callback=clearButton, bouncetime=300)  

    #range for each menu
    rangeMenu = [[0,0],[0,0],[1,5]]


    while True:
        #The splash screen 
        if state == 0:
            splashScreen(TimerCnt)
            if splashTimer < TimerCnt:
                state = 1
            TimerCnt += 1
            
        #The main display
        if state == 1:
            if stateFlag == True:
                mainScreen()
                stateFlag = False
                
            if (TimerCnt % 100) == 0:
                mainScreen()
                
            TimerCnt += 1

        if state == 2:
            #The menu screen
            if stateFlag == True:
                oldencoderValue = encoderValue
                selector = rangeMenu[state][0]
                menuScreen(selector)
                stateFlag = False
                #list of the states for the menu selection
                menuOut = [3,4,5,6,7]

            #check if the encoder has changed and update the menu

            if encoderValue>oldencoderValue:
                selector  += 1
                if selector >= rangeMenu[state][1]:
                    selector = rangeMenu[state][1]
                oldencoderValue = encoderValue
                menuScreen(selector)
            if encoderValue < oldencoderValue:
                selector -= 1
                if selector <= rangeMenu[state][0]:
                    selector = rangeMenu[state][0]
                oldencoderValue = encoderValue
                menuScreen(selector)

            #if the encoder button is pressed move to the next menu
            if encoderButtonPressed:
                state = menuOut[selector - 1]
                encoderButtonPressed = False
                stateFlag = True
                
        #Materials menu 
        if state == 3:
            print("Materials menu")
            state = 2
            
        #Connection menu
        if state == 4:
            print("Connection menu")
            state = 2
            
        #Settings menu
        if state == 5:
            print("Settings menu")
            state = 2
            
        #The About menu
        if state == 6:
            print("About menu")
            if stateFlag:
                aboutScreen()
                
            if encoderButtonPressed:
                state = 2
                encoderButtonPressed = False
                stateFlag = True
            
            
        #Return to the main menu
        if state == 7:
            state = 1
            

                

                        
           
        #check encoder if it has been changed
        if checkEncoder == True:
            encoderValue = e1.value
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

#Menu screen
def menuScreen(menuSelect):
    #draw the backgorund of the main menu
    padding = 2
    
    titleText = "Menu"      
    
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, disp.height, disp.width), outline=0, fill=(255,255,255))
    draw.rectangle((0, 0, disp.height-1, 36), outline=(255,255,255), fill=(100,100,100))

    #draw selected menu cursor
    draw.rectangle((padding,menuSelect * 36 , disp.height-padding, (menuSelect+1)*36), outline=(0,0,0), fill=(255,255,255))  

    draw.text(((disp.height-font.getsize(titleText)[0])/2, 4), titleText , font=font, fill="#FFFFFF")

    textArray = ["Materials","Connection","Settings","About","Exit Menu"]
    for i in range(0,5):
        draw.text((2*padding, 4+(i+1)*36), textArray[i] , font=font, fill=0)

    disp.image(image)

#About screen
def aboutScreen():
    #draw the backgorund of the main menu
    padding = 2
    
    titleText = "About"      
    
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, disp.height, disp.width), outline=0, fill=(255,255,255))
    draw.rectangle((0, 0, disp.height-1, 36), outline=(255,255,255), fill=(100,100,100))

    draw.text(((disp.height-font.getsize(titleText)[0])/2, 4), titleText , font=font, fill="#FFFFFF")

    textArray = ["Henniker Scientific","HW Ver","SW Ver","Support"]
    for i in range(0,4):
        draw.text((2*padding, 4+(i+1)*36), textArray[i] , font=font, fill=0)

    disp.image(image)

#encoder changed
def encoderChanged(value):
    global checkEncoder
    checkEncoder = True

#encoder button
def encoderButton(value):
    global state
    global stateFlag
    global encoderButtonPressed
    
    #if on main screen and button is pressed enable menu
    if state == 1:
        state = 2
        stateFlag = True
   
    elif state > 1:
        encoderButtonPressed = True

#clear button
def clearButton(value):
    print("Clear button pressed")
    exit()

#Start the runtime
runTime()
