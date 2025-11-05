/**
 * Football Bingo - Lógica do Jogo
 * Gerencia toda a funcionalidade do jogo Football Bingo
 */

// Variáveis globais do jogo
let categories = [];
let currentPlayer = null;
let wildcardUsed = false;
let gameOver = false;
let skipNext = false;

/**
 * Inicializa o jogo com as categorias do servidor
 * @param {Array} cats - Categorias do bingo card
 * @param {number} totalPlayers - Total de jogadores disponíveis
 */
function initializeGameBingo(cats, totalPlayers) {
    categories = cats;
    createBingoGrid();
    loadNextPlayer();
    updateStatusMessage('Selecione uma categoria para o jogador atual!', 'info');
}

/**
 * Cria o grid de bingo 4x4
 */
function createBingoGrid() {
    const grid = document.getElementById('bingoGrid');
    if (!grid) return;
    
    grid.innerHTML = '';
    
    categories.forEach((category, index) => {
        const cell = document.createElement('div');
        cell.className = 'bingo-cell';
        cell.id = `bingo-cell-${index}`;
        cell.dataset.categoryId = index;
        
        if (category.matched) {
            cell.classList.add('matched');
        }
        
        cell.innerHTML = `
            <div class="category-name">${escapeHtml(category.display)}</div>
            <div class="category-type">${getCategoryTypeLabel(category.type)}</div>
            ${category.matched && category.player_id ? `<div class="category-player">✓</div>` : ''}
        `;
        
        cell.addEventListener('click', () => selectCategory(index));
        
        grid.appendChild(cell);
    });
}

/**
 * Retorna o label do tipo de categoria
 */
function getCategoryTypeLabel(type) {
    const labels = {
        'team': 'Time',
        'country': 'País',
        'trophy': 'Troféu',
        'league': 'Liga',
        'manager': 'Técnico',
        'position': 'Posição',
        'teammate': 'Jogou com'
    };
    return labels[type] || type;
}

/**
 * Carrega o próximo jogador
 */
function loadNextPlayer() {
    if (gameOver) return;
    
    fetch('/game-bingo/get-player', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            updateStatusMessage(data.error, 'error');
            return;
        }
        
        if (data.game_over) {
            endGame(false, data.message || 'Todos os jogadores foram utilizados!');
            return;
        }
        
        currentPlayer = data.player;
        updatePlayerDisplay();
        updateStatusMessage('Selecione uma categoria para ' + currentPlayer.name, 'info');
        
        // Remove estado de skip se necessário
        skipNext = false;
    })
    .catch(error => {
        console.error('Erro ao carregar jogador:', error);
        updateStatusMessage('Erro ao carregar jogador. Tente novamente.', 'error');
    });
}

/**
 * Atualiza a exibição do jogador atual
 */
function updatePlayerDisplay() {
    const playerName = document.getElementById('playerName');
    const playerInfo = document.getElementById('playerInfo');
    
    if (!playerName || !currentPlayer) return;
    
    playerName.textContent = currentPlayer.name;
    
    let info = [];
    if (currentPlayer.position) {
        info.push(`Posição: ${currentPlayer.position}`);
    }
    
    playerInfo.textContent = info.join(' • ') || 'Carregando informações...';
}

/**
 * Seleciona uma categoria
 */
function selectCategory(categoryId) {
    if (!currentPlayer || gameOver || skipNext) {
        return;
    }
    
    const category = categories[categoryId];
    if (!category) return;
    
    if (category.matched) {
        updateStatusMessage('Esta categoria já foi preenchida!', 'error');
        return;
    }
    
    // Marca visualmente como selecionada
    const cell = document.getElementById(`bingo-cell-${categoryId}`);
    if (cell) {
        cell.classList.add('selected');
    }
    
    // Desabilita todas as células temporariamente
    disableAllCells();
    
    // Verifica a correspondência
    checkMatch(categoryId, false);
}

/**
 * Verifica se o jogador corresponde à categoria
 */
function checkMatch(categoryId, isWildcard) {
    fetch('/game-bingo/check-match', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            player_id: currentPlayer.id,
            category_id: categoryId,
            is_wildcard: isWildcard
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            updateStatusMessage(data.error, 'error');
            enableAllCells();
            removeSelection();
            return;
        }
        
        if (data.success) {
            // Sucesso!
            categories[categoryId].matched = true;
            categories[categoryId].player_id = currentPlayer.id;
            
            updateBingoCell(categoryId, true);
            updateStatusMessage(data.message, 'success');
            
            if (isWildcard) {
                wildcardUsed = true;
                updateWildcardButton();
            }
            
            // Verifica se o bingo foi completado
            if (data.bingo_complete) {
                setTimeout(() => {
                    endGame(true, 'Parabéns! Você completou o Bingo!');
                }, 1000);
            } else {
                // Carrega próximo jogador
                setTimeout(() => {
                    loadNextPlayer();
                    enableAllCells();
                }, 1500);
            }
        } else {
            // Erro - perde a vez
            updateStatusMessage(data.message, 'error');
            skipNext = true;
            
            setTimeout(() => {
                loadNextPlayer();
                enableAllCells();
                removeSelection();
            }, 2000);
        }
    })
    .catch(error => {
        console.error('Erro ao verificar correspondência:', error);
        updateStatusMessage('Erro ao verificar correspondência. Tente novamente.', 'error');
        enableAllCells();
        removeSelection();
    });
}

