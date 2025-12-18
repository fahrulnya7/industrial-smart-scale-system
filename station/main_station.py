import serial
from flask import Flask, render_template, jsonify, request
import requests
import re
from datetime import datetime
import os

app = Flask(__name__)

# --- KONFIGURASI HARDWARE ---
SERVER_URL = "http://192.168.1.100:8000" # Ganti dengan IP Server Ubuntu
SCALE_PORT = "/dev/ttyUSB0" # Sesuaikan
PRINTER_USB = "/dev/usb/lp0" # Sesuaikan

# --- LOGIC TIMBANGAN ---
def get_weight_from_scale():
    try:
        ser = serial.Serial(SCALE_PORT, 1200, serial.SEVENBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout=1)
        # Baca data serial, parsing angka
        raw_data = ser.readline().decode('utf-8').strip()
        # Regex ambil angka saja
        weight = re.findall(r"[-+]?\d*\.\d+|\d+", raw_data)
        return float(weight[0]) if weight else 0.0
    except:
        return 0.0 # Return 0 jika error/offline

# --- LOGIC GENERATE LOT NUMBER (SESUAI REQUEST) ---
def generate_lot_number(data_input):
    # Format: 1 + Mesin + KodeBahan + Warna + Tebal + Tanggal + Shift + Counter
    
    # 1. Kode Cabang (Static)
    part1 = "1"
    
    # 2. Mesin (01-05)
    part2 = data_input['no_mesin']
    
    # 3. Kode Bahan (PP, HI, PE) & 5. Tebal
    item_name = data_input['item_name_text'] # Contoh: "HIPS NATURAL 0,60 x 365"
    
    part3 = "PP" # Default
    if "HIPS" in item_name.upper(): part3 = "HI"
    elif "PET" in item_name.upper(): part3 = "PE"
    
    # Ambil tebal (0,60 -> 060)
    tebal_match = re.search(r'(\d+)[.,](\d+)', item_name)
    if tebal_match:
        part5 = tebal_match.group(1) + tebal_match.group(2)
        if len(part5) < 3: part5 = part5.ljust(3, '0') # Padding
    else:
        part5 = "000"
        
    # 4. Warna (NT, CT, dll)
    part4 = data_input['warna']
    
    # 6. Tanggal (161225)
    now = datetime.now()
    part6 = now.strftime("%d%m%y")
    
    # 7. Shift (01)
    part7 = data_input['shift']
    
    # 8. Counter (0002) - Ambil dari Master Data Product (via API Server nanti)
    counter = str(data_input['counter_value']).zfill(4)
    
    lot_full = f"{part1}{part2}{part3}{part4}{part5}{part6}{part7}-{counter}"
    return lot_full

# --- LOGIC PRINTER ZEBRA (ZPL) ---
def print_zebra(data):
    # ZPL Code Template
    zpl = f"""
    ^XA
    ^FO50,50^ADN,36,20^FDItem: {data['item_name']}^FS
    ^FO50,100^ADN,36,20^FDLOT: {data['lot_number']}^FS
    ^FO50,150^ADN,36,20^FDWeight: {data['berat']} KG^FS
    ^FO50,200^ADN,36,20^FDOpr: {data['operator']} / {data['helper']}^FS
    ^FO400,50^BQN,2,5^FDQA,{data['lot_number']}^FS
    ^XZ
    """
    try:
        with open(PRINTER_USB, 'wb') as p:
            p.write(zpl.encode('utf-8'))
        return True
    except Exception as e:
        print(f"Print Error: {e}")
        return False

# --- ROUTES STATION ---
@app.route('/')
def index():
    # Ambil data dropdown dari Server Pusat
    try:
        response = requests.get(f"{SERVER_URL}/api/get_master_data")
        master_data = response.json()
    except:
        master_data = {} # Handle jika offline
    return render_template('station_ui.html', data=master_data)

@app.route('/get_weight')
def weight_api():
    return jsonify({'weight': get_weight_from_scale()})

@app.route('/process_print', methods=['POST'])
def process_print():
    data = request.json
    # 1. Generate LOT
    lot = generate_lot_number(data)
    data['lot_number'] = lot
    
    # 2. Print
    print_zebra(data)
    
    # 3. Kirim ke Server Pusat untuk disimpan
    requests.post(f"{SERVER_URL}/api/submit_production", json=data)
    
    return jsonify({'status': 'success', 'lot': lot})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
