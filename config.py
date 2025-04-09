import os

class Config:
    SECRET_KEY = 'chave_secreta'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///abrigo.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
