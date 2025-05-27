import paho.mqtt.client as mqtt
from inputs import get_gamepad
import time

broker = "localhost"

topic = "controller/input"

client = mqtt.Client()
client.connect(broker, 1883, 60)

last_values = {0: 0, 1: 0, 2: 0, 3: 0}  

def calculate_delta(current, last):
    return current - last  

print("Drücke einen Knopf..")

while True:
    events = get_gamepad()
    for event in events:
        if event.ev_type == "Absolute":  
            channel = None
            delta = None
            
            if event.code == "ABS_X":
                channel = 0
            elif event.code == "ABS_Y":
                channel = 1
            elif event.code == "ABS_RX":
                channel = 2
            elif event.code == "ABS_RY":
                channel = 3
            
            if channel is not None:
                delta = calculate_delta(event.state, last_values[channel])
                last_values[channel] = event.state  

                message = f"{channel}:1:{delta}" 
                client.publish(topic, message)
                print(f"Nachricht gesendet: {message}")

        elif event.ev_type == "Key" and event.state == 1:
            if event.code == "BTN_SOUTH":
                message = "2"
                client.publish(topic, message)
                print(f"Nachricht gesendet: {message}")

    time.sleep(0.01)
