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
let totalPlayers = 0;
let usedPlayers = 0;
let remainingPlayers = 0;

/**
 * Inicializa o jogo com as categorias do servidor
 * @param {Array} cats - Categorias do bingo card
 * @param {number} totalPlayersCount - Total de jogadores disponíveis
 */
function initializeGameBingo(cats, totalPlayersCount) {
    categories = cats;
    totalPlayers = totalPlayersCount;
    usedPlayers = 0;
    remainingPlayers = totalPlayers;
    updatePlayersInfo();
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
    .then(response => {
        // Se a resposta for 403 (Forbidden), significa que já jogou
        if (response.status === 403) {
            window.location.href = '/game-bingo/';
            return null;
        }
        return response.json();
    })
    .then(data => {
        if (!data) return; // Já redirecionou
        
        if (data.error) {
            // Se o erro for sobre já ter jogado, redireciona
            if (data.error.includes('já jogou') || data.already_played) {
                window.location.href = '/game-bingo/';
                return;
            }
            updateStatusMessage(data.error, 'error');
            return;
        }
        
        if (data.already_played) {
            // Usuário já jogou - redireciona para tela de resultado
            window.location.href = '/game-bingo/';
            return;
        }
        
        if (data.game_over) {
            // Atualiza informações dos jogadores antes de terminar o jogo
            if (data.total_players !== undefined) {
                totalPlayers = data.total_players;
                usedPlayers = data.used_players || 0;
                remainingPlayers = data.remaining_players || 0;
                updatePlayersInfo();
            }
            endGame(false, data.message || 'Todos os jogadores foram utilizados!');
            // Após um delay, redireciona para verificar se já jogou
            setTimeout(() => {
                window.location.href = '/game-bingo/';
            }, 3000);
            return;
        }
        
        currentPlayer = data.player;
        
        // Atualiza informações dos jogadores se disponíveis
        if (data.total_players !== undefined) {
            totalPlayers = data.total_players;
            usedPlayers = data.used_players || 0;
            remainingPlayers = data.remaining_players || 0;
            updatePlayersInfo();
        }
        
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
        if (data.already_played) {
            // Usuário já jogou - redireciona para tela de resultado
            window.location.href = '/game-bingo/';
            return;
        }
        
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
            // Erro - perde a vez (penalidade por escolha errada)
            updateStatusMessage(data.message + ' Você perdeu uma oportunidade!', 'error');
            skipNext = true;
            
            // Pula o próximo jogador como penalidade
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
 * Usa o wildcard para completar todas as categorias que o jogador atual cobre
 */
function useWildcard() {
    if (wildcardUsed || !currentPlayer || gameOver) {
        return;
    }
    
    if (!confirm('Deseja usar o wildcard? Ele completará todas as categorias que o jogador atual cobre. Você só pode usar uma vez!')) {
        return;
    }
    
    disableAllCells();
    
    fetch('/game-bingo/use-wildcard', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            player_id: currentPlayer.id
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.already_played) {
            // Usuário já jogou - redireciona para tela de resultado
            window.location.href = '/game-bingo/';
            return;
        }
        
        if (data.error) {
            updateStatusMessage(data.error, 'error');
            enableAllCells();
            return;
        }
        
        if (data.success) {
            // Atualiza todas as categorias que foram completadas
            data.matched_categories.forEach(matchedCat => {
                categories[matchedCat.id].matched = true;
                categories[matchedCat.id].player_id = currentPlayer.id;
                updateBingoCell(matchedCat.id, true);
            });
            
            wildcardUsed = true;
            updateWildcardButton();
            updateStatusMessage(data.message, 'success');
            
            // Verifica se o bingo foi completado
            if (data.bingo_complete) {
                setTimeout(() => {
                    endGame(true, 'Parabéns! Você completou o Bingo!');
                    // Após um delay, redireciona para verificar se já jogou
                    setTimeout(() => {
                        window.location.href = '/game-bingo/';
                    }, 3000);
                }, 1000);
            } else {
                // Carrega próximo jogador
                setTimeout(() => {
                    loadNextPlayer();
                    enableAllCells();
                }, 1500);
            }
        }
    })
    .catch(error => {
        console.error('Erro ao usar wildcard:', error);
        updateStatusMessage('Erro ao usar wildcard. Tente novamente.', 'error');
        enableAllCells();
    });
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
 * Atualiza as informações sobre os jogadores
 */
function updatePlayersInfo() {
    const playersRemainingEl = document.getElementById('playersRemaining');
    const playerNumberEl = document.getElementById('playerNumber');
    
    if (playersRemainingEl) {
        playersRemainingEl.textContent = remainingPlayers;
    }
    if (playerNumberEl) {
        // Mostra o número do jogador atual (usedPlayers + 1, ou usado se já foi usado)
        playerNumberEl.textContent = usedPlayers > 0 ? usedPlayers : 1;
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

