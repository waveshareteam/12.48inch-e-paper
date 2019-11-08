/*****************************************************************************
* | File      	:   SRAM_23LC.h
* | Author      :   Waveshare electronics
* | Function    :	23LCxx Driver
* | Info        :   Driver for Microchip Technology Inc. 23LC (23LCV) SPI SRAM 
* |                 chips for AVR, SAM3X (Due), and SAM M0+ (SAMD, SAML, SAMC) 
* |                 microcontrollers on the Arduino platform.
*----------------
* | Supported Chips
* | 128KB
* | 23LCV1024
* | 23LC1024, 23A1024
* | 64KB
* | 23LCV512
* | 23LC512, 23A512
* | 32KB
* | 23A256, 23K256
* | 8KB
* | 23A640, 23K640
*----------------
* |	This version:   V2.0
* | Date        :   2019-03-15
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
#ifndef __SPI_RAM_H_
#define __SPI_RAM_H_

#include "DEV_Config.h"

// 128KB
#define ADDR_23LCV1024 128000
#define ADDR_23LC1024 128000
#define ADDR_23A1024 128000
// 64KB
#define ADDR_23LCV512 (64)
#define ADDR_23LC512 (64)
#define ADDR_23A512 (64)
// 32KB
#define ADDR_23A256 (32)
#define ADDR_23K256 (32)
// 8KB
#define ADDR_23A640 (8)
#define ADDR_23K640 (8)

#define ADDR_MAX ADDR_23LC1024

/**
 * SRAM opcodes
**/
#define CMD_WREN  0x06
#define CMD_WRDI  0x04
#define CMD_RDSR  0x05
#define CMD_WRSR  0x01
#define CMD_READ  0x03
#define CMD_WRITE 0x02

/**
 * SRAM modes
**/
#define BYTE_MODE   0x00
#define PAGE_MODE   0x80
#define STREAM_MODE 0x40


typedef struct {
    UBYTE CS_Pin;
} SRAM;

void SRAM_Init(void);
void SRAM_Set_Mode(UBYTE mode);

UBYTE SRAM_ReadByte(UDOUBLE Addr);
void SRAM_WriteByte(UDOUBLE Addr, UBYTE Data);

void SRAM_ReadPage(UDOUBLE Addr, UBYTE *pBuf);
void SRAM_WritePage(UDOUBLE Addr, UBYTE *pBuf);

void SRAM_ReadStream(UDOUBLE Addr, UBYTE *pBuf, UDOUBLE Len);
void SRAM_WriteStream(UDOUBLE Addr, UBYTE *pBuf, UDOUBLE Len);
#endif
