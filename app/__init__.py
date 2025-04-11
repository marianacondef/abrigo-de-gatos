from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    from app import models  # ← IMPORTANTE! Isso ativa seus models no banco

    return app