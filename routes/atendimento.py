from config import app, db, os, supabase_client
from models import Paciente, Atendimento, Agendamento, Usuario
from flask import render_template, request, redirect, flash, Blueprint, jsonify
from datetime import datetime
from flask_login import current_user, login_required
from .recursos import Status
from werkzeug.utils import secure_filename

atendimento_bp = Blueprint('atendimento_bp', __name__)

#################### RENDERS ####################

@atendimento_bp.route('/atendimento/<int:id_do_atendimento>', methods=['GET'])
@login_required
def ver_atendimento(id_do_atendimento):
    atendimento = db.session.query(Atendimento).filter(Atendimento.id == id_do_atendimento).first()
    if atendimento and atendimento.paciente.usuario.id == current_user.id:
        return render_template("logado/editar_atendimento.html", atendimento=atendimento, nome_do_paciente=atendimento.paciente.nome_completo)
    return 404

@atendimento_bp.route("/cadastrar/<int:id_do_paciente>", methods=['GET'])
@login_required
def cadastrar_atendimento(id_do_paciente):
    paciente = db.session.query(Paciente).join(Usuario).filter(
        Paciente.id == id_do_paciente,
        Usuario.id == current_user.id
    ).first()
    return render_template("logado/cadastro_atendimento.html", paciente=paciente)

@atendimento_bp.route("/atendimentos/<int:id_do_paciente>", methods=["GET"])
@login_required
def atendimentos(id_do_paciente):
    paciente = db.session.query(Paciente).join(Usuario).filter(
        Paciente.id == id_do_paciente,
        Usuario.id == current_user.id
    ).first()

    atendimentos_formatados = []
    for atendimento in paciente.atendimentos:
        data_procedimento_br = atendimento.data_procedimento.strftime('%d/%m/%Y') if atendimento.data_procedimento else ''
        hora_procedimento_br = atendimento.hora_procedimento.strftime('%H:%M') if atendimento.hora_procedimento else ''
        data_retorno_br = atendimento.data_retorno.strftime('%d/%m/%Y') if atendimento.data_retorno else ''
        hora_retorno_br = atendimento.hora_retorno.strftime('%H:%M') if atendimento.hora_retorno else ''
        
        atendimentos_formatados.append({
            'id': atendimento.id,
            'nome_procedimento': atendimento.nome_procedimento,
            'data_procedimento': data_procedimento_br,
            'hora_procedimento': hora_procedimento_br,
            'data_retorno': data_retorno_br,
            'hora_retorno': hora_retorno_br,
        })
    
    return render_template("logado/atendimentos.html", paciente=paciente, atendimentos=atendimentos_formatados)

#################### ROUTES ####################

@atendimento_bp.route("/editar/<int:id_do_atendimento>", methods=['POST'])
@login_required
def editar_atendimento_post(id_do_atendimento):    
    status = Status("[SUCESSO] Atendimento editado com sucesso!", "sucess")

    atendimento = Atendimento.query.get(id_do_atendimento)

    atendimento.nome_procedimento = request.form.get('nome-procedimento')
    data_procedimento = request.form.get('data-procedimento')
    atendimento.data_procedimento = datetime.strptime(data_procedimento, '%Y-%m-%d').date()
    
    hora_procedimento = request.form.get('hora-procedimento')
    atendimento.hora_procedimento = datetime.strptime(hora_procedimento, '%H:%M').time() if hora_procedimento else None
    
    atendimento.preparo = request.form.get('preparo')
    atendimento.evolucao = request.form.get('evolucao')
    
    data_retorno = request.form.get('data-retorno')
    atendimento.data_retorno = datetime.strptime(data_retorno, '%Y-%m-%d').date() if data_retorno else None
    
    hora_retorno = request.form.get('hora-retorno')
    atendimento.hora_retorno = datetime.strptime(hora_retorno, '%H:%M').time() if hora_retorno else None
    
    atendimento.observacoes_retorno = request.form.get('observacoes-retorno')

    termo_consentimento = request.files.get('termo-consentimento')
    extensao = os.path.splitext(termo_consentimento.filename)[-1].lower()        
    if termo_consentimento.filename != '':
        if extensao not in app.config['ALLOWED_EXTENSIONS']:
            return jsonify({"status": "ERROR", "message": "Arquivo não permitido."})

        filename = secure_filename(f"Termo-de-responsabilidade_{atendimento.id}{extensao}")
        diretorio_do_arquivo = f"{current_user.id}/{atendimento.paciente.id}/termos/{filename}"

        atendimento.termo_filepath = diretorio_do_arquivo

    try:
        
        db.session.commit()
        status.message = "[SUCESSO] Atendimento editado com sucesso!"
        status.category = "sucess"
        if termo_consentimento.filename != '':
            supabase_client.storage.from_(app.config['UPLOAD_FOLDER']).upload(file = termo_consentimento.read(), path=diretorio_do_arquivo, 
            file_options={'upsert':'true'}                                                             
        )
    except Exception as e:
        status.message = "[ERROR]"
        print(e)
        status.category = "error"
        db.session.rollback()

    flash(status.message, status.category)
    return redirect(f"/atendimento/atendimentos/{atendimento.paciente.id}")

