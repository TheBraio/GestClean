function abrirModalAgendamento() {
    document.getElementById('modal-agendamento').style.display = 'block';
}

function fecharModalAgendamento() {
    document.getElementById('modal-agendamento').style.display = 'none';
}

function abrirModalEditarAgendamento(id, data, horario, pacienteId, procedimento) {
    // Preencher o formulário com os dados atuais
    document.getElementById('editar-agendamento-id').value = id;
    document.getElementById('editar-data').value = data;
    document.getElementById('editar-horario').value = horario;
    document.getElementById('editar-paciente').value = pacienteId;
    document.getElementById('editar-procedimento').value = procedimento;
    
    // Configurar a action do formulário
    document.getElementById('form-editar-agendamento').action = `/agenda/editar/${id}`;
    
    // Mostrar o modal
    document.getElementById('modal-editar-agendamento').style.display = 'block';
}

function fecharModalEditarAgendamento() {
    document.getElementById('modal-editar-agendamento').style.display = 'none';
}

// Fechar modal quando clicar fora dele
window.onclick = function(event) {
    const modal = document.getElementById('modal-agendamento');
    const modalEditar = document.getElementById('modal-editar-agendamento');
    if (event.target === modal) {
        fecharModalAgendamento();
    }
    if (event.target === modalEditar) {
        fecharModalEditarAgendamento();
    }
}

// Função para verificar agendamentos que passaram em tempo real
function verificarAgendamentosPassados() {
    const agora = new Date();
    const agendamentos = document.querySelectorAll('.agendamento-item');
    
    agendamentos.forEach(function(agendamento) {
        const dataElement = agendamento.querySelector('.data');
        const horaElement = agendamento.querySelector('.horario');
        
        if (dataElement && horaElement) {
            const dataTexto = dataElement.textContent;
            const horaTexto = horaElement.textContent;
            
            // Converter para objeto Date
            const [dia, mes, ano] = dataTexto.split('/');
            const [hora, minuto] = horaTexto.split(':');
            const dataAgendamento = new Date(ano, mes - 1, dia, hora, minuto);
            
            // Se já passou e não tem a classe, adicionar
            if (dataAgendamento < agora && !agendamento.classList.contains('agendamento-passado')) {
                agendamento.classList.add('agendamento-passado');
            }
        }
    });
}

// Verificar a cada minuto
setInterval(verificarAgendamentosPassados, 60000);

// Verificar na primeira carga da página
document.addEventListener('DOMContentLoaded', () => {
    verificarAgendamentosPassados();

    // Botão Adicionar Agendamento
    const btnAdicionar = document.querySelector('.adicionar-agendamento');
    if (btnAdicionar) {
        btnAdicionar.addEventListener('click', abrirModalAgendamento);
    }

    // Botões fechar modal de adicionar agendamento
    const btnFecharAdicionar = document.querySelectorAll('#modal-agendamento .close, #modal-agendamento .btn-cancelar');
    btnFecharAdicionar.forEach(btn => {
        btn.addEventListener('click', fecharModalAgendamento);
    });

    // Botões Editar Agendamento
    const btnsEditar = document.querySelectorAll('.editar-agendamento');
    btnsEditar.forEach(btn => {
        btn.addEventListener('click', (event) => {
            const button = event.currentTarget;
            const id = button.dataset.id;
            const data = button.dataset.data;
            const horario = button.dataset.horario;
            const pacienteId = button.dataset.pacienteId;
            const procedimento = button.dataset.procedimento;
            abrirModalEditarAgendamento(id, data, horario, pacienteId, procedimento);
        });
    });

    // Botões fechar modal de editar agendamento
    const btnFecharEditar = document.querySelectorAll('#modal-editar-agendamento .close, #modal-editar-agendamento .btn-cancelar');
    btnFecharEditar.forEach(btn => {
        btn.addEventListener('click', fecharModalEditarAgendamento);
    });

    // Formulários de cancelamento
    const formsCancelar = document.querySelectorAll('form.cancelar-agendamento');
    formsCancelar.forEach(form => {
        form.addEventListener('submit', (event) => {
            if (!confirm('Tem certeza que deseja cancelar este agendamento?')) {
                event.preventDefault();
            }
        });
    });
});
