import paho.mqtt.client as paho
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
StepPins = [12,16,20,21]


for pin in StepPins:
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin,False)

StepCount = 4
TargetAngle = 526

Seq_1 = [[0,0,0,1],
         [0,0,1,0],
         [0,1,0,0],
         [1,0,0,0]]

Seq_2 = [[1,0,0,0],
         [0,1,0,0],
         [0,0,1,0],
         [0,0,0,1]]

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    StepCounter = 0
    StepAccum = 0

    if(int(msg.payload) == 1):
        while 1:
            for pin in range(0, 4):
                xpin = StepPins[pin]
                if Seq_1[StepCounter][pin]!=0:
                    GPIO.output(xpin, True)
                else:
                    GPIO.output(xpin, False)

            StepCounter += 1
            StepAccum += 1

            if (StepCounter == StepCount):
                StepCounter = 0
            if (StepCounter<0):
                StepCounter = StepCount

            if (StepAccum == TargetAngle):
                StepAccum = 0
                break
            else:
                time.sleep(0.002)
    else:
        while 1:
            for pin in range(0, 4):
                xpin = StepPins[pin]
                if Seq_2[StepCounter][pin]!=0:
                    GPIO.output(xpin, True)
                else:
                    GPIO.output(xpin, False)      

            StepCounter += 1
            StepAccum += 1

            if (StepCounter == StepCount):
                StepCounter = 0
            if (StepCounter<0):
                StepCounter = StepCount

            if (StepAccum == TargetAngle):
                StepAccum = 0
                break
            else:
                time.sleep(0.002)

client = paho.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect('test.mosquitto.org')
client.subscribe("step", qos=1)

client.loop_forever()
