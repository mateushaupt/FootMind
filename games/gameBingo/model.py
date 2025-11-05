"""
Model do Football Bingo
Contém toda a lógica de negócio e acesso ao banco de dados relacionada ao jogo
"""
import random
from models.Player import Player
from extensions import db


def get_random_player_list(used_player_ids=None):
    """
    Busca uma lista de jogadores aleatórios do banco de dados.
    
    Args:
        used_player_ids (list): Lista de IDs de jogadores já usados
        
    Returns:
        list: Lista de objetos Player aleatórios
    """
    if used_player_ids is None:
        used_player_ids = []
    
    # Busca todos os jogadores que ainda não foram usados
    query = Player.query
    if used_player_ids:
        query = query.filter(~Player.id.in_(used_player_ids))
    
    players = query.all()
    
    if not players:
        return []
    
    # Embaralha a lista de jogadores
    random.shuffle(players)
    return players


def get_player_by_id(player_id):
    """
    Busca um jogador pelo ID.
    
    Args:
        player_id (int): ID do jogador
        
    Returns:
        Player: Objeto Player ou None se não encontrado
    """
    return Player.query.get(player_id)


def generate_bingo_categories():
    """
    Gera um card de bingo com 16 categorias aleatórias baseadas nos dados dos jogadores.
    
    Returns:
        list: Lista de 16 categorias (dicionários com 'id', 'name', 'type')
    """
    # Tipos de categorias possíveis
    category_types = {
        'team': 'Time',
        'country': 'País',
        'trophy': 'Troféu',
        'league': 'Liga',
        'manager': 'Técnico',
        'position': 'Posição'
    }
    
    # Busca todos os jogadores para gerar categorias baseadas nos dados reais
    all_players = Player.query.all()
    
    categories = []
    used_categories = set()
    
    # Gera categorias baseadas nos dados dos jogadores
    potential_categories = []
    
    for player in all_players:
        # Times (playedAt)
        if player.playedAt:
            teams = [t.strip() for t in player.playedAt.split(',') if t.strip()]
            for team in teams:
                potential_categories.append({
                    'name': team,
                    'type': 'team',
                    'display': team
                })
        
        # Países (nationality)
        if player.nationality:
            potential_categories.append({
                'name': player.nationality,
                'type': 'country',
                'display': player.nationality
            })
        
        # Troféus (trophiesEarned)
        if player.trophiesEarned:
            trophies = [t.strip() for t in player.trophiesEarned.split(',') if t.strip()]
            for trophy in trophies:
                potential_categories.append({
                    'name': trophy,
                    'type': 'trophy',
                    'display': trophy
                })
        
        # Ligas (leaguesPlayed)
        if player.leaguesPlayed:
            leagues = [l.strip() for l in player.leaguesPlayed.split(',') if l.strip()]
            for league in leagues:
                potential_categories.append({
                    'name': league,
                    'type': 'league',
                    'display': league
                })
        
        # Técnicos (managedBy)
        if player.managedBy:
            managers = [m.strip() for m in player.managedBy.split(',') if m.strip()]
            for manager in managers:
                potential_categories.append({
                    'name': manager,
                    'type': 'manager',
                    'display': manager
                })
        
        # Com quem jogou (playedWith)
        if player.playedWith:
            teammates = [t.strip() for t in player.playedWith.split(',') if t.strip()]
            for teammate in teammates:
                potential_categories.append({
                    'name': teammate,
                    'type': 'teammate',
                    'display': teammate
                })
    
    # Remove duplicatas mantendo apenas o primeiro
    seen = set()
    unique_categories = []
    for cat in potential_categories:
        key = (cat['name'], cat['type'])
        if key not in seen:
            seen.add(key)
            unique_categories.append(cat)
    
    # Embaralha e pega 16 categorias aleatórias
    random.shuffle(unique_categories)
    
    # Se não houver categorias suficientes, duplica algumas aleatórias
    while len(unique_categories) < 16:
        # Adiciona algumas categorias aleatórias novamente
        if unique_categories:
            unique_categories.extend(random.sample(unique_categories, min(16 - len(unique_categories), len(unique_categories))))
        else:
            # Se não houver nenhuma categoria, retorna categorias padrão
            return generate_default_categories()
    
    selected = unique_categories[:16]
    
    # Adiciona IDs às categorias
    for idx, cat in enumerate(selected):
        categories.append({
            'id': idx,
            'name': cat['name'],
            'type': cat['type'],
            'display': cat['display'],
            'matched': False,
            'player_id': None
        })
    
    return categories


