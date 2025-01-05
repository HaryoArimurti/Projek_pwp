from datetime import datetime
from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    # id: Integer, primary key dengan auto-increment
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # username: Varchar(255), unik dan tidak boleh kosong
    username = db.Column(db.String(255), unique=True, nullable=False)
    
    # role: Varchar(50), default 'user', tidak boleh kosong
    role = db.Column(db.String(50), nullable=False, default='user')  # Menambahkan default 'user'
    
    # email: Varchar(255), unik dan tidak boleh kosong
    email = db.Column(db.String(255), unique=True, nullable=False)
    
    # password_hash: Varchar(255), tidak boleh kosong
    password_hash = db.Column(db.String(255), nullable=False)
    
    # is_admin: Boolean, default False
    is_admin = db.Column(db.Boolean, default=False)  # Tinyint(1) set sebagai Boolean
    
    # date_created: Timestamp default saat ini
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'
