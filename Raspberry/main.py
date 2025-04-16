import paho.mqtt.client as mqtt
import serial
import time
import json

# === CONFIGURATION ===
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPICS = [("loratest", 0), ("data", 0), ("kpis", 0)]  # topics à écouter

SERIAL_PORT = "/dev/serial0"
BAUDRATE = 9600

# === SEUILS ===
THRESHOLDS = {
    "temperature": 20.0,
    "humidity": 30.0,
    "pressure": 950.0,
}

# === SETUP SERIAL (LoRa) ===
ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
time.sleep(1)

# === CALLBACK MQTT ===
def on_message(client, userdata, msg):
    topic = msg.topic
    message = msg.payload.decode()
    print(f"[MQTT] {topic}: {message}")

    try:
        payload = f"{topic}:{message}\n"
        ser.write(payload.encode())
        print("[LoRa] Message envoyé.")
    except Exception as e:
        print(f"[LoRa] Erreur d'envoi: {e}")

    if topic == "data":
        try:
            data_json = json.loads(message)
            data_type = data_json.get("type")
            data_value = float(data_json.get("data"))

            print(f"[Analyse] Type: {data_type}, Valeur: {data_value}")

            if data_type in THRESHOLDS:
                threshold = THRESHOLDS[data_type]
                alarm_state = 1 if data_value < threshold else 0

                print(f"[Seuil] Seuil pour {data_type} = {threshold}, état alarme = {alarm_state}")

                client.publish("alarm", str(alarm_state))
        except Exception as e:
            print(f"[Erreur Analyse] Impossible de traiter les données du topic 'data': {e}")

# === INITIALISATION MQTT ===
client = mqtt.Client()
client.on_message = on_message

print("[MQTT] Connexion au broker...")
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe(MQTT_TOPICS)

print("[MQTT] En écoute...")
client.loop_forever()
