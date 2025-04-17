# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import webrepl
from time import sleep_ms
WIFI_NAME = 'Mi 11i'
WIFI_PASS = 'Bleu6214!'

def connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(WIFI_NAME, WIFI_PASS)
    print('network config:', sta_if.ifconfig())
    
def showip():
    import network
    sta_if = network.WLAN(network.STA_IF)
    print('network config:', sta_if.ifconfig())
    
    
connect()
webrepl.start()

sleep_ms(2000)
import Sensors_MQTT