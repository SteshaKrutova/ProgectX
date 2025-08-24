# test_connection.py
from app import create_app, db
from app.models import User
from sqlalchemy import text  # Добавить импорт

app = create_app()

with app.app_context():
    try:
        # Проверяем подключение к БД (используем text())
        result = db.session.execute(text('SELECT version()')).fetchone()
        print(f'+ Подключение к PostgreSQL успешно: {result[0]}')
        
        # Проверяем существование таблиц
        tables = db.inspect(db.engine).get_table_names()
        print(f'+ Таблицы в БД: {tables}')
        
        # Проверяем конфигурацию
        print(f'+ SECRET_KEY: {app.config["SECRET_KEY"][:10]}...')
        print(f'+ DB_URI: {app.config["SQLALCHEMY_DATABASE_URI"].replace("your_password", "***")}')
        
    except Exception as e:
        print(f'- Ошибка подключения: {e}')