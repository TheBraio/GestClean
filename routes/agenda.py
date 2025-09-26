from config import db
from models import Paciente, Agendamento, Usuario
from flask import render_template, request, redirect, flash, Blueprint, jsonify
from datetime import datetime, date
from flask_login import login_required, current_user
from .recursos import Status
from forms import AgendamentoForm

agenda_bp =  Blueprint('agenda_bp', __name__)

#################### RENDERS ####################

@agenda_bp.route('/', methods=['GET', 'POST'])
@login_required
def agenda():
    form = AgendamentoForm()
    filtro_data = request.args.get('filtro-data')
    if filtro_data:
        agendamentos = db.session.query(Agendamento).join(Usuario).filter(
            Usuario.id == current_user.id,
            Agendamento.data == filtro_data
        ).order_by(Agendamento.hora.asc()).all()
        filtro_data = True
    else:
        agendamentos = db.session.query(Agendamento).join(Usuario).filter(
            Usuario.id == current_user.id
        ).order_by(Agendamento.data.asc(), Agendamento.hora.asc()).all()
        filtro_data = False
        
    hoje = date.today()
    agora = datetime.now().time()

    for agendamento in agendamentos:
        if agendamento.data < hoje:
            agendamento.passou = True
        # Se é hoje, verificar se a hora já passou
        elif agendamento.data == hoje:
            agendamento.passou = agendamento.hora < agora
        else:
            agendamento.passou = False
        
        
    pacientes = db.session.query(Paciente).join(Usuario).filter(
        Usuario.id == current_user.id
    ).order_by(Paciente.nome_completo.asc()).all()
    return render_template('logado/agenda.html', agendamentos=agendamentos, pacientes=pacientes, filtro_data=filtro_data, form=form)


#################### ROUTES ####################


@agenda_bp.route('/editar/<int:id_do_agendamento>', methods=['POST'])
@login_required
def editar_agendamento(id_do_agendamento):
    status = Status("[SUCESSO] Agendamento editado com sucesso!", "sucess")
    agendamento = db.session.query(Agendamento).join(Usuario).filter(
        Usuario.id == current_user.id,
        Agendamento.id == id_do_agendamento
    ).first()

    if not agendamento:
        return jsonify({"status": "ERROR", "message": "Você não tem permissão para editar esse agendamento."})

    form = AgendamentoForm()

    paciente_id = request.form.get('paciente')
    data_agendamento = request.form.get('data')
    hora_agendamento = request.form.get('horario')
    nome_procedimento = request.form.get('procedimento')
    
    if not all([paciente_id, data_agendamento, hora_agendamento, nome_procedimento]):
        status.message = "[ERROR] Todos os campos são obrigatórios."
        status.category = "error"
        flash(status.message, status.category)
        return redirect('/agenda')

    agendamento.paciente_id = paciente_id
    agendamento.data = datetime.strptime(data_agendamento, '%Y-%m-%d').date()
    agendamento.hora = datetime.strptime(hora_agendamento, '%H:%M').time()
    agendamento.nome_procedimento = nome_procedimento

    try:
        db.session.commit()
        status.message = "[SUCESSO] Agendamento editado com sucesso!"
        status.category = "sucess"
    except Exception as e:
        status.message = "[ERROR] Ocorreu um erro ao editar o agendamento."
        status.category = "error"
        db.session.rollback()

    flash(status.message, status.category)
    return redirect('/agenda')

@agenda_bp.route('/cancelar/<int:id_do_agendamento>', methods=['POST'])
@login_required
def cancelar_agendamento(id_do_agendamento):
    status = Status("[SUCESSO] Agendamento cancelado com sucesso!", "sucess")
    agendamento = db.session.query(Agendamento).join(Usuario).filter(
        Usuario.id == current_user.id,
        Agendamento.id == id_do_agendamento
    ).first()
    try: 
        db.session.delete(agendamento)
        db.session.commit()
        status.message = "[SUCESSO] Agendamento cancelado com sucesso!"
        status.category = "sucess"
    except Exception as e:
        status.message = "[ERROR] Ocorreu um erro ao cancelar o agendamento."
        status.category = "error"
        db.session.rollback()

    flash(status.message, status.category)
    return redirect('/agenda')

@agenda_bp.route('/adicionar', methods=['POST'])
@login_required
def adicionar_agendamento():
    status = Status("[SUCESSO] Agendamento adicionado com sucesso!", "sucess")
    form_data = request.form
    paciente_id = form_data.get('paciente')
    data_agendamento = form_data.get('data')
    hora_agendamento = form_data.get('horario')
    nome_procedimento = form_data.get('procedimento')

    # Validar se todos os campos obrigatórios foram preenchidos
    if not all([paciente_id, data_agendamento, hora_agendamento, nome_procedimento]):
        status.message = "[ERROR] Todos os campos são obrigatórios."
        status.category = "error"
        flash(status.message, status.category)
        return redirect('/agenda')

    try:
        data_obj = datetime.strptime(data_agendamento, '%Y-%m-%d').date()
        hora_obj = datetime.strptime(hora_agendamento, '%H:%M').time()
    except ValueError:
        status.message = "[ERROR] Formato de data ou hora inválido."
        status.category = "error"
        flash(status.message, status.category)
        return redirect('/agenda')

    new_agendamento = Agendamento(
        paciente_id=paciente_id,
        usuario_id=current_user.id,
        data=data_obj,
        hora=hora_obj,
        nome_procedimento=nome_procedimento
    )
    
    try:
        db.session.add(new_agendamento)
        db.session.commit()
        status.message = "[SUCESSO] Agendamento adicionado com sucesso!"
        status.category = "sucess"
    except Exception as e:
        status.message = "[ERROR] Ocorreu um erro ao adicionar o agendamento."
        status.category = "error"
        db.session.rollback()

    flash(status.message, status.category)
    return redirect('/agenda')




