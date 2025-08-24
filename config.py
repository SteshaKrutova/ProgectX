# config.py
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # Подключение к БД
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False