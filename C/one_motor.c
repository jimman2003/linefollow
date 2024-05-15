#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "pico/time.h"
#include "hardware/pwm.h"
#include "hardware/clocks.h"

#define MOTOR_PWM_PIN_A 12 // Example pin for motor PWM A, change to your pin
#define MOTOR_PWM_PIN_B 13 // Example pin for motor PWM B, change to your pin
#define PWM_RANGE 65535    // PWM range
typedef uint32_t pin_size_t;
static uint32_t analogScale = 255;
static uint32_t analogFreq = 1000;
static uint32_t pwmInitted = 0;


void analogWrite(pin_size_t pin, int val) {
    
    if (!(pwmInitted & (1 << pwm_gpio_to_slice_num(pin)))) {
        pwm_config c = pwm_get_default_config();
        pwm_config_set_clkdiv(&c, clock_get_hz(clk_sys) / ((float)analogScale * analogFreq));
        pwm_config_set_wrap(&c, analogScale - 1);
        pwm_init(pwm_gpio_to_slice_num(pin), &c, true);
        pwmInitted |= 1 << pwm_gpio_to_slice_num(pin);
    }

    if (val < 0) {
        val = 0;
    } else if ((uint32_t)val > analogScale) {
        val = analogScale;
    }

    gpio_set_function(pin, GPIO_FUNC_PWM);
    pwm_set_gpio_level(pin, val);
}

void set_motor_speed(int speed) {
    if (speed >= 0) {
        analogWrite(MOTOR1_PWM_PIN_A, speed);
        analogWrite(MOTOR_PWM_PIN_B, 0);
    } else {
        analogWrite(MOTOR1_PWM_PIN_A, 0);
        analogWrite(MOTOR_PWM_PIN_B, -speed);
    }
}

int main() {
    stdio_init_all();
    
    int speedRight = 50; // Example speed, range from 0 to 100
    
    while (1) {
        speedRight = 50; // Change this to your desired speed control logic
        
        // Convert speed to PWM duty cycle range
        uint16_t pwm_duty = (uint16_t)((float)speedRight / 100.0f * (float)PWM_RANGE);
        
        set_motor_speed(pwm_duty);
        
        sleep_ms(100); // Example: control frequency, adjust as needed
    }
    
    return 0;
}