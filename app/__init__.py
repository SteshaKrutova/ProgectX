
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Создаем экземпляры расширений
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login' # Куда перенаправлять неавторизованных пользователей
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config') # Загружаем конфигурацию

    # Инициализируем расширения с приложением
    db.init_app(app)
    login_manager.init_app(app)

    # Импортируем и регистрируем Blueprints (пока заготовка)
    from .routes import auth_bp, main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    
    # Создаем таблицы БД при первом запуске
    with app.app_context():
        db.create_all()
        print('+ Таблицы БД созданы/проверены')

    return app

