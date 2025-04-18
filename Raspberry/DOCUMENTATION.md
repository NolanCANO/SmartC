# 📡 Raspberry Pi MQTT Setup & Script Autostart

Ce projet configure une Raspberry Pi pour :

- Utiliser **Mosquitto** comme broker MQTT (au démarrage).
- Lancer un script **Python automatiquement** au boot.
- S'assurer que les **ports MQTT (1883)**, **SSH (22)**, **Grafana (3000)** et **InfluxDB(8086)** sont ouverts.

---

## 🛠️ Pré-requis

- Raspberry Pi 5 avec Raspberry Pi OS (Lite ou Desktop).
- Accès root ou `sudo`.
- Connexion Internet.

---

## 🚀 Étapes d'installation

### 1. Mise à jour du système

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Installation de Mosquitto (MQTT Broker)

```bash
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto
```

### 3. Configuration du pare-feu (UFW)

```bash
sudo apt install ufw -y
sudo ufw allow 22
sudo ufw allow 1883
sudo ufw allow 3000
sudo ufw allow 8086
sudo ufw enable
```

### 4. Installation de influxDB

```bash
curl --silent --location -O \
https://repos.influxdata.com/influxdata-archive.key
echo "943666881a1b8d9b849b74caebf02d3465d6beb716510d86a39f6c8e8dac7515  influxdata-archive.key" \
| sha256sum --check - && cat influxdata-archive.key \
| gpg --dearmor \
| sudo tee /etc/apt/trusted.gpg.d/influxdata-archive.gpg > /dev/null \
&& echo 'deb [signed-by=/etc/apt/trusted.gpg.d/influxdata-archive.gpg] https://repos.influxdata.com/debian stable main' \
| sudo tee /etc/apt/sources.list.d/influxdata.list

sudo apt-get update && sudo apt-get install influxdb2

sudo service influxdb start
```

### 5. Mise en place de Telegraf

```bash
sudo apt-get install telegraf
```

- Lancer le GUI de influxdb, present sur le port 8086 et configurer l'organisation, le bucket.

- Copier mqtt.conf dans `/etc/telegraf/telegraf.d/mqtt.conf` après avoir changer l'og, le bucket et le token.

```bash
sudo systemctl restart telegraf
```

### 6. Mise en place de Grafana

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://apt.grafana.com/gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/grafana.gpg


echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | \
sudo tee /etc/apt/sources.list.d/grafana.list > /dev/null

sudo apt update
sudo apt install grafana -y

sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

- Connecter vous sur Grafana sur le port 3000 avec admin admin.

- Aller sur `Settings > Data Sources`

- Cliquer sur "Add data source" puis choisir "influxDB" puis rajouter les données suivante:

```
Query Language: Flux
URL: http://localhost:8086
Organization: <l'org InfluxDB>
Token: <le token API InfluxDB>
Default Bucket: <le bucket InfluxDB>
```

- Cliquer sur "Save & Test"

### 7. Mise en place du projet Python

Après avoir copier requirement.txt, setup.sh et main.py.

```bash
chmod +x setup.sh
./setup.sh
```

### 8. Lancer le script Python automatiquement au démarrage

```bash
sudo nano /etc/systemd/system/rasp.service
```

Puis coller:
```ini
[Unit]
Description=Script Python avec venv
After=network.target mosquitto.service

[Service]
ExecStart=/home/pi/path/to/project/venv/bin/python /home/pi/path/to/project/main.py
WorkingDirectory=/home/pi/path/to/project
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

Puis
```bash
sudo systemctl daemon-reload
sudo systemctl enable rasp.service
sudo systemctl start rasp.service
```

### 9. Redemarrage final

```bash
sudo reboot
```

### Resultat

Vous avez donc une interface influcDB sur le port 8086, Grafana sur le port 3000, Un accès SSH sur le port 22 lorsque connecté sur le même reseau.

La Raspberry va aussi pouvoir servir de broker MQTT, les données passant par elle et avec le script python va pouvoir rapidement réagir si un problème est detecté.
