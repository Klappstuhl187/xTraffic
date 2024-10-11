import serial
import os
import configparser
import db_access as db
import time
import threading
import io
import webserver
import asyncio

config = configparser.ConfigParser()
path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
config.read(os.path.join(path, 'config.ini'))
port = config['arduino']['ARDUINO_PORT']
encoding = config['arduino']['ARDUINO_ENCODING']
sensor_distance_1 = float(config['arduino']['SENSOR_DISTANCE_1'])
sensor_distance_2 = float(config['arduino']['SENSOR_DISTANCE_2'])
safe_distance = float(config['arduino']['SAFE_DISTANCE'])
distance_between_sensors = sensor_distance_1 - sensor_distance_2
ser = serial.Serial(port, 9600, timeout=1)

def write(data):
    print("Sending to arduino:", data)
    ser.write(data)
    
def toggle_lights(state: bool):
    write(f"Lights {state}")

def toggle_gate(state: bool):
    write(f"Gates {state}")

def start():
    while True:
        if ser.in_waiting > 0:
            # Daten vom Arduino lesen
            data = ser.readline().decode('latin-1').rstrip()
            crossing_id = 1
            print("From arduino:", data)

            if (data == 'Sensor1'):
                print('Sensor 1 wurde aktiviert. Ein Eintrag wird erstellt.')
                db.insert_entry(crossing_id, time.time())

            elif (data == 'Sensor2'):
                print('Sensor 2 wurde aktiviert. Geschwindigkeit und Zeit werden berechnet...')
                entry = db.get_entry(crossing_id)
                entry.time2 = time.time()
                
                print('delta_t',entry.time1 - entry.time2)
                speed_mps = distance_between_sensors / (entry.time2 - entry.time1)
                countdown_distance = sensor_distance_2 - safe_distance
                countdown_time = round(countdown_distance / speed_mps)
                
                entry.speed = speed_mps
                entry.countdown = countdown_time
                db.save_entry(entry)
                asyncio.run(webserver.send_countdown({ "crossingId": crossing_id, "time": countdown_time }))
                
                # Countdown Delay
                print("=============")
                for i in range(countdown_time,0,-1):
                    print(f"{i}...", end="\r", flush=True)
                    time.sleep(1)
                print("=============")
                asyncio.run(webserver.send_update({ "crossingId": crossing_id, "state": False }))
                write(("Gates False").encode())
                asyncio.run(webserver.send_traffic_data(entry))

            elif (data.startswith("Gates")):
                data = data[6:]
                if data == "1":
                    data = True;
                elif data == "0":
                    data = False;
                else:
                    print("Received an invalid Gates message:", data)
                asyncio.run(webserver.send_update({ "crossingId": crossing_id, "state": data }))

arduino_thread = threading.Thread(target=start, daemon=True)
arduino_thread.start()