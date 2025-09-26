#
# Apenas recursos para usar em outros controllers
#
from config import app, os, db
from models import Paciente, Usuario, Agendamento
from flask_login import current_user
from datetime import datetime, timezone
from sqlalchemy import extract

class Status:
    def __init__(self, message: str, category: str):
        self.message = message
        self.category = category

def contar_novos_pacientes(mes=0,ano=0):
    data_atual = datetime.now(timezone.utc)
    novos_pacientes_mes = db.session.query(Paciente).join(Usuario).filter(
        Usuario.id == current_user.id,
        extract('month', Paciente.data_de_cadastro) == (data_atual.month + mes),
        extract('year', Paciente.data_de_cadastro) == (data_atual.year + ano)
    ).count()

    return novos_pacientes_mes

def contar_consultas(data=None):
    if data is None:
        data = datetime.now(timezone.utc)
    consultas = db.session.query(Agendamento).join(Usuario).filter(
        Usuario.id == current_user.id,
        extract('month', Agendamento.data) == data.month,
        extract('year', Agendamento.data) == data.year,
        extract('day', Agendamento.data) == data.day
    ).count()

    return consultas

@app.template_filter('filename')
def filename(filepath):
    return os.path.basename(filepath)

