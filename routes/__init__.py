from .agenda import agenda_bp
from .atendimento import atendimento_bp
from .arquivo import arquivo_bp
from .gerais import gerais_bp
from .login import login_bp
from .paciente import paciente_bp
from .protocolo import protocolo_bp
from .configuracoes import configuracoes_bp

from .teste import teste_bp

blueprints = {
    'agenda': agenda_bp,
    'atendimento': atendimento_bp,
    'arquivo': arquivo_bp,
    '': gerais_bp,
    'login': login_bp,
    'paciente': paciente_bp,
    'protocolo': protocolo_bp,
    'configuracoes': configuracoes_bp,

    'teste': teste_bp,
}