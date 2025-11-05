/**
 * FootWordle - Lógica do Jogo
 * Gerencia toda a funcionalidade do jogo FootWordle
 */

// Variáveis globais do jogo
let currentAttempt = 0;
const maxAttempts = 5;
let wordLength;
let guessUrl;

/**
 * Inicializa o jogo com os parâmetros do servidor
 * @param {number} length - Tamanho da palavra/jogador
 * @param {string} url - URL do endpoint de palpite
 */
function initializeGameWordle(length, url) {
    wordLength = length;
    guessUrl = url;
    createBoard();
    setupEventListeners();
}

/**
 * Cria o tabuleiro do jogo
 */
function createBoard() {
    const gameBoard = document.getElementById('gameBoard');
    if (!gameBoard) return;
    
    gameBoard.innerHTML = ''; // Limpa o tabuleiro se já existir
    
    for (let i = 0; i < maxAttempts; i++) {
        const row = document.createElement('div');
        row.className = 'guess-row';
        for (let j = 0; j < wordLength; j++) {
            const box = document.createElement('div');
            box.className = 'letter-box';
            row.appendChild(box);
        }
        gameBoard.appendChild(row);
    }
}

/**
 * Configura os event listeners do jogo
 */
function setupEventListeners() {
    const guessInput = document.getElementById('guessInput');
    if (!guessInput) return;
    
    // Enter para enviar
    guessInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !guessInput.disabled) {
            makeGuess();
        }
    });

    // Focar no input quando a página carregar
    guessInput.focus();

    // Limitar entrada ao tamanho da palavra
    guessInput.addEventListener('input', function(e) {
        this.value = this.value.toUpperCase().slice(0, wordLength);
    });
}

/**
 * Processa o palpite do usuário
 */
function makeGuess() {
    const guessInput = document.getElementById('guessInput');
    const guessButton = document.getElementById('guessButton');
    
    if (!guessInput || !guessButton) return;
    
    const guess = guessInput.value.toUpperCase().trim();
    
    if (guess.length !== wordLength) {
        alert(`O nome deve ter exatamente ${wordLength} letras!`);
        return;
    }

    // Desabilita input e botão durante a requisição
    guessInput.disabled = true;
    guessButton.disabled = true;

    fetch(guessUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            guess: guess,
            attempt: currentAttempt
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            guessInput.disabled = false;
            guessButton.disabled = false;
            return;
        }

        const row = document.getElementsByClassName('guess-row')[currentAttempt];
        if (!row) return;
        
        const boxes = row.children;

        // Anima a revelação das letras
        data.result.forEach((result, index) => {
            setTimeout(() => {
                boxes[index].textContent = result.letter;
                boxes[index].classList.add(result.color);
            }, index * 100);
        });

        const message = document.getElementById('message');

        if (data.won) {
            setTimeout(() => {
                if (message) {
                    message.textContent = '🎉 Parabéns! Você acertou!';
                    message.style.background = 'var(--success-color)';
                    message.style.color = 'white';
                }
                guessInput.disabled = true;
                guessButton.disabled = true;
            }, wordLength * 100);
        } else if (data.gameOver) {
            setTimeout(() => {
                if (message) {
                    message.textContent = `Game Over! O jogador era ${data.answer}`;
                    message.style.background = 'var(--danger-color)';
                    message.style.color = 'white';
                }
                guessInput.disabled = true;
                guessButton.disabled = true;
            }, wordLength * 100);
        } else {
            // Continua o jogo
            currentAttempt++;
            guessInput.value = '';
            guessInput.disabled = false;
            guessButton.disabled = false;
            guessInput.focus();
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao processar palpite. Tente novamente.');
        guessInput.disabled = false;
        guessButton.disabled = false;
    });
}

// Expor a função makeGuess globalmente para o onclick do botão
window.makeGuess = makeGuess;

