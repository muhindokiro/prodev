import os

class Config:


    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://blaise:tribune@localhost/projo'
    SECRET_KEY = 'matatu'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    

    # email configurations
   
    
class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    pass

class TestConfig(Config):

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://blaise:tribune@localhost/projo'

# class Config(Config):
#     SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://blaise:tribune@localhost/projo'

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://blaise:tribune@localhost/projo'

    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig
}
