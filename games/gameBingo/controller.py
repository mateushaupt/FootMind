"""
Controller do Football Bingo
Contém apenas as rotas e lógica de HTTP/Flask
Toda a lógica de negócio está em model.py
"""
import random
from flask import Blueprint, render_template, request, jsonify, session
from games.gameBingo.model import (
    get_random_player_list,
    get_player_by_id,
    generate_bingo_categories,
    check_player_matches_category,
    is_bingo_complete,
    get_bingo_lines
)
from history.model import save_game_result

game_bingo_bp = Blueprint('game_bingo', __name__, template_folder='../../templates/games')


@game_bingo_bp.route('/')
def home():
    """
    Rota principal do jogo Football Bingo.
    Inicializa o jogo gerando um novo card de bingo com a mesma configuração do dia.
    Verifica se o usuário já jogou o jogo do dia.
    """
    from history.model import get_or_create_history_game, get_today_date_string, has_user_played_today
    from models.HistoryGame import HistoryGame
    import hashlib
    
    # Verifica PRIMEIRO se há resultado salvo na sessão (jogo já foi finalizado)
    if session.get('bingo_result_saved', False) and 'user_id' in session:
        # Busca o resultado do banco de dados
        today = get_today_date_string()
        all_players = get_random_player_list()
        if all_players:
            date_hash = int(hashlib.md5(today.encode()).hexdigest(), 16)
            random.seed(date_hash)
            selected_players = random.sample(all_players, min(42, len(all_players)))
            selected_player_ids = [p.id for p in selected_players]
            random.seed()
            config_data = {'selected_player_ids': sorted(selected_player_ids)}
            
            has_played, user_game = has_user_played_today(
                session['user_id'],
                'bingo',
                config_data
            )
            
            if has_played:
                # Limpa todas as variáveis de sessão do bingo
                session.pop('bingo_categories', None)
                session.pop('bingo_selected_player_ids', None)
                session.pop('bingo_used_player_ids', None)
                session.pop('bingo_current_player_index', None)
                session.pop('bingo_wildcard_used', None)
                session.pop('bingo_skipped', None)
                session.pop('bingo_game_over', None)
                session.pop('bingo_result_saved', None)
                session.pop('bingo_history_game_id', None)
                
                history_game = HistoryGame.query.get(user_game.gameId)
                return render_template(
                    'games/game_result.html',
                    game_type='bingo',
                    game_type_display='Football Bingo',
                    won=user_game.result == 1,
                    date=history_game.dateCreated if history_game else today
                )
    
    # Busca todos os jogadores disponíveis
    all_players = get_random_player_list()
    
    if not all_players:
        return render_template('games/game_bingo.html', 
                             error="Nenhum jogador encontrado no banco de dados. Por favor, execute o seed_players.py primeiro.")
    
    # Usa a data como seed para garantir a mesma configuração para todos no mesmo dia
    today = get_today_date_string()
    date_hash = int(hashlib.md5(today.encode()).hexdigest(), 16)
    random.seed(date_hash)
    
    # Seleciona 42 jogadores aleatórios baseado no seed da data
    selected_players = random.sample(all_players, min(42, len(all_players)))
    selected_player_ids = [p.id for p in selected_players]
    
    # Restaura o seed aleatório
    random.seed()
    
    # Cria o configHash do dia para garantir que todos usem a mesma configuração
    config_data = {
        'selected_player_ids': sorted(selected_player_ids)
    }
    
    # Verifica se o usuário já jogou hoje (se estiver logado)
    if 'user_id' in session:
        has_played, user_game = has_user_played_today(
            session['user_id'],
            'bingo',
            config_data
        )
        
        if has_played:
            # Limpa todas as variáveis de sessão do bingo para evitar conflitos
            session.pop('bingo_categories', None)
            session.pop('bingo_selected_player_ids', None)
            session.pop('bingo_used_player_ids', None)
            session.pop('bingo_current_player_index', None)
            session.pop('bingo_wildcard_used', None)
            session.pop('bingo_skipped', None)
            session.pop('bingo_game_over', None)
            session.pop('bingo_result_saved', None)
            session.pop('bingo_history_game_id', None)
            
            # Usuário já jogou - mostra resultado
            history_game = HistoryGame.query.get(user_game.gameId)
            return render_template(
                'games/game_result.html',
                game_type='bingo',
                game_type_display='Football Bingo',
                won=user_game.result == 1,
                date=history_game.dateCreated if history_game else today
            )
    
    # Se chegou aqui, o usuário pode jogar (não está logado ou ainda não jogou hoje)
    # Busca todos os jogadores disponíveis
    all_players = get_random_player_list()
    
    if not all_players:
        return render_template('games/game_bingo.html', 
                             error="Nenhum jogador encontrado no banco de dados. Por favor, execute o seed_players.py primeiro.")
    
    # Usa a data como seed para garantir a mesma configuração para todos no mesmo dia
    today = get_today_date_string()
    date_hash = int(hashlib.md5(today.encode()).hexdigest(), 16)
    random.seed(date_hash)
    
    # Seleciona 42 jogadores aleatórios baseado no seed da data
    selected_players = random.sample(all_players, min(42, len(all_players)))
    selected_player_ids = [p.id for p in selected_players]
    
    # Restaura o seed aleatório
    random.seed()
    
    # Cria o configHash do dia para garantir que todos usem a mesma configuração
    config_data = {
        'selected_player_ids': sorted(selected_player_ids)
    }
    
    # Só gera o jogo se o usuário ainda não jogou
    history_game = get_or_create_history_game('bingo', config_data)
    
    # Gera um novo card de bingo baseado apenas nos 42 jogadores selecionados
    categories = generate_bingo_categories(selected_players=selected_players)
    
    # Limpa variáveis de sessão anteriores antes de inicializar novo jogo
    session.pop('bingo_categories', None)
    session.pop('bingo_selected_player_ids', None)
    session.pop('bingo_used_player_ids', None)
    session.pop('bingo_current_player_index', None)
    session.pop('bingo_wildcard_used', None)
    session.pop('bingo_skipped', None)
    session.pop('bingo_game_over', None)
    session.pop('bingo_result_saved', None)
    session.pop('bingo_history_game_id', None)
    
    # Inicializa o estado do jogo na sessão
    session['bingo_categories'] = categories
    session['bingo_selected_player_ids'] = selected_player_ids  # Armazena os IDs dos 42 jogadores
    session['bingo_used_player_ids'] = []
    session['bingo_current_player_index'] = 0
    session['bingo_wildcard_used'] = False
    session['bingo_skipped'] = False
    session['bingo_game_over'] = False
    session['bingo_result_saved'] = False
    session['bingo_history_game_id'] = history_game.id
    
    # Renderiza a página do jogo
    return render_template('games/game_bingo.html', 
                         categories=categories,
                         total_players=len(selected_players))


