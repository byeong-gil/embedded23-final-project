import sys
import signal
import time

import VL53L1X

# FIXME: If the address of i2c is already 0x30, this code generate an error
#        In that case, you should plug out and in again a sensor or
#        replace Line 10, 11, 12, 13 to tof = VL53L1X.VL53L1X(i2c_bus=0, i2c_address=0x30).
tof = VL53L1X.VL53L1X(i2c_bus=0, i2c_address=0x29)
tof.open()
tof.change_address(0x30)
tof.close()
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
