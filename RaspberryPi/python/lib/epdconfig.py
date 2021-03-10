# /*****************************************************************************
# * | File        :	  epdconfig.py
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
import os
import logging
import sys


class RaspberryPi:

    # Pin definitions
    EPD_M1_CS_PIN    = 8
    EPD_S1_CS_PIN    = 7
    EPD_M2_CS_PIN    = 17
    EPD_S2_CS_PIN    = 18

    EPD_M1S1_DC_PIN  = 13
    EPD_M2S2_DC_PIN  = 22

    EPD_M1S1_RST_PIN = 6
    EPD_M2S2_RST_PIN = 23

    EPD_M1_BUSY_PIN  = 5
    EPD_S1_BUSY_PIN  = 19
    EPD_M2_BUSY_PIN  = 27
    EPD_S2_BUSY_PIN  = 24

    def __init__(self):
        import spidev
        import RPi.GPIO

        logging.debug("Using RaspberryPi implementation.")

        self.GPIO = RPi.GPIO
        self.SPI = spidev.SpiDev()

    def digital_write(self, pin, value):
        self.GPIO.output(pin, value)

    def digital_read(self, pin):
        return self.GPIO.input(pin)

    def spi_writebyte(self, data):
        self.SPI.writebytes(data)

    def spi_writebytes(self, data):
        self.SPI.writebytes2(data)

    def spi_readbyte(self):
        bytes = self.SPI.readbytes(2)
        logging.debug("spi_readbyte: %s" % (str(bytes)))
        return bytes[0]

    def delay_ms(self, delaytime):
        time.sleep(delaytime / 1000.0)

    def module_init(self):
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setwarnings(False)

        logging.debug("python call wiringPi Lib")

        self.GPIO.setup(self.EPD_M2S2_RST_PIN, self.GPIO.OUT)
        self.GPIO.setup(self.EPD_M1S1_RST_PIN, self.GPIO.OUT)
        self.GPIO.setup(self.EPD_M2S2_DC_PIN, self.GPIO.OUT)
        self.GPIO.setup(self.EPD_M1S1_DC_PIN, self.GPIO.OUT)
        self.GPIO.setup(self.EPD_S1_CS_PIN, self.GPIO.OUT)
        self.GPIO.setup(self.EPD_S2_CS_PIN, self.GPIO.OUT)
        self.GPIO.setup(self.EPD_M1_CS_PIN, self.GPIO.OUT)
        self.GPIO.setup(self.EPD_M2_CS_PIN, self.GPIO.OUT)

        self.GPIO.setup(self.EPD_S1_BUSY_PIN, self.GPIO.IN)
        self.GPIO.setup(self.EPD_S2_BUSY_PIN, self.GPIO.IN)
        self.GPIO.setup(self.EPD_M1_BUSY_PIN, self.GPIO.IN)
        self.GPIO.setup(self.EPD_M2_BUSY_PIN, self.GPIO.IN)

        # SPI device, bus = 0, device = 0
        self.SPI.open(0, 0)
        self.SPI.max_speed_hz = 4000000
        self.SPI.mode = 0b00

        # Tell spidev we do not want the kernel SPI driver
        # using the CE01 line
        self.SPI.no_cs = True

        self.digital_write(self.EPD_M1_CS_PIN, 1)
        self.digital_write(self.EPD_S1_CS_PIN, 1)
        self.digital_write(self.EPD_M2_CS_PIN, 1)
        self.digital_write(self.EPD_S2_CS_PIN, 1)

        self.digital_write(self.EPD_M2S2_RST_PIN, 0)
        self.digital_write(self.EPD_M1S1_RST_PIN, 0)
        self.digital_write(self.EPD_M2S2_DC_PIN, 1)
        self.digital_write(self.EPD_M1S1_DC_PIN, 1)

        return 0

    def module_exit(self):
        self.SPI.close()
        logging.debug("close 5V, Module enters 0 power consumption ...")

        self.GPIO.output(self.EPD_M1S1_RST_PIN, 0)
        self.GPIO.output(self.EPD_M2S2_RST_PIN, 0)
        self.GPIO.output(self.EPD_M2S2_DC_PIN, 0)
        self.GPIO.output(self.EPD_M1S1_DC_PIN, 0)

        self.digital_write(self.EPD_S1_CS_PIN, 1)
        self.digital_write(self.EPD_S2_CS_PIN, 1)
        self.digital_write(self.EPD_M1_CS_PIN, 1)
        self.digital_write(self.EPD_M2_CS_PIN, 1)

        self.GPIO.cleanup()

  

if os.path.exists('/sys/bus/platform/drivers/gpiomem-bcm2835'):
    implementation = RaspberryPi()

for func in [x for x in dir(implementation) if not x.startswith('_')]:
    setattr(sys.modules[__name__], func, getattr(implementation, func))