import paho.mqtt.client as paho

available_people = 0
sensor_state = [0, 0]

##FIXME: Do not close the gate when there is a person!!


def handle_change(mqtt_client, change):
    global available_people
    if change == 1:
        if available_people == 0:
            # Open the gate
            mqtt_client.publish('embed/motor', "1")
            print("send 1 to motor, open")
        available_people += 1
    elif change < 0:
        prev_num_people = available_people
        available_people += change

        if prev_num_people > 0 and available_people <= 0:
            # Close the gate
            mqtt_client.publish('embed/motor', "0")
            print("send 0 to motor, close")
    
    mqtt_client.publish('embed/web', str(available_people))
    print("send %d to the website" % available_people)

def distinguish_peoople(mqtt_client):
    if sensor_state[0] != 0 and sensor_state[1] != 0:
        # The payload between two sensors is 20 cm 
        # The detected length = 20 cm - sensor_state[0] - sensor_state[1]
        # Let's conclude there are two people when the length > 12cm 
        # sensor_state[0] + sensor_state[1] < 8 cm
        if sensor_state[0] + sensor_state[1] < 8:
            # Two people
            print("Two people")
            handle_change(mqtt_client, -2)
        else:
            # One people
            print("One people")
            handle_change(mqtt_client, -1)

        sensor_state[0] = 0
        sensor_state[1] = 0

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload.decode("utf-8")))

    publisher_id, data = msg.payload.decode("utf-8").split(' ')
    publisher_id = int(publisher_id)
    data = int(data)

    if publisher_id == 0 or publisher_id == 1:
        sensor_state[publisher_id] = data
        distinguish_peoople(client)
    elif publisher_id == 2:
        print("%s from the web" % data)
        handle_change(client, data)

mqtt_client = paho.Client()
mqtt_client.on_subscribe = on_subscribe
mqtt_client.on_publish = on_publish
mqtt_client.on_message = on_message
mqtt_client.connect('test.mosquitto.org')
mqtt_client.subscribe("embed/control", qos=1)

mqtt_client.loop_forever()