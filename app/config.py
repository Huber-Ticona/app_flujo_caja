from datetime import timedelta
import os

class Config():
    SECRET_KEY = os.getenv("SECRET_KEY")
    REMEMBER_COOKIE_DURATION = timedelta(days=30)
    # Flask-Caching related configs
    CACHE_TYPE = "SimpleCache"  
    CACHE_DEFAULT_TIMEOUT = 300

class ConfigDevelop(Config):

    # BASE DE DATOS CONFIGURACION
    DB= os.getenv('DB')
    USER=os.getenv('USER')
    PASSWORD=os.getenv('PASSWORD')
    HOST=os.getenv('HOST')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG  = True

""" class ConfigTesting(Config):

    # BASE DE DATOS CONFIGURACION
    DB= os.getenv('TEST_DB')
    USER=os.getenv('USER')
    PASSWORD=os.getenv('PASSWORD')
    HOST=os.getenv('HOST')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False """

class ConfigProduction(Config):
    
    # BASE DE DATOS CONFIGURACION
    DB= os.getenv('TEST_DB')
    USER=os.getenv('TEST_USER')
    PASSWORD=os.getenv('TEST_PASSWORD')
    HOST=os.getenv('TEST_HOST')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG  = False