/*****************************************************************************
* | File      	:   DEV_Config.h
* | Author      :   Waveshare electronics
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
#ifndef _DEV_CONFIG_H_
#define _DEV_CONFIG_H_

#include <stdint.h>
#include <stdio.h>
#include "Debug.h"
#include <SPI.h>

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
#define EPD_MOSI_PIN  11
#define EPD_MISO_PIN  12

#define EPD_M1_CS_PIN  2
#define EPD_S1_CS_PIN  3
#define EPD_M2_CS_PIN  A4
#define EPD_S2_CS_PIN  A0

#define EPD_M1S1_DC_PIN 6
#define EPD_M2S2_DC_PIN A3

#define EPD_M1S1_RST_PIN 5
#define EPD_M2S2_RST_PIN A2

#define EPD_M1_BUSY_PIN  4
#define EPD_S1_BUSY_PIN  7
#define EPD_M2_BUSY_PIN  A1
#define EPD_S2_BUSY_PIN  A5

#define SRAM_CS1_PIN 10
#define SRAM_CS2_PIN 9
#define SRAM_CS3_PIN 8

/**
 * GPIO read and write
**/
#define DEV_Digital_Write(_pin, _value) digitalWrite(_pin, _value == 0? LOW:HIGH)
#define DEV_Digital_Read(_pin) digitalRead(_pin)

/**
 * SPI
**/
#define DEV_SPI_WriteByte(__DATA) SPI.transfer(__DATA)
#define DEV_SPI_ReadByte(__DATA) SPI.transfer(__DATA)

/**
 * delay x ms
**/
#define DEV_Delay_ms(__xms) delay(__xms)

/*------------------------------------------------------------------------------------------------------*/
UBYTE DEV_ModuleInit(void);
void DEV_ModuleExit(void);


void DEV_Delay_us(UWORD xus);

#endif
