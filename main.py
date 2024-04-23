from machine import Pin
from motor_driver import *
import time
motor = motor_driver("GP13","GP12","GP11","GP10") 
irs=[machine.Pin(i,Pin.IN) for i in range(18,23)]
min_motor_speed=35
lookup_table={0b00001:4,0b00011:3,0b00010:2,0b00110:1,0b00100:0,0b01100:-1,0b01000:-2,0b11000:-3,0b10000:-4}

p=8
last_error=0
error=0
def measure():
    return [sensor.value() for sensor in irs]
def derivation(measurement):
    return sum(map(lambda x,y: x*y,measurement,[-4,-2,0,2,4]))/len(list(filter(lambda x: x == 0,measurement)))

with open("m.csv","a") as f:
    f.write("measurement,error,lasterror\n")
    while True:
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
            #error = lookup_table.get(measurement,0)
            error=int(derivation(measurement))
        motor.speed(min_motor_speed-(error*p),min_motor_speed+(error*p))
        last_error = error
        f.write(f"{measurement},{error},{last_error}\n")
        f.flush()

def measure_og():
    measurement = 0
    for sensor in irs:
        measurement = measurement << 1
        measurement +=sensor.value()
    return measurement

