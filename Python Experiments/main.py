from machine import Pin
from motor_driver import *
import time 
motor = motor_driver("GP13","GP12","GP11","GP10") 
irs=[machine.Pin(i,Pin.IN) for i in range(18,23)]
lookup_table={0b00001:4,0b00011:3,0b00010:2,0b00110:1,0b00100:0,0b01100:-1,0b01000:-2,0b11000:-3,0b10000:-4}
p=10
last_error=0
error=0
def speed (error):
    min_speed = 40
    ethresh = 0
    ρ = 5
    c = (100-min_speed)
    μ = 1.1
    if abs(error)>=ethresh:
        s= 1 - ((abs(error)-ethresh)/ρ-ethresh)
    else:
        s = 1     
    speed = min_speed +  c*(s**μ)
    return int(speed)
@rp2.asm_pio(set_init=rp2.PIO.IN_LOW,autopush=True)
def read_sensors():
    in_(pins, 5)
    
sm = rp2.StateMachine(0,read_sensors, freq=1_000_000, in_base=machine.Pin(18), push_thresh=5)

 
sm.active(1)
while True:
    measurement = sm.get()
    print(bin(measurement))
    if measurement == 0b00000:
        if last_error > 0:
            error = 5
        else:
            error = -5
    elif measurement == 0b11111:
        motor.brake()
        #time.sleep(5)
    else:
        error = lookup_table.get(measurement,0)
    accel=speed(error)
    motor.speed(accel+(error*p),accel-(error*p))
    last_error = error
    time.sleep(0.01)


