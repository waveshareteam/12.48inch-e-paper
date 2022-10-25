#!/usr/bin/python
# -*- coding:utf-8 -*-

#This program is provided for educational purposes only and should 
# not be used for any commercial purpose. If there is any infringement,
# please contact me to delete.

import os
import urllib
import sys
import logging

logging.basicConfig(level=logging.INFO)#DEBUG

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from Weather import Get_EN_Weather
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor
from PIL import Image

if (len(sys.argv) == 1):
    import epd12in48
    print ('epd12in48')
    Color_Type   = 1
    Inage_WIDTH  = epd12in48.EPD_WIDTH
    Inage_HEIGHT = epd12in48.EPD_HEIGHT
    epd = epd12in48.EPD()
    
elif(sys.argv[1] == 'help' or sys.argv[1] == 'HELP'):
    print ('If you are using epd_12in48 please run: sudo python %s '%sys.argv[0])
    print ('If you are using epd_12in48B please run: sudo python %s B'%sys.argv[0])
    sys.exit(0)
    
elif(sys.argv[1] == 'B' or sys.argv[1] == 'b'):
    import epd12in48b
    print ('epd12in48b')
    Color_Type   = 2
    Inage_WIDTH  = epd12in48b.EPD_WIDTH
    Inage_HEIGHT = epd12in48b.EPD_HEIGHT
    epd = epd12in48b.EPD()

print ("Please wait, it will take some time to download the data!!!!")  
##################################################
Blackimage = Image.new("1", (Inage_WIDTH, Inage_HEIGHT), 255)
Otherimage = Image.new("1", (Inage_WIDTH, Inage_HEIGHT), 255)
Black = ImageDraw.Draw(Blackimage)
Other = ImageDraw.Draw(Otherimage)
if(Color_Type == 1):
    Painting = Black
    Painting_image = Blackimage
else:
    Painting = Other
    Painting_image = Otherimage
##################################################

def Display_Init():
    print("12.48inch e-paper ...")
    epd.Init()
    # print("clearing...")
    # epd.clear()

def Display():
    if(Color_Type == 1):
        epd.display(Blackimage)
    else:
        epd.display(Blackimage, Otherimage)
    time.sleep(2)

def Display_END():
    print("goto sleep...")
    epd.EPD_Sleep()
##################################################

font20 = ImageFont.truetype(picdir+"/Font.ttc",  20)
font25 = ImageFont.truetype(picdir+"/Font.ttc",  25)
font30 = ImageFont.truetype(picdir+"/Font.ttc",  30)
font35 = ImageFont.truetype(picdir+"/Font.ttc",  35)
font40 = ImageFont.truetype(picdir+"/Font.ttc",  40)
font45 = ImageFont.truetype(picdir+"/Font.ttc",  45)
font50 = ImageFont.truetype(picdir+"/Font.ttc",  50)
font55 = ImageFont.truetype(picdir+"/Font.ttc",  55)
font60 = ImageFont.truetype(picdir+"/Font.ttc",  60)
font70 = ImageFont.truetype(picdir+"/Font.ttc",  70)
font80 = ImageFont.truetype(picdir+"/Font.ttc",  80)
font110 = ImageFont.truetype(picdir+"/Font.ttc", 110)

W_Proportion = int(Inage_WIDTH/6)
H_Proportion = int(Inage_HEIGHT/3)

Weather = Get_EN_Weather.Weather()


Week = Weather.Extract_Week()
Date = Weather.Extract_Date()
Wea  = Weather.Extract_Wea()
TemHigh  = Weather.Extract_TemHigh()
TemLow  = Weather.Extract_TemLow()
TemHourly  = Weather.Extract_TemHourly()
TimeHourly  = Weather.Extract_TimeHourly()
Tem  = Weather.Extract_Tem()
OtherData  = Weather.Extract_OtherData()
City  = Weather.Extract_City()
RealTimeWeather  = Weather.Extract_RealTimeWeather()
Weather.Extract_Map()

# Weather.Extract_Map()
# print Week
# print Date
# print TemHourly
# print TimeHourly

Display_Init()
#############################################################
Black.text((10,10), City, font = font80, fill = "BLUE")
Black.text((210,H_Proportion/3), RealTimeWeather, font = font50, fill = "BLUE")

Painting.text((117-len(Tem)*50,H_Proportion/3),Tem, font = font110, fill = "BLUE")
Black.text((117-len(Tem)*50+120,H_Proportion/3),u'°F', font = font40, fill = "BLUE")

Black.text((W_Proportion,H_Proportion/5*3), OtherData[0], font = font30, fill = "BLUE")
Black.text((W_Proportion,H_Proportion/5*4), OtherData[1], font = font30, fill = "BLUE")

Black.text((int(W_Proportion*2.5),H_Proportion/5*3), OtherData[2], font = font30, fill = "BLUE")
Black.text((int(W_Proportion*2.5),H_Proportion/5*4), OtherData[3], font = font30, fill = "BLUE")

Black.text((int(W_Proportion*4),H_Proportion/5*3), OtherData[4], font = font30, fill = "BLUE")
Black.text((int(W_Proportion*4),H_Proportion/5*4), OtherData[5], font = font30, fill = "BLUE")

for i in range(0, Inage_WIDTH, 10):
    Black.ellipse([i-2, H_Proportion-20-2, i+2, H_Proportion-20+2], fill = "BLUE")
