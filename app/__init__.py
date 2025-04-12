from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    from app import models  # # ← IMPORTANTE! Isso ativa seus models no banco
    
    #  Carregador do usuário
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import Usuario
        return Usuario.query.get(int(user_id))

    # Registro de blueprint
    from app.routes import main
    app.register_blueprint(main)
    
    # Criação das tabelas automaticamente
    with app.app_context():
        db.create_all()

    return app