#include "test.h"
#include "EPD_12in48.h"

int EPD_12in48_test(void)
{
    printf("12.48inch e-Paper demo\r\n");
    DEV_ModuleInit();

    if(EPD_12in48_Init() != 0) {
        printf("e-Paper init failed\r\n");
        return -1;
    } else {
        printf("e-Paper init...\r\n");
    }
	printf("EPD_12in48_Clear \r\n");
    EPD_12in48_Clear();

    //Create a new image cache
    UBYTE  *BlackImage;
    UDOUBLE Imagesize = (((EPD_12in48_MAX_WIDTH%8==0)?(EPD_12in48_MAX_WIDTH/8):(EPD_12in48_MAX_WIDTH/8+1)) * EPD_12in48_MAX_HEIGHT);
    if((BlackImage = (UBYTE *)malloc(Imagesize)) == NULL) {
        printf("Failed to apply for black memory...\r\n");
        return -1;
    }

    Paint_NewImage(BlackImage, EPD_12in48_MAX_WIDTH, EPD_12in48_MAX_HEIGHT, 0, 0);
    Paint_SelectImage(BlackImage);
    Paint_Clear(WHITE);

#if 1   // Drawing on the image    
    printf("**************\r\n");
    printf("Drawing on the image:\r\n");

    //1.Select Image
    printf("SelectImage:BlackImage\r\n");
    Paint_SelectImage(BlackImage);
    Paint_Clear(WHITE);

    // 2.Drawing on the image
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
    Paint_DrawRectangle(500, 40, 900, 440, BLACK, DRAW_FILL_FULL, DOT_PIXEL_3X3);
    Paint_DrawCircle(240, 240, 180, BLACK, DRAW_FILL_EMPTY, DOT_PIXEL_3X3);
    Paint_DrawCircle(700, 240, 180, WHITE, DRAW_FILL_FULL, DOT_PIXEL_2X2);
    Paint_DrawLine(500, 40, 900, 440, BLACK, LINE_STYLE_DOTTED, DOT_PIXEL_2X2);
    Paint_DrawLine(500, 440, 900, 40, BLACK, LINE_STYLE_DOTTED, DOT_PIXEL_2X2);

    Paint_DrawString_EN(920, 50, "waveshare", &Font12, WHITE, BLACK);
    Paint_DrawString_EN(920, 60, "waveshare", &Font16, WHITE, BLACK);
    Paint_DrawString_EN(920, 75, "waveshare", &Font20, WHITE, BLACK);
    Paint_DrawString_EN(920, 90, "waveshare", &Font24, WHITE, BLACK);
    Paint_DrawString_EN(920, 120, "hello world", &Font24, WHITE, BLACK);
    Paint_DrawNum(920, 150, 123456789, &Font24, BLACK, WHITE);
    Paint_DrawNum(920, 180, 987654321, &Font24, WHITE, BLACK);
    Paint_DrawString_CN(920, 210,"ÄãºÃabcÊ÷Ý®ÅÉ", &Font24CN, BLACK, WHITE);
    Paint_DrawString_CN(920, 260,"Î¢Ñ©µç×Ó", &Font24CN, WHITE, BLACK);

    GUI_ReadBmp("./pic/icon.bmp", 0, 540);
    printf("EPD_Display\r\n");
    EPD_12in48_Display(BlackImage);
    DEV_Delay_ms(2000);

    printf("**************\r\n");
#endif

#if 1   // show bmp 
    printf("**************\r\n");
    printf("Read BMP file:\r\n");

    GUI_ReadBmp("./pic/1304x984.bmp", 0, 0);
    EPD_12in48_Display(BlackImage);
    DEV_Delay_ms(500);

    printf("**************\r\n");

#endif
    printf("Clear and goto Sleep mode...\r\n");
    Paint_SelectImage(BlackImage);
    Paint_Clear(WHITE);

    EPD_12in48_Clear();
    EPD_12in48_Sleep();
    free(BlackImage);
    BlackImage = NULL;

    return 0;
}