@atendimento_bp.route("/cadastrar/<int:id_do_paciente>", methods=['POST'])
@login_required
def cadastrar_atendimento_post(id_do_paciente):
    status = Status("[SUCESSO] Atendimento cadastrado com sucesso!", "sucess")

    nome_procedimento = request.form.get('nome-procedimento')
    data_procedimento = request.form.get('data-procedimento')
    data_procedimento = datetime.strptime(data_procedimento, '%Y-%m-%d').date()
    hora_procedimento = request.form.get('hora-procedimento')
    hora_procedimento = datetime.strptime(hora_procedimento, '%H:%M').time() if hora_procedimento else None
    historico_saude = request.form.get('historico-saude')
    preparo = request.form.get('preparo')
    evolucao = request.form.get('evolucao')
    data_retorno = request.form.get('data-retorno')
    data_retorno = datetime.strptime(data_retorno, '%Y-%m-%d').date() if data_retorno else None
    hora_retorno = request.form.get('hora-retorno')
    hora_retorno = datetime.strptime(hora_retorno, '%H:%M').time() if hora_retorno else None
    observacoes_retorno = request.form.get('observacoes-retorno')

    new_atendimento = Atendimento(
        paciente_id = id_do_paciente,
        nome_procedimento = nome_procedimento,
        data_procedimento = data_procedimento,
        hora_procedimento = hora_procedimento,
        historico_saude = historico_saude,
        preparo = preparo,
        evolucao = evolucao,
        data_retorno = data_retorno,
        hora_retorno = hora_retorno,
        observacoes_retorno = observacoes_retorno,
        termo_filepath = ''
    )

    db.session.add(new_atendimento)
    db.session.flush()

    termo_consentimento = request.files.get('termo-consentimento')
    extensao = os.path.splitext(termo_consentimento.filename)[-1].lower()
    diretorio_do_arquivo = False
    if termo_consentimento.filename != '':
        if extensao not in app.config['ALLOWED_EXTENSIONS']:
            return jsonify({"status": "ERROR", "message": "Arquivo não permitido."})


        filename = secure_filename(f"Termo-de-responsabilidade_{new_atendimento.id}{extensao}")
        diretorio_do_arquivo = f"{current_user.id}/{new_atendimento.paciente.id}/termos/{filename}"

        new_atendimento.termo_filepath = diretorio_do_arquivo


    new_agendamento = Agendamento(
        paciente_id = id_do_paciente,
        usuario_id = current_user.id,
        data = data_retorno,
        hora = hora_retorno,
        nome_procedimento = nome_procedimento+" - Retorno"
    )

    db.session.add(new_agendamento)
    try:
        db.session.commit()
        status.message = "[SUCESSO] Atendimento cadastrado com sucesso!"
        status.category = "sucess"
        if termo_consentimento.filename != '':
            supabase_client.storage.from_(app.config['UPLOAD_FOLDER']).upload(file = termo_consentimento.read(), path=diretorio_do_arquivo)

        return redirect(f"/atendimento/atendimento/{new_atendimento.id}")

    except Exception as e:
        status.message = "[ERROR] Ocorreu um erro ao cadastrar o atendimento."
        print(e)
        status.category = "error"
        db.session.rollback()

    flash(status.message, status.category)
    return redirect(f"/atendimento/atendimentos")

@atendimento_bp.route('/excluir/<int:id_do_atendimento>', methods=['POST'])
@login_required
def excluir_atendimento(id_do_atendimento):
    status = Status("[SUCESSO] Atendimento excluido com sucesso!", "sucess")

    atendimento = Atendimento.query.get_or_404(id_do_atendimento) 
    id_paciente = atendimento.paciente.id

    try:
        supabase_client.storage.from_(app.config['UPLOAD_FOLDER']).remove([atendimento.termo_filepath])
        db.session.delete(atendimento) 
        db.session.commit() 
    except Exception as e:
        db.session.rollback()
        status.message = "[ERROR] Ocorreu um erro ao excluir o atendimento."
        print(e)
        status.category = "error"
    
    flash(status.message, status.category)
    return redirect(f"/atendimento/atendimentos/{id_paciente}")











