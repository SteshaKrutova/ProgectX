# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask
from flask_mail import Mail

app = Flask(__name__)

# Создаем экземпляры расширений
db = SQLAlchemy()
login_manager = LoginManager()

login_manager.login_view = 'auth.login' # Куда перенаправлять неавторизованных пользователей
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config') # Загружаем конфигурацию
    app.config['MAIL_SERVER'] = 'smtp.yandex.ru'  # SMTP-сервер Yandex
    app.config['MAIL_PORT'] = 465  # Порт для SSL (Yandex рекомендует 465)
    app.config['MAIL_USE_SSL'] = True  # Использование SSL вместо TLS
    app.config['MAIL_USERNAME'] = 'mira.kru@yandex.ru'  # Ваш email
    app.config['MAIL_PASSWORD'] = '89218680828'  # Пароль от почты
    app.config['MAIL_DEFAULT_SENDER'] = 'mira.kru@yandex.ru'  # Отправитель

    mail = Mail(app)
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


