/*****************************************************************************
* | File      	:   DEV_Config.h
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
#ifndef _DEV_CONFIG_H_
#define _DEV_CONFIG_H_

#include "main.h"

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
#define SPI_SCK_PIN  SPI1_SCK_GPIO_Port, SPI1_SCK_Pin
#define SPI_MOSI_PIN  SPI1_SCK_GPIO_Port, SPI1_MOSI_Pin
#define SPI_MISO_PIN  SPI1_MISO_GPIO_Port, SPI1_MISO_Pin

#define EPD_M1_CS_PIN  EPD_M1_CS_PIN_GPIO_Port, EPD_M1_CS_PIN_Pin
#define EPD_S1_CS_PIN  EPD_S1_CS_PIN_GPIO_Port, EPD_S1_CS_PIN_Pin
#define EPD_M2_CS_PIN  EPD_M2_CS_PIN_GPIO_Port, EPD_M2_CS_PIN_Pin
#define EPD_S2_CS_PIN  EPD_S2_CS_PIN_GPIO_Port, EPD_S2_CS_PIN_Pin

#define EPD_M1S1_DC_PIN  EPD_M1S1_DC_PIN_GPIO_Port, EPD_M1S1_DC_PIN_Pin
#define EPD_M2S2_DC_PIN  EPD_M2S2_DC_PIN_GPIO_Port, EPD_M2S2_DC_PIN_Pin

#define EPD_M1S1_RST_PIN EPD_M1S1_RST_PIN_GPIO_Port, EPD_M1S1_RST_PIN_Pin
#define EPD_M2S2_RST_PIN EPD_M2S2_RST_PIN_GPIO_Port, EPD_M2S2_RST_PIN_Pin

#define EPD_M1_BUSY_PIN  EPD_M1_BUSY_PIN_GPIO_Port, EPD_M1_BUSY_PIN_Pin
#define EPD_S1_BUSY_PIN  EPD_S1_BUSY_PIN_GPIO_Port, EPD_S1_BUSY_PIN_Pin
#define EPD_M2_BUSY_PIN  EPD_M2_BUSY_PIN_GPIO_Port, EPD_M2_BUSY_PIN_Pin
#define EPD_S2_BUSY_PIN  EPD_S2_BUSY_PIN_GPIO_Port, EPD_S2_BUSY_PIN_Pin

/**
 * GPIO read and write
**/
#define DEV_Digital_Write(_pin, _value) HAL_GPIO_WritePin(_pin, _value == 0? GPIO_PIN_RESET:GPIO_PIN_SET)
#define DEV_Digital_Read(_pin) HAL_GPIO_ReadPin(_pin)

/**
 * delay x ms
**/
#define DEV_Delay_ms(__xms) HAL_Delay(__xms)

/*------------------------------------------------------------------------------------------------------*/
UBYTE DEV_ModuleInit(void);
void DEV_Delay_us(UWORD xus);
UBYTE DEV_SPI_WriteByte(UBYTE value);
UBYTE DEV_SPI_ReadByte(UBYTE Reg);
void DEV_ModuleExit(void);


#endif
