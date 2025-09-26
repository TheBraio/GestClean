document.addEventListener("DOMContentLoaded", function() {
    const botao_excluir = document.querySelectorAll(".form-excluir");


    botao_excluir.forEach(form => {
        form.addEventListener("submit", function(event) {
            const confirmar = confirm("Tem certeza que deseja excluir este paciente?");
            if (!confirmar) {
                event.preventDefault();
            }
        }) 
    })
})
