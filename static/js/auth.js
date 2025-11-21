/**
 * Autenticação - Lógica de Login e Registro
 */

// Login Form
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(loginForm);
        const data = {
            nickname: formData.get('nickname'),
            password: formData.get('password')
        };
        
        try {
            const response = await fetch('/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Redireciona para home após login bem-sucedido
                window.location.href = '/';
            } else {
                // Mostra mensagem de erro
                showFlashMessage(result.message, 'error');
            }
        } catch (error) {
            console.error('Erro ao fazer login:', error);
            showFlashMessage('Erro ao fazer login. Tente novamente.', 'error');
        }
    });
}

// Register Form
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(registerForm);
        const password = formData.get('password');
        const confirmPassword = formData.get('confirm_password');
        
        // Validação no frontend
        if (password !== confirmPassword) {
            showFlashMessage('As senhas não coincidem!', 'error');
            return;
        }
        
        const data = {
            nickname: formData.get('nickname'),
            password: password,
            confirm_password: confirmPassword
        };
        
        try {
            const response = await fetch('/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Redireciona para home após registro bem-sucedido
                window.location.href = '/';
            } else {
                // Mostra mensagem de erro
                showFlashMessage(result.message, 'error');
            }
        } catch (error) {
            console.error('Erro ao registrar:', error);
            showFlashMessage('Erro ao criar conta. Tente novamente.', 'error');
        }
    });
}

/**
 * Mostra uma mensagem flash
 */
function showFlashMessage(message, type) {
    const flashContainer = document.querySelector('.flash-messages');
    if (!flashContainer) {
        // Cria container se não existir
        const form = document.querySelector('.auth-form');
        if (form) {
            const container = document.createElement('div');
            container.className = 'flash-messages';
            form.parentNode.insertBefore(container, form);
        }
    }
    
    const flashDiv = document.createElement('div');
    flashDiv.className = `flash-message flash-${type}`;
    flashDiv.textContent = message;
    
    const container = document.querySelector('.flash-messages');
    if (container) {
        container.innerHTML = '';
        container.appendChild(flashDiv);
    }
}

