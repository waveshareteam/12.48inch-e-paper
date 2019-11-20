#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)


import epd12in48
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

from PIL import Image

import json

print("12.48inch e-paper Demo...")

epd = epd12in48.EPD()
try:
    epd.Init()
    print("clearing...")
    epd.clear()

    image1 = Image.new("1", (epd12in48.EPD_WIDTH, epd12in48.EPD_HEIGHT), 255)
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype(picdir+"/Font.ttc", 300)
    font10 = ImageFont.truetype(picdir+"/Font.ttc",60)

    print("drawing...")
    draw.rectangle([(40,40),(440,440)],fill = "BLUE")
    draw.rectangle([(43,43),(437,437)],fill = "WHITE")
    draw.line([(40,40),(440,440)], fill = "BLUE",width = 3)
    draw.line([(440,40),(40,440)], fill = "BLUE",width = 3)
    draw.arc([50, 50, 430, 430], 0, 360, fill = "BLUE")
    draw.text((60,500), u'微雪电子 ', font = font, fill = "BLUE")
    draw.text((600, 90), 'Waveshare Electronic ', font = font10, fill = "BLUE")
    draw.text((600, 170), '12.48 inch e-paper ', font = font10, fill = "BLUE")
    draw.text((600, 250), 'Test Program ', font = font10, fill = "BLUE")

    image1=image1.rotate(0) 
    epd.display(image1)
    time.sleep(2)

    print("open pic...")
    image = Image.open(picdir+"/1304x984.jpg")	
    epd.display(image)
    time.sleep(2)

    print("clearing...")
    epd.clear()

    print("goto sleep...")
    epd.EPD_Sleep()
except:
    print("goto sleep...")
    epd.EPD_Sleep()


