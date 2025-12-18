#!/bin/bash
echo "=== INSTALLER SERVER UBUNTU ==="
sudo apt update
sudo apt install -y python3-pip python3-venv
python3 -m venv venv
source venv/bin/activate
pip install flask flask-sqlalchemy flask-login pandas openpyxl
echo "Setup selesai! Jalankan dengan: ./venv/bin/python app.py"
