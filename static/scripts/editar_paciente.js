function excluirArquivo(id_do_arquivo, container) {
    if (confirm("Tem certeza que deseja excluir este arquivo?")) {
        fetch("/arquivo/excluir", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id: id_do_arquivo
            })
        })
        .then(res => res.text())
        .then(status => {
            if (status === "OK") {
                container.remove();
            } else {
                console.log(status)
                alert("Ocorreu um erro ao excluir o arquivo.");
            }
        });
    }
}

function adicionarArquivo(formData) {

}

document.addEventListener('DOMContentLoaded', function() { 
    const form = document.querySelector(".form-pop");
    const lista_de_containers_de_arquivos = document.getElementById("filesList");
    const template_arquivos = document.getElementById("fileContainerTemplate"); 

    form.addEventListener("submit", function(event) {
        event.preventDefault();
        const formData = new FormData(form);
        id_do_paciente = this.dataset.id
        formData.append("id_do_paciente", id_do_paciente);
        fetch("/arquivo/adicionar", {
            method: "POST",
            body: formData
        })
        .then(res => res.json())
        .then(response => {
            if (response.status === "OK") {
                const novo_container_de_arquivo = template_arquivos.content.cloneNode(true).children[0];

                const titulo_do_arquivo = novo_container_de_arquivo.querySelector(".file-title");
                const nome_do_arquivo = novo_container_de_arquivo.querySelector(".file-name");

                const titulo = formData.get("titulo");

                titulo_do_arquivo.textContent =  titulo;
                nome_do_arquivo.textContent = response.nome_do_arquivo;
                lista_de_containers_de_arquivos.appendChild(novo_container_de_arquivo);
                let link = novo_container_de_arquivo.querySelector("#link-baixar-arquivo");
                let id_do_arquivo = response.id_do_arquivo;
                
                link.href = `/arquivo/download/${id_do_arquivo}`;
                form.reset()

                console.log(id_do_arquivo)
                const botao_de_remover = novo_container_de_arquivo.querySelector(".remove-file-button");
                botao_de_remover.addEventListener("click", function() {
                    if (id_do_arquivo) {
                        excluirArquivo(id_do_arquivo, this.closest('.file-item'));
                    }
                });
            } else if (response.status === "ERROR") {
                alert(response.message);
            } else {
                console.log(response.status)
                alert("Ocorreu um erro ao adicionar o arquivo.");
            }
        });
   
        

        fecharModalPop();
    });

    document.querySelectorAll('.remove-file-button').forEach(botao => {
        botao.addEventListener("click", function() {
            excluirArquivo(this.dataset.id, this.closest('.file-item'));
        })
    });    
})



function abrirModalPop() {
    document.getElementById('modal-pop').style.display = 'block';
}
function fecharModalPop() {
    document.getElementById('modal-pop').style.display = 'none';
}
window.onclick = function(event) {
    const modal = document.getElementById('modal-pop');
    if (event.target === modal) {
        fecharModalPop();
    }
}