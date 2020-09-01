#include "test.h"
#include "EPD_12in48.h"

int EPD_12in48_test(void)
{
	printf("12.48inch e-Paper Demo\r\n");
	DEV_ModuleInit();
	
	if(EPD_12in48_Init() != 0) {
				printf("e-Paper init failed\r\n");
		}else{
				printf("e-Paper init...\r\n");
		}
		EPD_12in48_Clear();		

#if 1   // show image for array   
    printf("show image for array\r\n");
    EPD_12in48_Display(gImage_b);
    DEV_Delay_ms(500);
#endif
		
#if 1   // Drawing on the image
		//Create a new image cache
    UBYTE *BlackImage;
		UWORD xsize = 648, ysize = 300;// 648 x 492 
    UWORD Imagesize = ((xsize % 8 == 0)? (xsize / 8 ): (xsize / 8 + 1)) * ysize;
    if((BlackImage = (UBYTE *)malloc(Imagesize)) == NULL) {
        printf("Failed to apply for black memory...\r\n");
        return -1;
    }
    printf("Paint_NewImage\r\n");
    Paint_NewImage(BlackImage, xsize, ysize, 0, WHITE);
    Paint_SelectImage(BlackImage);
    Paint_Clear(WHITE);	
		
		
    //1.Select Image
    printf("SelectImage:BlackImage\r\n");
    Paint_SelectImage(BlackImage);
    Paint_Clear(WHITE);
		
    // 2.Drawing on the image
    printf("Drawing:BlackImage\r\n");
    Paint_DrawPoint(10, 80, BLACK, DOT_PIXEL_1X1, DOT_STYLE_DFT);
    Paint_DrawPoint(10, 90, BLACK, DOT_PIXEL_2X2, DOT_STYLE_DFT);
    Paint_DrawPoint(10, 100, BLACK, DOT_PIXEL_3X3, DOT_STYLE_DFT);
    Paint_DrawLine(20, 70, 70, 120, BLACK, LINE_STYLE_SOLID, DOT_PIXEL_1X1);
    Paint_DrawLine(70, 70, 20, 120, BLACK, LINE_STYLE_SOLID, DOT_PIXEL_1X1);    
    Paint_DrawRectangle(20, 70, 70, 120, BLACK, DRAW_FILL_EMPTY, DOT_PIXEL_1X1);
    Paint_DrawRectangle(80, 70, 130, 120, BLACK, DRAW_FILL_FULL, DOT_PIXEL_1X1);
    Paint_DrawCircle(45, 95, 20, BLACK, DRAW_FILL_EMPTY, DOT_PIXEL_1X1);
    Paint_DrawCircle(105, 95, 20, WHITE, DRAW_FILL_FULL, DOT_PIXEL_1X1);
    Paint_DrawLine(85, 95, 125, 95, BLACK, LINE_STYLE_DOTTED, DOT_PIXEL_1X1);
    Paint_DrawLine(105, 75, 105, 115, BLACK, LINE_STYLE_DOTTED, DOT_PIXEL_1X1);
    Paint_DrawString_EN(10, 0, "waveshare", &Font16, BLACK, WHITE);
    Paint_DrawString_EN(10, 20, "hello world", &Font12, WHITE, BLACK);
    Paint_DrawNum(10, 33, 123456789, &Font12, BLACK, WHITE);
    Paint_DrawNum(10, 50, 987654321, &Font16, WHITE, BLACK);
    Paint_DrawString_CN(130, 0, " ���abc", &Font12CN, BLACK, WHITE);
    Paint_DrawString_CN(130, 20, "΢ѩ����", &Font24CN, WHITE, BLACK);

    printf("EPD_Display\r\n");
    EPD_12in48_Display648x300(BlackImage);
		free(BlackImage);
    BlackImage = NULL;
#endif

    DEV_Delay_ms(2000);
    printf("e-paper clear and sleep\n");
		EPD_12in48_Clear();
    EPD_12in48_Sleep();	
		
		printf("power off...\n");
		DEV_ModuleExit();
		return 0; 
}




