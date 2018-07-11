from os import path
import os
from dotenv import load_dotenv

env_path = path.join(path.dirname(__file__) , '.env')
load_dotenv(env_path)
# import pdb; pdb.set_trace()

class Config():
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_PROD')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY = os.getenv('SECRET_KEY')

class DevelopementConfig(Config):
     DEBUG = True
     SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_DEV')
     SQLALCHEMY_TRACK_MODIFICATIONS=True
     
class TestConfig(Config):
     SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_TEST')
     TESTING = True


app_config = {
    "production": Config,
    "development": DevelopementConfig,
    "test": TestConfig
}




