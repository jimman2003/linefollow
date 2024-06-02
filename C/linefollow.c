#include "pico/stdlib.h"
#include <stdlib.h>
#include "pico/double.h"
#include "motor_driver.h"
#include "hardware/gpio.h"
#include <stdio.h>

const uint min_motor_speed = 1023 * 0.7; // up to 1023
int lookup_table[32] = {0};

const uint8_t ir_pins[] = {18, 19, 20, 21, 22}; // Pins of the Digital Outputs of the IR Sensor

int speed(int error) // Speed adjusting algorithm (not used)
{
    int ethresh = 0;
    int r = 5;
    int c = 1023 - min_motor_speed;
    int m = 2.2;
    double s = 0;
    if (abs(error) >= ethresh)
    {
        s = 1 - ((abs(error) - ethresh) / r - ethresh);
    }
    else
    {
        s = 1;
    }
    int test = min_motor_speed + c * (pow(s, m));
    // return  min_motor_speed + c * (pow(s,m));  //If we were to use it we would return this variable
    return 1023; // Bypass
}
int main()
{
    stdio_init_all();
    // Create Lookup table for the error
    lookup_table[0b00001] = 4;
    lookup_table[0b00011] = 3;
    lookup_table[0b00010] = 2;
    lookup_table[0b00110] = 1;
    lookup_table[0b00100] = 0;
    lookup_table[0b01100] = -1;
    lookup_table[0b01000] = -2;
    lookup_table[0b11000] = -3;
    lookup_table[0b10000] = -4;
    // Set up the IR sensors as inputs
    for (int i = 0; i < 5; i++)
    {
        gpio_init(ir_pins[i]);
        gpio_set_dir(ir_pins[i], GPIO_IN);
    }

    const uint8_t num_ir_sensors = 5;
    const uint8_t p = 150;
    int last_error = 0;

    while (true)
    {
        uint8_t measurement = 0;

        for (int i = 0; i < num_ir_sensors; i++) // Loop to get all sensor readouts
        {
            measurement = measurement << 1;
            measurement |= gpio_get(ir_pins[i]);
        }

        int error = 0;
        if (measurement == 0b00000) // If the robot is off the line (all white)
        {
            error = (last_error > 0) ? 5 : -5;
        }
        else if (measurement == 0b11111) // If the robot is off the line (all black)
        {
            motor_brake();
            sleep_ms(5000);
            continue;
        }
        else
        {
            error = lookup_table[measurement]; // For every other condition the error is selected from the LUT
        }
        printf("%d\n", measurement);
        // P Controller
        int left_motor = speed(error) + (error * p);
        int right_motor = speed(error) - (error * p);
        // Ensuring that the motors' speed is not negative
        if (left_motor < 0)
        {
            left_motor = 0;
        }
        if (right_motor < 0)
        {
            right_motor = 0;
        }
        set_motors_speed(left_motor, right_motor);
        last_error = error;
    }

    return 0;
}
