from . import db
from flask_login import UserMixin
from datetime import datetime

# Usuário
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    # Indica o grupo do qual o usuário faz parte
    tipo = db.Column(db.String(20), default="geral")

    def __repr__(self):
        return f"<Usuario {self.nome}>"

    favoritos = db.relationship("Gato", secondary="favoritos", backref="favoritado_por")
    adotou = db.relationship("Adocao", backref="usuario", lazy=True)

# Gatos
class Gato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer)
    peso = db.Column(db.Float)
    chip = db.Column(db.String(50), unique=True)
    imagem = db.Column(db.String(200))
    # Indica a situação do animal em questão (Em tratamento, adotado, em recuperação, etc)
    status = db.Column(db.String(50), default="disponível")

    adocoes = db.relationship("Adocao", backref="gato", lazy=True)

# Adoção
class Adocao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    gato_id = db.Column(db.Integer, db.ForeignKey("gato.id"), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    # Indica o status em que se encontra o processo (Em análise, recusada, aprovada, etc)
    status = db.Column(db.String(50), default="Em análise")

# Medicamento
class Medicacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gato_id = db.Column(db.Integer, db.ForeignKey("gato.id"), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    dosagem = db.Column(db.String(100), nullable=False)
    frequencia = db.Column(db.String(100), nullable=False)
    data_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    data_fim = db.Column(db.DateTime, nullable=True)

    gato = db.relationship("Gato", backref=db.backref("medicacoes", lazy=True))
    
favoritos = db.Table("favoritos",
    db.Column("usuario_id", db.Integer, db.ForeignKey("usuario.id")),
    db.Column("gato_id", db.Integer, db.ForeignKey("gato.id"))
)