@game_bingo_bp.route('/get-player', methods=['GET'])
def get_player():
    """
    Retorna o próximo jogador aleatório para o jogo.
    """
    # Verifica se o usuário já jogou hoje (se estiver logado)
    if 'user_id' in session:
        from history.model import has_user_played_today, get_today_date_string
        today = get_today_date_string()
        selected_player_ids = session.get('bingo_selected_player_ids', [])
        config_data = {
            'selected_player_ids': sorted(selected_player_ids) if selected_player_ids else []
        }
        has_played, _ = has_user_played_today(
            session['user_id'],
            'bingo',
            config_data
        )
        if has_played:
            return jsonify({'error': 'Você já jogou este jogo hoje!', 'already_played': True}), 403
    
    if 'bingo_used_player_ids' not in session:
        return jsonify({'error': 'Jogo não inicializado'}), 400
    
    used_player_ids = session.get('bingo_used_player_ids', [])
    selected_player_ids = session.get('bingo_selected_player_ids', None)
    players = get_random_player_list(used_player_ids, selected_player_ids)
    
    if not players:
        # Calcula informações sobre os jogadores quando o jogo termina
        selected_player_ids = session.get('bingo_selected_player_ids', [])
        total_players = len(selected_player_ids) if selected_player_ids else 0
        used_count = len(used_player_ids)
        remaining_count = total_players - used_count
        
        # Se o jogo terminou sem completar o bingo, salva como derrota
        if 'user_id' in session and not session.get('bingo_result_saved', False):
            from history.model import save_game_result
            config_data = {
                'selected_player_ids': sorted(selected_player_ids) if selected_player_ids else []
            }
            try:
                # Verifica se o bingo foi completado
                categories = session.get('bingo_categories', [])
                from games.gameBingo.model import is_bingo_complete
                bingo_complete = is_bingo_complete(categories)
                
                save_game_result(
                    user_id=session['user_id'],
                    game_type='bingo',
                    config_data=config_data,
                    won=bingo_complete
                )
                session['bingo_result_saved'] = True
                session['bingo_game_over'] = True
            except Exception as e:
                print(f"Erro ao salvar histórico: {e}")
        
        return jsonify({
            'player': None,
            'game_over': True,
            'message': 'Todos os jogadores foram utilizados!',
            'total_players': total_players,
            'used_players': used_count,
            'remaining_players': remaining_count
        })
    
    # Pega o próximo jogador
    player = players[0]
    used_player_ids.append(player.id)
    
    # Calcula informações sobre os jogadores
    selected_player_ids = session.get('bingo_selected_player_ids', [])
    total_players = len(selected_player_ids) if selected_player_ids else 0
    used_count = len(used_player_ids)
    remaining_count = total_players - used_count
    
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
        'game_over': False,
        'total_players': total_players,
        'used_players': used_count,
        'remaining_players': remaining_count
    })


