#!/bin/bash

echo "🔧 Création de l'environnement virtuel Python..."
cd "$(dirname "$0")" || exit 1

if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

echo "📦 Installation des dépendances dans le venv..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Environnement prêt."
