import paho.mqtt.client as mqtt
import serial
import time

# === CONFIGURATION ===
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPICS = [("loratest", 0)]      # topic(s) à écouter

SERIAL_PORT = "/dev/serial0"
BAUDRATE = 9600

# === SETUP SERIAL (LoRa) ===
ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
time.sleep(1)

# === CALLBACK quand un message MQTT est reçu ===
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"[MQTT] {msg.topic}: {message}")
    
    # Envoie le message sur LoRa
    try:
        payload = f"{msg.topic}:{message}\n"
        ser.write(payload.encode())
        print("[LoRa] Message envoyé.")
    except Exception as e:
        print(f"[LoRa] Erreur d'envoi: {e}")

# === INITIALISATION MQTT ===
client = mqtt.Client()
client.on_message = on_message

print("[MQTT] Connexion au broker...")
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe(MQTT_TOPICS)

print("[MQTT] En écoute...")
client.loop_forever()
