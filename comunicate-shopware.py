# -*- coding: utf-8 -*-

import time
import json
from shopware import Shopware

import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# Raspberry Pi pin configuration:
RST = 24
BTN = 4

# Note you can change the I2C address by passing an i2c_address parameter like:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)
GPIO.setup(BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height

run = True
clicked = False
doubleClicked = False

padding = 3
top = padding

# Load default font.
font = ImageFont.load_default()
font20 = ImageFont.truetype('Minecraftia.ttf', size=15)

# Move left to right keeping track of the current x position for drawing shapes.
x = 18

image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

starttime = 0


def callback(channel):
    global run, clicked, doubleClicked, starttime, disp

    print('!!! ------------- Click')

    run = False

    clearScreen()
    disp.image(image)
    disp.display()

    if clicked:
        doubleClicked = True
        clicked = False
        time.sleep(0.5)
        return

    clicked = True

    print('!!! -------- set starttime')
    starttime = time.time()
    time.sleep(0.5)


def clearScreen():
    global draw, width, height

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)


def runDisplay():
    global run, clicked, doubleClicked, starttime, buttoncode, width, api

    start()

    productData = api.getProduct()
    floatingText = u'' + productData['title']

    maxwidth, unused = draw.textsize(floatingText, font=font20)
    velocity = -2
    startpos = width
    pos = startpos

    while True:
        print('Clicked - doubleClick - run')
        print(clicked, doubleClicked, run)

        if clicked:
            print('Clicked - ones')
            if starttime == 0:
                time.sleep(0.5)
            print('Time Diff ', time.time() - starttime)
            if (time.time() - 30) < starttime:
                print('Clicked - show Screen')
                get_product()
            else:
                print('Clicked - timeout')
                resetVars()
        elif doubleClicked:
            print('Clicked - Twice')
            time.sleep(0.5)
            trigger_click()
            time.sleep(0.5)
            resetVars()
        else:
            while run:
                # Clear image buffer by drawing a black filled box.
                clearScreen()
                draw.text((x, top), ' - Dash Button - ', font=font, fill=255)
                # Enumerate characters and draw them offset vertically based on a sine wave.
                runText(floatingText, pos, top + 20, width)
                pos += velocity
                # Start over if text has scrolled completely off left side of screen.
                if pos < -maxwidth:
                    pos = startpos


def runText(floatingText, left, ytop, width):
    for i, c in enumerate(floatingText):
        # Stop drawing if off the right side of screen.
        if left > width:
            break
        # Calculate width but skip drawing if off the left side of screen.
        if left < -10:
            char_width, char_height = draw.textsize(c, font=font20)
            left += char_width
            continue
        # Draw text.
        draw.text((left, ytop), c, font=font20, fill=255)
        # Increment x position based on chacacter width.
        char_width, char_height = draw.textsize(c, font=font20)
        left += char_width
    # Draw the image buffer.
    disp.image(image)
    disp.display()


def resetVars():
    global clicked, doubleClicked, run, starttime
    clicked = doubleClicked = False
    run = True
    starttime = 0


def start():
    global draw, disp, image

    clearScreen()
    # Write two lines of text.
    draw.text((x, top), ' - Dash Button - ', font=font, fill=255)
    draw.text((x, top + 20), 'Willkommen!', font=font20, fill=255)
    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(2)


def get_product():
    global draw, disp, image, api

    # Write two lines of text.
    draw.text((0, top), 'Zahlungspflichting', font=font, fill=255)
    draw.text((60, top + 11), 'bestellen?', font=font, fill=255)
    draw.text((0, top + 22), u' - Erneut drücken! - ', font=font, fill=255)

    productdata = api.getProduct()
    productPrice = u'Preis: ' + str(productdata['price']) + u' \u20ac'

    draw.text((5, top + 40), productPrice, font=font20, fill=255)
    # Display image.
    disp.image(image)
    disp.display()

    time.sleep(2)
    clearScreen()


def trigger_click():
    global draw, disp, image, api

    headpadding = x-2
    textpadding = 12

    # Write two lines of text.
    draw.text((headpadding, top), ' - Bitte warten - ', font=font, fill=255)
    draw.text((textpadding, top + 20), '...Sending...', font=font20, fill=255)
    # Display image.
    disp.image(image)
    disp.display()

    result = api.triggerClick()

    clearScreen()
    disp.image(image)
    disp.display()

    draw.text((headpadding, top), ' - Bitte warten - ', font=font, fill=255)
    if result:
        draw.text((textpadding, top + 20), 'Erfolg!', font=font20, fill=255)
    else:
        draw.text((textpadding, top + 20), 'Fehler!', font=font20, fill=255)

    disp.image(image)
    disp.display()

    time.sleep(2)
    clearScreen()


def init():
    global url, buttoncode, api

    configfile = open('config.json', 'r')
    config = json.load(configfile)

    url = config['url']
    buttoncode = config['buttoncode']

    api = Shopware(url, buttoncode)

    GPIO.add_event_detect(BTN, GPIO.FALLING, callback=callback, bouncetime=1000)
    runDisplay()


def cleanup():
    GPIO.cleanup()  # clean up GPIO on CTRL+C exit

    clearScreen()
    disp.image(image)
    disp.display()


try:
    init()
except KeyboardInterrupt:
    cleanup()

cleanup()  # clean up GPIO on normal exit
