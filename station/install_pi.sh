#!/bin/bash
echo "=== INSTALLER RASPBERRY PI STATION ==="
# 1. Update System
sudo apt update
sudo apt install -y python3-pip python3-venv python3-serial

# 2. Setup Permissions (Agar bisa akses USB tanpa root)
sudo usermod -a -G dialout $USER
sudo usermod -a -G lp $USER

# 3. Setup Python Env
python3 -m venv venv
source venv/bin/activate
pip install flask requests pyserial

# 4. Buat Autostart (Agar pas nyala langsung buka browser Fullscreen)
mkdir -p ~/.config/autostart
cat <<EOF > ~/.config/autostart/kiosk.desktop
[Desktop Entry]
Type=Application
Name=Kiosk
Exec=/usr/bin/chromium-browser --kiosk --disable-restore-session-state http://localhost:5000
EOF

echo "Instalasi Selesai! Restart Pi Anda."
