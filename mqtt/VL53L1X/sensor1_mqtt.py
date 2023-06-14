import time
import board
import adafruit_vl53l1x
import paho.mqtt.client as paho

broker="test.mosquitto.org"

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

sensor_client= paho.Client("sensor1")                           #create client object
sensor_client.on_publish = on_publish                          #assign function to callback
sensor_client.connect(broker)                                 #establish connection

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

vl53 = adafruit_vl53l1x.VL53L1X(i2c)

# OPTIONAL: can set non-default values
vl53.distance_mode = 1
vl53.timing_budget = 33

vl53.start_ranging()

guideline = 15
max_difference = 30
threshold = 3

def main():
    count_blocked = 0
    count_unblocked = 0

    while True:
        if vl53.data_ready:
            #print("Distance: {} cm".format(vl53.distance))
            if vl53.distance is not None and  vl53.distance < guideline:
                count_blocked += 1
                count_unblocked = 0
                if count_blocked == threshold:
                    sensor_client.publish("embed/control", "1 " + str(vl53.distance))
                    print("Send %s" % str(vl53.distance))
                    
            elif vl53.distance is not None and count_blocked != 0:
                count_unblocked += 1
                if count_unblocked == 2:
                    count_blocked = 0
                    count_unblocked = 0


            vl53.clear_interrupt()
            time.sleep(0.025)

if (__name__ == '__main__'):
    main()
