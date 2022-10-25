#include "DEV_Config.h"
#include "EPD_12in48.h"
#include "GUI_Paint.h"
#include "SRAM_23LC.h"
#include "imagedata.h"

void setup()
{
    DEV_ModuleInit();
    Serial.print("12.48 e-Paper\n");
 
}

void loop()
{
	Serial.print("Init \n");
	EPD_12in48_Init();
	SRAM_Init();
	    
    Serial.print("Clear \n");
	EPD_12in48_Clear();
	DEV_Delay_ms(500);  
	EPD_12in48_ClearBlack();
	DEV_Delay_ms(500);  
#if 0
    Serial.print("New Image and clear\n");
    Paint_NewImage(BLACKIMAGE,1304, 984, ROTATE_0, WHITE);
    Paint_Clear();
    
    Serial.print("Picture drawing, please wait...\n\r");
    Paint_SelectImage(BLACKIMAGE);
    Paint_DrawPoint(1200, 80, BLACK, DOT_PIXEL_1X1, DOT_STYLE_DFT);
    Paint_DrawPoint(1200, 85, BLACK, DOT_PIXEL_2X2, DOT_STYLE_DFT);
    Paint_DrawPoint(1200, 95, BLACK, DOT_PIXEL_3X3, DOT_STYLE_DFT);
    Paint_DrawPoint(1200, 110, BLACK, DOT_PIXEL_4X4, DOT_STYLE_DFT);
    Paint_DrawPoint(1200, 125, BLACK, DOT_PIXEL_5X5, DOT_STYLE_DFT);
    Paint_DrawPoint(1200, 160, BLACK, DOT_PIXEL_6X6, DOT_STYLE_DFT);
    Paint_DrawPoint(1200, 205, BLACK, DOT_PIXEL_7X7, DOT_STYLE_DFT);
    Paint_DrawPoint(1200, 260, BLACK, DOT_PIXEL_8X8, DOT_STYLE_DFT);

    Paint_DrawLine(40, 40, 440, 440, BLACK, LINE_STYLE_SOLID, DOT_PIXEL_3X3);
    Paint_DrawLine(440, 40, 40, 440, BLACK, LINE_STYLE_SOLID, DOT_PIXEL_3X3);
    Paint_DrawRectangle(40, 40, 440, 440, BLACK, DRAW_FILL_EMPTY, DOT_PIXEL_3X3);
    Paint_DrawRectangle(500, 40, 900, 440, BLACK, DRAW_FILL_EMPTY, DOT_PIXEL_3X3);
    Paint_DrawCircle(240, 240, 180, BLACK, DRAW_FILL_EMPTY, DOT_PIXEL_3X3);
    Paint_DrawCircle(700, 240, 180, BLACK, DRAW_FILL_EMPTY, DOT_PIXEL_2X2);
    Paint_DrawLine(500, 40, 900, 440, BLACK, LINE_STYLE_DOTTED, DOT_PIXEL_2X2);
    Paint_DrawLine(500, 440, 900, 40, BLACK, LINE_STYLE_DOTTED, DOT_PIXEL_2X2);

    Paint_DrawString_EN(920, 50, "waveshare", &Font12, WHITE, BLACK);
    Paint_DrawString_EN(920, 100, "waveshare", &Font16, WHITE, BLACK);
    Paint_DrawString_EN(920, 150, "waveshare", &Font20, WHITE, BLACK);
    Paint_DrawString_EN(920, 200, "waveshare", &Font24, WHITE, BLACK);
    Paint_DrawString_EN(920, 250, "hello world", &Font24, WHITE, BLACK);
    Paint_DrawNum(920, 300, 123456789, &Font24, BLACK, WHITE);
    Paint_DrawNum(920, 400, 987654321, &Font24, WHITE, BLACK);  

    Paint_DrawString_EN(920, 500, "waveshare", &Font12, WHITE, BLACK);
    Paint_DrawString_EN(920, 600, "waveshare", &Font16, WHITE, BLACK);
    Paint_DrawString_EN(920, 700, "waveshare", &Font20, WHITE, BLACK);
    Paint_DrawString_EN(920, 800, "waveshare", &Font24, WHITE, BLACK);
    Paint_DrawString_EN(920, 900, "hello world", &Font24, WHITE, BLACK);

    Paint_DrawString_EN(600, 500, "waveshare", &Font12, WHITE, BLACK);
    Paint_DrawString_EN(600, 600, "waveshare", &Font16, WHITE, BLACK);
    Paint_DrawString_EN(600, 700, "waveshare", &Font20, WHITE, BLACK);
    Paint_DrawString_EN(600, 800, "waveshare", &Font24, WHITE, BLACK);
    Paint_DrawString_EN(600, 900, "hello world", &Font24, WHITE, BLACK);

    Paint_DrawString_CN(200, 500, "abc树莓派", &Font12CN, WHITE, BLACK);
    Paint_DrawString_CN(200, 650, "abc树莓派", &Font24CN, WHITE, BLACK);
    Paint_DrawString_CN(200, 800, "微雪电子", &Font24CN, WHITE, BLACK);
    
    //Serial.print("EPD_Display\n");
    EPD_12in48_Display();
#endif

#if 1
    Paint_NewImage(BLACKIMAGE, 1304, 984, ROTATE_0, WHITE);
    Paint_Clear();
    
    Serial.print("Picture drawing, please wait...\n\r");
    Paint_DrawImage(gImage_240x240logo, 240, 0, 240, 240);
    Paint_DrawImage(gImage_240x240logo, 720, 0, 240, 240);
    Paint_DrawImage(gImage_240x240logo, 240, 240, 240, 240);
    Paint_DrawImage(gImage_240x240logo, 720, 240, 240, 240);
    Paint_DrawImage(gImage_240x240logo, 240, 492, 240, 240);
    Paint_DrawImage(gImage_240x240logo, 720, 492, 240, 240);
    Paint_DrawImage(gImage_240x240logo, 240, 732, 240, 240);
    Paint_DrawImage(gImage_240x240logo, 720, 732, 240, 240);
    
    Serial.print("EPD_Display\n");
    EPD_12in48_Display();
#endif   

    DEV_Delay_ms(500);
    Serial.print("EPD_Sleep\n");
    EPD_12in48_Clear();
    EPD_12in48_Sleep();
}
