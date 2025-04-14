from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    from app import models

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import Usuario
        return Usuario.query.get(int(user_id))

    from app.routes import main
    app.register_blueprint(main)

    # ✅ Protege o banco: só cria se não existir
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace("sqlite:///", "")
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()

    return app