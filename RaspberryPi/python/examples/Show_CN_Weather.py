#!/usr/bin/python
# -*- coding:utf-8 -*-

#This program is provided for educational purposes only and should 
# not be used for any commercial purpose. If there is any infringement,
# please contact me to delete.

import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import epd12in48b
from Weather import Get_CN_Weather
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

from PIL import Image

import re

import requests# sudo python3 -m pip install requests
import logging

print ('Weather forecast 12.48 e-Paper test code')


logging.basicConfig(level=logging.INFO)

if (len(sys.argv) == 1):
    import epd12in48
    print ('epd12in48')
    Color_Type   = 1
    Inage_WIDTH  = epd12in48.EPD_WIDTH
    Inage_HEIGHT = epd12in48.EPD_HEIGHT
    epd = epd12in48.EPD()
    
elif(sys.argv[1] == 'help' or sys.argv[1] == 'HELP'):
    print ('If you are using epd_12in48 please run: sudo python %s '%sys.argv[0])
    print ('                                     or sudo python3 %s'%sys.argv[0])
    print ('If you are using epd_12in48B please run: sudo python %s B'%sys.argv[0])
    print ('                                      or sudo python3 %s B'%sys.argv[0])
    sys.exit(0)
    
elif(sys.argv[1] == 'B' or sys.argv[1] == 'b'):
    import epd12in48b
    print ('epd12in48b')
    Color_Type   = 2
    Inage_WIDTH  = epd12in48b.EPD_WIDTH
    Inage_HEIGHT = epd12in48b.EPD_HEIGHT
    epd = epd12in48b.EPD()

Blackimage = Image.new("1", (Inage_WIDTH, Inage_HEIGHT), 255)
Otherimage = Image.new("1", (Inage_WIDTH, Inage_HEIGHT), 255)
Black = ImageDraw.Draw(Blackimage)

if(Color_Type == 1):
    Other = Black
else:
    Other = ImageDraw.Draw(Otherimage)


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


'''This api is only for cities in China.'''
Weather = Get_CN_Weather.Weather()


Wea = Weather.Extract_Wea()
Week = Weather.Extract_Week()
Date = Weather.Extract_Date()
TemLow = Weather.Extract_TemLow()
TemHigh = Weather.Extract_TemHigh()
Tem = Weather.Extract_Tem()
WinSpeed = Weather.Extract_WinSpeed()
Win = Weather.Extract_Win()
Air = Weather.Extract_Air()
AirLevel = Weather.Extract_AirLevel()
AirTips = Weather.Extract_AirTips()

TodayHours = Weather.Extract_TodayHours()
TodayWea = Weather.Extract_TodayWea()
TodayTem = Weather.Extract_TodayTem()
TodayWin = Weather.Extract_TodayWin()
TodayWinSpeed = Weather.Extract_TodayWinSpeed()
Level = Weather.Extract_Level()
City = Weather.Extract_City()

# print Wea[0],Wea[1],Wea[2],Wea[3],Wea[4],Wea[5]
# print Week[0],Week[1],Week[2],Week[3],Week[4],Week[5]
# print Date[0],Date[1],Date[2],Date[3],Date[4],Date[5]
# print TemLow[0],TemLow[1],TemLow[2],TemLow[3],TemLow[4],TemLow[5]
# print TemHigh[0],TemHigh[1],TemHigh[2],TemHigh[3],TemHigh[4],TemHigh[5]
# print Tem[0],Tem[1],Tem[2],Tem[3],Tem[4],Tem[5]
# print WinSpeed[0],WinSpeed[1],WinSpeed[2],WinSpeed[3],WinSpeed[4],WinSpeed[5]
# print Win[0],Win[1],Win[2],Win[3],Win[4],Win[5]
# print Air
# print AirLevel
# print AirTips

# print 'saa',TodayHours[0],TodayHours[1],TodayHours[2],TodayHours[3],TodayHours[4],TodayHours[5]
# print TodayWea[0],TodayWea[1],TodayWea[2],TodayWea[3],TodayWea[4],TodayWea[5]
# print TodayTem[0],TodayTem[1],TodayTem[2],TodayTem[3],TodayTem[4],TodayTem[5]
# print TodayWin[0],TodayWin[1],TodayWin[2],TodayWin[3],TodayWin[4],TodayWin[5]
# print TodayWinSpeed[0],TodayWinSpeed[1],TodayWinSpeed[2],TodayWinSpeed[3],TodayWinSpeed[4],TodayWinSpeed[5]
# print Level[0],Level[1],Level[2],Level[3],Level[4],Level[5]
# print City

