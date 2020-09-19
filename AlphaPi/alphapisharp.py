import time
import subprocess
import board
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont

import keyboard
import string
import curses


# 400x240 Sharp Memory Display
import adafruit_sharpmemorydisplay
spi = busio.SPI(board.SCK, MOSI=board.MOSI)
scs = digitalio.DigitalInOut(board.D6)
disp = adafruit_sharpmemorydisplay.SharpMemoryDisplay(spi, scs, 400, 240)
FONTSIZE = 40
font = ImageFont.truetype("usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)


# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height

# Splash screen (removed until get image with correct dimensions)
# image = Image.open(r'piskel.png')
# image = image.convert('1')
# disp.image(image)
# disp.show()
# time.sleep(3)

image = Image.new('1', (width, height))
 
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
 
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


#The version of the string that is saved to file
outputstring = ""
#The version of the string that is displayed
copy_of_output = ""
black = "black"
white = "white"
#FUNCTIONS

modifier = 0
every_21 = 0

location_x = 0

first_line = 17
second_line = 34
third_line = 51
fourth_line = 68
fifth_line = 85
sixth_line = 102


def main(stdscr):
    #stdscr.nodelay(True)
    print("Display output: " + copy_of_output + "\n")
    print("Saved output: " + outputstring + "\n")
    return stdscr.getch()

def fontchooser():
    return ("Nothing")

def linewriter(copy_of_output,string_adj_len):
  
    if string_adj_len <= first_line:
        draw.text((x, top+0), copy_of_output, font=font, fill=white)
    elif string_adj_len <= second_line:
        draw.text((x, top+0), copy_of_output[:first_line], font=font, fill=white)
        draw.text((x, top+40), copy_of_output[first_line:], font=font, fill=white)
    elif string_adj_len <= third_line:
        draw.text((x, top+0), copy_of_output[:first_line], font=font, fill=white)
        draw.text((x, top+40), copy_of_output[first_line:second_line], font=font, fill=white)
        draw.text((x, top+80), copy_of_output[second_line:], font=font, fill=white)
    # Changes distance from top to prevent last line from going off of screen
    elif string_adj_len <= fourth_line:
        draw.text((x, top+0), copy_of_output[:first_line], font=font, fill=white)
        draw.text((x, top+40), copy_of_output[first_line:second_line], font=font, fill=white)
        draw.text((x, top+80), copy_of_output[second_line:third_line], font=font, fill=white)
        draw.text((x, top+120), copy_of_output[third_line:], font=font, fill=white)

while True:
    # This is the section that logs keypresses for the whole running of the program...might need to move it to a separate section though if line_writer becomes its own "app"
    keypress = curses.wrapper(main)
    #print ("key:", keypress)
    if (keypress == curses.KEY_ENTER or keypress == 10 or keypress == 13):
        outputstring = outputstring + "\n"
        if len(copy_of_output) <= 21:
            modifier = 21 - len(copy_of_output)
        else:
            modifier = 21- (len(copy_of_output)%21)
        i = 0
        while i < modifier:
            copy_of_output = copy_of_output + " "
            print (i)
            i += 1
    elif (keypress <= 255):
        outputstring = outputstring + chr(keypress)
        copy_of_output = copy_of_output + chr(keypress)
    elif (keypress == 256 or keypress == curses.KEY_BACKSPACE):
        outputstring = outputstring[:-1]
        copy_of_output = copy_of_output[:-1]
        if ((len(copy_of_output)//20) - (len(copy_of_output) % 20)) == 1:
            copy_of_output = copy_of_output.rstrip()
    draw.rectangle((0,0,width,height),outline=0,fill=black)
    if (len(copy_of_output)>84):
        copy_of_output = copy_of_output[21:]
    linewriter(copy_of_output,len(copy_of_output))
    disp.image(image)
    disp.show()