import os

class Config:


    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://phirifo:1234@localhost/newsacco'
    SECRET_KEY = 'matatu'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    

    # email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USERNAME='juniormango2015@gmail.com'
    MAIL_PASSWORD='hmladlpbpvcyluyv'


   
    
class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    pass

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://phirifo:1234@localhost/newsacco_test'

# class Config(Config):
#     SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://blaise:tribune@localhost/projo'

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://phirifo:1234@localhost/newsacco'

    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig
}
