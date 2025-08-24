from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def update_timestamp(self):
        self.updated_at = datetime.utcnow()
    
    def __repr__(self):
        return f'<User {self.username}, Role: {self.role}>'
    
    # Ы Т: получить всех клиентов
    @staticmethod
    def get_all_clients():
        return User.query.filter_by(role='client').order_by(User.username).all()

# ункция для Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
