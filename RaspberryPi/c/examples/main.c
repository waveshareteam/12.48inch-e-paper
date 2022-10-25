#include <stdlib.h>     //exit()
#include <signal.h>     //signal()
#include <time.h>
#include "test.h"

int Version;

void  Handler(int signo)
{
    //System Exit
    printf("\r\nHandler:Goto Sleep mode\r\n");
    // EPD_12in48_Sleep();
    DEV_ModuleExit();
    exit(0);
}

int main(void)
{
    // Exception handling:ctrl + c
    signal(SIGINT, Handler);
    
	// EPD_12in48_test();
	// EPD_12in48B_test();
	EPD_12in48B_V2_test();
    
    
    DEV_ModuleExit();
    return 0;
}
