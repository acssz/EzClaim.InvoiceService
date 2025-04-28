import os
from dotenv import load_dotenv

from google.cloud.sql.connector import Connector

load_dotenv()

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConf(BaseConfig):
    DEBUG = True
    ENV = "dev"
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+pg8000://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}"
        f"@127.0.0.1:5432/{os.getenv('DATABASE_NAME')}"
    )
    SQLALCHEMY_ENGINE_OPTIONS = {}

class ProdConf(BaseConfig):
    DEBUG = False
    ENV = "prod"
    SQLALCHEMY_DATABASE_URI = "postgresql+pg8000://"
    SQLALCHEMY_ENGINE_OPTIONS = {
        "creator": lambda: connect_with_connector()
    }


connector = Connector(refresh_strategy="lazy")

def connect_with_connector():
    return connector.connect(
        os.getenv('INSTANCE_CONNECTION_NAME'),
        "pg8000",
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        db=os.getenv('DATABASE_NAME'),
        ip_type=os.getenv('IP_TYPE', 'public')
    )

def get_config():
    env = os.getenv('ENV', 'prod')
    if env == 'dev':
        return DevConf
    return ProdConf
