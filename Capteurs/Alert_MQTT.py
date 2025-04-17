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
topic_pub_gaslim = b'gaslimit'
topic_pub_gasval = b'gas'
topic_sub_alert = b'alert'

#MQ2
signalDO = Pin(16, Pin.IN)
signalAO = ADC(Pin(34))
#signalAO.width(ADC.WIDTH_12BIT)
signalAO.atten(ADC.ATTN_11DB) # ~3.3V

#Alert
pin_alert = Pin(2, mode=Pin.OUT)

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

def sub_cb(topic, msg):
  print((topic, msg))
  if topic == b'alert' and msg == b'1':
    pin_alert.on()
  elif topic == b'alert' and msg == b'0':
    pin_alert.off()
    

def connect_mqtt():
  global client_id, mqtt_server, alert_sub
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub_alert)
  print(f'Connected to %s MQTT broker' % (mqtt_server))
  return client

try:
  client = connect_mqtt()
except OSError as e:
  print(f"Connection to MQTT broker failed failed : {e}")
  exit()
  
while True:
  try:
    time.sleep_ms(2000)
    client.check_msg()
  except OSError as e:
    restart_and_reconnect()