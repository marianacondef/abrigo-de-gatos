from . import db
from flask_login import UserMixin
from datetime import datetime


class Usuario(UserMixin, db.Model):
    """
    Representa os usuarios no sistema.

    Atributos:
        id (int): ID unico do usuario.
        nome (str): Nome do usuario.
        email (str): Email do usuario.
        senha (str): Hash da senha do usuario.
        is_admin (bool): Indica se o usuario tem privilegios de administrador.
    """

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    # Indica o grupo do qual o usuario faz parte
    tipo = db.Column(db.String(20), default="geral")

    @property
    def is_admin(self):
        return self.tipo == 'admin'

    def __repr__(self):
        return f"<Usuario {self.nome}>"

    favoritos = db.relationship("Gato", secondary="favoritos", backref="favoritado_por")
    adotou = db.relationship("Adocao", backref="usuario", lazy=True)

# Gatos
class Gato(db.Model):
    """
       Representa os gatos no sistema.

       Atributos:
           id (int): ID unico do gato.
           nome (str): Nome do gato.
           idade (int): Idade do gato (em anos).
           peso (float): Peso do gato (em quilogramas).
           chip (str): Numero do chip do gato (se aplicavel).
           status (str): Status atual do gato (ex: "Disponivel", "Adotado").
           imagem (str): Caminho para a imagem do gato.
       """

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
    """
       Representa as adocoes de gatos pelos usuarios.

       Atributos:
           id (int): ID unico da adocao.
           usuario_id (int): ID do usuario que fez a adocao.
           gato_id (int): ID do gato sendo adotado.
           status (str): Status da adocao (ex: "Em analise", "Aceita", "Recusada").
       """

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    gato_id = db.Column(db.Integer, db.ForeignKey("gato.id"), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    # Indica o status em que se encontra o processo (Em análise, recusada, aprovada, etc)
    status = db.Column(db.String(50), default="Em análise")

# Medicamento
class Medicacao(db.Model):
    """
        Representa as medicacoes administradas aos gatos.

        Atributos:
            id (int): ID unico da medicacao.
            nome (str): Nome da medicacao.
            dosagem (str): Dosagem administrada.
            frequencia (str): Frequencia da administracao.
            data_inicio (date): Data inicial da administracao.
            data_fim (date, opcional): Data final da administracao.
            gato_id (int): ID do gato relacionado a medicacao.
        """

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