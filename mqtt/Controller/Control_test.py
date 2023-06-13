import paho.mqtt.client as paho
import time

broker="test.mosquitto.org"
#port=1883

def on_publish(client,userdata,result):   
    print("data published \n")
    pass

sensor= paho.Client("control1")   
sensor.on_publish = on_publish
sensor.connect(broker)

time.sleep(2)

sensor.publish("embed/control","2 1")
print("1 from web")
time.sleep(2)

sensor.publish("embed/control","0 9")
print("9 from sensor 0")
time.sleep(2)

sensor.publish("embed/control","1 8")
print("8 from sensor 1")
time.sleep(2)

sensor.publish("embed/control","2 1")
print("1 from web")
time.sleep(2)

sensor.publish("embed/control","2 -1")
print("-1 from web")
time.sleep(2)

sensor.publish("embed/control","0 3")
print("send 1")
time.sleep(2)

sensor.publish("embed/control","1 2")
print("send 2")
time.sleep(2)

