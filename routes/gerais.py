from flask import render_template, Blueprint, url_for, redirect
from flask_login import login_required, logout_user, current_user
from .recursos import contar_novos_pacientes, contar_consultas
from datetime import datetime, timezone

gerais_bp = Blueprint('gerais_bp', __name__)

@gerais_bp.route('/painel', methods=['GET'])
@login_required
def painel():

    novos_pacientes_mes = contar_novos_pacientes()
    pacientes_mes_anterior = contar_novos_pacientes(-1)

    percentual_de_pacientes = 0
    if pacientes_mes_anterior == 0 and novos_pacientes_mes != 0:
        percentual_de_pacientes = float('inf')
    elif pacientes_mes_anterior != 0 and novos_pacientes_mes != 0:
        percentual_de_pacientes = ((novos_pacientes_mes / pacientes_mes_anterior) * 100) - 100
        percentual_de_pacientes = round(percentual_de_pacientes, 2)

    consultas_hoje = contar_consultas()
    consultas_ontem = contar_consultas(datetime.now(timezone.utc).replace(day=datetime.now(timezone.utc).day - 1))

    percentual_de_consultas = 0
    if consultas_ontem == 0 and consultas_hoje != 0:
        percentual_de_consultas = float('inf')
    elif consultas_ontem != 0 and consultas_hoje != 0:
        percentual_de_consultas = ((consultas_hoje / consultas_ontem) * 100) - 100
        percentual_de_consultas = round(percentual_de_consultas, 2)

    return render_template('logado/painel.html', usuario=current_user, 
    pacientes = {
        'novos': novos_pacientes_mes,
        'percentual': percentual_de_pacientes
    }, consultas={
        'hoje': consultas_hoje,
        'percentual': percentual_de_consultas
    })

@gerais_bp.route('/logout', methods=['GET']) # Rota para sair do sistema
def logout():
    logout_user()
    return url_for('gerais_bp.home')

@gerais_bp.route('/', methods=['GET'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('gerais_bp.painel'))
    return render_template('padrao/home.html')