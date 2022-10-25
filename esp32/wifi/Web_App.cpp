/*****************************************************************************
* | File      	:   ESP32_Server.c
* | Author      :   Waveshare team
* | Function    :   Electronic paper driver
* | Info        :
*----------------
* | This version:   V1.0
* | Date        :   2019-07-15
* | Info        :
*
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documnetation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to  whom the Software is
* furished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
* THE SOFTWARE.
*
******************************************************************************/
#include "Web_App.h"
#include <WebServer.h>
#include <WiFi.h>
#include <WiFiClient.h>

//web 
#include "Web_Scripts.h" // JavaScript code
#include "Web_CSS.h"     // Cascading Style Sheets
#include "Web_HTML.h"    // HTML page of the tool

//e-paper
#include "EPD_12in48.h"
#include "EPD_12in48b.h"
#include "Debug.h"

void Web_EPD_Init();
void Web_EPD_LoadA();
void Web_EPD_LoadB();
void Web_EPD_Show();

const char *WIFI_ssid = "JSBPI"; //"your ssid";
const char *WIFI_password = "waveshare0755";   //"your password";

/* Server and IP address ------------------------------------------------------*/
WebServer server(80); // Wifi server exemplar using port 80
IPAddress myIP;       // IP address in your local wifi net

/* The 'index' page flag ------------------------------------------------------*/
bool isIndexPage = true; // true : GET  request, client needs 'index' page;
// false: POST request, server sends empty page.

void Web_Init(void)
{
    // Applying SSID and password
    Debugprint("Connecting to Wifi:");
    Debugprintln(WIFI_ssid);
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_ssid, WIFI_password);

    // Waiting the connection to a router
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Debugprint(".");
    }
    Debugprintln("\r\nWiFi connected");
    Debugprint("Server started, ip: ");
    Debugprintln(myIP = WiFi.localIP());

    server.on("/", Web_SendHTML);
    server.on("/index.css", Web_SendCSS);
	server.on("/Web_SendJS_A.js", Web_SendJS_A);
    server.on("/EPD", Web_EPD_Init);
    server.on("/LOADA", Web_EPD_LoadA);
    server.on("/LOADB", Web_EPD_LoadB);
    server.on("/SHOW", Web_EPD_Show);
    server.begin();
    Debugprintln("HTTP server started");
}

void Web_Listen(void)
{
    server.handleClient();
}

UDOUBLE Btime, RYtime;
String epd; 
void Web_EPD_Init()
{
    Btime = 0;
    RYtime = 0;
    epd = server.arg(0);
    if(epd == "12.48inch e-Paper"){
        Serial.println("12.48inch e-Paper");
        EPD_12in48_Init();
        // EPD_12in48_Clear();
    }else if(epd == "12.48inch e-Paper (B)"){
        Serial.println("12.48inch e-Paper b");
        EPD_12in48B_Init();
        // EPD_12in48B_Clear();
    }
    server.send(200, "text/plain", "Init ok\r\n");    
}


