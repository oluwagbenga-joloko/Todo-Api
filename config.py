from os import path
import os
from dotenv import load_dotenv

env_path = path.join(path.dirname(__file__) , '.env')
load_dotenv(env_path, override= True)
# import pdb; pdb.set_trace()

class Config():
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_PROD')

class DevelopementConfig():
     SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_DEV')
     
class TestConfig():
     SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_TEST')


app_config = {
    "production": Config,
    "development": DevelopementConfig,
    "test": TestConfig
}




