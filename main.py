from machine import Pin,Timer
from motor_driver import *
from micropython import alloc_emergency_exception_buf
import time

alloc_emergency_exception_buf(100)
motor = motor_driver("GP13","GP12","GP11","GP10") 
irs=[Pin(i,Pin.IN) for i in range(18,23)]
min_motor_speed=40

kp=10
ki=0
kd=0
last_error=0
error=0
correction=0
error_sum=0
def measure():
    return [sensor.value() for sensor in irs]
def derivation(measurement):
    return sum(map(lambda x,y: x*y,measurement,[-4,-2,0,2,4]))/len(list(filter(lambda x: x == 0,measurement)))
def pid(timer):
    global error_sum
    global last_error
    global correction
    error_sum+=error
    derivative = error - last_error
    intergal = ki*error_sum
    #print(int(intergal))
    correction = int(error*kp + intergal + kd*derivative)
    last_error = error
    

timer= Timer(-1)
timer.init(mode=Timer.PERIODIC,callback=pid,freq=200)
with open("m.csv","a") as f:
    f.write("measurement,error,lasterror\n")
    while True:
        try:
            measurement = measure()
            #if measurement == 0b00000:
            #if measurement == [0,0,0,0,0]:
            if measurement == [1,1,1,1,1]:
                if last_error > 0:
                    error = 5
                else:
                    error = -5
            elif measurement == [0,0,0,0,0]:
            #elif measurement == [1,1,1,1,1]:
                motor.brake()
                time.sleep(5)
            else:
                error=int(derivation(measurement))
            motor.speed(min_motor_speed-correction,min_motor_speed+correction)
            f.write(f"{measurement},{error},{last_error}\n")
            f.flush()
        except KeyboardInterrupt as e:
            timer.deinit()
            raise e

