from flask import Blueprint
from models import Usuario
from config import db
teste_bp = Blueprint('teste_bp', __name__)

@teste_bp.route("/") # Rota para efetuar testes, APAGAR APÓS TESTES
def testes():
    usuario = Usuario()
    usuario.nome = "admin"
    usuario.email = "bryancarvalho20@gmail.com"
    usuario.senha = "123"
    db.session.add(usuario)
    db.session.commit()
    return "Teste"





        



