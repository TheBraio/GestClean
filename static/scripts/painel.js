// // Simular dados do gráfico
// function initChart() {
//     const canvas = document.getElementById('consultasChart');
//     if (canvas) {
//         const ctx = canvas.getContext('2d');
        
//         // Desenhar um gráfico simples
//         ctx.fillStyle = '#667eea';
//         ctx.fillRect(50, 150, 40, 50);
//         ctx.fillRect(100, 120, 40, 80);
//         ctx.fillRect(150, 100, 40, 100);
//         ctx.fillRect(200, 80, 40, 120);
//         ctx.fillRect(250, 60, 40, 140);
//         ctx.fillRect(300, 40, 40, 160);
        
//         // Adicionar texto
//         ctx.fillStyle = '#64748b';
//         ctx.font = '12px Arial';
//         ctx.fillText('Jan', 50, 180);
//         ctx.fillText('Fev', 100, 180);
//         ctx.fillText('Mar', 150, 180);
//         ctx.fillText('Abr', 200, 180);
//         ctx.fillText('Mai', 250, 180);
//         ctx.fillText('Jun', 300, 180);
//     }
// }



document.addEventListener("DOMContentLoaded", () => {
    const btn_cadastrar_paciente = document.getElementById("novo_paciente")
    const btn_agendar_consulta = document.getElementById("agendar_consulta")
    const btn_protocolos = document.getElementById("protocolos")

    // Função para navegação
    function navigateTo(url) {
        window.location.href = url;
    }

    if (btn_cadastrar_paciente) {
        btn_cadastrar_paciente.addEventListener('click', () => {
            navigateTo('/paciente/cadastrar')
        })
    }

    if (btn_agendar_consulta) {
        btn_agendar_consulta.addEventListener('click', () => {
            navigateTo('/agenda')
        })
    }

    if (btn_protocolos) {
        btn_protocolos.addEventListener('click', () => {
            navigateTo('/protocolo/protocolos')
        })
    }

    // initChart();

})




// // Adicionar interatividade aos botões do gráfico
// document.querySelectorAll('.btn-small').forEach(btn => {
//     btn.addEventListener('click', function() {
//         // Remove active class from all buttons
//         document.querySelectorAll('.btn-small').forEach(b => b.classList.remove('active'));
//         // Add active class to clicked button
//         this.classList.add('active');
        
//         // Aqui você pode adicionar lógica para atualizar o gráfico
//         const period = this.getAttribute('data-period');
//         updateChart(period);
//     });
// });

// // Função para atualizar o gráfico (mock)
// function updateChart(period) {
//     console.log('Atualizando gráfico para período:', period);
//     // Aqui você pode integrar com uma biblioteca de gráficos como Chart.js
// }

