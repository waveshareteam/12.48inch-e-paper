/*****************************************************************************
* | File      	:   SRAM_23LC.c
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
#include "DEV_Config.h"
#include "SRAM_23LC.h"

// 3 chip
#define CHIPS 3
SRAM sram[CHIPS];

#define CHIPNUM(_addr) ((ADDR_MAX < _addr) ? (_addr / ADDR_MAX) : 0)
#define CHIPADDR(_addr) ((ADDR_MAX < _addr) ? (_addr % ADDR_MAX) : _addr)

void SRAM_ConfigChip(void);

/******************************************************************************
function:	Set the SRAM control mode
parameter:
See definition in SRAM.h, support byte mode, page mode, has any length mode
    BYTE_MODE
    PAGE_MODE
    STREAM_MODE
******************************************************************************/
void SRAM_Init(void)
{
    SRAM_ConfigChip();
    SRAM_Set_Mode(BYTE_MODE);
}

/******************************************************************************
function:	Set the SRAM control mode
parameter:
See definition in SRAM.h, support byte mode, page mode, has any length mode
    BYTE_MODE
    PAGE_MODE
    STREAM_MODE
******************************************************************************/
static void SRAM_ConfigChip(void)
{
    sram[0].CS_Pin = SRAM_CS1_PIN;
    sram[1].CS_Pin = SRAM_CS2_PIN;
    sram[2].CS_Pin = SRAM_CS3_PIN;
}

/******************************************************************************
function:	Set the SRAM control mode
parameter:
See definition in SRAM.h, support byte mode, page mode, has any length mode
    BYTE_MODE
    PAGE_MODE
    STREAM_MODE
******************************************************************************/
void SRAM_Set_Mode(UBYTE mode)
{
    UBYTE i = 0;
    for(i = 0; i < CHIPS; i++) {
        // Debug("cs = ");
        // Debug(sram[i].CS_Pin);
        // Debug("\n");
        DEV_Digital_Write(sram[i].CS_Pin, 0);

        DEV_SPI_WriteByte(CMD_WRSR);
        DEV_SPI_WriteByte(mode);

        DEV_Digital_Write(sram[i].CS_Pin, 1);
    }
}

/******************************************************************************
function:	Read one byte
parameter:
    Addr : An address
******************************************************************************/
UBYTE SRAM_ReadByte(UDOUBLE Addr)
{
    UBYTE Read_Byte;

    DEV_Digital_Write(sram[CHIPNUM(Addr)].CS_Pin, 0);
    DEV_SPI_WriteByte(CMD_READ);

    DEV_SPI_WriteByte((UBYTE)(CHIPADDR(Addr) >> 16));
    DEV_SPI_WriteByte((UBYTE)(CHIPADDR(Addr) >> 8));
    DEV_SPI_WriteByte((UBYTE)CHIPADDR(Addr));

    Read_Byte = DEV_SPI_ReadByte(0x00);
    DEV_Digital_Write(sram[CHIPNUM(Addr)].CS_Pin, 1);

    return Read_Byte;
}

/******************************************************************************
function:	Write a char data at an address
parameter:
    Addr : address
    Data : Written data
******************************************************************************/
void SRAM_WriteByte(UDOUBLE Addr, const UBYTE Data)
{    
    DEV_Digital_Write(sram[CHIPNUM(Addr)].CS_Pin, 0);
    
    DEV_SPI_WriteByte(CMD_WRITE);

    DEV_SPI_WriteByte((UBYTE)(CHIPADDR(Addr) >> 16));
    DEV_SPI_WriteByte((UBYTE)(CHIPADDR(Addr) >> 8));
    DEV_SPI_WriteByte((UBYTE)CHIPADDR(Addr));

    DEV_SPI_WriteByte(Data);
    DEV_Digital_Write(sram[CHIPNUM(Addr)].CS_Pin, 1);
}

