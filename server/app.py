from flask import Flask, render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user
import pandas as pd
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'GANTI_PASSWORD_INI_BIAR_AMAN' # SECURITY POINT
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///production.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

# --- MODEL DATABASE ---
class MasterProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(200))
    jumlah_terproduksi = db.Column(db.Integer, default=0)
    # ... field lain sesuai CSV

class ProduksiHasil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    no_wo = db.Column(db.String(50))
    lot_number = db.Column(db.String(100))
    berat = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    # ... field lain sesuai request

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50)) # operator, helper, machine, shift
    value = db.Column(db.String(50))

# --- ROUTES ---
@app.route('/api/get_master_data')
def get_data():
    # API untuk dipanggil oleh Raspberry Pi
    products = MasterProduct.query.all()
    settings = Settings.query.all()
    return jsonify({'products': [p.to_dict() for p in products], 'settings': [s.to_dict() for s in settings]})

@app.route('/api/submit_production', methods=['POST'])
def submit_prod():
    # Menerima data dari Raspberry Pi
    data = request.json
    # Simpan ke ProduksiHasil
    # Update Counter di MasterProduct
    return jsonify({'status': 'success'})

# ... Route lain untuk Halaman Admin, Upload CSV, Dashboard, Login ...

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8000)
