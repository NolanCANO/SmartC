from machine import Pin, ADC
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

ssid = 'HONOR Magic5 Lite 5G'
password = 'azerttreza'
mqtt_server = '192.168.212.82'
mqtt_user = ''
mqtt_pass = ''

client_id = ubinascii.hexlify(machine.unique_id())
topic_pub_temp = b'temperature'
topic_pub_hum = b'humidity'
topic_pub_wat = b'water'
topic_pub_gaslim = b'gaslimit'
topic_pub_gasval = b'gas'

#DHT22
sensor_dht = dht.DHT22(Pin(23))

#V247
powerV247 = Pin(17, Pin.OUT)
powerV247.value(0)
signalV247 = ADC(Pin(36))
signalV247.width(ADC.WIDTH_12BIT)
signalV247.atten(ADC.ATTN_11DB) # ~3.3V

#MQ2
signalDO = Pin(16, Pin.IN)
signalAO = ADC(Pin(34))
#signalAO.width(ADC.WIDTH_12BIT)
signalAO.atten(ADC.ATTN_11DB) # ~3.3V

lastSensor = ""

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
  
def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

while (1): 
    try:
        #DHT22 - Temperature and Humidity
        lastSensor = "DHT22"
        sensor_dht.measure()
        humidity = sensor_dht.humidity()
        temperature = sensor_dht.temperature()
        print(f"Humidité : {humidity} %")
        print(f"Température: {temperature} C")
        #print(f"Température CPU: {cput} C")
        
        #V247 - Water
        lastSensor = "V247"
        powerV247.value(1)
        time.sleep_ms(10)
        waterValue = signalV247.read()
        water = map_value(waterValue, 0, 2088, 0, 4) #2088 * 4095
        powerV247.value(0)
        print(f"Eau: {waterValue} ")
        print(f"Niveau Eau: {water} ")
        
        #MQ-2 - Gaz and Smoke
        lastSensor = "MQ2"
        gasLimit = signalDO.value()
        gasValue = signalAO.read()
        print(f"Limite Gaz: {gasLimit}")
        print(f"Valeur Gaz: {gasValue}")
        
        #MQTT - Data Sending
        lastSensor = "MQTT"
        client.ping()
        client.publish(topic_pub_temp, str(temperature).encode())
        client.publish(topic_pub_hum, str(humidity).encode())
        client.publish(topic_pub_wat, str(water).encode())
        client.publish(topic_pub_gaslim, str(gasLimit).encode())
        client.publish(topic_pub_gasval, str(gasValue).encode())
    except Exception as e:
        print(f"Erreur Capteur {lastSensor}: {e}")
        humidity = None
        temperature = None
        water = None
    sleep(3)

