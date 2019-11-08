/*****************************************************************************
* | File      	:   Readme_EN.txt
* | Author      :   Waveshare team
* | Function    :   Help with use
* | Info        :
*----------------
* |	This version:   V1.0
* | Date        :   2019-06-25
* | Info        :   Here is an English version of the documentation for your quick use.
******************************************************************************/
This file is to help you use this routine.
1. Basic information:
This routine was developed based on Raspberry Pi 3B, and the routines were verified on Raspberry Pi 3B.
This routine was verified using the 12.48inch e-Paper Module.
This example uses an analog SPI.

2. Pin connection:
Pin connections can be viewed in Config.py or config.h, and are repeated here:
OLED              => RPI(BCM)
VCC               -> 3.3
GND               -> GND
EPD_SCK_PIN       -> 11
EPD_MOSI_PIN      -> 10

EPD_M1_CS_PIN     -> 8
EPD_S1_CS_PIN     -> 7
EPD_M2_CS_PIN     -> 17
EPD_S2_CS_PIN     -> 18

EPD_M1S1_DC_PIN   -> 13
EPD_M2S2_DC_PIN   -> 22

EPD_M1S1_RST_PIN  -> 6
EPD_M2S2_RST_PIN  -> 23

EPD_M1_BUSY_PIN   -> 5
EPD_S1_BUSY_PIN   -> 19
EPD_M2_BUSY_PIN   -> 27
EPD_S2_BUSY_PIN   -> 24

3. Basic use:
C language
     1. Install the library
         BCM2835 library see: http://www.airspayce.com/mikem/bcm2835/
         WiringPi library see: http://wiringpi.com/download-and-install/
         Note: For Raspberry Pi 4, the WiringPi library needs to be updated to version 2.52 or above.

     2. Change the current directory to the location of the Makefile and demo files.
     3. Compile the file:
             If you need to view the debug information, clear the execution:
                 Make DEBUG = -DDEBUG
             Using different libraries needs to be modified in the Makefile
                 # USELIB = USE_BCM2835_LIB
                 USELIB = USE_WIRINGPI_LIB
                 # USELIB = USE_DEV_LIB
             Note: USE_DEV_LIB is a read file IO control device, which is slow but does not require any libraries to be installed.
             In this example, it is not recommended to use USE_DEV_LIB, and the analog SPI and file control IO port is extremely slow.
    4. Run the demo routine
         Run: sudo ./epd

Python
    1. Install the library
        Because Python calls the C language library to speed up data transfer
        So you need to install the corresponding GPIO library and the WiringPi library in C language.
            Sudo python3 -m pip install requests
    2. Run the demo routine
        There are 4 routines in the python/examples folder that all support python2/3
        Test code
            If it is a 12.48 e-Paper screen please run
                Run: sudo python epd_12in48_test.py
                Run: sudo python3 epd_12in48_test.py
            If it is 12.48 e-Paper (B) screen please run
                Run: sudo python epd_12in48b_test.py
                Run: sudo python3 epd_12in48b_test.py
        Extension code
            This program needs to connect to the network
            Show_CN_Weather.py and Show_EN_Weather.py both show weather programs and need to connect to the network.
            So make sure your Raspberry Pi connects to the Internet before using it:
                Run: sudo python Show_CN_Weather.py help
                Run: sudo python Show_EN_Weather.py help
            Can see help information
            If you are using 12.48inch e-Paper (B), please add a B parameter after the command.
                Sudo python Show_CN_Weather.py B
                Sudo python Show_EN_Weather.py B
             If you use the 12.48inch e-Paper, you don't need to add
                Sudo python Show_CN_Weather.py
                Sudo python Show_EN_Weather.py
            Weather
                In the Weather folder, Get_CN_Weather.py and Get_EN_Weather.py use two methods.
                To get the weather, Get_CN_Weather.py uses the API mode, but only the weather in China.
                Show_EN_Weather.py uses crawling webpage data to get global weather, both through IP
                Address to determine the city.
                Https://www.tianqiapi.com/
                https://www.msn.com/en-us/Weather

4. Statement
    This program is provided for educational purposes only and should not be used for any commercial purpose. If there is any infringement, please contact me to delete.
    Http://www.waveshare.net
5. Python program analysis
    Only two show programs are analyzed here.
    Find directory
        Picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
        Libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')

    Set the output log level
    logging.basicConfig(level=logging.INFO)
        Log level
        DEBUG details, which are typically of interest when debugging problems. Detailed debug information.
        INFO proves that things work as expected. Key events.
        WARNING indicates that some accident has occurred, or that a problem will occur in the near future (such as 'disk full'). The software is still working.
        ERROR Due to a more serious problem, the software is no longer able to perform some functions. General error message.
        CRITICAL is a serious error indicating that the software is no longer working.
        NOTICE is not an error, but it may need to be processed. Ordinary but important event.
        ALERT needs to be fixed immediately, such as a system database corruption.
        EMERGENCY In case of emergency, the system is not available (for example, the system crashes) and all users are generally notified.
        (You can try changing to logging.basicConfig(level=logging.DEBUG) to see what happened)

    Input parameter list
        Sys.argv[]

    Access to internet data
        Requests.get(Url, timeout=5)
        Url: URL
        Timeout: timeout