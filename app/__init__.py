from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    """
      Inicializa o aplicativo e registra os blueprints.

      Este arquivo contem a configuracao base do aplicativo Flask, incluindo
      a inicializacao de extensoes e o registro de blueprints.
      """

    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'main.login'

    from app import models
    from app.routes import register_blueprints
    register_blueprints(app)

    # ✅ Protege o banco: só cria se não existir
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace("sqlite:///", "")
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import Usuario
        return Usuario.query.get(int(user_id))

    return app