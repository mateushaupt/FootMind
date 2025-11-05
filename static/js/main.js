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

    // Link de login (futuro)
    if (loginLink) {
        loginLink.addEventListener('click', function(e) {
            e.preventDefault();
            // TODO: Implementar modal/login quando autenticação estiver pronta
            console.log('Login - Em desenvolvimento');
            // showLoginModal();
        });
    }

    // Link de logout (futuro)
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            e.preventDefault();
            // TODO: Implementar logout quando autenticação estiver pronta
            console.log('Logout - Em desenvolvimento');
            // handleLogout();
        });
    }
}

/**
 * Verifica o status de autenticação do usuário
 * TODO: Implementar quando autenticação estiver pronta
 */
function checkAuthenticationStatus() {
    // Por enquanto, sempre mostra como não logado
    const isLoggedIn = false; // TODO: Verificar session/cookie
    
    const userMenu = document.getElementById('user-menu');
    const loginLink = document.getElementById('login-link');
    
    if (isLoggedIn) {
        if (userMenu) userMenu.style.display = 'flex';
        if (loginLink) loginLink.style.display = 'none';
    } else {
        if (userMenu) userMenu.style.display = 'none';
        if (loginLink) loginLink.style.display = 'inline-block';
    }
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
 * TODO: Implementar quando autenticação estiver pronta
 */
function handleLogout() {
    // Implementação futura
    console.log('Processar logout');
    // Fazer requisição para /logout
    // Limpar session/cookies
    // Recarregar página
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

