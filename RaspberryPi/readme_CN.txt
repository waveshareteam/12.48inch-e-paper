/*****************************************************************************
* | File      	:   Readme_CN.txt
* | Author      :   Waveshare team
* | Function    :   Help with use
* | Info        :
*----------------
* |	This version:   V1.1
* | Date        :   2022-09-14
* | Info        :   在这里提供一个中文版本的使用文档，以便你的快速使用
******************************************************************************/
这个文件是帮助您使用本例程。

1.基本信息：
本例程是基于树莓派3B进行开发的，例程均在树莓派3B上进行了验证;
本例程使用12.48inch e-Paper Module模块进行了验证。
本例程使用的是模拟SPI。

2.管脚连接：
管脚连接你可以在Config.py或者config.h中查看，这里也再重述一次：
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

3.基本使用：
由于本工程是一个综合工程，对于使用而言，你可能需要阅读以下内容：
C语言
    1. 安装库
        BCM2835库参见 ：http：//www.airspayce.com/mikem/bcm2835/
        WiringPi库参见：http://wiringpi.com/download-and-install/
        注: 对于树莓派4，WiringPi库需要更新为2.52或者以上版本才可以

    2. 将当前目录更改为Makefile和demo文件所在的位置。
    3. 编译文件：
            如果需要查看调试信息，请清除执行：
                make DEBUG = -DDEBUG
            使用不同的库需要在Makefile文件里去修改
                # USELIB = USE_BCM2835_LIB　　　　
                USELIB = USE_WIRINGPI_LIB
                # USELIB = USE_DEV_LIB
            注: USE_DEV_LIB为读取文件IO控制设备，速度慢但是不需要安装任何库
                在本例程成不建议使用USE_DEV_LIB,采用模拟SPI和文件控制IO口速度极其慢。
    4. 运行演示例程
        运行: sudo ./epd
python
    1. 安装库
        由于python调用的是C语言的库来加快数据传输速度
        所以需要安装对应的GPIO库和C语言的WiringPi库
            sudo python3 -m pip install requests
    2. 运行演示例程
        在python/examples文件夹下有4个例程全部支持python2/3
        测试代码
            如果是12.48 e-Paper 屏幕请运行
                运行：sudo python epd_12in48_test.py
                运行：sudo python3 epd_12in48_test.py
            如果是12.48 e-Paper (B)屏幕请运行
                运行：sudo python epd_12in48b_test.py
                运行：sudo python3 epd_12in48b_test.py
        扩展代码
            此程序需要连接网络
            Show_CN_Weather.py和Show_EN_Weather.py都是显示天气程序，需要连接网络，
            所以在使用前保证你的树莓派连接了互联网：
                运行：sudo python Show_CN_Weather.py help
                运行：sudo python Show_EN_Weather.py help
            可以看到帮助信息
            如果使用的12.48inch e-Paper(B)请在命令后面加上一个B的参数
                sudo python Show_CN_Weather.py B
                sudo python Show_EN_Weather.py B
             如果使用的12.48inch e-Paper则不需要加
                sudo python Show_CN_Weather.py
                sudo python Show_EN_Weather.py 
            Weather
                在Weather文件夹中，Get_CN_Weather.py和Get_EN_Weather.py采用了两种方法
                来获取天气，Get_CN_Weather.py采用调用API模式，但是只能查询到中国天气
                Show_EN_Weather.py采用爬网页数据，可以获取全球的天气，两者都是通过IP
                地址来确定城市。
                https://www.tianqiapi.com/
                https://www.msn.com/en-us/Weather

4.声明                           
    此程序全部只是提供用于学习用途，不得用于任何商业用途。如有侵权请联系我删除。
    http://www.waveshare.net
5. python程序分析
    这里只分析两个Show程序
    查找目录
        picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
        libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')

    设置输出日志等级
    logging.basicConfig(level=logging.INFO)
        日志等级
        DEBUG           详细信息，典型地调试问题时会感兴趣。 详细的debug信息。
        INFO            证明事情按预期工作。 关键事件。
        WARNING         表明发生了一些意外，或者不久的将来会发生问题（如‘磁盘满了’）。软件还是在正常工作。
        ERROR           由于更严重的问题，软件已不能执行一些功能了。 一般错误消息。
        CRITICAL        严重错误，表明软件已不能继续运行了。
        NOTICE          不是错误，但是可能需要处理。普通但是重要的事件。
        ALERT           需要立即修复，例如系统数据库损坏。
        EMERGENCY       紧急情况，系统不可用（例如系统崩溃），一般会通知所有用户。
        (你可以试一试改为logging.basicConfig(level=logging.DEBUG)看看出现了什么)

    输入的参数列表
        sys.argv[]

    访问互联网数据
        requests.get(Url, timeout=5)
        Url : 网址
        timeout： 超时








