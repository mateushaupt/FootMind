/**
 * FootMind - JavaScript Principal
 * Gerencia funcionalidades globais da aplicação
 */

// ============================================
// Inicialização
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Inicializa a aplicação
 */
function initializeApp() {
    setupNavigation();
    checkAuthenticationStatus();
    setupEventListeners();
}

// ============================================
// Navegação e Autenticação
// ============================================

/**
 * Configura os links de navegação
 */
function setupNavigation() {
    const historyLink = document.getElementById('history-link');
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');

    // Link de histórico (futuro)
    if (historyLink) {
        historyLink.addEventListener('click', function(e) {
            e.preventDefault();
            // TODO: Implementar rota de histórico quando autenticação estiver pronta
            console.log('Histórico - Em desenvolvimento');
            // window.location.href = '/history';
        });
    }

    // Link de logout
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            e.preventDefault();
            handleLogout();
        });
    }
}

/**
 * Verifica o status de autenticação do usuário
 */
async function checkAuthenticationStatus() {
    try {
        const response = await fetch('/auth/check-auth');
        const data = await response.json();
        
        const userMenu = document.getElementById('user-menu');
        const navMenu = document.getElementById('nav-menu');
        const userName = document.getElementById('user-name');
        
        if (data.authenticated && data.user) {
            // Usuário logado
            if (userMenu) {
                userMenu.style.display = 'flex';
            }
            if (navMenu) {
                // Esconde links de login/registro
                const loginLink = document.getElementById('login-link');
                const registerLink = document.getElementById('register-link');
                if (loginLink) loginLink.style.display = 'none';
                if (registerLink) registerLink.style.display = 'none';
            }
            if (userName) {
                userName.textContent = data.user.nickname;
            }
        } else {
            // Usuário não logado
            if (userMenu) {
                userMenu.style.display = 'none';
            }
            if (navMenu) {
                // Mostra links de login/registro
                const loginLink = document.getElementById('login-link');
                const registerLink = document.getElementById('register-link');
                if (loginLink) loginLink.style.display = 'inline-block';
                if (registerLink) registerLink.style.display = 'inline-block';
            }
        }
    } catch (error) {
        console.error('Erro ao verificar autenticação:', error);
        // Em caso de erro, assume que não está logado
        const userMenu = document.getElementById('user-menu');
        if (userMenu) userMenu.style.display = 'none';
    }
    
    // Configura o dropdown do usuário
    setupUserDropdown();
}

/**
 * Configura o dropdown do menu do usuário
 */
function setupUserDropdown() {
    const userNameBtn = document.getElementById('user-name-btn');
    const dropdownMenu = document.getElementById('user-dropdown-menu');
    
    if (!userNameBtn || !dropdownMenu) return;
    
    // Toggle dropdown ao clicar no nome do usuário
    userNameBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        dropdownMenu.classList.toggle('show');
        userNameBtn.classList.toggle('active');
    });
    
    // Fecha dropdown ao clicar fora
    document.addEventListener('click', (e) => {
        if (!userNameBtn.contains(e.target) && !dropdownMenu.contains(e.target)) {
            dropdownMenu.classList.remove('show');
            userNameBtn.classList.remove('active');
        }
    });
    
    // Fecha dropdown ao clicar em um item
    const dropdownItems = dropdownMenu.querySelectorAll('.dropdown-item');
    dropdownItems.forEach(item => {
        item.addEventListener('click', () => {
            dropdownMenu.classList.remove('show');
            userNameBtn.classList.remove('active');
        });
    });
}

/**
 * Configura event listeners globais
 */
function setupEventListeners() {
    // Adicionar event listeners globais aqui conforme necessário
}

// ============================================
// Funções de Autenticação (Futuro)
// ============================================

/**
 * Mostra modal de login
 * TODO: Implementar quando autenticação estiver pronta
 */
function showLoginModal() {
    // Implementação futura
    console.log('Mostrar modal de login');
}

/**
 * Processa logout do usuário
 */
async function handleLogout() {
    try {
        const response = await fetch('/auth/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Recarrega a página para atualizar o estado
            window.location.href = '/';
        } else {
            console.error('Erro ao fazer logout:', data.message);
        }
    } catch (error) {
        console.error('Erro ao fazer logout:', error);
        // Mesmo com erro, tenta recarregar a página
        window.location.href = '/';
    }
}

// ============================================
// Funções de Histórico (Futuro)
// ============================================

/**
 * Carrega histórico de jogos do usuário
 * TODO: Implementar quando histórico estiver pronto
 */
function loadUserHistory() {
    // Implementação futura
    console.log('Carregar histórico do usuário');
    // Fazer requisição AJAX para /api/history
    // Renderizar histórico
}

// ============================================
// Utilitários
// ============================================

/**
 * Faz requisição AJAX genérica
 * @param {string} url - URL da requisição
 * @param {string} method - Método HTTP (GET, POST, etc.)
 * @param {Object} data - Dados a serem enviados
 * @returns {Promise} Promise com a resposta
 */
function makeRequest(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
    };

    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }

    return fetch(url, options)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .catch(error => {
            console.error('Erro na requisição:', error);
            throw error;
        });
}

/**
 * Exibe mensagem de notificação
 * TODO: Implementar sistema de notificações mais robusto
 */
function showNotification(message, type = 'info') {
    // Implementação futura de sistema de notificações
    console.log(`[${type.toUpperCase()}] ${message}`);
    // Pode usar uma biblioteca de notificações ou criar um componente próprio
}