@game_bingo_bp.route('/check-match', methods=['POST'])
def check_match():
    """
    Verifica se o jogador atual corresponde à categoria selecionada.
    """
    # Verifica se o usuário já jogou hoje (se estiver logado)
    if 'user_id' in session:
        from history.model import has_user_played_today, get_today_date_string
        today = get_today_date_string()
        selected_player_ids = session.get('bingo_selected_player_ids', [])
        config_data = {
            'selected_player_ids': sorted(selected_player_ids) if selected_player_ids else []
        }
        has_played, _ = has_user_played_today(
            session['user_id'],
            'bingo',
            config_data
        )
        if has_played:
            return jsonify({'error': 'Você já jogou este jogo hoje!', 'already_played': True}), 403
    
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
        
        # Se o bingo foi completado, salva no histórico
        if bingo_complete and 'user_id' in session and not session.get('bingo_result_saved', False):
            selected_player_ids = session.get('bingo_selected_player_ids', [])
            # ConfigHash para Bingo: sequência de jogadores selecionados (ordenados para consistência)
            config_data = {
                'selected_player_ids': sorted(selected_player_ids)
            }
            try:
                save_game_result(
                    user_id=session['user_id'],
                    game_type='bingo',
                    config_data=config_data,
                    won=True
                )
                session['bingo_game_over'] = True
                session['bingo_result_saved'] = True
            except Exception as e:
                # Log do erro mas não interrompe o jogo
                print(f"Erro ao salvar histórico: {e}")
        
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
        # Resposta incorreta - perde a vez (penalidade)
        # Marca o jogador como usado para que não apareça novamente nesta rodada
        used_player_ids = session.get('bingo_used_player_ids', [])
        if player_id not in used_player_ids:
            used_player_ids.append(player_id)
            session['bingo_used_player_ids'] = used_player_ids
        
        return jsonify({
            'success': False,
            'is_match': False,
            'message': 'Jogador não corresponde à categoria selecionada.',
            'skip_next': True,
            'penalty': True
        })


@game_bingo_bp.route('/skip', methods=['POST'])
def skip():
    """
    Pula o jogador atual sem penalidade.
    """
    # Verifica se o usuário já jogou hoje (se estiver logado)
    if 'user_id' in session:
        from history.model import has_user_played_today, get_today_date_string
        today = get_today_date_string()
        selected_player_ids = session.get('bingo_selected_player_ids', [])
        config_data = {
            'selected_player_ids': sorted(selected_player_ids) if selected_player_ids else []
        }
        has_played, _ = has_user_played_today(
            session['user_id'],
            'bingo',
            config_data
        )
        if has_played:
            return jsonify({'error': 'Você já jogou este jogo hoje!', 'already_played': True}), 403
    
    if 'bingo_used_player_ids' not in session:
        return jsonify({'error': 'Jogo não inicializado'}), 400
    
    session['bingo_skipped'] = True
    
    return jsonify({
        'success': True,
        'message': 'Jogador pulado com sucesso!'
    })


