#!/usr/bin/python
# -*- coding:utf-8 -*-

'''This example uses https://www.msn.com/en-us/weather webpage 
data, here only for learning, can not use any commercial use, if 
there is any infringement, please contact me, I will delete'''

import os
import urllib
import sys
import logging

from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor
from PIL import Image

import re
import requests# sudo python3 -m pip install requests

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
ur = 'https://www.msn.com/en-us/Weather/?day=1'

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

def Download_PNG(Url,Name):#Download image   
    import requests
    r = Get_Html(Url)  
    with open(Name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=32):
            f.write(chunk)
    f.close()
    
    #Read the file and convert it to a bitmap
    #Increase portability
    PNG = Image.open(Name).convert('LA')
    gray = PNG.convert('L')
    bw = gray.point(lambda x: 255 if x<128 else 0, '1')#Turn into bitmap and color flip
    bw.save(Name)#save Picture

class Weather:
    def __init__(self):
        self.Weather_data = Get_Html(ur).text.encode('utf-8').decode('utf-8')
        self.Weather_Info = (''.join(re.findall(r'\w*<div class="weather-info">[\s\S]*?</div>', self.Weather_data)))
        self.Forecast_List = (''.join(re.findall(r'\w*<ul class="forecast-list">[\s\S]*?</ul>', self.Weather_data)))
        self.Extract_Map()

    def Get_WeatherData(self):
        self.Weather_data = Get_Html(ur).text.encode('utf-8').decode('utf-8')
        self.Weather_Info = (''.join(re.findall(r'\w*<div class="weather-info">[\s\S]*?</div>', self.Weather_data)))
        self.Forecast_List = (''.join(re.findall(r'\w*<ul class="forecast-list">[\s\S]*?</ul>', self.Weather_data)))
        self.Extract_Map()

    def Extract_RealTimeWeather(self):
        RealTimeWeather_t = (''.join(re.findall(r'\w*<span>[\s\S]*?</span>', self.Weather_Info)))
        RealTimeWeather_t = re.sub('</span>', ' ', re.sub('<span>', '', RealTimeWeather_t)).strip()
        RealTimeWeather   = re.split(' ', RealTimeWeather_t)
        return RealTimeWeather[0]
        
    def Extract_City(self):
        city_t  = (''.join(re.findall(r'\w*"mylocations" data-loc="n=[\s\S]*?&', self.Weather_data)))
        city_t  = (''.join(re.findall(r'\W*%2C%20[\s\S]*?&', city_t)))
        city_t = re.sub('%20', ' ', re.sub('%2C', '', city_t)).strip()
        city_t = re.sub('&', '', city_t)
        city = city_t
        return city
        
    def Extract_PrecipicnHourly(self):
        precipicn_t = (''.join(re.findall(r'\W*<div class="precipicn"><span>[\s\S]*?</span>', self.Weather_data)))
        precipicn_t = (''.join(re.findall(r'\W*"><span>[\s\S]*?<', precipicn_t)))
        precipicn_t = re.sub('<', ' ', re.sub('><span>', '', precipicn_t))
        precipicn_t = re.sub('  ', ' ', re.sub('"', '', precipicn_t)).strip()
        precipicn_hourly = re.split(' ', precipicn_t)
        return precipicn_hourly
        
    def Extract_TemHourly(self):
        tem_t = (''.join(re.findall(r'\W*<p class="temp">[\s\S]*?&', self.Weather_data)))
        tem_t = re.sub('[^0-9/]' ,'', re.sub('<p class="temp">', '', tem_t)).strip()
        tem_t = re.sub('/', ' ', tem_t).strip()
        tem_hourly = re.split(' ', tem_t)
        return tem_hourly
        
    def Extract_TimeHourly(self):
        Time_t = (''.join(re.findall(r'\W*<p class="time">[\s\S]*?<', self.Weather_data)))
        Time_t = re.sub('<' ,'', re.sub('<p class="time">', '', Time_t)).strip()
        Time_t = re.sub('[^A-Za-z0-9]', ' ', Time_t).strip()
        Time_t = re.sub('  ', ' ', Time_t)
        Time_Hourly = re.split(' ', Time_t)
        return Time_Hourly

    def Extract_Tem(self):
        tem_t    = (''.join(re.findall(r'\w*<span class="current" aria-label[\s\S]*?</span>', self.Weather_data)))
        tem_t  = (''.join(re.findall(r'\w*>[\s\S]*?<', tem_t)))
        tem = re.sub('<', '', re.sub('>', '', tem_t)).strip()
        return tem

    def Extract_Week(self):
        week_t = (''.join(re.findall(r'\w*forecast for [\s\S]*?,', self.Forecast_List))).encode('utf-8').decode('utf-8')
        week_t = re.sub(',', ' ', re.sub('forecast for ', '', week_t)).strip()
        week   = re.split(' ', week_t)
        return week
        
    def Extract_TemLow(self):
        tem1_t = (''.join(re.findall(r'\w*low of [\s\S]*?&', self.Forecast_List))).encode('utf-8').decode('utf-8')
        tem1_t = re.sub('&', ' ', re.sub('low of ', '', tem1_t)).strip()
        tem1   = re.split(' ', tem1_t)
        return tem1
        
    def Extract_TemHigh(self):
        tem2_t = (''.join(re.findall(r'\w*High of [\s\S]*?&', self.Forecast_List))).encode('utf-8').decode('utf-8')
        tem2_t = re.sub('&', ' ', re.sub('High of ', '', tem2_t)).strip()
        tem2   = re.split(' ', tem2_t)
        return tem2
        
    def Extract_Wea(self):
        wea_t = (''.join(re.findall(r'\W* is [\s\S]*?High', self.Forecast_List))).encode('utf-8').decode('utf-8')
        wea_t = re.sub('High', '', re.sub(' is ', '', wea_t))
        wea_t = re.sub(r'\W*.  ', '', wea_t)
        wea_t = re.sub(r'[^A-Za-z0-9_ -]', '#', wea_t)
        wea_t = re.sub(r'# ', '#', wea_t).strip()
        wea   = re.split('#', wea_t)
        return wea

    def Extract_MapAddress(self):
        map_address_t = (''.join(re.findall(r'\W*src="//[\s\S]*?" ', self.Forecast_List)))
        map_address_t = re.sub('" ', ' ', re.sub('src="', '', map_address_t)).strip()
        map_address_t = re.sub('  ', ' ', map_address_t).strip()
        map_address   = re.split(' ', map_address_t)
        return map_address
        
    def Extract_Date(self):
        Date_t = (''.join(re.findall(r'\W*, [\s\S]*?is', self.Forecast_List)))
        Date_t = re.sub('is', ' ', re.sub(', ', '', Date_t)).strip()
        Date_t = re.sub('  ', ' ', Date_t).strip()
        Date   = re.split(' ', Date_t)
        return Date

    def Extract_PrecipicnDay(self):
        precipicn_t = (''.join(re.findall(r'\W*<div title="Precipitation"[\s\S]*?</div>', self.Forecast_List)))
        precipicn_t = (''.join(re.findall(r'\W*"><span>[\s\S]*?<', precipicn_t)))
        precipicn_t = re.sub('<', ' ', re.sub('><span>', '', precipicn_t))
        precipicn_t = re.sub('  ', ' ', re.sub('"', '', precipicn_t)).strip()
        precipicn_day = re.split('#', precipicn_t)
        return precipicn_day

    def Extract_OtherData(self):
        Other_Data_t = ''.join(re.findall(r'\W*<ul>[\s\S]*?</ul>', self.Weather_Info))
        Other_Data_t = re.sub('</ul>', '', re.sub('<ul>', '', Other_Data_t))
        Other_Data_t = re.sub('</span>', '', re.sub('<li><span>', '', Other_Data_t))
        Other_Data_t = re.sub('&#176', '', re.sub('</li>', '#', Other_Data_t))
        Other_Data_t = re.sub(r'[^A-Za-z0-9% -#.]', '', Other_Data_t)
        Other_Data   = re.split('#', Other_Data_t)
        return Other_Data

    def Extract_Map(self):
        map_address = self.Extract_MapAddress()
        for i in range(0, 6):#10 sheets available, 6 defaults here
            logging.debug ("http:"+map_address[i])
            Download_PNG("http:"+map_address[i], 'Weather/'+str(i)+'.png')
        #If you want to be faster, it is recommended to use multi-threading.

if __name__ == "__main__":
    Weather = Weather()
    Weather.Get_WeatherData()
    
    print (Weather.Extract_OtherData())
    print (Weather.Extract_City())
    print (Weather.Extract_TemLow())
    print (Weather.Extract_TemHigh())
    print (Weather.Extract_Tem())
    print (Weather.Extract_Week())
    print (Weather.Extract_Wea())
    print (Weather.Extract_PrecipicnDay())
    print (Weather.Extract_PrecipicnHourly())
    print (Weather.Extract_TemHourly())
    print (Weather.Extract_MapAddress())
    print (Weather.Extract_TimeHourly())
    print (Weather.Extract_Date())
    print (Weather.Extract_RealTimeWeather())
    # Weather.Extract_Map()

