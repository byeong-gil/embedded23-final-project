import paho.mqtt.client as paho
import time

broker="test.mosquitto.org"

Count = 4
Target = 526

Direction = 0
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
    if(Direction == 1):
        ret= client1.publish("embed/motor",1)   #publish
    else:
        ret= client1.publish("embed/motor",0)   #publish      

    Counter += 1
    Accum += 1

    if (Counter == Count):
        Counter = 0
    if (Counter < 0):
        Counter = Count

    if (Accum == Target):
        if(Direction == 1):
            Direction = 0
        else:
            Direction = 1
        time.sleep(0.1)
        Accum = 0
    else:
        time.sleep(0.002)