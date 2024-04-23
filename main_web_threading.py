from machine import Pin
from motor_driver import *
import network
import time
import socket
import _thread


# Wi-Fi credentials
ssid = 'COSMOTE-657800'
password = 'esbbfu4n95g9s99c'

running = False
state = "Off"

motor = motor_driver("GP13","GP12","GP11","GP10") 
irs=[machine.Pin(i,Pin.IN) for i in range(18,23)]
last_error = 0
min_motor_speed=25
lookup_table={0b00001:4,0b00011:3,0b00010:2,0b00110:1,0b00100:0,0b01100:-1,0b01000:-2,0b11000:-3,0b10000:-4}
p=10
error = 0

def webpage(state):
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Ο ΑΚΟΛΟΥΘΗΤΗΣ</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
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
        </body>
        </html>
        """
    return str(html)

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
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen()

print('Listening on', addr)

def linefollow(running):
    global last_error
    global lookup_table
    global min_motor_speed
    global motor
    global p
    global error
    
    while True:
        while running:
            measurement = 0
            for sensor in irs:
                measurement = measurement << 1
                measurement += sensor.value()  
            if measurement == 0b11111:
                motor.brake()
                time.sleep(5)
            else:
                error = lookup_table.get(measurement,0)
            error*=p
            motor.speed(min_motor_speed+error,min_motor_speed-error)
            
            
        #motor.brake()
    
_thread.start_new_thread(linefollow, ([True]))

while True:
    try:
        conn, addr = s.accept()
        print('Got a connection from', addr)
        
        # Receive and parse the request
        request = conn.recv(1024)
        request = str(request)
        

        try:
            request = request.split()[1]
            
        except IndexError:
            pass
        
        # Process the request and update variables
        if request == '/start_following?':
            running = True
            state = "ON"
            print("received state: ON ")
        elif request == '/stop_following?':
            running = False
            state = 'OFF'
            print("received state: OFF ")

        # Generate HTML response
        response = webpage(state)  

        # Send the HTTP response and close the connection
        conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        conn.send(response)
        conn.close()
    except OSError as e:
        conn.close()
        print('Connection closed')