#......................................................................#
#  Match string is used to find the image corresponding to the Weather #
#......................................................................#
# print Wea
BMP_table_t = ''
for i in range(0, 6):
    if re.search(u'雷阵雨', Wea[i]):
        BMP_table_t = BMP_table_t + 'thunder_shower '
    elif re.search(u'雨', Wea[i]):
        BMP_table_t = BMP_table_t + 'rain '
    elif re.search(u'晴', Wea[i]):
        BMP_table_t = BMP_table_t + 'sunny '
    elif re.search(u'阴', Wea[i]):
        BMP_table_t = BMP_table_t + 'yin '
    elif re.search(u'多云', Wea[i]):
        BMP_table_t = BMP_table_t + 'cloudy '
BMP_table   = re.split(' ', BMP_table_t)
# print BMP_table[0],BMP_table[1]


# print Date[0][5:]

Display_Init()

if(Color_Type == 1):
    Painting = Black
else:
    Painting = Other

font = ImageFont.truetype(picdir+"/Font.ttc", 100)
font40 = ImageFont.truetype(picdir+"/Font.ttc", 40)
font30 = ImageFont.truetype(picdir+"/Font.ttc",30)
font25 = ImageFont.truetype(picdir+"/Font.ttc",25)
font70 = ImageFont.truetype(picdir+"/Font.ttc",70)

#The input display needs to be determined to be converted to utf-8.
Black.text((10,10), time.strftime('%Y') + u'年' + time.strftime('%m') +u'月'+ time.strftime('%d') \
            + u'日' + "  " + Week[0], font = font25, fill = "BLUE")
Black.text((0+(180-len(City)*20),40), City, font = font40, fill = "BLUE")
BMP = Image.open(picdir+"/"+ BMP_table[0] +".bmp")	
Blackimage.paste(BMP, (148,90)) 

Other.text((80,150), Tem[0], font = font, fill = "BLUE")
Black.text((200,170), u'°C', font = font30, fill = "BLUE")
Black.text((200,210), u'(实时)', font = font30, fill = "BLUE")
Black.text((110,250), TemHigh[0]+ u'°C~' +TemLow[0]+ u'°C', font = font30, fill = "BLUE")
Other.text((0+(180-len(Wea[0])*15),290),Wea[0], font = font30, fill = "BLUE")
Black.text((0+(180-len(Win[0])*15),330),Win[0], font = font30, fill = "BLUE")
Black.text((0+(180-len(WinSpeed[0])*10),370),WinSpeed[0], font = font30, fill = "BLUE")  
Black.rectangle([(132,409),(228,443)],fill = "BLUE")
Black.text((195,410), Level[4], font = font30, fill = "WHITE")
Black.text((140,410), Air, font = font30, fill = "WHITE")

Black.line([(360,40),(360,450)], fill = "BLUE",width = 3)

###############################################################################################
for i in range(1, 6):
    Black.line([(360+i*180,40),(360+i*180,450)], fill = "BLUE",width = 3)
    Black.text((400+(i-1)*180,50), Week[i], font = font30, fill = "BLUE")
    Black.text((405+(i-1)*180,90), Date[i][5:], font = font30, fill = "BLUE")
    BMP = Image.open(picdir+"/"+ BMP_table[i] +".bmp")	
    Blackimage.paste(BMP, (418+(i-1)*180,150)) 
    Black.text((380+(i-1)*180,250), TemHigh[i]+ u'°C~' +TemLow[i]+ u'°C', font = font30, fill = "BLUE")
    if (len(Wea[i])<6):
        Black.text((360+(i-1)*180+(90-len(Wea[i])*15),290),Wea[i], font = font30, fill = "BLUE")
    else :
        Black.text((360+(i-1)*180+(90-len(Wea[i])*13),290),Wea[i], font = font25, fill = "BLUE")
    if (len(Win[i])<6):
        Black.text((360+(i-1)*180+(90-len(Win[i])*15),330),Win[i], font = font30, fill = "BLUE")
    else :
        Black.text((360+(i-1)*180+(90-len(Win[i])*13),330),Win[i], font = font25, fill = "BLUE")  
        
    
    Black.text((360+(90-len(WinSpeed[i])*10)+(i-1)*180,370),WinSpeed[i], font = font30, fill = "BLUE")  
    Black.rectangle([(430+(i-1)*180,409),(470+(i-1)*180,443)],fill = "BLUE")
    Black.text((435+(i-1)*180,410), Level[9+(i-1)*5], font = font30, fill = "WHITE")
