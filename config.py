class Config:
    SECRET_KEY = 'your_secret_key_here'
    # Sesuaikan dengan kredensial MySQL Anda
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/Users'  # Ganti 'username' dan 'password' dengan yang sesuai
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True  # Mengaktifkan mode debug di Flask
