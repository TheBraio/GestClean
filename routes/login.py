from models import Usuario
from flask import render_template, flash, redirect, Blueprint, request
from flask_login import login_user
from forms import LoginForm

login_bp = Blueprint('login_bp', __name__)


@login_bp.route('/', methods=['GET', 'POST']) # Rota para processar o formulário de login
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        senha = form.senha.data

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.check_password(senha):
            login_user(usuario)
            return redirect('/painel')
        
        flash("Email ou senha inválidos!", "error")

    if form.errors and request.method == 'POST':
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{field.capitalize()}: {error}", 'error')
                    
    return render_template('padrao/login.html', form=form)


