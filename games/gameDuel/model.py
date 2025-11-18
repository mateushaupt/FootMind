"""
Model do Game Duel
Contém toda a lógica de negócio e acesso ao banco de dados relacionada ao jogo
"""
import random
from models.Player import Player


# Estatísticas disponíveis no jogo
ESTATISTICAS = {
    "totalGames": "Jogos",
    "goals": "Gols",
    "assists": "Assistências",
    "totalTrophies": "Troféus",
    "redCards": "Cartões Vermelhos"
}


def get_random_players(count=2):
    """
    Busca jogadores aleatórios do banco de dados.
    
    Args:
        count (int): Número de jogadores a retornar (padrão: 2)
        
    Returns:
        list: Lista de objetos Player ou lista vazia se não houver jogadores suficientes
    """
    players = Player.query.all()
    if not players or len(players) < count:
        return []
    return random.sample(players, count)


def get_player_stat_value(player, stat_key):
    """
    Retorna o valor de uma estatística específica de um jogador.
    
    Args:
        player: Objeto Player
        stat_key (str): Chave da estatística ('totalGames', 'goals', 'assists', 'totalTrophies', 'redCards')
        
    Returns:
        int: Valor da estatística ou 0 se não existir
    """
    if stat_key == 'totalGames':
        return player.totalGames if player.totalGames is not None else 0
    elif stat_key == 'goals':
        return player.goals if player.goals is not None else 0
    elif stat_key == 'assists':
        return player.assists if player.assists is not None else 0
    elif stat_key == 'totalTrophies':
        return player.totalTrophies if player.totalTrophies is not None else 0
    elif stat_key == 'redCards':
        return player.redCards if player.redCards is not None else 0
    return 0


def prepare_round():
    """
    Prepara uma rodada do jogo sorteando dois jogadores e uma estatística.
    Garante que os valores sejam diferentes para evitar empates.
    
    Returns:
        dict: Dicionário com informações da rodada ou None se não houver jogadores
        {
            'jogador1': Player,
            'jogador2': Player,
            'stat_key': str,
            'stat_nome': str,
            'valor1': int,
            'valor2': int,
            'resposta_correta': str ('jogador1' ou 'jogador2')
        }
    """
    players = get_random_players(2)
    if not players:
        return None
    
    jogador1, jogador2 = players
    
    # Sorteia uma estatística
    stat_key = random.choice(list(ESTATISTICAS.keys()))
    stat_nome = ESTATISTICAS[stat_key]
    
    valor1 = get_player_stat_value(jogador1, stat_key)
    valor2 = get_player_stat_value(jogador2, stat_key)
    
    # Se os valores forem iguais, tenta novamente (recursão limitada)
    if valor1 == valor2:
        # Tenta até 10 vezes encontrar uma combinação com valores diferentes
        for _ in range(10):
            players = get_random_players(2)
            if not players:
                return None
            jogador1, jogador2 = players
            valor1 = get_player_stat_value(jogador1, stat_key)
            valor2 = get_player_stat_value(jogador2, stat_key)
            if valor1 != valor2:
                break
        
        # Se ainda estiverem iguais, tenta outra estatística
        if valor1 == valor2:
            for stat in ESTATISTICAS.keys():
                if stat != stat_key:
                    stat_key = stat
                    stat_nome = ESTATISTICAS[stat_key]
                    valor1 = get_player_stat_value(jogador1, stat_key)
                    valor2 = get_player_stat_value(jogador2, stat_key)
                    if valor1 != valor2:
                        break
    
    # Determina a resposta correta
    if valor1 > valor2:
        resposta_correta = 'jogador1'
    elif valor2 > valor1:
        resposta_correta = 'jogador2'
    else:
        # Se ainda estiverem iguais, retorna None para indicar erro
        return None
    
    return {
        'jogador1': jogador1,
        'jogador2': jogador2,
        'stat_key': stat_key,
        'stat_nome': stat_nome,
        'valor1': valor1,
        'valor2': valor2,
        'resposta_correta': resposta_correta
    }


def check_answer(escolha, resposta_correta):
    """
    Verifica se a escolha do usuário está correta.
    
    Args:
        escolha (str): Escolha do usuário ('jogador1' ou 'jogador2')
        resposta_correta (str): Resposta correta ('jogador1' ou 'jogador2')
        
    Returns:
        bool: True se a resposta estiver correta, False caso contrário
    """
    return escolha == resposta_correta

