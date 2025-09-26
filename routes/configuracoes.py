from config import db
from flask import render_template, Blueprint, redirect, request, flash
from flask_login import login_required, logout_user, current_user
from .recursos import Status
configuracoes_bp = Blueprint('configuracoes_bp', __name__)

@configuracoes_bp.route('/', methods=['GET'])
@login_required
def configuracoes():
    return render_template('logado/configuracoes.html', usuario=current_user)

@configuracoes_bp.route('/trocar-senha', methods=['POST'])
@login_required
def trocar_senha():
    status = Status("Senha alterada com sucesso!", "success")


    senha_atual = request.form.get('senha_atual')
    nova_senha = request.form.get('nova_senha')

    if senha_atual and nova_senha:
        if current_user.check_password(senha_atual):
            current_user.senha = nova_senha
            db.session.commit()
        else:
            status.message = "Senha atual incorreta!"
            status.category = "error"
    else:
        status.message = "Por favor, preencha todos os campos!"
        status.category = "error"

    flash(status.message, status.category)
    return redirect('/configuracoes')