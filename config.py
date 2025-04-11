import os

class Config:
    SECRET_KEY = 'chave_secreta'
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'abrigo.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
