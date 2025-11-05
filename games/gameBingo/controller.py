"""
Controller do Football Bingo
Contém apenas as rotas e lógica de HTTP/Flask
Toda a lógica de negócio está em model.py
"""
from flask import Blueprint, render_template, request, jsonify, session
from games.gameBingo.model import (
    get_random_player_list,
    get_player_by_id,
    generate_bingo_categories,
    check_player_matches_category,
    is_bingo_complete,
    get_bingo_lines
)

game_bingo_bp = Blueprint('game_bingo', __name__, template_folder='../../templates/games')


@game_bingo_bp.route('/')
def home():
    """
    Rota principal do jogo Football Bingo.
    Inicializa o jogo gerando um novo card de bingo.
    """
    # Gera um novo card de bingo
    categories = generate_bingo_categories()
    
    # Busca lista inicial de jogadores
    players = get_random_player_list()
    
    if not players:
        return render_template('games/game_bingo.html', 
                             error="Nenhum jogador encontrado no banco de dados. Por favor, execute o seed_players.py primeiro.")
    
    # Inicializa o estado do jogo na sessão
    session['bingo_categories'] = categories
    session['bingo_used_player_ids'] = []
    session['bingo_current_player_index'] = 0
    session['bingo_wildcard_used'] = False
    session['bingo_skipped'] = False
    session['bingo_game_over'] = False
    
    # Renderiza a página do jogo
    return render_template('games/game_bingo.html', 
                         categories=categories,
                         total_players=len(players))


@game_bingo_bp.route('/get-player', methods=['GET'])
def get_player():
    """
    Retorna o próximo jogador aleatório para o jogo.
    """
    if 'bingo_used_player_ids' not in session:
        return jsonify({'error': 'Jogo não inicializado'}), 400
    
    used_player_ids = session.get('bingo_used_player_ids', [])
    players = get_random_player_list(used_player_ids)
    
    if not players:
        return jsonify({
            'player': None,
            'game_over': True,
            'message': 'Todos os jogadores foram utilizados!'
        })
    
    # Pega o próximo jogador
    player = players[0]
    used_player_ids.append(player.id)
    
    # Atualiza a sessão
    session['bingo_used_player_ids'] = used_player_ids
    session['bingo_current_player_index'] = len(used_player_ids) - 1
    
    return jsonify({
        'player': {
            'id': player.id,
            'name': player.name,
            'nationality': player.nationality,
            'position': player.position
        },
        'game_over': False
    })


@game_bingo_bp.route('/check-match', methods=['POST'])
def check_match():
    """
    Verifica se o jogador atual corresponde à categoria selecionada.
    """
    if 'bingo_categories' not in session:
        return jsonify({'error': 'Jogo não inicializado'}), 400
    
    data = request.json
    player_id = data.get('player_id')
    category_id = data.get('category_id')
    is_wildcard = data.get('is_wildcard', False)
    
    # Verifica se o wildcard já foi usado
    if is_wildcard and session.get('bingo_wildcard_used', False):
        return jsonify({'error': 'Wildcard já foi usado!'}), 400
    
    # Busca o jogador
    player = get_player_by_id(player_id)
    if not player:
        return jsonify({'error': 'Jogador não encontrado'}), 404
    
    # Busca a categoria
    categories = session.get('bingo_categories', [])
    if category_id >= len(categories) or category_id < 0:
        return jsonify({'error': 'Categoria inválida'}), 400
    
    category = categories[category_id]
    
    # Verifica se a categoria já foi preenchida
    if category.get('matched', False) and not is_wildcard:
        return jsonify({'error': 'Categoria já foi preenchida!'}), 400
    
    # Verifica se o jogador corresponde à categoria
    is_match = check_player_matches_category(player, category['name'], category['type'])
    
    if is_match or is_wildcard:
        # Marca a categoria como preenchida
        category['matched'] = True
        category['player_id'] = player_id
        categories[category_id] = category
        
        # Atualiza a sessão
        session['bingo_categories'] = categories
        
        if is_wildcard:
            session['bingo_wildcard_used'] = True
        
        # Verifica se o bingo foi completado
        bingo_complete = is_bingo_complete(categories)
        completed_lines = get_bingo_lines(categories) if bingo_complete else []
        
        return jsonify({
            'success': True,
            'is_match': True,
            'wildcard_used': is_wildcard,
            'category': category,
            'bingo_complete': bingo_complete,
            'completed_lines': completed_lines,
            'message': 'Categoria preenchida com sucesso!' if is_match else 'Wildcard usado com sucesso!'
        })
    else:
        # Resposta incorreta - perde a vez
        return jsonify({
            'success': False,
            'is_match': False,
            'message': 'Jogador não corresponde à categoria selecionada. Você perdeu a vez!',
            'skip_next': True
        })


@game_bingo_bp.route('/skip', methods=['POST'])
def skip():
    """
    Pula o jogador atual sem penalidade.
    """
    if 'bingo_used_player_ids' not in session:
        return jsonify({'error': 'Jogo não inicializado'}), 400
    
    session['bingo_skipped'] = True
    
    return jsonify({
        'success': True,
        'message': 'Jogador pulado com sucesso!'
    })


@game_bingo_bp.route('/get-state', methods=['GET'])
def get_state():
    """
    Retorna o estado atual do jogo.
    """
    return jsonify({
        'categories': session.get('bingo_categories', []),
        'wildcard_used': session.get('bingo_wildcard_used', False),
        'used_players_count': len(session.get('bingo_used_player_ids', []))
    })

