#include "DEV_Config.h"
#include "EPD_12in48b_V2.h"
#include "GUI_Paint.h"
#include "SRAM_23LC.h"
#include "imagedata.h"

void setup()
{
    DEV_ModuleInit();
    Serial.print("12.48inch e-Paper (B) V2\n");

}

void loop()
{
    SRAM_Init();
	Serial.print("Init \n");
    EPD_12in48B_V2_Init();
	
    Serial.print("Clear \n");
    EPD_12in48B_V2_Clear();
    DEV_Delay_ms(500);  
	Serial.print("Clear Black\n");
    EPD_12in48B_V2_ClearBlack();
    DEV_Delay_ms(500);  
	Serial.print("Clear Red\n");
    EPD_12in48B_V2_ClearRed();

#if 0
    Paint_NewImage(BLACKIMAGE, 1304, 984, ROTATE_0, WHITE);
    Paint_Clear();
    
    Paint_NewImage(REDIMAGE, 1304, 984, ROTATE_0, WHITE);
    Paint_Clear();
    
    Serial.print("Picture drawing, please wait...\n\r");
    Paint_SelectImage(BLACKIMAGE);
    Paint_DrawLine(40, 40, 440, 440, BLACK, LINE_STYLE_SOLID, DOT_PIXEL_3X3);
    Paint_DrawLine(440, 40, 40, 440, BLACK, LINE_STYLE_SOLID, DOT_PIXEL_3X3);
    Paint_DrawRectangle(40, 40, 440, 440, BLACK, DRAW_FILL_EMPTY, DOT_PIXEL_3X3);    
    Paint_DrawCircle(240, 240, 180, BLACK, DRAW_FILL_EMPTY, DOT_PIXEL_3X3);

    Paint_DrawString_EN(920, 50, "waveshare", &Font12, WHITE, BLACK);
    Paint_DrawString_EN(920, 100, "waveshare", &Font16, WHITE, BLACK);
    Paint_DrawString_EN(920, 150, "waveshare", &Font20, WHITE, BLACK);
    Paint_DrawNum(920, 200, 987654321, &Font24, WHITE, BLACK);  
    
    Paint_SelectImage(REDIMAGE);
    Paint_DrawPoint(1200, 125, RED, DOT_PIXEL_5X5, DOT_STYLE_DFT);
    Paint_DrawPoint(1200, 160, RED, DOT_PIXEL_6X6, DOT_STYLE_DFT);
    Paint_DrawPoint(1200, 205, RED, DOT_PIXEL_7X7, DOT_STYLE_DFT);
    Paint_DrawPoint(1200, 260, RED, DOT_PIXEL_8X8, DOT_STYLE_DFT);
    
    Paint_DrawLine(500, 40, 900, 440, RED, LINE_STYLE_DOTTED, DOT_PIXEL_2X2);
    Paint_DrawLine(500, 440, 900, 40, RED, LINE_STYLE_DOTTED, DOT_PIXEL_2X2);    
    Paint_DrawRectangle(500, 40, 900, 440, RED, DRAW_FILL_EMPTY, DOT_PIXEL_3X3);
    Paint_DrawCircle(700, 240, 180, RED, DRAW_FILL_EMPTY, DOT_PIXEL_2X2);
    
    Paint_DrawString_EN(920, 300, "waveshare", &Font16, WHITE, RED);
    Paint_DrawString_CN(920, 350, "微雪电子", &Font24CN, WHITE, RED);
    
    Serial.print("EPD_Display\n");
    EPD_12in48B_V2_Display();
#endif

#if 1
    Serial.print("New Image and clear\n");
    Paint_NewImage(BLACKIMAGE, 1304, 984, ROTATE_0, WHITE);
    Paint_Clear();
    
    Paint_NewImage(REDIMAGE, 1304, 984, ROTATE_0, WHITE);
    Paint_Clear();

    Serial.print("Picture drawing, please wait...\n\r");
    Paint_SelectImage(BLACKIMAGE);
    Paint_DrawImage(gImage_240x240logo, 240, 0, 240, 240);
    Paint_DrawImage(gImage_240x240logo, 720, 0, 240, 240);
    Paint_DrawImage(gImage_240x240logo, 240, 240, 240, 240);
    Paint_DrawImage(gImage_240x240logo, 720, 240, 240, 240);
    
    Paint_SelectImage(REDIMAGE);
    Paint_DrawImage(gImage_240x240logo, 240, 492, 240, 240);
    Paint_DrawImage(gImage_240x240logo, 720, 492, 240, 240);
    Paint_DrawImage(gImage_240x240logo, 240, 732, 240, 240);
    Paint_DrawImage(gImage_240x240logo, 720, 732, 240, 240);
    Serial.print("EPD_Display\n");
    EPD_12in48B_V2_Display();
#endif

    DEV_Delay_ms(500);    
    Serial.print("EPD_Sleep\n");
    EPD_12in48B_V2_Clear();
    EPD_12in48B_V2_Sleep();
}
