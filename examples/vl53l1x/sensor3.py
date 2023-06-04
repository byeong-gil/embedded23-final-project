import sys
import signal
import time

import VL53L1X
import RPi.GPIO as GPIO

# GPIO for Sensor1 shutdown pin
sensor1_shutdown = 23

# GPIO for Sensor2 shutdown pin
sensor2_shutdown = 24

# Setup GPIO for shutdown pins on each VL53L0X
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor1_shutdown, GPIO.OUT)
GPIO.setup(sensor2_shutdown, GPIO.OUT)

# Set all shutdown pins low to turn off each VL53L0X
GPIO.output(sensor1_shutdown, GPIO.LOW)
GPIO.output(sensor2_shutdown, GPIO.LOW)

# Keep all low for 500 ms or so to make sure they reset
time.sleep(0.50)

print("""
Press Ctrl+C to exit
""")

tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
tof.open()
GPIO.output(sensor_1_shutdown, GPIO.HIGH)
GPIO.output(sensor_2_shutdown, GPIO.HIGH)
tof.start_ranging(1) # 1 means short range

select = 0
count = 0

limit = 1000

running = True

def exit_handler(signal, frame):
    global running
    running = False
    tof.stop_ranging()
    print()
    sys.exit(0)

signal.signal(signal.SIGINT, exit_handler)

while 1:
    if select == 0:
        GPIO.output(sensor1_shutdown, GPIO.LOW)
        GPIO.output(sensor2_shutdown, GPIO.HIGH)

        while running:
            distance_in_mm = tof.get_distance()
             print("Distance_1: {}mm".format(distance_in_mm))
            time.sleep(0.1)
            count += 1
            if count == limit:
                count = 0
                select = 1
                break 

    else:
        GPIO.output(sensor1_shutdown, GPIO.HIGH)
        GPIO.output(sensor2_shutdown, GPIO.LOW)

        while running:
            distance_in_mm = tof.get_distance()
            print("Distance_2: {}mm".format(distance_in_mm))
            time.sleep(0.1)
            count += 1
            if count == limit: 
                count = 0 
                select = 0
                break 
