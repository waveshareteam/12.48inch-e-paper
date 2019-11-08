/*****************************************************************************
* | File      	:   DEV_Config.h
* | Author      :   Waveshare team
* | Function    :   Hardware underlying interface
* | Info        :
*                Used to shield the underlying layers of each master
*                and enhance portability,software spi.
*----------------
* |	This version:   V1.0
* | Date        :   2019-02-26
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
#ifndef _DEV_CONFIG_H_
#define _DEV_CONFIG_H_

#include <Arduino.h>
#include <stdint.h>
#include <stdio.h>

/**
 * data
**/
#define UBYTE   uint8_t
#define UWORD   uint16_t
#define UDOUBLE uint32_t

/**
 * GPIO config
**/
#define EPD_SCK_PIN  13
#define EPD_MOSI_PIN 14

#define EPD_M1_CS_PIN 23
#define EPD_S1_CS_PIN 22
#define EPD_M2_CS_PIN 16
#define EPD_S2_CS_PIN 19

#define EPD_M1S1_DC_PIN  25
#define EPD_M2S2_DC_PIN  17

#define EPD_M1S1_RST_PIN 33
#define EPD_M2S2_RST_PIN 5

#define EPD_M1_BUSY_PIN  32
#define EPD_S1_BUSY_PIN  26
#define EPD_M2_BUSY_PIN  18
#define EPD_S2_BUSY_PIN  4

// 12.48 e-paper
#define EPD_12in48_SCK_PIN  EPD_SCK_PIN
#define EPD_12in48_MOSI_PIN EPD_MOSI_PIN

#define EPD_12in48_M1_CS_PIN EPD_M1_CS_PIN
#define EPD_12in48_S1_CS_PIN EPD_S1_CS_PIN
#define EPD_12in48_M2_CS_PIN EPD_M2_CS_PIN
#define EPD_12in48_S2_CS_PIN EPD_S2_CS_PIN

#define EPD_12in48_M1S1_DC_PIN  EPD_M1S1_DC_PIN
#define EPD_12in48_M2S2_DC_PIN  EPD_M2S2_DC_PIN

#define EPD_12in48_M1S1_RST_PIN EPD_M1S1_RST_PIN
#define EPD_12in48_M2S2_RST_PIN EPD_M2S2_RST_PIN

#define EPD_12in48_M1_BUSY_PIN  EPD_M1_BUSY_PIN
#define EPD_12in48_S1_BUSY_PIN  EPD_S1_BUSY_PIN
#define EPD_12in48_M2_BUSY_PIN  EPD_M2_BUSY_PIN
#define EPD_12in48_S2_BUSY_PIN  EPD_S2_BUSY_PIN

// 12.48 e-paper (B)
#define EPD_12in48b_SCK_PIN  EPD_SCK_PIN
#define EPD_12in48b_MOSI_PIN EPD_MOSI_PIN

#define EPD_12in48b_M1_CS_PIN EPD_M1_CS_PIN
#define EPD_12in48b_S1_CS_PIN EPD_S1_CS_PIN
#define EPD_12in48b_M2_CS_PIN EPD_M2_CS_PIN
#define EPD_12in48b_S2_CS_PIN EPD_S2_CS_PIN

#define EPD_12in48b_M1S1_DC_PIN  EPD_M1S1_DC_PIN
#define EPD_12in48b_M2S2_DC_PIN  EPD_M2S2_DC_PIN

#define EPD_12in48b_M1S1_RST_PIN EPD_M1S1_RST_PIN
#define EPD_12in48b_M2S2_RST_PIN EPD_M2S2_RST_PIN

#define EPD_12in48b_M1_BUSY_PIN  EPD_M1_BUSY_PIN
#define EPD_12in48b_S1_BUSY_PIN  EPD_S1_BUSY_PIN
#define EPD_12in48b_M2_BUSY_PIN  EPD_M2_BUSY_PIN
#define EPD_12in48b_S2_BUSY_PIN  EPD_S2_BUSY_PIN

#define LED 2


/**
 * GPIO read and write
**/
#define DEV_Digital_Write(_pin, _value) digitalWrite(_pin, _value == 0? LOW:HIGH)
#define DEV_Digital_Read(_pin) digitalRead(_pin)

/**
 * delay x ms
**/
#define DEV_Delay_ms(__xms) delay(__xms)

/*------------------------------------------------------------------------------------------------------*/
UBYTE DEV_ModuleInit(void);
void DEV_Delay_us(UWORD xus);
void DEV_TestLED(void);
void DEV_SPI_WriteByte(UBYTE value);
UBYTE DEV_SPI_ReadByte(char x);

#endif
