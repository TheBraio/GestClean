from config import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Protocolo(db.Model):
    __tablename__ = 'protocolo'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    filepath = db.Column(db.String(200), nullable=False)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete="CASCADE"), nullable=False)
    usuario = db.relationship('Usuario', back_populates='protocolos')

class Arquivo(db.Model):
    __tablename__ = 'arquivo'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    filepath = db.Column(db.String(200), nullable=False)

    # Relacionamentos
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id', ondelete="CASCADE"), nullable=False)
    paciente = db.relationship('Paciente', back_populates='arquivos')


class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    __senha = db.Column(db.String(200), nullable=False)

    # Relacionamentos
    pacientes = db.relationship("Paciente", back_populates="usuario", cascade="all, delete-orphan")
    agendamentos = db.relationship("Agendamento", back_populates="usuario", cascade="all, delete-orphan")
    protocolos = db.relationship("Protocolo", back_populates="usuario", cascade="all, delete-orphan")

    @property
    def senha(self):
        return self.__senha

    @senha.setter
    def senha(self, senha):
        self.__senha = generate_password_hash(senha)
    
    def check_password(self, senha):
        return check_password_hash(self.senha, senha)


class Paciente(db.Model):
    __tablename__ = 'paciente'
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False) 
    cpf = db.Column(db.String(14), unique=True, nullable=False) 
    endereco = db.Column(db.String(200), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)

    data_de_cadastro = db.Column(db.Date, nullable=False)


    # Relacionamentos
    atendimentos = db.relationship("Atendimento", back_populates="paciente", cascade="all, delete-orphan")
    agendamentos = db.relationship("Agendamento", back_populates="paciente", cascade="all, delete-orphan")
    usuario = db.relationship("Usuario", back_populates="pacientes")
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete="CASCADE"), nullable=False)
    arquivos = db.relationship("Arquivo", back_populates="paciente", cascade="all, delete-orphan")

class Agendamento(db.Model):
    __tablename__ = 'agendamento'
    id = db.Column(db.Integer, primary_key=True)
    
    data = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    nome_procedimento = db.Column(db.String(100), nullable=False)

    # Relacionamentos
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id', ondelete="CASCADE"), nullable=False)
    paciente = db.relationship('Paciente', back_populates='agendamentos')

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete="CASCADE"), nullable=False)
    usuario = db.relationship('Usuario', back_populates='agendamentos')

class Atendimento(db.Model):
    __tablename__ = 'atendimento'
    id = db.Column(db.Integer, primary_key=True)

    data_procedimento = db.Column(db.Date, nullable=False)
    hora_procedimento = db.Column(db.Time, nullable=True)
    nome_procedimento = db.Column(db.String(100), nullable=False)

    historico_saude = db.Column(db.Text, nullable=True)

    preparo = db.Column(db.Text, nullable=True)
    evolucao = db.Column(db.Text, nullable=True)
    data_retorno = db.Column(db.Date, nullable=True)
    hora_retorno = db.Column(db.Time, nullable=True)
    observacoes_retorno = db.Column(db.Text, nullable=True)
    termo_filepath = db.Column(db.String(200), nullable=True)
    

    #Relacionamentos 
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id', ondelete="CASCADE"), nullable=False)
    paciente = db.relationship('Paciente', back_populates='atendimentos')

