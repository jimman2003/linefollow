#include "hardware/pwm.h"
#include "hardware/clocks.h"
#include "hardware/gpio.h"

#define MOTOR1_PWM_PIN_A 13 // Motor 1A
#define MOTOR1_PWM_PIN_B 12 // Motor 1B

#define MOTOR2_PWM_PIN_A 11 // Motor 2A
#define MOTOR2_PWM_PIN_B 10 // Motor 2B

static uint32_t analogScale = 1023;
static uint32_t analogFreq = 200;
static uint32_t pwmInitted = 0;
static bool scaleInitted = false;
static uint16_t analogWritePseudoScale = 1;
static uint16_t analogWriteSlowScale = 1;

// Inspired from arduino-pico library
void analogWrite(uint8_t pin, int val)
{
    if (!scaleInitted)
    {
        // For low frequencies, we need to scale the output max value up to achieve lower periods
        analogWritePseudoScale = 1;
        while (((clock_get_hz(clk_sys) / ((float)analogScale * analogFreq)) > 255.0) && (analogScale < 32678))
        {
            analogWritePseudoScale++;
            analogScale *= 2;
        }
        // For high frequencies, we need to scale the output max value down to actually hit the frequency target
        analogWriteSlowScale = 1;
        while (((clock_get_hz(clk_sys) / ((float)analogScale * analogFreq)) < 1.0) && (analogScale >= 6))
        {
            analogWriteSlowScale++;
            analogScale /= 2;
        }
        scaleInitted = true;
    }
    if (!(pwmInitted & (1 << pwm_gpio_to_slice_num(pin))))
    {
        pwm_config c = pwm_get_default_config();
        pwm_config_set_clkdiv(&c, clock_get_hz(clk_sys) / ((float)analogScale * analogFreq));
        pwm_config_set_wrap(&c, analogScale - 1);
        pwm_init(pwm_gpio_to_slice_num(pin), &c, true);
        pwmInitted |= 1 << pwm_gpio_to_slice_num(pin);
    }
    val <<= analogWritePseudoScale;
    val >>= analogWriteSlowScale;
    if (val < 0)
    {
        val = 0;
    }
    else if ((uint32_t)val > analogScale)
    {
        val = analogScale;
    }

    gpio_set_function(pin, GPIO_FUNC_PWM);
    pwm_set_gpio_level(pin, val);
}
//Adapted from https://github.com/CytronTechnologies/CytronMotorDriver/blob/master/CytronMotorDriver.cpp
void set_motor_speed(uint8_t pin_a,uint8_t pin_b,int speed)
{
    if (speed >= 0)
    {
        analogWrite(pin_a, speed);
        analogWrite(pin_b, 0);
    }
    else
    {
        analogWrite(pin_a, 0);
        analogWrite(pin_b, -speed);
    }
}
//Adapted from https://github.com/CytronTechnologies/CytronMotorDriver/blob/master/CytronMotorDriver.cpp
void set_motors_speed(int speedLeft, int speedRight){
    set_motor_speed(MOTOR1_PWM_PIN_A,MOTOR1_PWM_PIN_B,speedLeft);
    set_motor_speed(MOTOR2_PWM_PIN_A,MOTOR2_PWM_PIN_B,speedRight);
}
//Adapted from https://github.com/CytronTechnologies/CytronMotorDriver/blob/master/CytronMotorDriver.cpp
void motor_brake() {
    set_motors_speed(0,0);
}
