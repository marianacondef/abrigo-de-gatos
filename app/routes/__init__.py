from app.routes.main import main as main_bp
from app.routes.gatos import gatos as gatos_bp
from app.routes.adocoes import adocoes as adocoes_bp
from app.routes.medicacoes import medicacoes as medicacoes_bp

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(gatos_bp, url_prefix="/gatos")
    app.register_blueprint(adocoes_bp, url_prefix="/adocoes")
    app.register_blueprint(medicacoes_bp, url_prefix="/medicacoes")
