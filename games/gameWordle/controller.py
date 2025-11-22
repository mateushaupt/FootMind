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
from history.model import save_game_result

game_wordle_bp = Blueprint('game_wordle', __name__, template_folder='../../templates/games')

# Configurações do jogo
MAX_ATTEMPTS = 5


@game_wordle_bp.route('/')
def home():
    """
    Rota principal do jogo FootWordle.
    Seleciona o jogador do dia (mesmo para todos os usuários) e inicializa a sessão do jogo.
    Verifica se o usuário já jogou o jogo do dia.
    """
    from history.model import get_or_create_history_game, get_today_date_string, has_user_played_today
    from models.HistoryGame import HistoryGame
    from models.Player import Player
    import random
    import hashlib
    
    # Busca todos os jogadores
    all_players = Player.query.all()
    if not all_players:
        return render_template('games/game_wordle.html', 
                             word_length=0, 
                             error="Nenhum jogador encontrado no banco de dados. Por favor, adicione jogadores primeiro.")
    
    # Usa a data como seed para garantir o mesmo jogador para todos no mesmo dia
    today = get_today_date_string()
    # Cria um hash da data para usar como seed
    date_hash = int(hashlib.md5(today.encode()).hexdigest(), 16)
    random.seed(date_hash)
    
    # Seleciona um jogador aleatório baseado no seed da data
    player = random.choice(all_players)
    
    # Restaura o seed aleatório
    random.seed()
    
    # Obtém o nome do jogador em maiúsculas
    player_name = get_player_name(player)
    
    # Cria o configHash do dia para garantir que todos usem o mesmo jogador
    config_data = {
        'player_id': player.id,
        'player_name': player_name
    }
    
    # Verifica se o usuário já jogou hoje (se estiver logado)
    if 'user_id' in session:
        has_played, user_game = has_user_played_today(
            session['user_id'],
            'wordle',
            config_data
        )
        
        if has_played:
            # Usuário já jogou - mostra resultado
            history_game = HistoryGame.query.get(user_game.gameId)
            return render_template(
                'games/game_result.html',
                game_type='wordle',
                game_type_display='FootWordle',
                won=user_game.result == 1,
                date=history_game.dateCreated if history_game else today,
                answer=player_name
            )
    
    history_game = get_or_create_history_game('wordle', config_data)
    
    # Armazena a resposta na sessão
    session['current_answer'] = player_name
    session['current_player_id'] = player.id
    session['wordle_history_game_id'] = history_game.id
    
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
    
    # Se o jogo terminou, salva no histórico
    if game_over and 'user_id' in session:
        player_id = session.get('current_player_id')
        # ConfigHash para Wordle: nome do jogador do dia
        config_data = {
            'player_id': player_id,
            'player_name': current_answer
        }
        try:
            save_game_result(
                user_id=session['user_id'],
                game_type='wordle',
                config_data=config_data,
                won=won
            )
        except Exception as e:
            # Log do erro mas não interrompe o jogo
            print(f"Erro ao salvar histórico: {e}")
    
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
