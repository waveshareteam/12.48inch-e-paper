/*****************************************************************************
* | File      	:   DEV_Config.c
* | Author      :   Waveshare team
* | Function    :   Hardware underlying interface
* | Info        :
*                Used to shield the underlying layers of each master
*                and enhance portability,software spi.
*----------------
* |	This version:   V1.0
* | Date        :   2018-11-29
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

void GPIO_Config(void)
{
    // SPI
    pinMode(EPD_SCK_PIN, OUTPUT);
    pinMode(EPD_MOSI_PIN, OUTPUT);

    // GPIO
    pinMode(EPD_M1_CS_PIN,  OUTPUT);
    pinMode(EPD_S1_CS_PIN,  OUTPUT);
    pinMode(EPD_M2_CS_PIN,  OUTPUT);
    pinMode(EPD_S2_CS_PIN,  OUTPUT);
    pinMode(EPD_M1S1_DC_PIN,  OUTPUT);
    pinMode(EPD_M2S2_DC_PIN,  OUTPUT);
    pinMode(EPD_M1S1_RST_PIN,  OUTPUT);
    pinMode(EPD_M2S2_RST_PIN,  OUTPUT);

    pinMode(EPD_M1_BUSY_PIN,  INPUT);
    pinMode(EPD_S1_BUSY_PIN,  INPUT);
    pinMode(EPD_M2_BUSY_PIN,  INPUT);
    pinMode(EPD_S2_BUSY_PIN,  INPUT);

    // Init
    DEV_Digital_Write(EPD_M1_CS_PIN,  HIGH);
    DEV_Digital_Write(EPD_S1_CS_PIN,  HIGH);
    DEV_Digital_Write(EPD_M2_CS_PIN,  HIGH);
    DEV_Digital_Write(EPD_S2_CS_PIN,  HIGH);
    DEV_Digital_Write(EPD_SCK_PIN, LOW);
	
	DEV_Digital_Write(EPD_SCK_PIN, 0);
    DEV_Digital_Write(EPD_MOSI_PIN, 0);
    DEV_Digital_Write(EPD_M1_CS_PIN,  0);
    DEV_Digital_Write(EPD_S1_CS_PIN,  0);
    DEV_Digital_Write(EPD_M2_CS_PIN,  0);
    DEV_Digital_Write(EPD_S2_CS_PIN,  0);
    DEV_Digital_Write(EPD_M1S1_DC_PIN,  0);
    DEV_Digital_Write(EPD_M2S2_DC_PIN,  0);
    DEV_Digital_Write(EPD_M1S1_RST_PIN,  0);
    DEV_Digital_Write(EPD_M2S2_RST_PIN,  0);
    DEV_Digital_Write(EPD_M1_BUSY_PIN,  0);
    DEV_Digital_Write(EPD_S1_BUSY_PIN,  0);
    DEV_Digital_Write(EPD_M2_BUSY_PIN,  0);
    DEV_Digital_Write(EPD_S2_BUSY_PIN,  0);
}
/******************************************************************************
function:	Module Initialize, the BCM2835 library and initialize the pins, SPI protocol
parameter:
Info:
******************************************************************************/
UBYTE DEV_ModuleInit(void)
{
    GPIO_Config();
    pinMode(LED, OUTPUT);
    return 0;
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

void DEV_TestLED(void)
{
    DEV_Digital_Write(LED, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(1000);              // wait for a second
    DEV_Digital_Write(LED, LOW);    // turn the LED off by making the voltage LOW
    delay(1000);              // wait for a second
}

/******************************************************************************
function:
			SPI read and write
******************************************************************************/
void DEV_SPI_WriteByte(UBYTE value)
{
    char i;
    DEV_Digital_Write(EPD_SCK_PIN, 0);
    for(i = 0; i < 8; i++) {
        DEV_Digital_Write(EPD_SCK_PIN, 0);
        DEV_Delay_us(5);
        if((value << i)  & 0x80) {
            DEV_Digital_Write(EPD_MOSI_PIN, 1);
        } else {
            DEV_Digital_Write(EPD_MOSI_PIN, 0);
        }
        DEV_Delay_us(5);
        DEV_Digital_Write(EPD_SCK_PIN, 1);
        DEV_Delay_us(5);
    }
}

UBYTE DEV_SPI_ReadByte(char x)
{
    UBYTE i,temp=0;
    
    // pinMode(EPD_MOSI_PIN,  INPUT);
    // for(i = 0; i < 8; i++) {
        // DEV_Digital_Write(EPD_SCK_PIN, 0);
        // temp = temp << 1;
        // DEV_Delay_us(5);
        // if(DEV_Digital_Read(EPD_MOSI_PIN) == 1) {
            // temp |= 0x01;
        // } else {
            // temp &= 0xfe;
        // }
        // DEV_Delay_us(5);
        // DEV_Digital_Write(EPD_SCK_PIN, 1);
        // DEV_Delay_us(5);
    // }    
    // pinMode(EPD_MOSI_PIN,  OUTPUT);
    
    return temp;
}
