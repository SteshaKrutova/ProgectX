# test_env.py
from dotenv import load_dotenv
import os

load_dotenv()

print(' Проверка переменных окружения:')
print(f'secret_key: {os.environ.get("secret_key")}')
print(f'db_uri: {os.environ.get("sqlalchemy_database_uri")}')
