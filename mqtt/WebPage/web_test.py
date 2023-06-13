import paho.mqtt.client as paho
import time

broker="test.mosquitto.org"
#port=1883

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

virtual_control= paho.Client("control1")                           #create client object
virtual_control.on_publish = on_publish                          #assign function to callback
virtual_control.connect(broker)                                 #establish connection

time.sleep(3)

virtual_control.publish("embed/web","1")
print("send 1")
time.sleep(5)

virtual_control.publish("embed/web","1")
print("send 1")
time.sleep(5)

virtual_control.publish("embed/web","2")
print("send 2")
time.sleep(5)

virtual_control.publish("embed/web","1")
print("send 1")
time.sleep(5)

virtual_control.publish("embed/web","1")
print("send 1")
time.sleep(5)

virtual_control.publish("embed/web","1")
print("send 1")
time.sleep(5)

