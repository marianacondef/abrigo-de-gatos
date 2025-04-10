from . import db
from flask_login import UserMixin
from datetime import datetime

# Usuário
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(20), default="geral")  # admin, funcionario, candidato, geral

    favoritos = db.relationship("Gato", secondary="favoritos", backref="favoritado_por")
    adotou = db.relationship("Adocao", backref="usuario", lazy=True)

# Gato
class Gato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer)
    peso = db.Column(db.Float)
    chip = db.Column(db.String(50), unique=True)
    status = db.Column(db.String(50), default="disponível")  # adotado, em tratamento, etc.

    adocoes = db.relationship("Adocao", backref="gato", lazy=True)

# Adoção
class Adocao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    gato_id = db.Column(db.Integer, db.ForeignKey("gato.id"), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="em análise")  # aprovada, recusada, etc.

# Tabela de Favoritos (relacionamento muitos para muitos)
favoritos = db.Table("favoritos",
    db.Column("usuario_id", db.Integer, db.ForeignKey("usuario.id")),
    db.Column("gato_id", db.Integer, db.ForeignKey("gato.id"))
)