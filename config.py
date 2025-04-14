import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'chave_secreta'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'abrigo.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False