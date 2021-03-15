# /*****************************************************************************
# * | File        :	  epd12in48.py
# * | Author      :   Waveshare electrices
# * | Function    :   Hardware underlying interface
# * | Info        :
# *----------------
# * |	This version:   V1.0
# * | Date        :   2019-11-01
# * | Info        :   
# ******************************************************************************/
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
import time
import logging

import epdconfig

import PIL
from PIL import Image

EPD_WIDTH       = 1304
EPD_HEIGHT      = 984

EDP_M1S2_WIDTH  = 648
EPD_M1S2_HEIGHT = 492

EDP_M2S1_WIDTH  = 656
EPD_M2S1_HEIGHT = 492

class EPD(object):
    def __init__(self):
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        
        self.EPD_M1_CS_PIN  = epdconfig.EPD_M1_CS_PIN
        self.EPD_S1_CS_PIN  = epdconfig.EPD_S1_CS_PIN
        self.EPD_M2_CS_PIN  = epdconfig.EPD_M2_CS_PIN
        self.EPD_S2_CS_PIN  = epdconfig.EPD_S2_CS_PIN

        self.EPD_M1S1_DC_PIN  = epdconfig.EPD_M1S1_DC_PIN
        self.EPD_M2S2_DC_PIN  = epdconfig.EPD_M2S2_DC_PIN

        self.EPD_M1S1_RST_PIN = epdconfig.EPD_M1S1_RST_PIN
        self.EPD_M2S2_RST_PIN = epdconfig.EPD_M2S2_RST_PIN

        self.EPD_M1_BUSY_PIN  = epdconfig.EPD_M1_BUSY_PIN
        self.EPD_S1_BUSY_PIN  = epdconfig.EPD_S1_BUSY_PIN
        self.EPD_M2_BUSY_PIN  = epdconfig.EPD_M2_BUSY_PIN
        self.EPD_S2_BUSY_PIN  = epdconfig.EPD_S2_BUSY_PIN

    def Init(self):
        if (epdconfig.module_init() != 0):
            return -1
        
        epdconfig.digital_write(self.EPD_M1_CS_PIN, 1)
        epdconfig.digital_write(self.EPD_S1_CS_PIN, 1)
        epdconfig.digital_write(self.EPD_M2_CS_PIN, 1)
        epdconfig.digital_write(self.EPD_S2_CS_PIN, 1)

        self.Reset()

        #panel setting
        self.M1_SendCommand(0x00) 
        self.M1_SendData(0x2f) 	#KW-3f   KWR-2F	BWROTP 0f	BWOTP 1f
        self.S1_SendCommand(0x00) 
        self.S1_SendData(0x2f) 
        self.M2_SendCommand(0x00) 
        self.M2_SendData(0x23) 
        self.S2_SendCommand(0x00) 
        self.S2_SendData(0x23) 

        # POWER SETTING
        self.M1_SendCommand(0x01)
        self.M1_SendData(0x07)
        self.M1_SendData(0x17)	# VGH=20V,VGL=-20V
        self.M1_SendData(0x3F)  # VDH=15V
        self.M1_SendData(0x3F)  # VDL=-15V
        self.M1_SendData(0x0d)
        self.M2_SendCommand(0x01)
        self.M2_SendData(0x07)
        self.M2_SendData(0x17)	# VGH=20V,VGL=-20V
        self.M2_SendData(0x3F)	# VDH=15V
        self.M2_SendData(0x3F)  # VDL=-15V
        self.M2_SendData(0x0d)
        
        # booster soft start
        self.M1_SendCommand(0x06)
        self.M1_SendData(0x17)	# A
        self.M1_SendData(0x17)	# B
        self.M1_SendData(0x39)	# C
        self.M1_SendData(0x17)
        self.M2_SendCommand(0x06)
        self.M2_SendData(0x17)
        self.M2_SendData(0x17)
        self.M2_SendData(0x39)
        self.M2_SendData(0x17)

        #resolution setting
        self.M1_SendCommand(0x61)
        self.M1_SendData(0x02)
        self.M1_SendData(0x88)	# source 648
        self.M1_SendData(0x01)	# gate 492
        self.M1_SendData(0xEC)
        self.S1_SendCommand(0x61)
        self.S1_SendData(0x02)
        self.S1_SendData(0x90)	# source 656
        self.S1_SendData(0x01)	# gate 492
        self.S1_SendData(0xEC)
        self.M2_SendCommand(0x61)
        self.M2_SendData(0x02)
        self.M2_SendData(0x90)	# source 656
        self.M2_SendData(0x01)	# gate 492
        self.M2_SendData(0xEC)
        self.S2_SendCommand(0x61)
        self.S2_SendData(0x02)
        self.S2_SendData(0x88)	# source 648
        self.S2_SendData(0x01)	# gate 492
        self.S2_SendData(0xEC)

        self.M1S1M2S2_SendCommand(0x15)	# DUSPI
        self.M1S1M2S2_SendData(0x20)

        self.M1S1M2S2_SendCommand(0x30)	# PLL
        self.M1S1M2S2_SendData(0x08)

        self.M1S1M2S2_SendCommand(0x50)	# Vcom and data interval setting
        self.M1S1M2S2_SendData(0x31)
        self.M1S1M2S2_SendData(0x07)

        self.M1S1M2S2_SendCommand(0x60) # TCON
        self.M1S1M2S2_SendData(0x22)

        self.M1_SendCommand(0xE0)   # POWER SETTING
        self.M1_SendData(0x01)
        self.M2_SendCommand(0xE0)	# POWER SETTING
        self.M2_SendData(0x01)

        self.M1S1M2S2_SendCommand(0xE3)
        self.M1S1M2S2_SendData(0x00)

        self.M1_SendCommand(0x82)
        self.M1_SendData(0x1c)
        self.M2_SendCommand(0x82)
        self.M2_SendData(0x1c)

        self.SetLut()

    def display(self, BlackImage, RedImage):
        start = time.perf_counter()

        # Check if we need to rotate the black image
        imwidth, imheight = BlackImage.size
        if(imwidth == self.width and imheight == self.height):
            black_image_temp = BlackImage
        elif(imwidth == self.height and imheight == self.width):
            black_image_temp = BlackImage.rotate(90, expand=True)
        else:
            logging.warning("Invalid black image dimensions: %d x %d, expected %d x %d" % (imwidth, imheight, self.width, self.height))
        image_monocolor = black_image_temp.convert('1')
        buf_black = bytearray(image_monocolor.tobytes('raw'))

        # Check if we need to rotate the red image
        imwidth, imheight = RedImage.size
        if(imwidth == self.width and imheight == self.height):
            red_image_temp = RedImage
        elif(imwidth == self.height and imheight == self.width):
            red_image_temp = RedImage.rotate(90, expand=True)
        else:
            logging.warning("Invalid red image dimensions: %d x %d, expected %d x %d" % (imwidth, imheight, self.width, self.height))
        image_monocolor = red_image_temp.convert('1')
        buf_red = bytearray(image_monocolor.tobytes('raw'))

        end = time.perf_counter()
        logging.debug("format pixels time: %f" % (end - start))
        start = time.perf_counter()

        buf_M2S1_black = [0xFF] * int((EDP_M2S1_WIDTH * EPD_M2S1_HEIGHT)/8)
        buf_M1S2_black = [0xFF] * int((EDP_M1S2_WIDTH * EPD_M1S2_HEIGHT)/8)
        buf_M2S1_red = [0x00] * int((EDP_M2S1_WIDTH * EPD_M2S1_HEIGHT)/8)
        buf_M1S2_red = [0x00] * int((EDP_M1S2_WIDTH * EPD_M1S2_HEIGHT)/8)

        #M1 part 648*492
        idx = 0
        for y in  range(492, 984):
            for x in  range(0, 81):
                buf_M1S2_black[idx] = buf_black[y*163 + x]
                buf_M1S2_red[idx] = buf_red[y*163 + x]
                idx += 1
        self.M1_SendCommand(0x10)
        self.M1_SendDataBulk(buf_M1S2_black)
        self.M1_SendCommand(0x13)
        self.M1_SendDataBulk(buf_M1S2_red)

        #S1 part 656*492
        idx = 0
        for y in  range(492, 984):
            for x in  range(81, 163):
                buf_M2S1_black[idx] = buf_black[y*163 + x]
                buf_M2S1_red[idx] = buf_red[y*163 + x]
                idx += 1
        self.S1_SendCommand(0x10)
        self.S1_SendDataBulk(buf_M2S1_black)
        self.S1_SendCommand(0x13)
        self.S1_SendDataBulk(buf_M2S1_red)

        #M2 part 656*492
        idx = 0
        for y in  range(0, 492):
            for x in  range(81, 163):
                buf_M2S1_black[idx] = buf_black[y*163 + x]
                buf_M2S1_red[idx] = buf_red[y*163 + x]
                idx += 1
        self.M2_SendCommand(0x10)
        self.M2_SendDataBulk(buf_M2S1_black)
        self.M2_SendCommand(0x13)
        self.M2_SendDataBulk(buf_M2S1_red)

        #S2 part 648*492
        idx = 0
        for y in  range(0, 492):
            for x in  range(0, 81):
                buf_M1S2_black[idx] = buf_black[y*163 + x]
                buf_M1S2_red[idx] = buf_red[y*163 + x]
                idx += 1
        self.S2_SendCommand(0x10)
        self.S2_SendDataBulk(buf_M1S2_black)
        self.S2_SendCommand(0x13)
        self.S2_SendDataBulk(buf_M1S2_red)

        end = time.perf_counter()
        logging.debug("send pixel time: %f" % (end - start))

        self.TurnOnDisplay()


    def clear(self):
        """Clear contents of image buffer"""
        start = time.perf_counter()

        # Set the black/white part of the display to white
        buf_M2S1_black = [0xFF] * int((EDP_M2S1_WIDTH * EPD_M2S1_HEIGHT)/8)
        buf_M1S2_black = [0xFF] * int((EDP_M1S2_WIDTH * EPD_M1S2_HEIGHT)/8)

        # Set the red part of the display to clear
        buf_M2S1_red = [0x00] * int((EDP_M2S1_WIDTH * EPD_M2S1_HEIGHT)/8)
        buf_M1S2_red = [0x00] * int((EDP_M1S2_WIDTH * EPD_M1S2_HEIGHT)/8)


        self.M1_SendCommand(0x10)
        self.M1_SendDataBulk(buf_M1S2_black)
        self.M1_SendCommand(0x13)
        self.M1_SendDataBulk(buf_M1S2_red)

        self.S1_SendCommand(0x10)
        self.S1_SendDataBulk(buf_M2S1_black)
        self.S1_SendCommand(0x13)
        self.S1_SendDataBulk(buf_M2S1_red)

        self.M2_SendCommand(0x10)
        self.M2_SendDataBulk(buf_M2S1_black)
        self.M2_SendCommand(0x13)
        self.M2_SendDataBulk(buf_M2S1_red)

        self.S2_SendCommand(0x10)
        self.S2_SendDataBulk(buf_M1S2_black)
        self.S2_SendCommand(0x13)
        self.S2_SendDataBulk(buf_M1S2_red)

        end = time.perf_counter()
        logging.debug("send clear pixel time: %f" % (end - start))

        self.TurnOnDisplay()
        
    def Reset(self):
        epdconfig.digital_write(self.EPD_M1S1_RST_PIN, 1)
        epdconfig.digital_write(self.EPD_M2S2_RST_PIN, 1)
        time.sleep(0.2)
        epdconfig.digital_write(self.EPD_M1S1_RST_PIN, 0)
        epdconfig.digital_write(self.EPD_M2S2_RST_PIN, 0)
        time.sleep(0.01)
        epdconfig.digital_write(self.EPD_M1S1_RST_PIN, 1)
        epdconfig.digital_write(self.EPD_M2S2_RST_PIN, 1)
        time.sleep(0.2)
    
    def EPD_Sleep(self):
        self.M1S1M2S2_SendCommand(0X02)
        time.sleep(0.3)

        self.M1S1M2S2_SendCommand(0X07)
        self.M1S1M2S2_SendData(0xA5) 
        time.sleep(0.3)
        logging.debug("module_exit")
        epdconfig.module_exit()

    def TurnOnDisplay(self):
        self.M1M2_SendCommand(0x04)
        time.sleep(0.3) 
        self.M1S1M2S2_SendCommand(0x12)
        self.M1_ReadBusy()
        # self.S1_ReadBusy()
        # self.M2_ReadBusy()
        # self.S2_ReadBusy()   
        
    """   M1S1M2S2 Write register address and data     """
    def M1S1M2S2_SendCommand(self, cmd):
        epdconfig.digital_write(self.EPD_M1S1_DC_PIN, 0)
        epdconfig.digital_write(self.EPD_M2S2_DC_PIN, 0)
        
        epdconfig.digital_write(self.EPD_M1_CS_PIN, 0)
        epdconfig.digital_write(self.EPD_S1_CS_PIN, 0)
        epdconfig.digital_write(self.EPD_M2_CS_PIN, 0)
        epdconfig.digital_write(self.EPD_S2_CS_PIN, 0)
        epdconfig.spi_writebyte([cmd]) 
        epdconfig.digital_write(self.EPD_M1_CS_PIN, 1)
        epdconfig.digital_write(self.EPD_S1_CS_PIN, 1)
        epdconfig.digital_write(self.EPD_M2_CS_PIN, 1)
        epdconfig.digital_write(self.EPD_S2_CS_PIN, 1)
    def M1S1M2S2_SendData(self, val):
        epdconfig.digital_write(self.EPD_M1S1_DC_PIN, 1)
        epdconfig.digital_write(self.EPD_M2S2_DC_PIN, 1)

        epdconfig.digital_write(self.EPD_M1_CS_PIN, 0)
        epdconfig.digital_write(self.EPD_S1_CS_PIN, 0)
        epdconfig.digital_write(self.EPD_M2_CS_PIN, 0)
        epdconfig.digital_write(self.EPD_S2_CS_PIN, 0)
        epdconfig.spi_writebyte([val]) 
        epdconfig.digital_write(self.EPD_M1_CS_PIN, 1)
        epdconfig.digital_write(self.EPD_S1_CS_PIN, 1)
        epdconfig.digital_write(self.EPD_M2_CS_PIN, 1)
        epdconfig.digital_write(self.EPD_S2_CS_PIN, 1)
    def M1S1M2S2_SendDataBulk(self, val):
        epdconfig.digital_write(self.EPD_M1S1_DC_PIN, 1)
        epdconfig.digital_write(self.EPD_M2S2_DC_PIN, 1)

        epdconfig.digital_write(self.EPD_M1_CS_PIN, 0)
        epdconfig.digital_write(self.EPD_S1_CS_PIN, 0)
        epdconfig.digital_write(self.EPD_M2_CS_PIN, 0)
        epdconfig.digital_write(self.EPD_S2_CS_PIN, 0)
        epdconfig.spi_writebytes(val) 
        epdconfig.digital_write(self.EPD_M1_CS_PIN, 1)
        epdconfig.digital_write(self.EPD_S1_CS_PIN, 1)
        epdconfig.digital_write(self.EPD_M2_CS_PIN, 1)
        epdconfig.digital_write(self.EPD_S2_CS_PIN, 1)

    """   M1M2 Write register address and data     """
    def M1M2_SendCommand(self, cmd):
        epdconfig.digital_write(self.EPD_M1S1_DC_PIN, 0)
        epdconfig.digital_write(self.EPD_M2S2_DC_PIN, 0)
        epdconfig.digital_write(self.EPD_M1_CS_PIN, 0)
        epdconfig.digital_write(self.EPD_M2_CS_PIN, 0)
        epdconfig.spi_writebyte([cmd])
        epdconfig.digital_write(self.EPD_M1_CS_PIN, 1)
        epdconfig.digital_write(self.EPD_M2_CS_PIN, 1)
    def M1M2_Sendata(self, val): 
        epdconfig.digital_write(self.EPD_M1S1_DC_PIN, 1)
        epdconfig.digital_write(self.EPD_M2S2_DC_PIN, 1)
        epdconfig.digital_write(self.EPD_M1_CS_PIN, 0)
        epdconfig.digital_write(self.EPD_M2_CS_PIN, 0)
        epdconfig.spi_writebyte([val])
        epdconfig.digital_write(self.EPD_M1_CS_PIN, 1)
        epdconfig.digital_write(self.EPD_M2_CS_PIN, 1)
    def M1M2_SendataBulk(self, val): 
        epdconfig.digital_write(self.EPD_M1S1_DC_PIN, 1)
        epdconfig.digital_write(self.EPD_M2S2_DC_PIN, 1)
        epdconfig.digital_write(self.EPD_M1_CS_PIN, 0)
        epdconfig.digital_write(self.EPD_M2_CS_PIN, 0)
        epdconfig.spi_writebytes(val)
        epdconfig.digital_write(self.EPD_M1_CS_PIN, 1)
        epdconfig.digital_write(self.EPD_M2_CS_PIN, 1)
          
    """   S2 Write register address and data     """
    def S2_SendCommand(self, cmd):
        epdconfig.digital_write(self.EPD_M2S2_DC_PIN, 0)
        epdconfig.digital_write(self.EPD_S2_CS_PIN, 0)
        epdconfig.spi_writebyte([cmd])
        epdconfig.digital_write(self.EPD_S2_CS_PIN, 1)
    def S2_SendData(self, val):
        epdconfig.digital_write(self.EPD_M2S2_DC_PIN, 1)
        epdconfig.digital_write(self.EPD_S2_CS_PIN, 0)
        epdconfig.spi_writebyte([val])
        epdconfig.digital_write(self.EPD_S2_CS_PIN, 1)
    def S2_SendDataBulk(self, val):
        epdconfig.digital_write(self.EPD_M2S2_DC_PIN, 1)
        epdconfig.digital_write(self.EPD_S2_CS_PIN, 0)
        epdconfig.spi_writebytes(val)
        epdconfig.digital_write(self.EPD_S2_CS_PIN, 1)
        
    """   M2 Write register address and data     """
    def M2_SendCommand(self, cmd):
        epdconfig.digital_write(self.EPD_M2S2_DC_PIN, 0)
        epdconfig.digital_write(self.EPD_M2_CS_PIN, 0)
        epdconfig.spi_writebyte([cmd]) 
        epdconfig.digital_write(self.EPD_M2_CS_PIN, 1)
    def M2_SendData(self, val):
        epdconfig.digital_write(self.EPD_M2S2_DC_PIN, 1)
        epdconfig.digital_write(self.EPD_M2_CS_PIN, 0)
        epdconfig.spi_writebyte([val]) 
        epdconfig.digital_write(self.EPD_M2_CS_PIN, 1)
    def M2_SendDataBulk(self, val):
        epdconfig.digital_write(self.EPD_M2S2_DC_PIN, 1)
        epdconfig.digital_write(self.EPD_M2_CS_PIN, 0)
        epdconfig.spi_writebytes(val)
        epdconfig.digital_write(self.EPD_M2_CS_PIN, 1)

    """   S1 Write register address and data     """
    def S1_SendCommand(self, cmd):
        epdconfig.digital_write(self.EPD_M1S1_DC_PIN, 0)
        epdconfig.digital_write(self.EPD_S1_CS_PIN, 0)
        epdconfig.spi_writebyte([cmd])
        epdconfig.digital_write(self.EPD_S1_CS_PIN, 1)
    def S1_SendData(self, val):
        epdconfig.digital_write(self.EPD_M1S1_DC_PIN, 1)
        epdconfig.digital_write(self.EPD_S1_CS_PIN, 0)
        epdconfig.spi_writebyte([val])
        epdconfig.digital_write(self.EPD_S1_CS_PIN, 1)
    def S1_SendDataBulk(self, val):
        epdconfig.digital_write(self.EPD_M1S1_DC_PIN, 1)
        epdconfig.digital_write(self.EPD_S1_CS_PIN, 0)
        epdconfig.spi_writebytes(val)
        epdconfig.digital_write(self.EPD_S1_CS_PIN, 1)
        
    """   M1 Write register address and data     """
    def M1_SendCommand(self, cmd):
        epdconfig.digital_write(self.EPD_M1S1_DC_PIN, 0)
        epdconfig.digital_write(self.EPD_M1_CS_PIN, 0)
        epdconfig.spi_writebyte([cmd])
        epdconfig.digital_write(self.EPD_M1_CS_PIN, 1)
    def M1_SendData(self, val):
        epdconfig.digital_write(self.EPD_M1S1_DC_PIN, 1)
        epdconfig.digital_write(self.EPD_M1_CS_PIN, 0)
        epdconfig.spi_writebyte([val])
        epdconfig.digital_write(self.EPD_M1_CS_PIN, 1)
    def M1_SendDataBulk(self, val):
        epdconfig.digital_write(self.EPD_M1S1_DC_PIN, 1)
        epdconfig.digital_write(self.EPD_M1_CS_PIN, 0)
        epdconfig.spi_writebytes(val)
        epdconfig.digital_write(self.EPD_M1_CS_PIN, 1)

    #Busy
    def M1_ReadBusy(self):
        self.M1_SendCommand(0x71) 
        busy = epdconfig.digital_read(self.EPD_M1_BUSY_PIN) 
        busy = not(busy & 0x01) 
        while(busy):
            self.M1_SendCommand(0x71) 
            busy = epdconfig.digital_read(self.EPD_M1_BUSY_PIN) 
            busy = not(busy & 0x01) 
        time.sleep(0.2)
    def M2_ReadBusy(self):
        self.M2_SendCommand(0x71) 
        busy = epdconfig.digital_read(self.EPD_M2_BUSY_PIN) 
        busy = not(busy & 0x01) 
        self.M2_SendCommand(0x71) 
        while(busy):
            self.M2_SendCommand(0x71) 
            busy = epdconfig.digital_read(self.EPD_M2_BUSY_PIN) 
            busy =not(busy & 0x01) 
        time.sleep(0.2)
    def S1_ReadBusy(self):
        self.S1_SendCommand(0x71) 
        busy = epdconfig.digital_read(self.EPD_S1_BUSY_PIN) 
        busy = not(busy & 0x01) 
        while(busy):
            self.S1_SendCommand(0x71) 
            busy = epdconfig.digital_read(self.EPD_S1_BUSY_PIN) 
            busy = not(busy & 0x01) 
        time.sleep(0.2)        
    def S2_ReadBusy(self):
        self.S2_SendCommand(0x71) 
        busy = epdconfig.digital_read(self.EPD_S2_BUSY_PIN) 
        busy = not(busy & 0x01) 
        while(busy):
            self.S2_SendCommand(0x71) 
            busy = epdconfig.digital_read(self.EPD_S2_BUSY_PIN) 
            busy = not(busy & 0x01) 
        time.sleep(0.2)            

    lut_vcom1 = [
        0x00,	0x10,	0x10,	0x01,	0x08,	0x01,
        0x00,	0x06,	0x01,	0x06,	0x01,	0x05,
        0x00,	0x08,	0x01,	0x08,	0x01,	0x06,
        0x00,	0x06,	0x01,	0x06,	0x01,	0x05,
        0x00,	0x05,	0x01,	0x1E,	0x0F,	0x06,
        0x00,	0x05,	0x01,	0x1E,	0x0F,	0x01,
        0x00,	0x04,	0x05,	0x08,	0x08,	0x01,
        0x00,	0x00,	0x00,	0x00,	0x00,	0x00,
        0x00,	0x00,	0x00,	0x00,	0x00,	0x00,
        0x00,	0x00,	0x00,	0x00,	0x00,	0x00,
    ]
    lut_ww1 = [
        0x91,	0x10,	0x10,	0x01,	0x08,	0x01,
        0x04,	0x06,	0x01,	0x06,	0x01,	0x05,
        0x84,	0x08,	0x01,	0x08,	0x01,	0x06,
        0x80,	0x06,	0x01,	0x06,	0x01,	0x05,
        0x00,	0x05,	0x01,	0x1E,	0x0F,	0x06,
        0x00,	0x05,	0x01,	0x1E,	0x0F,	0x01,
        0x08,	0x04,	0x05,	0x08,	0x08,	0x01,
        0x00,	0x00,	0x00,	0x00,	0x00,	0x00,
        0x00,	0x00,	0x00,	0x00,	0x00,	0x00,
        0x00,	0x00,	0x00,	0x00,	0x00,	0x00,
    ]
    lut_bw1 = [
        0xA8,	0x10,	0x10,	0x01,	0x08,	0x01,
        0x84,	0x06,	0x01,	0x06,	0x01,	0x05,
        0x84,	0x08,	0x01,	0x08,	0x01,	0x06,
        0x86,	0x06,	0x01,	0x06,	0x01,	0x05,
        0x8C,	0x05,	0x01,	0x1E,	0x0F,	0x06,
        0x8C,	0x05,	0x01,	0x1E,	0x0F,	0x01,
        0xF0,	0x04,	0x05,	0x08,	0x08,	0x01,
        0x00,	0x00,	0x00,	0x00,	0x00,	0x00,
        0x00,	0x00,	0x00,	0x00,	0x00,	0x00,
        0x00,	0x00,	0x00,	0x00,	0x00,	0x00,
    ]
    lut_wb1 = [
        0x91,	0x10,	0x10,	0x01,	0x08,	0x01,
        0x04,	0x06,	0x01,	0x06,	0x01,	0x05,
        0x84,	0x08,	0x01,	0x08,	0x01,	0x06,
        0x80,	0x06,	0x01,	0x06,	0x01,	0x05,
        0x00,	0x05,	0x01,	0x1E,	0x0F,	0x06,
        0x00,	0x05,	0x01,	0x1E,	0x0F,	0x01,
        0x08,	0x04,	0x05,	0x08,	0x08,	0x01,
        0x00,	0x00,	0x00,	0x00,	0x00,	0x00,
        0x00,	0x00,	0x00,	0x00,	0x00,	0x00,
        0x00,	0x00,	0x00,	0x00,	0x00,	0x00,
    ]
    lut_bb1 = [
        0x92,	0x10,	0x10,	0x01,	0x08,	0x01,
        0x80,	0x06,	0x01,	0x06,	0x01,	0x05,
        0x84,	0x08,	0x01,	0x08,	0x01,	0x06,
        0x04,	0x06,	0x01,	0x06,	0x01,	0x05,
        0x00,	0x05,	0x01,	0x1E,	0x0F,	0x06,
        0x00,	0x05,	0x01,	0x1E,	0x0F,	0x01,
        0x01,	0x04,	0x05,	0x08,	0x08,	0x01,
        0x00,	0x00,	0x00,	0x00,	0x00,	0x00,
        0x00,	0x00,	0x00,	0x00,	0x00,	0x00,
        0x00,	0x00,	0x00,	0x00,	0x00,	0x00,
    ]
    
    def SetLut(self):
        """Set the panel look up tables"""
        start = time.perf_counter()

        self.M1S1M2S2_SendCommand(0x20) #vcom
        self.M1S1M2S2_SendDataBulk(self.lut_vcom1)

        self.M1S1M2S2_SendCommand(0x21) #red not use
        self.M1S1M2S2_SendDataBulk(self.lut_ww1)

        self.M1S1M2S2_SendCommand(0x22) #bw r
        self.M1S1M2S2_SendDataBulk(self.lut_bw1)   # bw=r

        self.M1S1M2S2_SendCommand(0x23) #wb w
        self.M1S1M2S2_SendDataBulk(self.lut_wb1)   # wb=w

        self.M1S1M2S2_SendCommand(0x24) #bb b
        self.M1S1M2S2_SendDataBulk(self.lut_bb1)   # bb=b

        self.M1S1M2S2_SendCommand(0x25) #bb b
        self.M1S1M2S2_SendDataBulk(self.lut_ww1)   # bb=b

        end = time.perf_counter()
        logging.debug("set LUT time: %f" % (end - start))
