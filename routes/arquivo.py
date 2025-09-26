from config import db, os, app, supabase_client
from models import Arquivo,Atendimento
from flask import send_from_directory, Blueprint, request, jsonify, Response
from flask_login import login_required, current_user
from .recursos import Status
from werkzeug.utils import secure_filename

 
arquivo_bp = Blueprint('arquivo_bp', __name__)

@arquivo_bp.route('/excluir', methods=['POST'])
@login_required
def excluir_arquivo():
    id_do_arquivo = int(request.get_json()['id'])
    arquivo_para_deletar = db.session.query(Arquivo).filter(Arquivo.id == id_do_arquivo).first()
    paciente = arquivo_para_deletar.paciente
    if paciente.usuario_id == current_user.id:
        try:
            supabase_client.storage.from_(app.config['UPLOAD_FOLDER']).remove([arquivo_para_deletar.filepath])
            db.session.delete(arquivo_para_deletar)
            db.session.commit()
            return "OK"
        except Exception as e:
            db.session.rollback()
            print(e)

@arquivo_bp.route('/adicionar', methods=['POST'])
@login_required
def adicionar_arquivo():
    arquivo = request.files.get('arquivo') 
    extensao = os.path.splitext(arquivo.filename)[-1].lower()
    if extensao in app.config['ALLOWED_EXTENSIONS']:
        titulo = request.form.get('titulo')
        id_do_paciente = int(request.form.get('id_do_paciente'))
        if id_do_paciente:
            novo_arquivo = Arquivo(
                titulo=titulo,
                filepath=arquivo.filename,
                paciente_id=id_do_paciente,
            )

            db.session.add(novo_arquivo)
            db.session.flush()

            diretorio_do_arquivo = f"{current_user.id}/{id_do_paciente}/arquivos"

            filename = secure_filename(f"{titulo}_{novo_arquivo.id}{extensao}")
            filepath = diretorio_do_arquivo + '/' + filename
            novo_arquivo.filepath = filepath
            arquivo.filename = filename

            supabase_client.storage.from_(app.config['UPLOAD_FOLDER']).upload(file = arquivo.read(), path=filepath)

            db.session.commit()

            return jsonify({"status": "OK", "id_do_arquivo": novo_arquivo.id, "nome_do_arquivo": filename})
    else:
        return jsonify({"status": "ERROR", "message": "Arquivo não permitido."})
    
    

@arquivo_bp.route('/download/<int:id_do_arquivo>')
@login_required
def download_arquivo(id_do_arquivo):
    arquivo = Arquivo.query.get(id_do_arquivo)
    if arquivo.paciente_id != None:
        validado = arquivo.paciente.usuario_id == current_user.id
    elif arquivo.atendimento_id != None:
        validado = arquivo.atendimento.paciente.usuario_id == current_user.id
    else:
        validado = False

    if not validado:
        return jsonify({"status": "ERROR", "message": "Você não tem permissão para baixar este arquivo."})
    
    try:
        arquivo_binario = supabase_client.storage.from_(app.config['UPLOAD_FOLDER']).download(arquivo.filepath)

        if arquivo_binario is None:
            return jsonify({"status": "ERROR", "message": "Arquivo não encontrado."})
        
        headers = {
            "Content-Disposition": f"attachment; filename={os.path.basename(arquivo.filepath)}",
            "Content-Type": "application/octet-stream"
        }
    
        return Response(arquivo_binario, headers=headers)
    except Exception as e:
        print(e)
        return jsonify({"status": "ERROR", "message": "Erro ao baixar o arquivo."})

        
            

@arquivo_bp.route('/download/termo-responsabilidade/<int:id_do_atendimento>')
@login_required
def download_termo_responsabilidade(id_do_atendimento):
    atendimento = Atendimento.query.get(id_do_atendimento)
    if atendimento.paciente.usuario_id != current_user.id:
        return jsonify({"status": "ERROR", "message": "Você não tem permissão para baixar este arquivo."})
    filepath = atendimento.termo_filepath
    if filepath == '':
        return jsonify({"status": "ERROR", "message": "Você não tem termo de responsabilidade para este atendimento."})
    

    arquivo_binario = supabase_client.storage.from_(app.config['UPLOAD_FOLDER']).download(filepath)
    if arquivo_binario is None:
        return jsonify({"status": "ERROR", "message": "Arquivo não encontrado."})

    headers = {
        "Content-Disposition": f"attachment; filename={os.path.basename(filepath)}",
        "Content-Type": "application/octet-stream"
    }

    return Response(arquivo_binario, headers=headers)

# @download_bp.route('/anamnese/<int:id_do_paciente>')
# @login_required
# def download_anamnese(id_do_paciente):
#     paciente = Paciente.query.get(id_do_paciente)
#     diretorio_do_paciente = os.path.join(app.config['UPLOAD_FOLDER'], str(paciente.id))
#     return send_from_directory(diretorio_do_paciente, paciente.anamnese_filepath, as_attachment=True)

# @download_bp.route('/termo/<int:id_do_atendimento>')
# @login_required
# def download_termo(id_do_atendimento):
#     atendimento = Atendimento.query.get(id_do_atendimento)

#     diretorio_do_paciente = os.path.join(app.config['UPLOAD_FOLDER'], str(atendimento.paciente.id))
#     return send_from_directory(diretorio_do_paciente, atendimento.termo_filepath, as_attachment=True)