@game_bingo_bp.route('/use-wildcard', methods=['POST'])
def use_wildcard():
    """
    Usa o wildcard para completar todas as categorias que o jogador atual cobre.
    Pode ser usado apenas uma vez.
    """
    # Verifica se o usuário já jogou hoje (se estiver logado)
    if 'user_id' in session:
        from history.model import has_user_played_today, get_today_date_string
        today = get_today_date_string()
        selected_player_ids = session.get('bingo_selected_player_ids', [])
        config_data = {
            'selected_player_ids': sorted(selected_player_ids) if selected_player_ids else []
        }
        has_played, _ = has_user_played_today(
            session['user_id'],
            'bingo',
            config_data
        )
        if has_played:
            return jsonify({'error': 'Você já jogou este jogo hoje!', 'already_played': True}), 403
    
    if 'bingo_categories' not in session:
        return jsonify({'error': 'Jogo não inicializado'}), 400
    
    # Verifica se o wildcard já foi usado
    if session.get('bingo_wildcard_used', False):
        return jsonify({'error': 'Wildcard já foi usado!'}), 400
    
    data = request.json
    player_id = data.get('player_id')
    
    if not player_id:
        return jsonify({'error': 'ID do jogador não fornecido'}), 400
    
    # Busca o jogador
    player = get_player_by_id(player_id)
    if not player:
        return jsonify({'error': 'Jogador não encontrado'}), 404
    
    # Busca todas as categorias
    categories = session.get('bingo_categories', [])
    
    # Encontra todas as categorias que o jogador corresponde e que ainda não foram preenchidas
    matched_categories = []
    for idx, category in enumerate(categories):
        if not category.get('matched', False):
            is_match = check_player_matches_category(player, category['name'], category['type'])
            if is_match:
                # Marca a categoria como preenchida
                category['matched'] = True
                category['player_id'] = player_id
                categories[idx] = category
                matched_categories.append({
                    'id': idx,
                    'name': category['name'],
                    'type': category['type'],
                    'display': category['display']
                })
    
    # Atualiza a sessão
    session['bingo_categories'] = categories
    session['bingo_wildcard_used'] = True
    
    # Verifica se o bingo foi completado
    bingo_complete = is_bingo_complete(categories)
    completed_lines = get_bingo_lines(categories) if bingo_complete else []
    
    # Se o bingo foi completado, salva no histórico
    if bingo_complete and 'user_id' in session and not session.get('bingo_result_saved', False):
        selected_player_ids = session.get('bingo_selected_player_ids', [])
        # ConfigHash para Bingo: sequência de jogadores selecionados (ordenados para consistência)
        config_data = {
            'selected_player_ids': sorted(selected_player_ids)
        }
        try:
            save_game_result(
                user_id=session['user_id'],
                game_type='bingo',
                config_data=config_data,
                won=True
            )
            session['bingo_game_over'] = True
            session['bingo_result_saved'] = True
        except Exception as e:
            # Log do erro mas não interrompe o jogo
            print(f"Erro ao salvar histórico: {e}")
    
    # Mensagem baseada no número de categorias completadas
    if len(matched_categories) == 0:
        message = 'Wildcard usado, mas o jogador não corresponde a nenhuma categoria disponível!'
    elif len(matched_categories) == 1:
        message = f'Wildcard usado! 1 categoria completada: {matched_categories[0]["display"]}'
    else:
        message = f'Wildcard usado! {len(matched_categories)} categorias completadas!'
    
    return jsonify({
        'success': True,
        'wildcard_used': True,
        'matched_categories': matched_categories,
        'matched_count': len(matched_categories),
        'bingo_complete': bingo_complete,
        'completed_lines': completed_lines,
        'message': message
    })


@game_bingo_bp.route('/get-state', methods=['GET'])
def get_state():
    """
    Retorna o estado atual do jogo.
    """
    # Verifica se o usuário já jogou hoje (se estiver logado)
    if 'user_id' in session:
        from history.model import has_user_played_today, get_today_date_string
        today = get_today_date_string()
        selected_player_ids = session.get('bingo_selected_player_ids', [])
        config_data = {
            'selected_player_ids': sorted(selected_player_ids) if selected_player_ids else []
        }
        has_played, _ = has_user_played_today(
            session['user_id'],
            'bingo',
            config_data
        )
        if has_played:
            return jsonify({'error': 'Você já jogou este jogo hoje!', 'already_played': True}), 403
    
    selected_player_ids = session.get('bingo_selected_player_ids', [])
    used_player_ids = session.get('bingo_used_player_ids', [])
    total_players = len(selected_player_ids) if selected_player_ids else 0
    used_count = len(used_player_ids)
    remaining_count = total_players - used_count
    
    return jsonify({
        'categories': session.get('bingo_categories', []),
        'wildcard_used': session.get('bingo_wildcard_used', False),
        'used_players_count': used_count,
        'total_players': total_players,
        'remaining_players': remaining_count
    })