#############################################################
for i in range(0, 6):
    if (i != 0):
        Black.line([(W_Proportion*i,H_Proportion),(W_Proportion*i,H_Proportion*2)], 
                    fill = "BLUE",width = 3)
    Black.text((W_Proportion*i+117-len(Week[i])*9-len(Date[i])*9,H_Proportion + 0), 
            Week[i]+' '+Date[i], font = font25, fill = "BLUE")    
            
    Black.text((W_Proportion*i+117-len(Wea[i])*9,H_Proportion + 40), 
            Wea[i], font = font25, fill = "BLUE")
            
    PNG = Image.open("Weather/"+ str(i) +".png")	
    Painting_image.paste(PNG, (W_Proportion*i+73, H_Proportion + 80)) 
    
    Black.text((W_Proportion*i+117-len(TemHigh[i]+u'°F')*15,H_Proportion + 170), 
            TemHigh[i]+u'°F', font = font45, fill = "BLUE")

    Black.text((W_Proportion*i+117-len(TemHigh[i]+u'°F')*15,H_Proportion + 230), 
            TemLow[i]+u'°F', font = font45, fill = "BLUE")

##################################################
Black.line([(50,Inage_HEIGHT-30),(Inage_WIDTH-50,Inage_HEIGHT-30)],
            fill = "BLUE",width = 3)
Black.line([(50,Inage_HEIGHT-30),(50,Inage_HEIGHT-H_Proportion+20)],
            fill = "BLUE",width = 3)
            
Black.line([(Inage_WIDTH-50-5,Inage_HEIGHT-30-5),(Inage_WIDTH-50,Inage_HEIGHT-30)],
            fill = "BLUE",width = 3)
Black.line([(Inage_WIDTH-50-5,Inage_HEIGHT-30+5),(Inage_WIDTH-50,Inage_HEIGHT-30)],
            fill = "BLUE",width = 3)
            
Black.line([(50-5,Inage_HEIGHT-H_Proportion+20+5),(50,Inage_HEIGHT-H_Proportion+20)],
            fill = "BLUE",width = 3)
Black.line([(50+5,Inage_HEIGHT-H_Proportion+20+5),(50,Inage_HEIGHT-H_Proportion+20)],
            fill = "BLUE",width = 3)

temp = [None]*24
for i in range(0, 24):
    temp[i]  = int(TemHourly[i])

temp.sort()
tem_max = int(temp[len(temp)-1]/3.0+1)*3
tem_min = int(temp[0]/3)*3
tem_Proportion =  int(240/(tem_max - tem_min))

s = 1
# TimeHourly
for i in range(0,24, 1):#w == 50
    arc_dax = 4
    y1 = Inage_HEIGHT-30-30-int((int(TemHourly[i])-tem_min)*tem_Proportion)
    if(i!=23):
        y2 = Inage_HEIGHT-30-30-int((int(TemHourly[i+1])-tem_min)*tem_Proportion)
        Painting.line([(50+50*i,y1),(50+50*(i+1),y2)], fill = "BLUE",width = 3)
    else :
        Painting.text((50+50*i,y1-30), TemHourly[i]+u'°F', font = font20, fill = "BLUE")
        Black.ellipse([50+50*i-arc_dax, y1-arc_dax, 50+50*i+arc_dax, y1+arc_dax], fill = "BLUE")
        Black.text((50+50*i, Inage_HEIGHT-27), TimeHourly[i], font = font25, fill = "BLUE")
        
    
    if((int(TemHourly[i])>= temp[len(temp)-1] ) and s):
        s=0
        Painting.text((50+50*i,y1-30), TemHourly[i]+u'°F', font = font20, fill = "BLUE")
        Black.ellipse([50+50*i-arc_dax, y1-arc_dax, 50+50*i+arc_dax, y1+arc_dax], fill = "BLUE")
        Black.text((50+50*i, Inage_HEIGHT-27), TimeHourly[i], font = font25, fill = "BLUE")
    elif((int(TemHourly[i])<= temp[0] ) and s):
        s=0
        Painting.text((50+50*i,y1-30), TemHourly[i]+u'°F', font = font20, fill = "BLUE")
        Black.ellipse([50+50*i-arc_dax, y1-arc_dax, 50+50*i+arc_dax, y1+arc_dax], fill = "BLUE")
        Black.text((50+50*i, Inage_HEIGHT-27), TimeHourly[i], font = font25, fill = "BLUE")
    
    if((i%3) == 0):
        s=1
        Painting.text((50+50*i,y1-30), TemHourly[i]+u'°F', font = font20, fill = "BLUE")
        Black.ellipse([50+50*i-arc_dax, y1-arc_dax, 50+50*i+arc_dax, y1+arc_dax], fill = "BLUE")
        Black.text((50+50*i, Inage_HEIGHT-27), TimeHourly[i], font = font25, fill = "BLUE")
        
Black.text((10,Inage_HEIGHT-30-30),  str(tem_min+int((tem_max - tem_min)*0/4)), font = font30, fill = "BLUE")
Black.text((10,Inage_HEIGHT-30-90),  str(tem_min+int((tem_max - tem_min)*1/4)), font = font30, fill = "BLUE")
Black.text((10,Inage_HEIGHT-30-150), str(tem_min+int((tem_max - tem_min)*2/4)), font = font30, fill = "BLUE")
Black.text((10,Inage_HEIGHT-30-210), str(tem_min+int((tem_max - tem_min)*3/4)), font = font30, fill = "BLUE")
Black.text((10,Inage_HEIGHT-30-270), str(tem_min+int((tem_max - tem_min)*4/4)), font = font30, fill = "BLUE")
#############################################################  
Display()
Display_END()
