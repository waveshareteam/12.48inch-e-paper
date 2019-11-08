/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2019 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f1xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define EPD_M1_BUSY_PIN_Pin GPIO_PIN_0
#define EPD_M1_BUSY_PIN_GPIO_Port GPIOF
#define EPD_S1_BUSY_PIN_Pin GPIO_PIN_1
#define EPD_S1_BUSY_PIN_GPIO_Port GPIOF
#define EPD_M2_BUSY_PIN_Pin GPIO_PIN_2
#define EPD_M2_BUSY_PIN_GPIO_Port GPIOF
#define EPD_S2_BUSY_PIN_Pin GPIO_PIN_3
#define EPD_S2_BUSY_PIN_GPIO_Port GPIOF
#define EPD_M1_CS_PIN_Pin GPIO_PIN_4
#define EPD_M1_CS_PIN_GPIO_Port GPIOF
#define EPD_S1_CS_PIN_Pin GPIO_PIN_5
#define EPD_S1_CS_PIN_GPIO_Port GPIOF
#define EPD_M2_CS_PIN_Pin GPIO_PIN_6
#define EPD_M2_CS_PIN_GPIO_Port GPIOF
#define EPD_S2_CS_PIN_Pin GPIO_PIN_7
#define EPD_S2_CS_PIN_GPIO_Port GPIOF
#define SPI1_SCK_Pin GPIO_PIN_5
#define SPI1_SCK_GPIO_Port GPIOA
#define SPI1_MISO_Pin GPIO_PIN_6
#define SPI1_MISO_GPIO_Port GPIOA
#define SPI1_MOSI_Pin GPIO_PIN_7
#define SPI1_MOSI_GPIO_Port GPIOA
#define EPD_M1S1_DC_PIN_Pin GPIO_PIN_0
#define EPD_M1S1_DC_PIN_GPIO_Port GPIOB
#define EPD_M2S2_DC_PIN_Pin GPIO_PIN_1
#define EPD_M2S2_DC_PIN_GPIO_Port GPIOB
#define EPD_M1S1_RST_PIN_Pin GPIO_PIN_2
#define EPD_M1S1_RST_PIN_GPIO_Port GPIOB
#define EPD_M2S2_RST_PIN_Pin GPIO_PIN_3
#define EPD_M2S2_RST_PIN_GPIO_Port GPIOB
/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