void Web_EPD_LoadA()
{
    Serial.println("Web_EPD_LoadA");
    String bimg = server.arg(0);

    Debugprintln(bimg.length());
    Debugprint("Btime = ");Debugprintln(Btime);

    UDOUBLE index = 0;
    while (index < bimg.length()) {
        // Get current byte
        int value = ((((int)bimg[index] - 'a') << 4) + (((int)bimg[index + 1] - 'a') & 0x0f));
        if(epd == "12.48inch e-Paper"){
            if(Btime == 0){ // 162 * 492 / 2
                Serial.println("12.48inch e-Paper LoadA S2");
                EPD_12in48_cmdS2();
            }else if(Btime == 39852){ // 164 * 492 / 2
                Serial.println("12.48inch e-Paper LoadA M2");
                EPD_12in48_cmdM2();
            }else if(Btime == 80196){ // 162 * 492 / 2
                Serial.println("12.48inch e-Paper LoadA M1");
                EPD_12in48_cmdM1();
            }else if(Btime == 120048){ // 164 * 492 / 2
                Serial.println("12.48inch e-Paper LoadA S1");
                EPD_12in48_cmdS1();
            }
        
            if(Btime < 39852){
                EPD_12in48_dataS2((byte)value);
            }else if(Btime < 80196 && Btime >= 39852){
                EPD_12in48_dataM2((byte)value);
            }else if(Btime < 120048 && Btime >= 80196){
                EPD_12in48_dataM1((byte)value);
            }else if(Btime >= 120048){
                EPD_12in48_dataS1((byte)value);
            }
        }else if(epd == "12.48inch e-Paper (B)"){
            if(Btime == 0){ // 162 * 492 / 2
                Serial.println("12.48inch e-Paper B LoadA S2");
                EPD_12in48B_cmd1S2();
            }else if(Btime == 39852){ // 164 * 492 / 2
                Serial.println("12.48inch e-Paper B LoadA M2");
                EPD_12in48B_cmd1M2();
            }else if(Btime == 80196){ // 162 * 492 / 2
                Serial.println("12.48inch e-Paper B LoadA M1");
                EPD_12in48B_cmd1M1();
            }else if(Btime == 120048){ // 164 * 492 / 2
                Serial.println("12.48inch e-Paper B LoadA S1");
                EPD_12in48B_cmd1S1();
            }
    
            if(Btime < 39852){
                EPD_12in48B_data1S2((byte)value);
            }else if(Btime < 80196 && Btime >= 39852){
                EPD_12in48B_data1M2((byte)value);
            }else if(Btime < 120048 && Btime >= 80196){
                EPD_12in48B_data1M1((byte)value);
            }else if(Btime >= 120048){
                EPD_12in48B_data1S1((byte)value);
            }
        }

        // Increment the current byte index on 2 characters
        index += 2;
        Btime++;
    }
    server.send(200, "text/plain", "Load image A ok\r\n");
}

void Web_EPD_LoadB()
{
    Serial.println("Web_EPD_LoadB");
    String ryimg = server.arg(0);

    Debugprintln(ryimg.length());
    Debugprint("RYtime = ");Debugprintln(RYtime);

    UDOUBLE index = 0;
    while (index < ryimg.length()) {
        // Get current byte
        int value = ((((int)ryimg[index] - 'a') << 4) + (((int)ryimg[index + 1] - 'a') & 0x0f));
        
        if(RYtime == 0){ // 162 * 492 / 2
            Serial.println("Web_EPD_LoadB 0");
            EPD_12in48B_cmd2S2();
        }else if(RYtime == 39852){ // 164 * 492 / 2
            Serial.println("Web_EPD_LoadB 2");
            EPD_12in48B_cmd2M2();
        }else if(RYtime == 80196){ // 162 * 492 / 2
            Serial.println("Web_EPD_LoadB 6");
            EPD_12in48B_cmd2M1();
        }else if(RYtime == 120048){ // 164 * 492 / 2
            Serial.println("Web_EPD_LoadB 8");
            EPD_12in48B_cmd2S1();
        }
    
        if(RYtime < 39852){
            EPD_12in48B_data2S2((byte)value);
        }else if(RYtime < 80196 && RYtime >= 39852){
            EPD_12in48B_data2M2((byte)value);
        }else if(RYtime < 120048 && RYtime >= 80196){
            EPD_12in48B_data2M1((byte)value);
        }else if(RYtime >= 120048){
            EPD_12in48B_data2S1((byte)value);
        }
    
        // Increment the current byte index on 2 characters
        index += 2;
        RYtime++;
    }
    server.send(200, "text/plain", "Load image B ok\r\n");
}

void Web_EPD_Show()
{
    Serial.println("Web_EPD_Show");
    String show = server.arg(0);
    Debugprintln(show);
    if(show == "12.48inch e-Paper"){
        EPD_12in48_TurnOnDisplay();
    }else if(show == "12.48inch e-Paper (B)"){
        EPD_12in48B_TurnOnDisplay();
    }

    server.send(200, "text/plain", "Show ok\r\n");
}