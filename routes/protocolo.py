from config import app, os, db, supabase_client
from flask import render_template, request, Blueprint, jsonify, redirect, flash, Response
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import Protocolo, Usuario
from .recursos import Status


protocolo_bp = Blueprint('protocolo_bp', __name__)

@protocolo_bp.route('/protocolos/', methods=['GET'])
@login_required
def protocolos():
    protocolos = db.session.query(Protocolo).join(Usuario).filter(
        Usuario.id == current_user.id
    ).all()
    return render_template('logado/protocolos.html', protocolos=protocolos)

@protocolo_bp.route('/adicionar', methods=['POST'])
@login_required
def adicionar_protocolo():
    status = Status("[SUCESSO] Protocolo cadastrado com sucesso!", "sucess")
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    arquivo = request.files.get('arquivo')

    if arquivo.filename == '':
        return jsonify({"status": "ERROR", "message": "Você não selecionou um arquivo."})
    extensao = os.path.splitext(arquivo.filename)[-1].lower()
    if extensao not in app.config['ALLOWED_EXTENSIONS']:
        return jsonify({"status": "ERROR", "message": "Arquivo não permitido."})

    novo_protocolo = Protocolo(
        nome=nome,
        descricao=descricao,
        filepath="",
        usuario_id=current_user.id
    )

    db.session.add(novo_protocolo)
    db.session.flush()




    diretorio_do_protocolo = f"{current_user.id}/protocolos"

    filename = secure_filename(f"{nome}{novo_protocolo.id}{extensao}")
    filepath = f"{diretorio_do_protocolo}/{filename}"
    novo_protocolo.filepath = filepath
    

    try:
        supabase_client.storage.from_(app.config['UPLOAD_FOLDER']).upload(path=filepath, file=arquivo.read())
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        status.message = f"[ERRO] Falha ao salvar o protocolo"
        status.category = "error"

    flash(status.message, status.category)

    return redirect("/protocolo/protocolos")

@protocolo_bp.route('/editar/<int:id_do_protocolo>', methods=['POST'])
@login_required
def editar_protocolo(id_do_protocolo):
    status = Status("[SUCESSO] Protocolo editado com sucesso!", "sucess")
    protocolo = db.session.query(Protocolo).join(Usuario).filter(
        Usuario.id == current_user.id,
        Protocolo.id == id_do_protocolo
    ).first()
    if not protocolo:
        return jsonify({"status": "ERROR", "message": "Você não tem permissão para editar este protocolo."})

    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    arquivo = request.files.get('arquivo')

    if arquivo.filename != '':
        extensao = os.path.splitext(arquivo.filename)[-1].lower()
        if extensao not in app.config['ALLOWED_EXTENSIONS']:
            return jsonify({"status": "ERROR", "message": "Arquivo não permitido."})
        

        nome_do_arquivo = secure_filename(f"{nome}{protocolo.id}{extensao}")
        caminho_do_arquivo = f"{current_user.id}/protocolos/{nome_do_arquivo}"
  
        supabase_client.storage.from_(app.config['UPLOAD_FOLDER']).remove([protocolo.filepath])

        protocolo.filepath = caminho_do_arquivo
        supabase_client.storage.from_(app.config['UPLOAD_FOLDER']).upload(path=caminho_do_arquivo, file=arquivo.read())


    protocolo.nome = nome
    protocolo.descricao = descricao

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        status.message = f"[ERRO] Falha ao editar o protocolo."
        status.category = "error"

    flash(status.message, status.category)

    return redirect("/protocolo/protocolos")

@protocolo_bp.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_protocolo(id):
    status = Status("[SUCESSO] Protocolo excluído com sucesso!", "sucess")
    protocolo = db.session.query(Protocolo).join(Usuario).filter(
        Usuario.id == current_user.id,
        Protocolo.id == id
    ).first()
    if not protocolo:
        return jsonify({"status": "ERROR", "message": "Você não tem permissão para excluir este protocolo."})

    try:
        supabase_client.storage.from_(app.config['UPLOAD_FOLDER']).remove([protocolo.filepath])
        db.session.delete(protocolo)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "ERROR", "message": f"Falha ao excluir o protocolo: {e}"})

    flash(status.message, status.category)
    return redirect("/protocolo/protocolos")

@protocolo_bp.route('/download/<int:id_do_protocolo>', methods=['GET'])  
@login_required
def download_protocolo(id_do_protocolo):
    protocolo = db.session.query(Protocolo).join(Usuario).filter(
        Usuario.id == current_user.id,
        Protocolo.id == id_do_protocolo
    ).first()
    if not protocolo:
        return jsonify({"status": "ERROR", "message": "Você não tem permissão para baixar este protocolo."})

    arquivo_binario = supabase_client.storage.from_(app.config['UPLOAD_FOLDER']).download(protocolo.filepath)

    headers = {
        "Content-Disposition": f"attachment; filename={os.path.basename(protocolo.filepath)}",
        "Content-Type": "application/octet-stream"
    }

    return Response(arquivo_binario, headers=headers)