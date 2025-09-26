document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('modal-pop');
    const btnAdicionarProtocolo = document.getElementById('adicionar-arquivo');
    const closeModalButton = document.querySelector('.modal .close');
    const cancelarButton = document.querySelector('.btn-cancelar');
    const formProtocolo = document.getElementById('form-protocolo');
    const modalTitle = document.getElementById('modal-title');
    const inputNome = document.getElementById('nome');
    const inputDescricao = document.getElementById('descricao');
    const labelArquivo = document.getElementById('label-arquivo');
    const inputArquivo = document.getElementById('input-arquivo');

    function abrirModal() {
        modal.style.display = 'block';
    }

    function fecharModal() {
        modal.style.display = 'none';
        resetForm();
    }

    function resetForm() {
        formProtocolo.action = '/protocolo/adicionar';
        modalTitle.innerHTML = 'Novo Protocolo';
        inputNome.value = '';
        inputDescricao.value = '';
        labelArquivo.innerHTML = 'Arquivo:';
        inputArquivo.setAttribute('required', '');
        formProtocolo.onsubmit = null;
    }

    if (btnAdicionarProtocolo) {
        btnAdicionarProtocolo.addEventListener('click', abrirModal);
    }

    if (closeModalButton) {
        closeModalButton.addEventListener('click', fecharModal);
    }

    if (cancelarButton) {
        cancelarButton.addEventListener('click', fecharModal);
    }

    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            fecharModal();
        }
    });

    const btnsEditar = document.querySelectorAll('.btn-editar-protocolo');
    btnsEditar.forEach(btn => {
        btn.addEventListener('click', function (event) {
            event.preventDefault();
            const id = this.dataset.protocoloId;
            const nome = this.dataset.protocoloNome;
            const descricao = this.dataset.protocoloDescricao;

            inputNome.value = nome;
            inputDescricao.value = descricao;
            modalTitle.innerHTML = `Editar Protocolo ${id}`;
            labelArquivo.innerHTML = "Novo arquivo (opcional):";
            inputArquivo.removeAttribute('required');
            
            formProtocolo.action = `/protocolo/editar/${id}`;
            formProtocolo.onsubmit = function () {
                return confirm("Tem certeza que deseja salvar este protocolo? Ao adicionar outro arquivo o anterior será substituído.");
            }
            
            abrirModal();
        });
    });

    const formsExcluir = document.querySelectorAll('.form-excluir-protocolo');
    formsExcluir.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!confirm('Tem certeza que deseja excluir este protocolo?')) {
                event.preventDefault();
            }
        });
    });
});