from models import Paciente, Usuario, Arquivo
from config import app, db, os, supabase_client
from flask import request, flash, redirect, render_template, Blueprint
from .recursos import Status
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
import shutil

paciente_bp = Blueprint('paciente_bp', __name__)

#################### RENDERS ####################

@paciente_bp.route('/pacientes', methods=['GET'])
@login_required
def pacientes():
    pacientes = current_user.pacientes

    for paciente in pacientes:
        data_nascimento_br = paciente.data_nascimento.strftime('%d/%m/%Y')
        paciente.data_nascimento = data_nascimento_br
    return render_template('logado/pacientes.html', pacientes=pacientes)

@paciente_bp.route('/paciente/<int:id_do_paciente>', methods=['GET'])
@login_required
def ver_paciente(id_do_paciente):
    paciente = db.session.query(Paciente).join(Usuario).filter(
        Paciente.id == id_do_paciente,
        Usuario.id == current_user.id
    ).first()
    return render_template("logado/editar_paciente.html", paciente = paciente)

@paciente_bp.route('/cadastrar', methods=['GET'])
@login_required
def cadastrar_paciente_page():
    return render_template('logado/cadastro_paciente.html')


#################### ROUTES ####################

@paciente_bp.route('/cadastrar', methods=['POST'])
@login_required
def cadastrar_paciente_post():
    status = Status("[SUCESSO] Paciente cadastrado com sucesso!", "sucess")

    nome_completo = request.form['nome']
    data_nascimento = request.form['nascimento']
    data_nascimento =  datetime.strptime(data_nascimento, '%Y-%m-%d').date()
    cpf = request.form['cpf']
    endereco = request.form.get('endereco')
    telefone = request.form.get('telefone')
    email = request.form.get('email')
    

    novo_paciente = Paciente(
        nome_completo=nome_completo,
        data_nascimento=data_nascimento,
        cpf=cpf,
        endereco=endereco,
        telefone=telefone,
        email=email,
        usuario_id = current_user.id,
        data_de_cadastro = datetime.now(),
    )

    try:
        db.session.add(novo_paciente)
        db.session.commit()
        status.message = "[SUCESSO] Paciente cadastrado com sucesso!"
        status.category = "sucess"
        flash(status.message, status.category)
        return redirect(f"/paciente/paciente/{novo_paciente.id}")

    except Exception as e:
        print(e)
        status.message = "[ERROR] Ocorreu algum erro no cadastro do paciente!"
        status.category = "error"
        db.session.rollback()

    flash(status.message, status.category)
    return redirect("/paciente/pacientes")

@paciente_bp.route('/excluir/<int:id_do_paciente>', methods=['POST'])
@login_required
def excluir_paciente(id_do_paciente):
    status = Status("[SUCESSO] Paciente excluido com sucesso!", "sucess")

    paciente_para_deletar = db.session.query(Paciente).join(Usuario).filter(
        Paciente.id == id_do_paciente,
        Usuario.id == current_user.id
    ).first()

    diretorio = f"{current_user.id}/{paciente_para_deletar.id}"

    pastas = {
        "arquivos": supabase_client.storage.from_(app.config['UPLOAD_FOLDER']).list(f"{diretorio}/arquivos"),
        "termos": supabase_client.storage.from_(app.config['UPLOAD_FOLDER']).list(f"{diretorio}/termos")
    }

    caminhos_dos_arquivos = []
    for nome, arquivos in pastas.items():
        caminhos_dos_arquivos += [f"{diretorio}/{nome}/{item['name']}" for item in arquivos]

    caminhos_dos_arquivos = caminhos_dos_arquivos if len(caminhos_dos_arquivos) > 0 else ['']
    
    if paciente_para_deletar:
        try:
            supabase_client.storage.from_(app.config['UPLOAD_FOLDER']).remove(caminhos_dos_arquivos)
            db.session.delete( paciente_para_deletar)
            db.session.commit() 
        except Exception as e:
            db.session.rollback()
            status.message = "[ERROR] Ocorreu um erro ao excluir o paciente."
            print(e)
            status.category = "error"
    
    flash(status.message, status.category)
    return redirect("/paciente/pacientes")

@paciente_bp.route('/editar/<int:id_do_paciente>', methods=['POST'])
@login_required
def editar_paciente_post(id_do_paciente):
    status = Status("[SUCESSO] Paciente editado com sucesso!", "sucess")
    paciente = db.session.query(Paciente).join(Usuario).filter(
        Paciente.id == id_do_paciente,
        Usuario.id == current_user.id
    ).first()

    paciente.nome_completo = request.form['nome']
    data_nascimento = request.form['nascimento']
    paciente.data_nascimento =  datetime.strptime(data_nascimento, '%Y-%m-%d').date()
    paciente.cpf = request.form['cpf']
    paciente.endereco = request.form.get('endereco')
    paciente.telefone = request.form.get('telefone')
    paciente.email = request.form.get('email')

    anamnese = request.files.get('anamnese')

    if anamnese.filename != '':
        extensao = anamnese.filename.split('.')[-1]
        filename = secure_filename(f"anamnese.{extensao}")
        diretorio_do_paciente = os.path.join(app.config['UPLOAD_FOLDER'], str(paciente.id))
        filepath = os.path.join(diretorio_do_paciente, filename)

        if paciente.anamnese_filepath != '':
            filepath_antigo = os.path.join(diretorio_do_paciente, paciente.anamnese_filepath)
            os.remove(filepath_antigo)


        anamnese.save(filepath)
        paciente.anamnese_filepath = filename

    try:
        db.session.commit()
        status.message = "[SUCESSO] Paciente editado com sucesso!"
        status.category = "sucess"

    except Exception as e:
        status.message = "[ERROR]"
        status.category = "error"
        db.session.rollback()

    flash(status.message, status.category)
    return redirect(f'/ver-paciente/{paciente.id}')