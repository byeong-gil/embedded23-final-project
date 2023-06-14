import paho.mqtt.client as paho
import time

broker="test.mosquitto.org"

Count = 4
Target = 526

Toggle = True
Counter = 0
Accum = 0

#port=1883

def on_publish(client,userdata,result): #create function for callback
    print("data published \n")
    pass

client1= paho.Client("control1")        #create client object
client1.on_publish = on_publish         #assign function to callback
client1.connect(broker)                 #establish connection

while 1:
    if(Toggle):
        ret= client1.publish("embed/motor", 1)   #publish
        time.sleep(2)
        Toggle = False
    else:
        ret= client1.publish("embed/motor", 0)   #publish
        time.sleep(2)
        Toggle = True