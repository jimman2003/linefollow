#include "pico/stdlib.h"
#include "pico/time.h"
#include "motor_driver.h"




int main() {
    stdio_init_all();
    
    int speedRight = 50; // Example speed, range from 0 to 100
    
    while (1) {
        //speedRight = 50; // Change this to your desired speed control logic
        
        // Convert speed to PWM duty cycle range
        //uint16_t pwm_duty = (uint16_t)((float)speedRight / 100.0f * (float)PWM_RANGE);
        
        set_motors_speed(254/2,254/2);
        sleep_ms(500); // Example: control frequency, adjust as needed
    }
    
    return 0;
}