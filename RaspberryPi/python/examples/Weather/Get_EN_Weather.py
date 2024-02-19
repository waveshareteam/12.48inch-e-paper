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

def floyd_steinberg_bw_dithering(image_path, output_path):
    img = Image.open(image_path)
    img = img.convert('L')
    color_map = [0, 255]

    for y in range(0, img.height - 1):
        for x in range(0, img.width - 1):
            old_pixel = img.getpixel((x, y))
            new_pixel = min(color_map, key=lambda x: abs(x - old_pixel))
            img.putpixel((x, y), new_pixel)

            error = old_pixel - new_pixel
            if x==0:
                img.putpixel((x + 1, y), img.getpixel((x + 1, y)) + error * 7 // 16)
                img.putpixel((x, y + 1), img.getpixel((x, y + 1)) + error * 2 // 16)
                img.putpixel((x + 1, y + 1), img.getpixel((x + 1, y + 1)) + error * 7 // 16)
            elif x==img.width - 1:
                img.putpixel((x - 1, y + 1), img.getpixel((x - 1, y + 1)) + error * 7 // 16)
                img.putpixel((x, y + 1), img.getpixel((x, y + 1)) + error * 9 // 16)
            else:
                img.putpixel((x + 1, y), img.getpixel((x + 1, y)) + error * 7 // 16)
                img.putpixel((x - 1, y + 1), img.getpixel((x - 1, y + 1)) + error * 3 // 16)
                img.putpixel((x, y + 1), img.getpixel((x, y + 1)) + error * 5 // 16)
                img.putpixel((x + 1, y + 1), img.getpixel((x + 1, y + 1)) + error * 1 // 16)

    img = img.point(lambda x: 255 if x<128 else 0, '1')#Turn into bitmap and color flip
    img.save(output_path)
    

def Download_PNG(Url,Name):#Download image   
    import requests
    import cairosvg
    r = Get_Html(Url).text.encode('utf-8').decode('utf-8')
    cairosvg.svg2png(bytestring=r, write_to=Name)    
    floyd_steinberg_bw_dithering(Name, Name)

class Weather:
    def __init__(self):
        self.Weather_data = Get_Html(ur).text.encode('utf-8').decode('utf-8')
        self.Extract_Map()

    def Extract_RealTimeWeather(self):
        RealTimeWeather_t = (''.join(re.findall(r'<div class="labelWeather-E1_1">[\s\S]*?</div>', self.Weather_data)))
        RealTimeWeather_t = (''.join(re.findall(r'>[\s\S]*?<', RealTimeWeather_t)))
        RealTimeWeather   = (''.join(re.findall(r'[A-Za-z0-9, ]', RealTimeWeather_t)).strip())
        return RealTimeWeather
        
    def Extract_City(self):
        city_t  = (''.join(re.findall(r'"isWeatherCurrentCard2U":true,"currentLocation":{[\s\S]*?}', self.Weather_data)))
        city_t_country  = (''.join(re.findall(r'"country":"[\s\S]*?",', city_t)))
        city_t_country  = (''.join(re.findall(r':"[\s\S]*?",', city_t_country)))
        city_t_country  = (''.join(re.findall(r'[A-Za-z0-9 ]', city_t_country)).strip())
        city_t_displayName  = (''.join(re.findall(r'"displayName":"[\s\S]*?"}', city_t)))
        city_t_displayName  = (''.join(re.findall(r':"[\s\S]*?"', city_t_displayName)))
        city_t_displayName  = (''.join(re.findall(r'[A-Za-z0-9, ]', city_t_displayName)))
        if city_t_country in city_t_displayName:
            city = city_t_displayName
        else:
            city = city_t_displayName + ", " + city_t_country
        return city

    def Extract_TemHourly(self):
        tem_t = (''.join(re.findall(r'\w*<g class="tempLabels-E1_1">[\s\S]*?</g>', self.Weather_data)))
        tem_t = (''.join(re.findall(r'>[\s\S]*?<', tem_t)))
        tem_t = re.sub('<><>' ,' ',tem_t)
        tem_hourly = re.findall(r'\d+', tem_t)
        # tem_hourly = re.split(' ', tem_hourly)
        return tem_hourly
        
    def Extract_TimeHourly(self):
        Time_t = (''.join(re.findall(r'<g class="newTimeLabels-E1_1">[\s\S]*?</g>', self.Weather_data)))
        Time_t = (''.join(re.findall(r'>[\s\S]*?<', Time_t)))
        Time_t = re.sub('<><>' ,',', Time_t).strip()
        Time_t = (''.join(re.findall(r'[A-Za-z0-9, ]', Time_t)))
        Time_Hourly = re.split(',', Time_t)
        return Time_Hourly

    def Extract_Tem(self):
        tem_t = (''.join(re.findall(r'class="summaryTemperatureCompact-E1_1 summaryTemperatureHover-E1_1"[\s\S]*?</span></a>', self.Weather_data)))
        tem_t  = (''.join(re.findall(r'title="[\s\S]*?">', tem_t)))
        tem = (''.join(re.findall(r'[0-9]', tem_t)))
        return tem

    def Extract_Week(self):
        week_t = (''.join(re.findall(r'\w*<p class="headerV3-E1_1">[\s\S]*?</p>', self.Weather_data)))
        week_t = (''.join(re.findall(r'\w*">[\s\S]*? ', week_t)))
        week = re.sub('E1_1">', '', week_t).strip()
        week = re.split(' ', week)
        return week
        
    def Extract_TemLow(self):
        tem1_t = (''.join(re.findall(r'\w*class="temp-E1_1">[\s\S]*?</div>', self.Weather_data)))
        tem1_t = re.sub('</div>', ' ', re.sub('class="temp-E1_1">', '', tem1_t)).strip()
        tem1_t = (''.join(re.findall(r'[0-9 ]', tem1_t)).strip())
        tem1   = re.split(' ', tem1_t)
        tem1.pop(0)
        return tem1
        
    def Extract_TemHigh(self):
        tem2_t = (''.join(re.findall(r'\w*<div class="topTemp-E1_1 temp-E1_1">[\s\S]*?</div>', self.Weather_data)))
        tem2_t = re.sub('</div>', ' ', re.sub('<div class="topTemp-E1_1 temp-E1_1">', '', tem2_t)).strip()
        tem2_t = (''.join(re.findall(r'[0-9 ]', tem2_t)).strip())
        tem2   = re.split(' ', tem2_t)
        tem2.pop(0)
        return tem2
        
    def Extract_Wea(self):
        wea_t = (''.join(re.findall(r'\w*<img class="iconTempPartIcon-E1_1" [\s\S]*?</div>', self.Weather_data)))
        wea_t = (''.join(re.findall(r'\w*title="[\s\S]*?"/>', wea_t)))
        wea_t = re.sub(r'/>', ' ', re.sub(r'title="', '', wea_t)).strip('"')
        wea = re.split('" ', wea_t)
        wea.pop(0)
        return wea

    def Extract_MapAddress(self):
        self.Forecast_List = (''.join(re.findall(r'\w*<img class="iconTempPartIcon-E1_1"[\s\S]*?</div>', self.Weather_data)))
        map_address_t = (''.join(re.findall(r'\W*src="[\s\S]*?" ', self.Forecast_List)))
        map_address_t = re.sub('" ', ' ', re.sub('src="', '', map_address_t)).strip()
        map_address_t = re.sub('  ', ' ', map_address_t).strip()
        map_address   = re.split(' ', map_address_t)
        map_address.pop(0)
        return map_address
        
    def Extract_Date(self):
        Date_t = (''.join(re.findall(r'\w*<p class="headerV3-E1_1">[\s\S]*?</p>', self.Weather_data)))
        Date_t = (''.join(re.findall(r'\w*>[\s\S]*?<', Date_t)))
        Date_t = (' '.join(re.findall(r'\d+', Date_t)))
        Date = re.split(' ', Date_t)
        return Date

    def Extract_OtherData(self):
        Other_Data_t_Feels_like = (''.join(re.findall(r'Feels like[\s\S]*?</a>', self.Weather_data)))
        Other_Data_t_Feels_like = (''.join(re.findall(r'[0-9]', Other_Data_t_Feels_like)).strip())
        Other_Data_t_Feels_like = "Feels like " + Other_Data_t_Feels_like + " °F, "

        Other_Data_t_Wind_ALL = (''.join(re.findall(r'<div id="CurrentDetailLineWindValue">[\s\S]*?">', self.Weather_data)))
        Other_Data_t_Wind = (''.join(re.findall(r'">[\s\S]*?<', Other_Data_t_Wind_ALL)))
        Other_Data_t_Wind = (''.join(re.findall(r'[A-Za-z0-9 ]', Other_Data_t_Wind)).strip())
        Other_Data_t_Wind_1 = (''.join(re.findall(r'the [\s\S]*?">', Other_Data_t_Wind_ALL)))
        Other_Data_t_Wind_1 = (''.join(re.findall(r'[A-Z]', Other_Data_t_Wind_1)).strip())
        Other_Data_t_Wind = "Wind " + Other_Data_t_Wind_1 + " " + Other_Data_t_Wind + ", "

        Other_Data_t_Barometer = (''.join(re.findall(r'<div id="CurrentDetailLinePressureValue">[\s\S]*?</span>', self.Weather_data)))
        Other_Data_t_Barometer = (''.join(re.findall(r'[0-9.]', Other_Data_t_Barometer)).strip())
        Other_Data_t_Barometer = "Barometer " + Other_Data_t_Barometer + " in, "

        Other_Data_t_Visibility = (''.join(re.findall(r'<div id="CurrentDetailLineVisibilityValue">[\s\S]*?</span>', self.Weather_data)))
        Other_Data_t_Visibility = (''.join(re.findall(r'>[\s\S]*?<', Other_Data_t_Visibility)))
        Other_Data_t_Visibility = (''.join(re.findall(r'[A-Za-z0-9 ]', Other_Data_t_Visibility)).strip())
        Other_Data_t_Visibility = "Visibility " + Other_Data_t_Visibility + ", "

        Other_Data_t_Humidit = (''.join(re.findall(r'<div id="CurrentDetailLineHumidityValue">[\s\S]*?</span>', self.Weather_data)))
        Other_Data_t_Humidit = (''.join(re.findall(r'[0-9%]', Other_Data_t_Humidit)).strip())
        Other_Data_t_Humidit = "Humidit " + Other_Data_t_Humidit + ", "

        Other_Data_t_Dew_point = (''.join(re.findall(r'<div id="CurrentDetailLineDewPointValue">[\s\S]*?</span>', self.Weather_data)))
        Other_Data_t_Dew_point = (''.join(re.findall(r'[0-9]', Other_Data_t_Dew_point)).strip())
        Other_Data_t_Dew_point = "Dew point " + Other_Data_t_Dew_point+ " °F"
        
        Other_Data = Other_Data_t_Feels_like + Other_Data_t_Wind + Other_Data_t_Barometer + Other_Data_t_Visibility + Other_Data_t_Humidit + Other_Data_t_Dew_point
        Other_Data   = re.split(', ', Other_Data)
        return Other_Data
    

    def Extract_Map(self):
        map_address = self.Extract_MapAddress()
        for i in range(0, 6):#10 sheets available, 6 defaults here
            logging.debug (map_address[i])
            Download_PNG(map_address[i], 'Weather/'+str(i)+'.png')
        #If you want to be faster, it is recommended to use multi-threading.

if __name__ == "__main__":
    Weather = Weather()
    
    print (Weather.Extract_OtherData())
    print (Weather.Extract_City())
    print (Weather.Extract_TemLow())
    print (Weather.Extract_TemHigh())
    print (Weather.Extract_Tem())
    print (Weather.Extract_Week())
    print (Weather.Extract_Wea())
    print (Weather.Extract_TemHourly())
    print (Weather.Extract_MapAddress())
    print (Weather.Extract_TimeHourly())
    print (Weather.Extract_Date())
    print (Weather.Extract_RealTimeWeather())
    # Weather.Extract_Map()

