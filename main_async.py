from machine import Pin
from motor_driver import *
import network
import time
from microdot import Microdot,redirect
import asyncio
# Wi-Fi credentials
ssid = 'COSMOTE-657800'
password = 'esbbfu4n95g9s99c'



motor = motor_driver("GP13","GP12","GP11","GP10") 
irs=[machine.Pin(i,Pin.IN) for i in range(18,23)]
last_error = 0
min_motor_speed=25
lookup_table={0b00001:4,0b00011:3,0b00010:2,0b00110:1,0b00100:0,0b01100:-1,0b01000:-2,0b11000:-3,0b10000:-4}
p=10
error = 0
linefollow_task=None


# Connect to WLAN
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for Wi-Fi connection
connection_timeout = 10
while connection_timeout > 0:
    if wlan.status() >= 3:
        break
    connection_timeout -= 1
    print('Waiting for Wi-Fi connection...')
    time.sleep(1)

# Check if connection is successful
if wlan.status() != 3:
    raise RuntimeError('Failed to establish a network connection')
else:
    print('Connection successful!')
    network_info = wlan.ifconfig()
    print('IP address:', network_info[0])

# Set up socket and start listening



async def linefollow():
    try:
        global last_error
        global lookup_table
        global min_motor_speed
        global motor
        global p
        global error
        while True:
                measurement = 0
                for sensor in irs:
                    measurement = measurement << 1
                    measurement += sensor.value()
                if measurement == 0b00000:
                    if last_error > 0:
                        error = 5
                    else:
                        error = -5
                elif measurement == 0b11111:
                    motor.brake()
                    await asyncio.sleep(5)
                else:
                    error = lookup_table.get(measurement,0)
                error*=p
                motor.speed(min_motor_speed+error,min_motor_speed-error)
                last_error = error
                await asyncio.sleep_ms(0)
    except asyncio.CancelledError as e:
        motor.brake()
        raise e
    

app = Microdot()
state = "Off"
@app.route('/')
async def webpage(request):
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Ο ΑΚΟΛΟΥΘΗΤΗΣ</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <meta charset="UTF-8">
        </head>
        <body>
            <h1>Ο ΑΚΟΛΟΥΘΗΤΗΣ</h1>
            <h2>ΕΚΚΙΝΗΣΗ</h2>
            <form action="./start_following">
                <input type="submit" value="Start Following" />
            </form>
            <br>
            <form action="./stop_following">
                <input type="submit" value="Stop Following" />
            </form>
            <p>Program state: {state}</p>
            <p>Follow line: {running}</p>
        </body>
        </html>
        """
    return html,200,{'Content-Type': 'text/html'}

@app.route('/start_following')
async def start_following(request):
    global state
    global running
    global linefollow_task
    state = "On"
    if not running:
        linefollow_task = asyncio.create_task(linefollow())
        running = True
    return redirect('/')

@app.route('/stop_following')
async def stop_following(request):
    global state
    global running
    global linefollow_task
    state = "Off"
    if running:
        linefollow_task.cancel()
        running = False
    return redirect('/')

running = True
linefollow_task = asyncio.create_task(linefollow())    
app.run(port=80,debug=True)
