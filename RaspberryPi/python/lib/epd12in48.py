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

        # panel setting
        self.M1_SendCommand(0x00)
        self.M1_SendData(0x1f)  #KW-3f   KWR-2F BWROTP 0f   BWOTP 1f
        self.S1_SendCommand(0x00)
        self.S1_SendData(0x1f)
        self.M2_SendCommand(0x00)
        self.M2_SendData(0x13)
        self.S2_SendCommand(0x00)
        self.S2_SendData(0x13)

        # booster soft start
        self.M1_SendCommand(0x06)
        # A B C
        self.M1_SendDataBulk([0x17, 0x17, 0x39, 0x17])
        self.M2_SendCommand(0x06)
        # A B C
        self.M2_SendDataBulk([0x17, 0x17, 0x39, 0x17])

        #resolution setting
        self.M1_SendCommand(0x61)
        # Source 648, Gate 492
        self.M1_SendDataBulk([0x02, 0x88, 0x01, 0xEC])

        self.S1_SendCommand(0x61)
        # Source 656, Gate 492
        self.S1_SendDataBulk([0x02, 0x90, 0x01, 0xEC])

        self.M2_SendCommand(0x61)
        # Source 656, Gate 492
        self.M2_SendDataBulk([0x02, 0x90, 0x01, 0xEC])

        self.S2_SendCommand(0x61)
        # Source 648, Gate 492
        self.S2_SendDataBulk([0x02, 0x88, 0x01, 0xEC])

        self.M1S1M2S2_SendCommand(0x15) # DUSPI
        self.M1S1M2S2_SendData(0x20)

        self.M1S1M2S2_SendCommand(0x50) # Vcom and data interval setting
        self.M1S1M2S2_SendData(0x21)    # Border KW
        self.M1S1M2S2_SendData(0x07)

        self.M1S1M2S2_SendCommand(0x60) # TCON
        self.M1S1M2S2_SendData(0x22)

        self.M1S1M2S2_SendCommand(0xE3)
        self.M1S1M2S2_SendData(0x00)

        # temperature
        # Hardcoded for now, SPI reads are not working right
        temp = 19 #self.M1_ReadTemperature()

        self.M1S1M2S2_SendCommand(0xe0) #Cascade setting
        self.M1S1M2S2_SendData(0x03)
        self.M1S1M2S2_SendCommand(0xe5) #Force temperature
        self.M1S1M2S2_SendData(temp)


    def display(self, image):
        start = time.perf_counter()

        # Check if we need to rotate the image
        imwidth, imheight = image.size
        if(imwidth == self.width and imheight == self.height):
            image_temp = image
        elif(imwidth == self.height and imheight == self.width):
            image_temp = image.rotate(90, expand=True)
        else:
            logging.warning("Invalid image dimensions: %d x %d, expected %d x %d" % (imwidth, imheight, self.width, self.height))

        image_monocolor = image_temp.convert('1')
        buf = bytearray(image_monocolor.tobytes('raw'))

        end = time.perf_counter()
        logging.debug("format pixels time:%f" % (end - start))
        start = time.perf_counter()

        buf_M2S1 = [0xFF] * int((EDP_M2S1_WIDTH * EPD_M2S1_HEIGHT)/8)
        buf_M1S2 = [0xFF] * int((EDP_M1S2_WIDTH * EPD_M1S2_HEIGHT)/8)

        #M1 part 648*492
        idx = 0
        for y in  range(492, 984):
            for x in  range(0, 81):
                buf_M1S2[idx] = buf[y*163 + x]
                idx += 1
        self.M1_SendCommand(0x13)
        self.M1_SendDataBulk(buf_M1S2)

        #S1 part 656*492
        idx = 0
        for y in  range(492, 984):
            for x in  range(81, 163):
                buf_M2S1[idx] = buf[y*163 + x]
                idx += 1
        self.S1_SendCommand(0x13)
        self.S1_SendDataBulk(buf_M2S1)

        #M2 part 656*492
        idx = 0
        for y in  range(0, 492):
            for x in  range(81, 163):
                buf_M2S1[idx] = buf[y*163 + x]
                idx += 1
        self.M2_SendCommand(0x13)
        self.M2_SendDataBulk(buf_M2S1)


        #S2 part 648*492
        idx = 0
        for y in  range(0, 492):
            for x in  range(0, 81):
                buf_M1S2[idx] = buf[y*163 + x]
                idx += 1
        self.S2_SendCommand(0x13)
        self.S2_SendDataBulk(buf_M1S2)

        end = time.perf_counter()
        logging.debug("send pixel time: %f" % (end - start))

        self.TurnOnDisplay()


    def clear(self):
        """Clear contents of image buffer"""
        start = time.perf_counter()

        buf_M2S1 = [0xFF] * int((EDP_M2S1_WIDTH * EPD_M2S1_HEIGHT)/8)
        buf_M1S2 = [0xFF] * int((EDP_M1S2_WIDTH * EPD_M1S2_HEIGHT)/8)

        self.M1_SendCommand(0x13)
        self.M1_SendDataBulk(buf_M1S2)

        self.S1_SendCommand(0x13)
        self.S1_SendDataBulk(buf_M2S1)

        self.M2_SendCommand(0x13)
        self.M2_SendDataBulk(buf_M2S1)

        self.S2_SendCommand(0x13)
        self.S2_SendDataBulk(buf_M1S2)

        end = time.perf_counter()
        logging.debug("send clear pixel time: %f" % (end - start))

        self.TurnOnDisplay()

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

    """   M1M2 Write register address and data     """
    def M1M2_SendCommand(self, cmd):
        epdconfig.digital_write(self.EPD_M1S1_DC_PIN, 0)
        epdconfig.digital_write(self.EPD_M2S2_DC_PIN, 0)
        epdconfig.digital_write(self.EPD_M1_CS_PIN, 0)
        epdconfig.digital_write(self.EPD_M2_CS_PIN, 0)
        epdconfig.spi_writebyte([cmd])
        epdconfig.digital_write(self.EPD_M1_CS_PIN, 1)
        epdconfig.digital_write(self.EPD_M2_CS_PIN, 1)

    def M1S1M2S2_Senddata(self, val):
        epdconfig.digital_write(self.EPD_M1S1_DC_PIN, 1)
        epdconfig.digital_write(self.EPD_M2S2_DC_PIN, 1)
        epdconfig.digital_write(self.EPD_M1_CS_PIN, 0)
        epdconfig.digital_write(self.EPD_M2_CS_PIN, 0)
        epdconfig.spi_writebyte([val])
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


    def Reset(self):
        logging.debug("epd12in48 Reset")
        epdconfig.digital_write(self.EPD_M1S1_RST_PIN, 1)
        epdconfig.digital_write(self.EPD_M2S2_RST_PIN, 1)
        time.sleep(0.2)
        epdconfig.digital_write(self.EPD_M1S1_RST_PIN, 0)
        epdconfig.digital_write(self.EPD_M2S2_RST_PIN, 0)
        time.sleep(0.001)
        epdconfig.digital_write(self.EPD_M1S1_RST_PIN, 1)
        epdconfig.digital_write(self.EPD_M2S2_RST_PIN, 1)
        time.sleep(0.2)
        logging.debug("epd12in48 Reset done")


    def EPD_Sleep(self):
        logging.debug("epd12in48 EPD_Sleep")
        self.M1S1M2S2_SendCommand(0X02)
        time.sleep(0.3)
        self.M1S1M2S2_SendCommand(0X07)
        self.M1S1M2S2_SendData(0xA5)
        time.sleep(0.3)
        epdconfig.module_exit()


    def TurnOnDisplay(self):
        start = time.perf_counter()
        self.M1M2_SendCommand(0x04)
        time.sleep(0.3)
        self.M1S1M2S2_SendCommand(0x12)
        self.S1_ReadBusy()
        self.M2_ReadBusy()
        self.S2_ReadBusy()
        self.M1_ReadBusy()
        end = time.perf_counter()
        logging.debug("display draw time: %f" % (end - start))


    #Busy
    def M1_ReadBusy(self):
        self.M1_SendCommand(0x71)
        busy = epdconfig.digital_read(self.EPD_M1_BUSY_PIN)
        busy = not(busy & 0x01)
        logging.debug("M1_ReadBusy")
        while(busy):
            self.M1_SendCommand(0x71)
            busy = epdconfig.digital_read(self.EPD_M1_BUSY_PIN)
            busy = not(busy & 0x01)

    def M2_ReadBusy(self):
        self.M2_SendCommand(0x71)
        busy = epdconfig.digital_read(self.EPD_M2_BUSY_PIN)
        busy = not(busy & 0x01)
        logging.debug("M2_ReadBusy")
        while(busy):
            self.M2_SendCommand(0x71)
            busy = epdconfig.digital_read(self.EPD_M2_BUSY_PIN)
            busy =not(busy & 0x01)

    def S1_ReadBusy(self):
        self.S1_SendCommand(0x71)
        busy = epdconfig.digital_read(self.EPD_S1_BUSY_PIN)
        busy = not(busy & 0x01)
        logging.debug("s1_ReadBusy")
        while(busy):
            self.S1_SendCommand(0x71)
            busy = epdconfig.digital_read(self.EPD_S1_BUSY_PIN)
            busy = not(busy & 0x01)

    def S2_ReadBusy(self):
        self.S2_SendCommand(0x71)
        busy = epdconfig.digital_read(self.EPD_S2_BUSY_PIN)
        busy = not(busy & 0x01)
        logging.debug("S2_ReadBusy")
        while(busy):
            self.S2_SendCommand(0x71)
            busy = epdconfig.digital_read(self.EPD_S2_BUSY_PIN)
            busy = not(busy & 0x01)


    def M1_ReadTemperature(self):
        self.M1_SendCommand(0x43)
        self.M1_ReadBusy()
        time.sleep(0.3)

        epdconfig.digital_write(self.EPD_M1_CS_PIN, 0)
        epdconfig.digital_write(self.EPD_S1_CS_PIN, 1)
        epdconfig.digital_write(self.EPD_M2_CS_PIN, 1)
        epdconfig.digital_write(self.EPD_S2_CS_PIN, 1)

        epdconfig.digital_write(self.EPD_M1S1_DC_PIN, 1)
        time.sleep(0.1)

        temp = epdconfig.spi_readbyte()
        logging.debug("Read Temperature Reg: %d" % temp)
        epdconfig.digital_write(self.EPD_M1_CS_PIN, 1)
        return temp