def generate_default_categories():
    """
    Gera categorias padrão caso não haja jogadores no banco.
    
    Returns:
        list: Lista de 16 categorias padrão
    """
    default_categories = [
        {'name': 'Brasil', 'type': 'country', 'display': 'Brasil'},
        {'name': 'Argentina', 'type': 'country', 'display': 'Argentina'},
        {'name': 'Portugal', 'type': 'country', 'display': 'Portugal'},
        {'name': 'França', 'type': 'country', 'display': 'França'},
        {'name': 'Real Madrid', 'type': 'team', 'display': 'Real Madrid'},
        {'name': 'Barcelona', 'type': 'team', 'display': 'Barcelona'},
        {'name': 'PSG', 'type': 'team', 'display': 'PSG'},
        {'name': 'Manchester City', 'type': 'team', 'display': 'Manchester City'},
        {'name': 'Champions League', 'type': 'trophy', 'display': 'Champions League'},
        {'name': 'Copa do Mundo', 'type': 'trophy', 'display': 'Copa do Mundo'},
        {'name': 'Ballon dOr', 'type': 'trophy', 'display': 'Ballon dOr'},
        {'name': 'La Liga', 'type': 'league', 'display': 'La Liga'},
        {'name': 'Premier League', 'type': 'league', 'display': 'Premier League'},
        {'name': 'Ligue 1', 'type': 'league', 'display': 'Ligue 1'},
        {'name': 'Pep Guardiola', 'type': 'manager', 'display': 'Pep Guardiola'},
        {'name': 'Messi', 'type': 'teammate', 'display': 'Messi'},
    ]
    
    categories = []
    for idx, cat in enumerate(default_categories):
        categories.append({
            'id': idx,
            'name': cat['name'],
            'type': cat['type'],
            'display': cat['display'],
            'matched': False,
            'player_id': None
        })
    
    return categories


def check_player_matches_category(player, category_name, category_type):
    """
    Verifica se um jogador corresponde a uma categoria específica.
    
    Args:
        player (Player): Objeto Player
        category_name (str): Nome da categoria
        category_type (str): Tipo da categoria (team, country, trophy, etc.)
        
    Returns:
        bool: True se o jogador corresponde à categoria, False caso contrário
    """
    if not player:
        return False
    
    category_name = category_name.strip().upper()
    
    if category_type == 'team':
        if player.playedAt:
            teams = [t.strip().upper() for t in player.playedAt.split(',')]
            return category_name in teams
    
    elif category_type == 'country':
        if player.nationality:
            return player.nationality.strip().upper() == category_name
    
    elif category_type == 'trophy':
        if player.trophiesEarned:
            trophies = [t.strip().upper() for t in player.trophiesEarned.split(',')]
            return category_name in trophies
    
    elif category_type == 'league':
        if player.leaguesPlayed:
            leagues = [l.strip().upper() for l in player.leaguesPlayed.split(',')]
            return category_name in leagues
    
    elif category_type == 'manager':
        if player.managedBy:
            managers = [m.strip().upper() for m in player.managedBy.split(',')]
            return category_name in managers
    
    elif category_type == 'position':
        if player.position:
            return player.position.strip().upper() == category_name
    
    elif category_type == 'teammate':
        if player.playedWith:
            teammates = [t.strip().upper() for t in player.playedWith.split(',')]
            return category_name in teammates
    
    return False


def is_bingo_complete(categories):
    """
    Verifica se o bingo foi completado (todas as 16 categorias preenchidas).
    
    Args:
        categories (list): Lista de categorias do bingo
        
    Returns:
        bool: True se todas as categorias estão preenchidas, False caso contrário
    """
    if not categories:
        return False
    
    return all(cat.get('matched', False) for cat in categories)


def get_bingo_lines(categories):
    """
    Retorna as linhas do bingo que foram completadas.
    O bingo é uma grade 4x4.
    
    Args:
        categories (list): Lista de categorias do bingo
        
    Returns:
        list: Lista de linhas completadas (0-3 para linhas, 4-7 para colunas, 8-9 para diagonais)
    """
    if len(categories) != 16:
        return []
    
    completed_lines = []
    
    # Linhas horizontais (0-3)
    for row in range(4):
        start_idx = row * 4
        if all(categories[start_idx + i].get('matched', False) for i in range(4)):
            completed_lines.append(row)
    
    # Colunas verticais (4-7)
    for col in range(4):
        if all(categories[col + i * 4].get('matched', False) for i in range(4)):
            completed_lines.append(col + 4)
    
    # Diagonal principal (8)
    if all(categories[i * 5].get('matched', False) for i in range(4)):
        completed_lines.append(8)
    
    # Diagonal secundária (9)
    if all(categories[i * 3 + 3].get('matched', False) for i in range(4)):
        completed_lines.append(9)
    
    return completed_lines

