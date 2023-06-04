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

tof_1 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
tof_1.open()

tof_1.start_ranging(1) # 1 means short range

tof_2 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
tof_2.open()

tof_2.start_ranging(1) # 1 means short range

select = 0
count = 0

limit = 1000

running = True

def exit_handler_1(signal, frame):
    global running
    running = False
    tof_1.stop_ranging()
    print()
    sys.exit(0)

def exit_handler_2(signal, frame):
    global running
    running = False
    tof_2.stop_ranging()
    print()
    sys.exit(0)

while 1:
    if select == 0:
        signal.signal(signal.SIGINT, exit_handler_1)

        GPIO.output(sensor1_shutdown, GPIO.HIGH)
        GPIO.output(sensor2_shutdown, GPIO.LOW)

        while running:
            distance_in_mm = tof_1.get_distance()
            print("Distance_1: {}mm".format(distance_in_mm))
            time.sleep(0.1)
            count += 1
            if count == limit:
                count = 0
                select = 1 

    else:
        signal.signal(signal.SIGINT, exit_handler_2)

        GPIO.output(sensor1_shutdown, GPIO.LOW)
        GPIO.output(sensor2_shutdown, GPIO.HIGH)

        while running:
            distance_in_mm = tof_2.get_distance()
            print("Distance_2: {}mm".format(distance_in_mm))
            time.sleep(0.1)
            count += 1
            if count == limit: 
                count = 0 
                select = 0 
