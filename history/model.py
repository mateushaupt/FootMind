"""
Model de Histórico e Ranking
Contém lógica para gerenciar histórico de jogos e rankings
"""
import hashlib
from datetime import datetime, date
from models.HistoryGame import HistoryGame
from models.UserGame import UserGame
from models.User import User
from extensions import db


def get_today_date_string():
    """
    Retorna a data de hoje no formato YYYY-MM-DD.
    
    Returns:
        str: Data no formato YYYY-MM-DD
    """
    return date.today().strftime('%Y-%m-%d')


def generate_config_hash(game_type, config_data):
    """
    Gera um hash único para a configuração do jogo do dia.
    O hash inclui o tipo de jogo no início para facilitar a extração.
    
    Args:
        game_type (str): Tipo do jogo ('wordle', 'bingo', 'duel', etc.)
        config_data (dict): Dados da configuração do jogo
        
    Returns:
        str: Hash da configuração no formato "game_type:hash"
    """
    # Cria uma string única baseada na configuração
    config_string = str(sorted(config_data.items()))
    config_hash = hashlib.md5(config_string.encode()).hexdigest()
    # Retorna no formato "game_type:hash" para facilitar extração
    return f"{game_type}:{config_hash}"


def get_or_create_history_game(game_type, config_data):
    """
    Busca ou cria um HistoryGame para o dia atual com a configuração especificada.
    
    Args:
        game_type (str): Tipo do jogo ('wordle', 'bingo', 'duel', etc.)
        config_data (dict): Dados da configuração do jogo
        
    Returns:
        HistoryGame: Objeto HistoryGame do dia
    """
    today = get_today_date_string()
    config_hash = generate_config_hash(game_type, config_data)
    
    # Busca se já existe um HistoryGame para hoje com este configHash
    history_game = HistoryGame.query.filter_by(
        dateCreated=today,
        configHash=config_hash
    ).first()
    
    if not history_game:
        try:
            # Cria um novo HistoryGame para hoje
            history_game = HistoryGame(
                dateCreated=today,
                configHash=config_hash
            )
            db.session.add(history_game)
            db.session.commit()
        except Exception as e:
            # Se houver erro (ex: constraint violation), faz rollback e tenta buscar novamente
            db.session.rollback()
            # Tenta buscar novamente (pode ter sido criado por outra requisição simultânea)
            history_game = HistoryGame.query.filter_by(
                dateCreated=today,
                configHash=config_hash
            ).first()
            if not history_game:
                # Se ainda não existir, tenta criar novamente com tratamento de erro
                try:
                    history_game = HistoryGame(
                        dateCreated=today,
                        configHash=config_hash
                    )
                    db.session.add(history_game)
                    db.session.commit()
                except Exception:
                    # Se ainda falhar, faz rollback e busca uma última vez
                    db.session.rollback()
                    history_game = HistoryGame.query.filter_by(
                        dateCreated=today,
                        configHash=config_hash
                    ).first()
                    if not history_game:
                        raise e
    
    return history_game


def save_game_result(user_id, game_type, config_data, won, points=None):
    """
    Salva o resultado de um jogo no histórico.
    
    Args:
        user_id (int): ID do usuário
        game_type (str): Tipo do jogo
        config_data (dict): Dados da configuração do jogo
        won (bool): True se o usuário venceu, False caso contrário
        points (int, optional): Pontos obtidos no jogo (usado principalmente para Duel)
        
    Returns:
        UserGame: Objeto UserGame criado
    """
    # Busca ou cria o HistoryGame do dia
    history_game = get_or_create_history_game(game_type, config_data)
    
    # Verifica se o usuário já jogou este jogo hoje
    existing_user_game = UserGame.query.filter_by(
        userId=user_id,
        gameId=history_game.id
    ).first()
    
    if existing_user_game:
        # Atualiza o resultado existente
        existing_user_game.result = 1 if won else 0
        if points is not None:
            existing_user_game.points = points
        db.session.commit()
        return existing_user_game
    
    # Cria novo registro
    user_game = UserGame(
        userId=user_id,
        gameId=history_game.id,
        result=1 if won else 0,
        points=points if points is not None else 0
    )
    db.session.add(user_game)
    db.session.commit()
    
    return user_game


def get_user_history(user_id, game_type=None, limit=50):
    """
    Busca o histórico de jogos de um usuário.
    
    Args:
        user_id (int): ID do usuário
        game_type (str, optional): Filtrar por tipo de jogo
        limit (int): Limite de resultados
        
    Returns:
        list: Lista de dicionários com informações dos jogos
    """
    query = db.session.query(UserGame, HistoryGame).join(
        HistoryGame, UserGame.gameId == HistoryGame.id
    ).filter(UserGame.userId == user_id)
    
    if game_type:
        # Filtra por tipo de jogo baseado no configHash (formato "game_type:hash")
        query = query.filter(HistoryGame.configHash.like(f"{game_type}:%"))
    
    results = query.order_by(HistoryGame.dateCreated.desc()).limit(limit).all()
    
    history_list = []
    for user_game, history_game in results:
        # Extrai o tipo de jogo do configHash (formato "game_type:hash")
        game_type_from_hash = history_game.configHash.split(':')[0] if ':' in history_game.configHash else 'unknown'
        
        history_list.append({
            'id': user_game.id,
            'date': history_game.dateCreated,
            'game_type': game_type_from_hash,
            'game_type_display': get_game_type_display_name(game_type_from_hash),
            'won': user_game.result == 1,
            'result': user_game.result,
            'points': user_game.points if user_game.points else 0
        })
    
    return history_list