###############################################################################################

time_table_t=['8','11','14','17','20','23','2','5']
time_table  = [None]*8
Black.line([(70,520),(70,850)], fill = "BLUE",width = 3)
Black.line([(70,850),(1280,850)], fill = "BLUE",width = 3)
Black.line([(70,520),(70,850)], fill = "BLUE",width = 3)

Black.line([(70,520),(75,525)], fill = "BLUE",width = 3)
Black.line([(70,520),(65,525)], fill = "BLUE",width = 3)
Black.text((20,490), u'温度/°C', font = font25, fill = "BLUE")

Black.line([(1280,850),(1275,855)], fill = "BLUE",width = 3)
Black.line([(1280,850),(1275,845)], fill = "BLUE",width = 3)
Black.text((1250,855), u'时间', font = font25, fill = "BLUE")

time_H = int(time.strftime('%H'))

if(time_H>=8 and time_H<11):
    k=0
elif(time_H>=11 and time_H<14):
    k=1
elif(time_H>=14 and time_H<17):
    k=2
elif(time_H>=17 and time_H<20):
    k=3
elif(time_H>=20 and time_H<23):
    k=4
elif(time_H>=23 or  time_H<2):
    k=5
elif(time_H>=2 and time_H<5):
    k=6
elif(time_H>=5 and time_H<8):
    k=7

for i in range(0, 8):
    if(k+i < 8):
        time_table[i] =  time_table_t[k+i]
    elif(k+i >= 8):
        time_table[i] =  time_table_t[k+i-8]

Tem_table = [None]*8
Tem_table[0] = -1
Tem_table[0] = int(Tem[0])
for i in range(1,8):
    Tem_table[i] = int(TodayTem[k+i])

Tem_table.sort()
Tem_max = int(Tem_table[len(Tem_table)-1]/3+1)*3
Tem_min = int(Tem_table[0]/3)*3
Tem_gap =  int(240/(Tem_max - Tem_min))


Other.text((120,856), u'现在', font = font30, fill = "BLUE")
for i in range(1,8):
    Other.text((120+150*i,856), time_table[i]+u'点', font = font30, fill = "BLUE")

for i in range(0,7):
    y1 = 850-60-int((int(TodayTem[k+i])-Tem_min)*Tem_gap)
    y2 = 850-60-int((int(TodayTem[k+i+1])-Tem_min)*Tem_gap)
    arc_dax = 4
    Other.ellipse([120+150*i-arc_dax, y1-arc_dax, 120+150*i+arc_dax, y1+arc_dax], fill = "BLUE")
    Other.ellipse([120+150*(i+1)-arc_dax, y2-arc_dax, 120+150*(i+1)+arc_dax, y2+arc_dax], fill = "BLUE")
    Other.line([(120+150*i,y1),(120+150*(i+1),y2)], fill = "BLUE",width = 3)
    
    Other.text((120+150*i,y1-30), TodayTem[k+i]+u'°C', font = font25, fill = "BLUE")
    if(i==6):
        Other.text((120+150*(i+1),y2-30), TodayTem[k+i+1]+u'°C', font = font25, fill = "BLUE")
Other.text((20,850-60),  str(Tem_min+int((Tem_max - Tem_min)*0/4)), font = font30, fill = "BLUE")
Other.text((20,850-120), str(Tem_min+int((Tem_max - Tem_min)*1/4)), font = font30, fill = "BLUE")
Other.text((20,850-180), str(Tem_min+int((Tem_max - Tem_min)*2/4)), font = font30, fill = "BLUE")
Other.text((20,850-240), str(Tem_min+int((Tem_max - Tem_min)*3/4)), font = font30, fill = "BLUE")
Other.text((20,850-300), str(Tem_min+int((Tem_max - Tem_min)*4/4)), font = font30, fill = "BLUE")

Display()
time.sleep(2)

Display_END()