/**
 * Atualiza uma célula do bingo
 */
function updateBingoCell(categoryId, matched) {
    const cell = document.getElementById(`bingo-cell-${categoryId}`);
    if (!cell) return;
    
    const category = categories[categoryId];
    
    if (matched) {
        cell.classList.add('matched');
        cell.classList.remove('selected', 'disabled');
        cell.innerHTML = `
            <div class="category-name">${escapeHtml(category.display)}</div>
            <div class="category-type">${getCategoryTypeLabel(category.type)}</div>
            <div class="category-player">✓</div>
        `;
    }
}

/**
 * Pula o jogador atual
 */
function skipPlayer() {
    if (!currentPlayer || gameOver) return;
    
    fetch('/game-bingo/skip', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateStatusMessage('Jogador pulado!', 'info');
            loadNextPlayer();
        }
    })
    .catch(error => {
        console.error('Erro ao pular jogador:', error);
    });
}

/**
 * Usa o wildcard
 */
function useWildcard() {
    if (wildcardUsed || !currentPlayer || gameOver) {
        return;
    }
    
    if (!confirm('Deseja usar o wildcard? Você só pode usar uma vez!')) {
        return;
    }
    
    // Pergunta qual categoria usar
    const availableCategories = categories
        .map((cat, idx) => ({ ...cat, index: idx }))
        .filter(cat => !cat.matched);
    
    if (availableCategories.length === 0) {
        updateStatusMessage('Não há categorias disponíveis!', 'error');
        return;
    }
    
    // Por enquanto, usa a primeira categoria disponível
    // TODO: Permitir que o usuário escolha
    const categoryId = availableCategories[0].index;
    
    disableAllCells();
    checkMatch(categoryId, true);
}

/**
 * Atualiza o botão de wildcard
 */
function updateWildcardButton() {
    const wildcardBtn = document.getElementById('wildcardButton');
    if (wildcardBtn) {
        wildcardBtn.disabled = wildcardUsed;
        if (wildcardUsed) {
            wildcardBtn.textContent = '🎴 Wildcard (Usado)';
        }
    }
}

/**
 * Desabilita todas as células
 */
function disableAllCells() {
    categories.forEach((_, index) => {
        const cell = document.getElementById(`bingo-cell-${index}`);
        if (cell && !cell.classList.contains('matched')) {
            cell.classList.add('disabled');
        }
    });
}

/**
 * Habilita todas as células
 */
function enableAllCells() {
    categories.forEach((_, index) => {
        const cell = document.getElementById(`bingo-cell-${index}`);
        if (cell && !cell.classList.contains('matched')) {
            cell.classList.remove('disabled', 'selected');
        }
    });
}

/**
 * Remove seleção visual
 */
function removeSelection() {
    categories.forEach((_, index) => {
        const cell = document.getElementById(`bingo-cell-${index}`);
        if (cell) {
            cell.classList.remove('selected');
        }
    });
}

/**
 * Atualiza a mensagem de status
 */
function updateStatusMessage(message, type) {
    const statusMsg = document.getElementById('statusMessage');
    if (!statusMsg) return;
    
    statusMsg.textContent = message;
    statusMsg.className = `status-message ${type}`;
    
    if (message === '') {
        statusMsg.classList.add('hidden');
    } else {
        statusMsg.classList.remove('hidden');
    }
}

/**
 * Finaliza o jogo
 */
function endGame(won, message) {
    gameOver = true;
    const modal = document.getElementById('gameOverModal');
    const title = document.getElementById('gameOverTitle');
    const msg = document.getElementById('gameOverMessage');
    
    if (modal && title && msg) {
        title.textContent = won ? '🎉 Bingo Completo!' : '⏰ Fim de Jogo';
        msg.textContent = message;
        modal.classList.add('show');
    }
    
    disableAllCells();
}

/**
 * Escapa HTML para prevenir XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Expor funções globalmente
window.skipPlayer = skipPlayer;
window.useWildcard = useWildcard;

