from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager

# Inisialisasi ekstensi global
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Konfigurasi aplikasi dengan menggunakan MySQL
    app.config['SECRET_KEY'] = 'your_secret_key_here'  # Ganti dengan kunci rahasia Anda
    
    # Konfigurasi koneksi ke MySQL (ganti dengan kredensial Anda)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/User_Database'  # Ganti 'username' dan 'password' sesuai kredensial Anda
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True  # Mengaktifkan mode debug di Flask

    # Inisialisasi ekstensi dengan app
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Pengaturan login_manager
    login_manager.login_view = 'main.login'  # Halaman login yang diakses jika user belum login
    login_manager.login_message_category = 'info'  # Pesan default ketika belum login

    # Registrasi Blueprint
    from .routes import main
    app.register_blueprint(main)

    return app

# Fungsi untuk memuat user berdasarkan ID dari session
@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))
