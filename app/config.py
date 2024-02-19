from datetime import timedelta
import os

class Config():
    SECRET_KEY = os.getenv("SECRET_KEY")
    REMEMBER_COOKIE_DURATION = timedelta(days=30)
class ConfigDevelop(Config):

    # BASE DE DATOS CONFIGURACION
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://huber:huber123@localhost/app_flujo_caja'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG  = True



class ConfigProduction(Config):
    
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://huber:huber123@localhost/app_flujo_caja'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG  = False