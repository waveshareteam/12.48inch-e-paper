/*****************************************************************************
* | File      	:   DEV_Config.c
* | Author      :   Waveshare team
* | Function    :   Hardware underlying interface
* | Info        :
*                Used to shield the underlying layers of each master
*                and enhance portability,software spi.
*----------------
* |	This version:   V1.0
* | Date        :   2019-03-18
* | Info        :

#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
******************************************************************************/
#include "DEV_Config.h"

static void DEV_GPIOConfig(void)
{
    pinMode(EPD_SCK_PIN, OUTPUT);
    pinMode(EPD_MOSI_PIN, OUTPUT);
    pinMode(EPD_MISO_PIN, INPUT);

    pinMode(EPD_M1_CS_PIN, OUTPUT);
    pinMode(EPD_S1_CS_PIN, OUTPUT);
    pinMode(EPD_M2_CS_PIN, OUTPUT);
    pinMode(EPD_S2_CS_PIN, OUTPUT);

    pinMode(EPD_M1S1_DC_PIN, OUTPUT);
    pinMode(EPD_M2S2_DC_PIN, OUTPUT);

    pinMode(EPD_M1S1_RST_PIN, OUTPUT);
    pinMode(EPD_M2S2_RST_PIN, OUTPUT);

    pinMode(EPD_M1_BUSY_PIN, INPUT);
    pinMode(EPD_S1_BUSY_PIN, INPUT);
    pinMode(EPD_M2_BUSY_PIN, INPUT);
    pinMode(EPD_S2_BUSY_PIN, INPUT);

    pinMode(SRAM_CS1_PIN, OUTPUT);
    pinMode(SRAM_CS2_PIN, OUTPUT);
    pinMode(SRAM_CS3_PIN, OUTPUT);
    
    DEV_Digital_Write(EPD_M1_CS_PIN, 1);
    DEV_Digital_Write(EPD_S1_CS_PIN, 1);
    DEV_Digital_Write(EPD_M2_CS_PIN, 1);
    DEV_Digital_Write(EPD_S2_CS_PIN, 1);
    DEV_Digital_Write(SRAM_CS1_PIN, 1);
    DEV_Digital_Write(SRAM_CS2_PIN, 1);
    DEV_Digital_Write(SRAM_CS3_PIN, 1);
}

/******************************************************************************
function:	initialize the pins, SPI, Serial
parameter:
Info:
******************************************************************************/
UBYTE DEV_ModuleInit(void)
{
    DEV_GPIOConfig();
    
    SPI.setDataMode(SPI_MODE0);
    SPI.setBitOrder(MSBFIRST);
    SPI.setClockDivider(SPI_CLOCK_DIV4);
    SPI.begin();

    Serial.begin(115200);
    return 0;
}

void DEV_ModuleExit(void)
{
    SPI.end();
    
    DEV_Digital_Write(EPD_M1_CS_PIN, 0);
    DEV_Digital_Write(EPD_S1_CS_PIN, 0);
    DEV_Digital_Write(EPD_M2_CS_PIN, 0);
    DEV_Digital_Write(EPD_S2_CS_PIN, 0);
    DEV_Digital_Write(SRAM_CS1_PIN, 0);
    DEV_Digital_Write(SRAM_CS2_PIN, 0);
    DEV_Digital_Write(SRAM_CS3_PIN, 0);
    
    DEV_Digital_Write(EPD_M1S1_DC_PIN, 0);
    DEV_Digital_Write(EPD_M2S2_DC_PIN, 0);
    DEV_Digital_Write(EPD_M1S1_RST_PIN, 0);
    DEV_Digital_Write(EPD_M2S2_RST_PIN, 0);
}

/******************************************************************************
function:	Microsecond delay
parameter:
Info:
******************************************************************************/
void DEV_Delay_us(UWORD xus)
{
    UWORD i;
    while(xus) {
        for(i = 0; i < 30; i++);
        xus--;
    }
}
