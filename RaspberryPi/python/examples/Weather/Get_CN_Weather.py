#!/usr/bin/python
# -*- coding:utf-8 -*-

# This program is provided for educational purposes only and 
# should not be used for any commercial purpose. If there is 
# any infringement, please contact me to delete.

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor
from PIL import Image
import logging


import sys
import re
import requests# sudo python3 -m pip install requests

ur ='https://www.tianqiapi.com/api/?version=v1&&appid=[0]&appsecret=[0]'

def Get_Html(Url):#Timeout retry (failed if not successful 3 times)
    i = 0
    while i < 3:
        try:
            html = requests.get(Url, timeout=5)
            return html
        except requests.exceptions.RequestException as e:
            print(e)
            i += 1
    if(i==3):
        logging.critical("Network connection failed")
        sys.exit(0)

class Weather:
    def __init__(self):
        self.Weather = Get_Html(ur).text.encode('utf-8').decode("unicode_escape") #utf-8
        
        self.Day_Data_Passage = (''.join(re.findall(r'\w*"date":"[\s\S]*?"hours"', self.Weather))).encode('utf-8').decode('utf-8')
        self.Day_Data_Passage = re.sub(r'"hours"',' ',self.Day_Data_Passage)
        if(len(self.Day_Data_Passage) == 0):
            logging.critical("The website you entered is incorrect")
            logging.critical("Program exit")
            sys.exit(0)
    
    def Get_WeatherData(self):
        self.Weather = Get_Html(ur).text.encode('utf-8').decode("unicode_escape") #utf-8
        self.Day_Data_Passage = (''.join(re.findall(r'\w*"date":"[\s\S]*?"hours"', self.Weather))).encode('utf-8').decode('utf-8')
        self.Day_Data_Passage = re.sub(r'"hours"',' ',self.Day_Data_Passage)


    def Extract_Week(self):
        week_t =  (''.join(re.findall(r'\w*"week":"[\s\S]*?,', self.Day_Data_Passage)))
        week_t = re.sub('"week":"', '', week_t).strip()
        week   = re.split('",', week_t)
        return week

    def Extract_Wea(self):
        wea_t =  (''.join(re.findall(r'\w*"wea":"[\s\S]*?,', self.Day_Data_Passage)))
        wea_t = re.sub('"wea":"', '', wea_t).strip()
        wea   = re.split('",', wea_t)
        return wea

    def Extract_Date(self):
        date_t =  (''.join(re.findall(r'\w*"date":"[\s\S]*?,', self.Day_Data_Passage)))
        date_t = re.sub('"date":"', '', date_t).strip()
        date   = re.split('",', date_t)
        return date

    def Extract_TemLow(self):
        tem_t = (''.join(re.findall(r'\w*"tem1":"[\s\S]*?,', self.Day_Data_Passage)))
        tem_t = re.sub(r'[^0-9,]','', re.sub('"tem1":"', '', tem_t)).strip()
        tem   = re.split(',', tem_t)
        return tem
        
    def Extract_TemHigh(self):
        tem_t = (''.join(re.findall(r'\w*"tem2":"[\s\S]*?,', self.Day_Data_Passage)))
        tem_t = re.sub(r'[^0-9,]','', re.sub('"tem2":"', '', tem_t)).strip()
        tem   = re.split(',', tem_t)
        return tem
        
    def Extract_Tem(self):
        tem_t = (''.join(re.findall(r'\w*"tem":"[\s\S]*?,', self.Day_Data_Passage)))
        tem_t = re.sub(r'[^0-9,]','', re.sub('"tem":"', '', tem_t)).strip()
        tem   = re.split(',', tem_t)
        return tem
        
    def Extract_WinSpeed(self):
        win_speed_t =  (''.join(re.findall(r'\w*"win_speed":"[\s\S]*?"', self.Day_Data_Passage)))
        win_speed_t = re.sub('"win_speed":"', '', win_speed_t).strip()
        win_speed   = re.split('"', win_speed_t)
        return win_speed

    def Extract_Win(self):
        win_t = (''.join((re.findall(r'\w*"win":[\s\S]*?,', self.Day_Data_Passage)))).encode('utf-8').decode('utf-8')
        win_t = re.sub('win:\[', '', re.sub('"', '', win_t))
        win   = re.split(',', win_t)
        return win
        
    def Extract_Air(self):
        air_t =  (''.join(re.findall(r'\w*"air":[\s\S]*?,', self.Day_Data_Passage)))
        air = re.sub(',', ' ', re.sub('"air":', '', air_t)).strip()
        return air
        
    def Extract_AirLevel(self):
        air_level_t =  (''.join(re.findall(r'\w*"air_level":"[\s\S]*?,', self.Day_Data_Passage)))
        air_level = re.sub('"', ' ', re.sub(',', '', re.sub('"air_level":', ' ', air_level_t))).strip()
        return air_level
        
    def Extract_AirTips(self):
        air_tips_t =  (''.join(re.findall(r'\w*"air_tips":"[\s\S]*?,', self.Day_Data_Passage)))
        air_tips = re.sub('"', '', re.sub('",', '', re.sub('"air_tips":"', '', air_tips_t))).strip()
        return air_tips

    ##################################################################################
    #7 day


    def Extract_TodayHours(self):
        hours_t = (''.join(re.findall(r'\w*"hours":[\s\S]*?}]', self.Weather))).encode('utf-8').decode('utf-8')
        hours_day_t = (''.join(re.findall(r'\w*"day":"[\s\S]*?,', hours_t)))
        hours_day_t = re.sub('"', '', re.sub('"day":"', '', hours_day_t)).strip()
        hours_day   = re.split(',', hours_day_t)
        return hours_day
        
    def Extract_TodayWea(self):
        hours_t = (''.join(re.findall(r'\w*"hours":[\s\S]*?}]', self.Weather))).encode('utf-8').decode('utf-8')
        hours_wea_t = (''.join(re.findall(r'\w*"wea":"[\s\S]*?,', hours_t)))
        hours_wea_t = re.sub('"', '', re.sub('"wea":"', '', hours_wea_t)).strip()
        hours_wea   = re.split(',', hours_wea_t)
        return hours_wea

    def Extract_TodayTem(self):
        hours_t = (''.join(re.findall(r'\w*"hours":[\s\S]*?}]', self.Weather))).encode('utf-8').decode('utf-8')
        tem_t = (''.join(re.findall(r'\w*"tem":"[\s\S]*?,', hours_t)))
        tem_t = re.sub(r'[^0-9,]','', re.sub('"tem":"', '', tem_t)).strip()
        tem   = re.split(',', tem_t)
        return tem

    def Extract_TodayWin(self):
        hours_t = (''.join(re.findall(r'\w*"hours":[\s\S]*?}]', self.Weather))).encode('utf-8').decode('utf-8')
        hours_win_t = (''.join(re.findall(r'\w*"win":"[\s\S]*?,', hours_t)))
        hours_win_t = re.sub('"', '', re.sub('"win":"', ' ', hours_win_t)).strip()
        hours_win   = re.split(',', hours_win_t)
        return hours_win
        
    def Extract_TodayWinSpeed(self):
        hours_t = (''.join(re.findall(r'\w*"hours":[\s\S]*?}]', self.Weather))).encode('utf-8').decode('utf-8')
        hours_win_speed_t = (''.join(re.findall(r'\w*"win_speed":"[\s\S]*?"', hours_t)))
        hours_win_speed_t =re.sub('"}', ' ', re.sub('"win_speed":"', '', hours_win_speed_t)).strip()
        hours_win_speed   = re.split('"', hours_win_speed_t)
        return hours_win_speed

    def Extract_City(self):
        city_t =  (''.join(re.findall(r'\w*"city":"[\s\S]*?,', self.Weather))).encode('utf-8').decode('utf-8')
        city_t =re.sub('",', '', re.sub('"city":"', ' ', city_t))
        city = city_t.strip()
        return city

    def Extract_Level(self):
        #Various grades: 5 in order, UV index, glycemic index, dressing index, 
        #       car wash index, air pollution index
        # level_t
        level_t =  (''.join(re.findall(r'\w*"level":"[\s\S]*?,', self.Weather))).encode('utf-8').decode('utf-8')
        level_t = re.sub('",', ' ', re.sub('"level":"', '', level_t)).strip()
        level   = re.split(' ', level_t)
        return level