/******************************************************************************
function:	Starting from an address, reading a page of data
parameter:
    Addr : address
    pBuf : A pointer to cache a page of data
******************************************************************************/
void SRAM_ReadPage(UDOUBLE Addr, UBYTE *pBuf)
{
    UWORD i;

    // Write Addr, read data
    DEV_Digital_Write(sram[CHIPNUM(Addr)].CS_Pin, 0);
    DEV_SPI_WriteByte(CMD_READ);

    DEV_SPI_WriteByte((UBYTE)(CHIPADDR(Addr) >> 16));
    DEV_SPI_WriteByte((UBYTE)(CHIPADDR(Addr) >> 8));
    DEV_SPI_WriteByte((UBYTE)CHIPADDR(Addr));

    for (i = 0; i < 32; i++) {
        *pBuf = DEV_SPI_ReadByte(0x00);
        pBuf++;
    }
    DEV_Digital_Write(sram[CHIPNUM(Addr)].CS_Pin, 1);
}

/******************************************************************************
function:	Write a page of data starting from an address
parameter:
    Addr : address
    pBuf : A pointer to cache a page of data
******************************************************************************/
void SRAM_WritePage(UDOUBLE Addr, UBYTE *pBuf)
{
    UWORD i;

    // Write Addr, read data
    DEV_Digital_Write(sram[CHIPNUM(Addr)].CS_Pin, 0);
    DEV_SPI_WriteByte(CMD_WRITE);

    DEV_SPI_WriteByte((UBYTE)(CHIPADDR(Addr) >> 16));
    DEV_SPI_WriteByte((UBYTE)(CHIPADDR(Addr) >> 8));
    DEV_SPI_WriteByte((UBYTE)CHIPADDR(Addr));

    for (i = 0; i < 32; i++) {
        DEV_SPI_WriteByte(*pBuf);
        pBuf++;
    }
    DEV_Digital_Write(sram[CHIPNUM(Addr)].CS_Pin, 1);
}

/******************************************************************************
function:	Read data of length Len from an address and store it in the buffer pointing to pBuf
parameter:
    Addr : address
    pBuf : A pointer to cache a page of data
    Len  : The length of data read
******************************************************************************/
void SRAM_ReadStream(UDOUBLE Addr, UBYTE *pBuf, UDOUBLE Len)
{
    UWORD i;

    // Write Addr, read data
    DEV_Digital_Write(sram[CHIPNUM(Addr)].CS_Pin, 0);
    DEV_SPI_WriteByte(CMD_READ);

    DEV_SPI_WriteByte((UBYTE)(CHIPADDR(Addr) >> 16));
    DEV_SPI_WriteByte((UBYTE)(CHIPADDR(Addr) >> 8));
    DEV_SPI_WriteByte((UBYTE)CHIPADDR(Addr));

    for (i = 0; i < Len; i++) {
        *pBuf = DEV_SPI_ReadByte(0x00);
        pBuf++;
    }
    DEV_Digital_Write(sram[CHIPNUM(Addr)].CS_Pin, 1);
}

/******************************************************************************
function:	Writing fixed-length data from an address
parameter:
    Addr : address
    pBuf : A pointer to cache a page of data
    Len  : The length of data write
******************************************************************************/
void SRAM_WriteStream(UDOUBLE Addr, UBYTE *pBuf, UDOUBLE Len)
{
    UWORD i;

    // Write Addr, read data
    DEV_Digital_Write(sram[CHIPNUM(Addr)].CS_Pin, 0);
    DEV_SPI_WriteByte(CMD_WRITE);

    DEV_SPI_WriteByte((UBYTE)(CHIPADDR(Addr) >> 16));
    DEV_SPI_WriteByte((UBYTE)(CHIPADDR(Addr) >> 8));
    DEV_SPI_WriteByte((UBYTE)CHIPADDR(Addr));

    for (i = 0; i < Len; i++) {
        DEV_SPI_WriteByte(*pBuf);
        pBuf++;
    }
    DEV_Digital_Write(sram[CHIPNUM(Addr)].CS_Pin, 1);
}
