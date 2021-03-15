﻿#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
logging.basicConfig(level = logging.DEBUG)

import time
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
import epd12in48b

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

print("12.48inch e-paper B Demo...")
epd = epd12in48b.EPD()
try:
    epd.Init()
    print("clearing...")
    epd.clear()

    # Create blank image for drawing.
    Blackimage = Image.new("1", (epd12in48b.EPD_WIDTH, epd12in48b.EPD_HEIGHT), 255)
    Redimage = Image.new("1", (epd12in48b.EPD_WIDTH, epd12in48b.EPD_HEIGHT), 255)
    Blackdraw = ImageDraw.Draw(Blackimage)
    Reddraw = ImageDraw.Draw(Redimage)

    font = ImageFont.truetype(picdir+"/Font.ttc", 300)
    font10 = ImageFont.truetype(picdir+"/Font.ttc",60)

    print("drawing...")
    Blackdraw.rectangle([(40,40),(440,440)],fill = "Black",)
    Blackdraw.rectangle([(43,43),(437,437)],fill = "White")
    Blackdraw.line([(40,40),(440,440)], fill = "Black",width = 3)
    Blackdraw.line([(440,40),(40,440)], fill = "Black",width = 3)
    Reddraw.arc([50, 50, 430, 430], 0, 360, fill = "Black")
    Reddraw.text((60,500), u'微雪电子 ', font = font, fill = "Black")
    Reddraw.text((600, 90), 'Waveshare Electronic ', font = font10, fill = "Black")
    Reddraw.text((600, 170), '12.48 inch e-paper ', font = font10, fill = "Black")
    Reddraw.text((600, 250), 'Test Program ', font = font10, fill = "Black")

    Blackimage=Blackimage.rotate(180)
    Redimage=Redimage.rotate(180)
    epd.display(Blackimage, Redimage)
    time.sleep(2)

    print("open pic...")
    Blackimage2 = Image.new("1", (epd12in48b.EPD_WIDTH, epd12in48b.EPD_HEIGHT), 255)
    Redimage2 = Image.new("1", (epd12in48b.EPD_WIDTH, epd12in48b.EPD_HEIGHT), 255)
    Redimage2 = Image.open(picdir+"/1304x984.jpg")	
    epd.display(Blackimage2, Redimage2)
    time.sleep(2)

    # Clear the sceen to white for long term storage
    print("clearing...")
    epd.clear()

    print("goto sleep...")
    epd.EPD_Sleep()
except:
    print("goto sleep...")
    epd.EPD_Sleep()