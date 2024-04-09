import os
import logging
from datetime import timezone
from dotenv import load_dotenv


load_dotenv()
env = os.environ


def get_secret(file_path_env_var: str):
    secret_path = os.getenv(file_path_env_var)

    if not secret_path:
        return None

    path_exists = os.path.exists(secret_path)

    if path_exists:
        with open(secret_path, 'r', encoding='utf-8') as secret_file:
            secret_var = secret_file.read().rstrip('\n')
        return secret_var

    return None


def get_env_or_secret(env_var_name: str):
    env_var = os.getenv(env_var_name)
    if env_var:
        return env_var

    file_path_env_var = env_var_name + '_FILE'
    secret_var = get_secret(file_path_env_var)
    return secret_var


TIMEZONE = timezone.utc

ROOT_PATH = env.get('ROOT_PATH', 'api')

# logger
LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOG_LEVEL = env.get('LOG_LEVEL')
logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)

JWT_SECRET = env.get('JWT_SECRET')

# postgres
POSTGRES_HOST = env.get('POSTGRES_HOST')
POSTGRES_PORT = env.get('POSTGRES_PORT')
POSTGRES_DB = get_env_or_secret('POSTGRES_DBNAME')
POSTGRES_USER = get_env_or_secret('POSTGRES_USER')
POSTGRES_PASSWORD = get_env_or_secret('POSTGRES_PASS')

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}\
@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

ALEMBIC_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}\
@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

CORS_ORIGINS = env.get('CORS_ORIGINS', '').split(',')
ALLOWED_HOSTS = env.get('ALLOWED_HOSTS', '').split(',')

DEBUG = bool(int(env.get('DEBUG', 0)))
