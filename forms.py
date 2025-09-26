from flask_wtf import FlaskForm
import wtforms as field
from wtforms.validators import Email, InputRequired

class LoginForm(FlaskForm):
    email = field.EmailField('Email', validators=[
        InputRequired(),
        Email(message='Endereço de email inválido.')
    ])

    senha = field.PasswordField('Senha', validators=[
        InputRequired(message='A senha é obrigatória.')
    ])


class PacienteForm(FlaskForm):
    nome = field.StringField('Nome', validators=[
        InputRequired(message='O nome é obrigatório.')
    ])

    data_de_nascimento = field.DateField('Data de Nascimento', format='%Y-%m-%d', validators=[
        InputRequired(message='A data de nascimento é obrigatória.')
    ])

    cpf = field.StringField('CPF', validators=[
        InputRequired(message='O CPF é obrigatório.')
    ])

    endereco = field.StringField('Endereço', validators=[
        InputRequired(message='O endereço é obrigatório.')
    ])

    telefone = field.StringField('Telefone', validators=[
        InputRequired(message='O telefone é obrigatório.')
    ])

    email = field.EmailField('Email', validators=[
        InputRequired(message='O email é obrigatório.'),  
        Email(message='Endereço de email inválido.')
    ])

class AtendimentoForm(FlaskForm):
    data_do_procedimento = field.DateField('Data do Procedimento', format='%Y-%m-%d', validators=[
        InputRequired(message='A data do procedimento é obrigatória.')
    ])

    hora_do_procedimento = field.TimeField('Hora do Procedimento', format='%H:%M', validators=[
        InputRequired(message='A hora do procedimento é obrigatória.')
    ])

    nome_do_procedimento = field.StringField('Nome do Procedimento', validators=[
        InputRequired(message='O nome do procedimento é obrigatório.')
    ])

    termo_de_consentimento = field.FileField('Termo de Consentimento', validators=[
        InputRequired(message='O termo de consentimento é obrigatório.')
    ])

    preparo = field.StringField('Preparo', validators=[
        InputRequired(message='O preparo é obrigatório.')
    ])

    evolucao = field.StringField('Evolução', validators=[
        InputRequired(message='A evolução é obrigatória.')
    ])

    retorno_data = field.DateField('Data de Retorno', format='%Y-%m-%d', validators=[
        InputRequired(message='A data de retorno é obrigatória.')
    ])

    retorno_hora = field.TimeField('Hora de Retorno', format='%H:%M', validators=[
        InputRequired(message='A hora de retorno é obrigatória.') 
    ])

    observacoes_do_retorno = field.StringField('Observações do Retorno', validators=[
        InputRequired(message='As observações do retorno são obrigatórias.')
    ])

class AgendamentoForm(FlaskForm):
    data_do_agendamento = field.DateField('Data do Agendamento', format='%Y-%m-%d', validators=[
        InputRequired(message='A data do agendamento é obrigatória.')
    ])

    hora_do_agendamento = field.TimeField('Hora do Agendamento', format='%H:%M', validators=[
        InputRequired(message='A hora do agendamento é obrigatória.')
    ])

    paciente_id = field.IntegerField('ID do Paciente', validators=[
        InputRequired(message='O ID do paciente é obrigatório.')
    ])


class ProtocoloForm(FlaskForm):
    nome = field.StringField('Nome', validators=[
        InputRequired(message='O nome do protocolo é obrigatório.')
    ])

    descricao = field.TextAreaField('Descrição', validators=[
        InputRequired(message='A descrição do protocolo é obrigatória.')
    ])

    arquivo = field.FileField('Arquivo', validators=[
        InputRequired(message='O arquivo do protocolo é obrigatório.')
    ])