if __name__ == "__main__":
    Weather = Weather()

    wea = Weather.Extract_Wea()
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

    print (wea[0],wea[1],wea[2],wea[3],wea[4],wea[5])
    print (Week[0],Week[1],Week[2],Week[3],Week[4],Week[5])
    print (Date[0],Date[1],Date[2],Date[3],Date[4],Date[5])
    print (TemLow[0],TemLow[1],TemLow[2],TemLow[3],TemLow[4],TemLow[5])
    print (TemHigh[0],TemHigh[1],TemHigh[2],TemHigh[3],TemHigh[4],TemHigh[5])
    print (Tem[0],Tem[1],Tem[2],Tem[3],Tem[4],Tem[5])
    print (WinSpeed[0],WinSpeed[1],WinSpeed[2],WinSpeed[3],WinSpeed[4],WinSpeed[5])
    print (Win[0],Win[1],Win[2],Win[3],Win[4],Win[5])
    print (Air)
    print (AirLevel)
    print (AirTips)


    print (TodayHours[0],TodayHours[1],TodayHours[2],TodayHours[3],TodayHours[4],TodayHours[5])
    print (TodayWea[0],TodayWea[1],TodayWea[2],TodayWea[3],TodayWea[4],TodayWea[5])
    print (TodayTem[0],TodayTem[1],TodayTem[2],TodayTem[3],TodayTem[4],TodayTem[5])
    print (TodayWin[0],TodayWin[1],TodayWin[2],TodayWin[3],TodayWin[4],TodayWin[5])
    print (TodayWinSpeed[0],TodayWinSpeed[1],TodayWinSpeed[2],TodayWinSpeed[3],TodayWinSpeed[4],TodayWinSpeed[5])
    print (Level[0],Level[1],Level[2],Level[3],Level[4],Level[5])
    print (City)


        
