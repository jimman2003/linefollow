#include "pico/stdlib.h"
#include "motor_driver.h"
#include "hardware/gpio.h"
#include <stdio.h>

const uint min_motor_speed = 50;
int lookup_table[32] = {0};

const uint8_t ir_pins[] = {18, 19, 20, 21, 22};

int main()
{
    stdio_init_all();
    lookup_table[0b00001]=4;
    lookup_table[0b00011]=3;
    lookup_table[0b00010]=2;
    lookup_table[0b00110]=1;
    lookup_table[0b00100]=0;
    lookup_table[0b01100]=-1;
    lookup_table[0b01000]=-2;
    lookup_table[0b11000]=-3;
    lookup_table[0b10000]=-4;
    for (int i = 0; i < 5; i++)
    {
        gpio_init(ir_pins[i]);
        gpio_set_dir(ir_pins[i], GPIO_IN);
    }

    const uint8_t num_ir_sensors = 5;
    const uint8_t p = 10;
    int last_error = 0;

    while (true)
    {
        uint8_t measurement = 0;
        
        for (int i = 0; i < num_ir_sensors; i++)
        {
            measurement = measurement << 1;
            measurement |= gpio_get(ir_pins[i]);
        }

        int error = 0;
        if (measurement == 0b00000)
        {
            error = (last_error > 0) ? 5 : -5;
        }
        else if (measurement == 0b11111)
        {
            motor_brake();
            sleep_ms(5000);
            continue;
        }
        else
        {
            error = lookup_table[measurement];
        }
        printf("%d\n", measurement);
        set_motors_speed(min_motor_speed + (error*p), min_motor_speed - (error*p));
        last_error = error;
    }

    return 0;
}
