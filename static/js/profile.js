/**
 * Perfil - Lógica de Atualização de Dados
 */

// Update Nickname Form
const updateNicknameForm = document.getElementById('updateNicknameForm');
if (updateNicknameForm) {
    updateNicknameForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(updateNicknameForm);
        const data = {
            nickname: formData.get('nickname')
        };
        
        try {
            const response = await fetch('/auth/update-nickname', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Atualiza o nickname exibido
                const currentNicknameEl = document.getElementById('current-nickname');
                if (currentNicknameEl) {
                    currentNicknameEl.textContent = result.user.nickname;
                }
                
                // Atualiza o nickname no header
                const userNameEl = document.getElementById('user-name');
                if (userNameEl) {
                    userNameEl.textContent = result.user.nickname;
                }
                
                showFlashMessage(result.message, 'success');
            } else {
                showFlashMessage(result.message, 'error');
            }
        } catch (error) {
            console.error('Erro ao atualizar nickname:', error);
            showFlashMessage('Erro ao atualizar nickname. Tente novamente.', 'error');
        }
    });
}

// Update Password Form
const updatePasswordForm = document.getElementById('updatePasswordForm');
if (updatePasswordForm) {
    updatePasswordForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(updatePasswordForm);
        const password = formData.get('new_password');
        const confirmPassword = formData.get('confirm_password');
        
        // Validação no frontend
        if (password !== confirmPassword) {
            showFlashMessage('As senhas não coincidem!', 'error');
            return;
        }
        
        const data = {
            current_password: formData.get('current_password'),
            new_password: password,
            confirm_password: confirmPassword
        };
        
        try {
            const response = await fetch('/auth/update-password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Limpa o formulário
                updatePasswordForm.reset();
                showFlashMessage(result.message, 'success');
            } else {
                showFlashMessage(result.message, 'error');
            }
        } catch (error) {
            console.error('Erro ao atualizar senha:', error);
            showFlashMessage('Erro ao atualizar senha. Tente novamente.', 'error');
        }
    });
}

/**
 * Mostra uma mensagem flash
 */
function showFlashMessage(message, type) {
    let flashContainer = document.querySelector('.flash-messages');
    if (!flashContainer) {
        // Cria container se não existir
        const profileHeader = document.querySelector('.profile-header');
        if (profileHeader) {
            flashContainer = document.createElement('div');
            flashContainer.className = 'flash-messages';
            profileHeader.parentNode.insertBefore(flashContainer, profileHeader.nextSibling);
        }
    }
    
    if (flashContainer) {
        const flashDiv = document.createElement('div');
        flashDiv.className = `flash-message flash-${type}`;
        flashDiv.textContent = message;
        
        flashContainer.innerHTML = '';
        flashContainer.appendChild(flashDiv);
        
        // Remove a mensagem após 5 segundos
        setTimeout(() => {
            flashDiv.remove();
        }, 5000);
    }
}

