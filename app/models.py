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
    role = db.Column(db.String(20), nullable=False)  # Роль пользователя: 'client' или 'contractor'
    is_active = db.Column(db.Boolean, default=True)  # Активен ли аккаунт
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Дата создания аккаунта
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Дата обновления
    
    def set_password(self, password):
        """Установка хэшированного пароля."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Проверка пароля."""
        return check_password_hash(self.password_hash, password)
    
    def update_timestamp(self):
        """Обновление временной метки."""
        self.updated_at = datetime.utcnow()
    
    def __repr__(self):
        return f'<User {self.username}, Role: {self.role}>'
    
    @staticmethod
    def get_all_clients():
        """Получение всех клиентов."""
        return User.query.filter_by(role='client').order_by(User.username).all()


class Service(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Название услуги
    is_active = db.Column(db.Boolean, default=True)  # Статус услуги: включена/выключена
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # ID владельца услуги
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Дата создания услуги
    
    def __repr__(self):
        return f'<Service {self.name}, Active: {self.is_active}, User ID: {self.user_id}>'


# Функция для Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """Загрузка пользователя по ID."""
    return User.query.get(int(user_id))