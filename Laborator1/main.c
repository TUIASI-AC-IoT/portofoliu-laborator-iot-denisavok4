#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#define GPIO_OUTPUT_IO 4
#define GPIO_OUTPUT_PIN_SEL (1ULL<<GPIO_OUTPUT_IO)
#define GPIO_INPUT_I1 2
#define GPIO_INPUT_PIN_SEL (1ULL<<GPIO_INPUT_I)

static QueueHandle_t gpio_evt_queue = NULL;
#define ESP_INTR_FLAG_DEFAULT 0

static void IRAM_ATTR gpio_isr_handler(void* arg)
{
    uint32_t gpio_num = (uint32_t) arg;
    xQueueSendFromISR(gpio_evt_queue, &gpio_num, NULL);
}

static void gpio_task_example(void* arg)
{
    uint32_t io_num;
    for (;;) {
        if (xQueueReceive(gpio_evt_queue, &io_num, portMAX_DELAY)) {
            printf("GPIO[%"PRIu32"] intr, val: %d\n", io_num, gpio_get_level(io_num));
        }
    }
}

void app_main() {
    //zero-initialize the config structure.
    gpio_config_t io_conf = {};
    //disable interrupt
    io_conf.intr_type = GPIO_INTR_DISABLE;
    //set as output mode
    io_conf.mode = GPIO_MODE_OUTPUT;
    //bit mask of the pins that you want to set
    io_conf.pin_bit_mask = GPIO_OUTPUT_PIN_SEL;
    //disable pull-down mode
    io_conf.pull_down_en = 0;
    //disable pull-up mode
    io_conf.pull_up_en = 0;
    //configure GPIO with the given settings
    gpio_config(&io_conf);

    xTaskCreate(gpio_task_example, "gpio_task_example", 2048, NULL, 10, NULL);

    //install gpio isr service
    gpio_install_isr_service(ESP_INTR_FLAG_DEFAULT);
    //hook isr handler for specific gpio pin
    gpio_isr_handler_add( GPIO_INPUT_I1, gpio_isr_handler, (void*) GPIO_INPUT_I1);
    //remove isr handler for gpio number.
    gpio_isr_handler_remove(GPIO_INPUT_I1);
    //hook isr handler for specific gpio pin again
    gpio_isr_handler_add(GPIO_INPUT_I1, gpio_isr_handler, (void*) GPIO_INPUT_I1);

    int cnt = 0;
    while(1) {
        printf("cnt: %d\n", cnt++);
        vTaskDelay(1000 / portTICK_PERIOD_MS);
        gpio_set_level(GPIO_OUTPUT_IO, cnt % 2);

        /*vTaskDelay(1000 / portTICK_PERIOD_MS);
        gpio_set_level(GPIO_OUTPUT_IO, 1);
        printf("1s\n");

        vTaskDelay(500 / portTICK_PERIOD_MS);
        gpio_set_level(GPIO_OUTPUT_IO, 0);
        printf("0.5s\n");

        vTaskDelay(250 / portTICK_PERIOD_MS);
        gpio_set_level(GPIO_OUTPUT_IO, 1);
        printf("0.25s\n");

        vTaskDelay(750 / portTICK_PERIOD_MS);
        gpio_set_level(GPIO_OUTPUT_IO, 0);
        printf("0.75s\n");*/

    }
}
