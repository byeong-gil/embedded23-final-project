import sys
import signal
import time

import VL53L1X

print("""
Press Ctrl+C to exit
""")

tof = VL53L1X.VL53L1X(i2c_bus=0, i2c_address=0x29)
tof.open()

tof.start_ranging(1) # 1 means short range

running = True

def exit_handler(signal, frame):
    global running
    running = False
    tof.stop_ranging()
    print()
    sys.exit(0)

signal.signal(signal.SIGINT, exit_handler)

while running:
    distance_in_mm = tof.get_distance()
    print("Distance: {}mm".format(distance_in_mm))
    time.sleep(0.1)