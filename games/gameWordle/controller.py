"""
Controller do FootWordle
Contém apenas as rotas e lógica de HTTP/Flask
Toda a lógica de negócio está em model.py
"""
from flask import Blueprint, render_template, request, jsonify, session
from games.gameWordle.model import (
    get_random_player,
    get_player_name,
    check_guess as validate_guess,
    is_guess_correct,
    is_game_over
)

game_wordle_bp = Blueprint('game_wordle', __name__, template_folder='../../templates/games')

# Configurações do jogo
MAX_ATTEMPTS = 5


@game_wordle_bp.route('/')
def home():
    """
    Rota principal do jogo FootWordle.
    Seleciona um jogador aleatório e inicializa a sessão do jogo.
    """
    # Busca um jogador aleatório do banco de dados
    player = get_random_player()
    
    if not player:
        # Se não houver jogadores no banco, retorna erro
        return render_template('games/game_wordle.html', 
                             word_length=0, 
                             error="Nenhum jogador encontrado no banco de dados. Por favor, adicione jogadores primeiro.")
    
    # Obtém o nome do jogador em maiúsculas
    player_name = get_player_name(player)
    
    # Armazena a resposta na sessão
    session['current_answer'] = player_name
    session['current_player_id'] = player.id
    
    # Renderiza a página do jogo
    return render_template('games/game_wordle.html', word_length=len(player_name))


@game_wordle_bp.route('/guess', methods=['POST'])
def check_guess():
    """
    Rota para processar o palpite do usuário.
    Retorna JSON com o resultado da validação.
    """
    # Verifica se há uma resposta ativa na sessão
    if 'current_answer' not in session:
        return jsonify({'error': 'Nenhum jogo ativo. Por favor, recarregue a página.'}), 400
    
    current_answer = session['current_answer']
    guess = request.json.get('guess', '').upper().strip()
    attempt = request.json.get('attempt', 0)
    
    # Validação básica
    if not guess:
        return jsonify({'error': 'Palpite não pode estar vazio!'}), 400
    
    if len(guess) != len(current_answer):
        return jsonify({
            'error': f'O nome deve ter exatamente {len(current_answer)} letras!'
        }), 400
    
    # Processa o palpite usando a lógica do model
    result = validate_guess(guess, current_answer)
    won = is_guess_correct(guess, current_answer)
    game_over = is_game_over(attempt, MAX_ATTEMPTS, won)
    
    # Prepara a resposta
    response_data = {
        'result': result,
        'won': won,
        'gameOver': game_over,
        'answer': current_answer if game_over else None
    }
    
    # Se o jogo terminou, limpa a sessão
    if game_over:
        session.pop('current_answer', None)
        session.pop('current_player_id', None)
    
    return jsonify(response_data)