def get_ranking(game_type=None, limit=100):
    """
    Busca o ranking de usuários baseado em vitórias ou pontos (para Duel).
    
    Args:
        game_type (str, optional): Filtrar por tipo de jogo
        limit (int): Limite de resultados
        
    Returns:
        list: Lista de dicionários com informações do ranking
    """
    # Para Duel, usa pontos ao invés de vitórias
    if game_type == 'duel':
        # Query para somar pontos por usuário
        query = db.session.query(
            User.id,
            User.nickname,
            db.func.sum(UserGame.points).label('total_points'),
            db.func.count(UserGame.id).label('total_games'),
            db.func.max(UserGame.points).label('best_score')
        ).join(
            UserGame, User.id == UserGame.userId
        ).join(
            HistoryGame, UserGame.gameId == HistoryGame.id
        ).filter(
            HistoryGame.configHash.like('duel:%')
        ).group_by(User.id, User.nickname)
        
        results = query.order_by(db.desc('total_points'), db.desc('best_score')).limit(limit).all()
        
        ranking_list = []
        position = 1
        for user_id, nickname, total_points, total_games, best_score in results:
            ranking_list.append({
                'position': position,
                'user_id': user_id,
                'nickname': nickname,
                'total_points': total_points or 0,
                'best_score': best_score or 0,
                'total_games': total_games or 0,
                'avg_points': round((total_points or 0) / (total_games or 1), 1) if total_games > 0 else 0
            })
            position += 1
        
        return ranking_list
    else:
        # Para outros jogos (wordle, bingo) ou ranking geral, usa vitórias
        query = db.session.query(
            User.id,
            User.nickname,
            db.func.sum(db.case((UserGame.result == 1, 1), else_=0)).label('wins'),
            db.func.count(UserGame.id).label('total_games'),
            db.func.max(HistoryGame.dateCreated).label('last_game_date')
        ).join(
            UserGame, User.id == UserGame.userId
        ).join(
            HistoryGame, UserGame.gameId == HistoryGame.id
        )
        
        if game_type:
            # Filtra por tipo de jogo baseado no configHash (formato "game_type:hash")
            query = query.filter(HistoryGame.configHash.like(f"{game_type}:%"))
        else:
            # Ranking geral - exclui Duel (que usa pontos)
            query = query.filter(~HistoryGame.configHash.like('duel:%'))
        
        query = query.group_by(User.id, User.nickname)
        
        # Ordena por: primeiro quem tem mais vitórias, depois por quem jogou por último (data mais recente)
        results = query.order_by(db.desc('wins'), db.desc('last_game_date')).limit(limit).all()
        
        ranking_list = []
        position = 1
        for user_id, nickname, wins, total_games, last_game_date in results:
            ranking_list.append({
                'position': position,
                'user_id': user_id,
                'nickname': nickname,
                'wins': wins or 0,
                'total_games': total_games or 0,
                'win_rate': round((wins or 0) / (total_games or 1) * 100, 1) if total_games > 0 else 0,
                'last_game_date': last_game_date
            })
            position += 1
        
        return ranking_list


def get_user_ranking_position(user_id, game_type=None):
    """
    Retorna a posição do usuário no ranking.
    
    Args:
        user_id (int): ID do usuário
        game_type (str, optional): Filtrar por tipo de jogo
        
    Returns:
        int: Posição no ranking (None se não estiver no ranking)
    """
    ranking = get_ranking(game_type, limit=1000)
    
    for entry in ranking:
        if entry['user_id'] == user_id:
            return entry['position']
    
    return None


def get_game_type_display_name(game_type):
    """
    Retorna o nome de exibição do tipo de jogo.
    
    Args:
        game_type (str): Tipo do jogo
        
    Returns:
        str: Nome de exibição
    """
    game_names = {
        'wordle': 'FootWordle',
        'bingo': 'Football Bingo',
        'duel': 'Game Duel'
    }
    return game_names.get(game_type, game_type.capitalize())


def has_user_played_today(user_id, game_type, config_data):
    """
    Verifica se o usuário já jogou o jogo do dia.
    
    Args:
        user_id (int): ID do usuário
        game_type (str): Tipo do jogo
        config_data (dict): Dados da configuração do jogo
        
    Returns:
        tuple: (bool, UserGame) - True se já jogou e o objeto UserGame, ou (False, None)
    """
    today = get_today_date_string()
    config_hash = generate_config_hash(game_type, config_data)
    
    # Busca o HistoryGame do dia
    history_game = HistoryGame.query.filter_by(
        dateCreated=today,
        configHash=config_hash
    ).first()
    
    if not history_game:
        return False, None
    
    # Verifica se o usuário já jogou
    user_game = UserGame.query.filter_by(
        userId=user_id,
        gameId=history_game.id
    ).first()
    
    if user_game:
        return True, user_game
    
    return False, None

