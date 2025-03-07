from machine import Pin
from time import sleep
import dht
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()

ssid = 'chocolatAuLait'
password = 'tomate59'
mqtt_server = '192.168.31.106'
mqtt_user = ''
mqtt_pass = ''

client_id = ubinascii.hexlify(machine.unique_id())
topic_pub_temp = b'temperature'
topic_pub_hum = b'humidity'

sensor_dht = dht.DHT22(Pin(23))

timeout = 0
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print(f"Attempt to connect to SSID : {ssid}")
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        print('.', end = " ")
        time.sleep_ms(500)
        timeout = timeout + 500
        if (timeout >= 20000):
            print(f"Connection attempt failed : timeout")
            exit()

print("\nWi-Fi Config: ", wlan.ifconfig())
timeout = 0

def connect_mqtt():
  global client_id, mqtt_server
  client = MQTTClient(client_id, mqtt_server)
  client.connect()
  print(f'Connected to %s MQTT broker' % (mqtt_server))
  return client

try:
  client = connect_mqtt()
except OSError as e:
  print(f"Connection to MQTT broker failed failed : {e}")
  exit()

while (1): 
    try:
        sensor_dht.measure()
        humidity = sensor_dht.humidity()
        temperature = sensor_dht.temperature()
        print(f"Humidité : {humidity} %")
        print(f"Température: {temperature} C")
        print(f"Température CPU: {cput} C")
        client.ping()
        client.publish(topic_pub_temp, str(temperature).encode())
        client.publish(topic_pub_hum, str(humidity).encode())
    except Exception as e:
        print(f"Erreur DHT22 : {e}")
        humidity = None
        temperature = None
    sleep(3)