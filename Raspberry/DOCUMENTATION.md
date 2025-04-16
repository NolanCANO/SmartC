# 📡 Raspberry Pi MQTT Setup & Script Autostart

Ce projet configure une Raspberry Pi pour :

- Utiliser **Mosquitto** comme broker MQTT (au démarrage).
- Lancer un script **Python automatiquement** au boot.
- S'assurer que les **ports MQTT (1883)** et **SSH (22)** sont ouverts.

---

## 🛠️ Pré-requis

- Raspberry Pi avec Raspberry Pi OS (Lite ou Desktop).
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
sudo ufw enable
```

### 4. Mise en place du projet Python

Après avoir copier requirement.txt, setup.sh et main.py.

```bash
chmod +x setup.sh
./setup.sh
```

### 5. Lancer le script Python automatiquement au démarrage

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
sudo systemctl enable mon_script.service
sudo systemctl start mon_script.servic
```

### 6. Redemarrage final

```bash
sudo reboot
```
