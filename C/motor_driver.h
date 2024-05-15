#ifndef MOTOR_DRIVER_H
#define MOTOR_DRIVER_H
#define PWM_RANGE 65535
// Include any necessary libraries here

// Define any constants or macros here

// Declare function prototypes here
void set_motor_speed(uint8_t pin_a,uint8_t pin_b,int speed);
void set_motors_speed(int speedLeft, int speedRight);
void motor_brake();
#endif // MOTOR_DRIVER_H