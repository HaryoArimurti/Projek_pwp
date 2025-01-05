from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config
import logging

# Inisialisasi aplikasi Flask dan konfigurasi
app = Flask(__name__)
app.config.from_object(Config)

# Inisialisasi objek yang dibutuhkan (database, bcrypt, login manager)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'main.login'

# Import blueprints dan routes
from app.routes import main

# Daftarkan blueprint
app.register_blueprint(main)

# Konfigurasi logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Tambahkan logging pada aplikasi
@app.before_request
def before_request():
    logging.debug('Request: %s %s', request.method, request.path)

@app.after_request
def after_request(response):
    logging.debug('Response: %s', response.status_code)
    return response

@app.errorhandler(404)
def page_not_found(e):
    logging.error('Error 404: %s', e)
    return 'Halaman tidak ditemukan', 404

@app.errorhandler(500)
def internal_server_error(e):
    logging.error('Error 500: %s', e)
    return 'Internal Server Error', 500

if __name__ == '__main__':
    app.run(debug=True)
