/**
 * Script para gerenciar o estado ativo do menu
 */

function highlightActiveMenuItem() {
    const currentPath = window.location.pathname;
    const menuItems = document.querySelectorAll('.sidebar-menu a');
    
    // Remove todas as classes active
    menuItems.forEach(item => {
        item.classList.remove('active');
    });
    
    // Encontra e ativa o item correto
    menuItems.forEach(item => {
        const href = item.getAttribute('href');
        
        // Casos especiais para diferentes rotas
        if (currentPath === '/' && href === '/') {
            item.classList.add('active');
        } else if (currentPath === '/painel' && (href === '/' || href === '/painel')) {
            item.classList.add('active');
        } else if ( ( currentPath.startsWith('/paciente') || currentPath.startsWith('/atendimento') ) && href.startsWith('/paciente') ) {
            item.classList.add('active');
        } else if (currentPath.startsWith('/agenda') && href.startsWith('/agenda')) {
            item.classList.add('active');
        } else if (currentPath.startsWith('/protocolo') && href.startsWith('/protocolo')) {
            item.classList.add('active');
        } else if (currentPath.startsWith('/configuracoes') && href.startsWith('/configuracoes')) {
            item.classList.add('active');
        } else if (href !== '#' && currentPath === href) {
            item.classList.add('active');
        }
    });
}

// Executa quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    highlightActiveMenuItem();
    
    // Adiciona listeners para mudanças de URL (se necessário)
    window.addEventListener('popstate', highlightActiveMenuItem);
});

// Função para navegar e atualizar o menu
function navigateTo(url) {
    window.location.href = url;
    // O menu será atualizado automaticamente quando a página carregar
} 