"""
Controller de Histórico e Ranking
Contém apenas as rotas e lógica de HTTP/Flask
Toda a lógica de negócio está em model.py
"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from history.model import (
    get_user_history,
    get_ranking,
    get_user_ranking_position,
    get_today_date_string
)

history_bp = Blueprint('history', __name__, template_folder='../../templates')


@history_bp.route('/history')
def history():
    """
    Página de histórico de jogos do usuário.
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    game_type = request.args.get('game_type', None)
    
    # Busca histórico do usuário
    history_list = get_user_history(user_id, game_type=game_type)
    
    # Estatísticas do usuário
    total_games = len(history_list)
    total_wins = sum(1 for game in history_list if game['won'])
    win_rate = round((total_wins / total_games * 100) if total_games > 0 else 0, 1)
    
    # Agrupa por tipo de jogo
    games_by_type = {}
    for game in history_list:
        game_type_name = game['game_type']
        if game_type_name not in games_by_type:
            games_by_type[game_type_name] = {'total': 0, 'wins': 0, 'total_points': 0}
        games_by_type[game_type_name]['total'] += 1
        if game['won']:
            games_by_type[game_type_name]['wins'] += 1
        # Para Duel, acumula pontos
        if game_type_name == 'duel' and game.get('points', 0) > 0:
            games_by_type[game_type_name]['total_points'] = games_by_type[game_type_name].get('total_points', 0) + game['points']
    
    return render_template('history/history.html',
                         history=history_list,
                         total_games=total_games,
                         total_wins=total_wins,
                         win_rate=win_rate,
                         games_by_type=games_by_type)


@history_bp.route('/ranking')
def ranking():
    """
    Página de ranking de usuários.
    """
    game_type = request.args.get('game_type', None)
    
    # Busca ranking
    ranking_list = get_ranking(game_type=game_type)
    
    # Posição do usuário logado (se estiver logado)
    user_position = None
    if 'user_id' in session:
        user_position = get_user_ranking_position(session['user_id'], game_type=game_type)
    
    return render_template('history/ranking.html',
                         ranking=ranking_list,
                         user_position=user_position,
                         selected_game_type=game_type)


@history_bp.route('/api/history', methods=['GET'])
def api_history():
    """
    API para buscar histórico do usuário (JSON).
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Usuário não autenticado'}), 401
    
    user_id = session['user_id']
    game_type = request.args.get('game_type', None)
    limit = request.args.get('limit', 50, type=int)
    
    history_list = get_user_history(user_id, game_type=game_type, limit=limit)
    
    return jsonify({
        'success': True,
        'history': history_list
    })


@history_bp.route('/api/ranking', methods=['GET'])
def api_ranking():
    """
    API para buscar ranking (JSON).
    """
    game_type = request.args.get('game_type', None)
    limit = request.args.get('limit', 100, type=int)
    
    ranking_list = get_ranking(game_type=game_type, limit=limit)
    
    return jsonify({
        'success': True,
        'ranking': ranking_list
    })

