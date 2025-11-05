"""
Model do FootWordle
Contém toda a lógica de negócio e acesso ao banco de dados relacionada ao jogo
"""
import random
from models.Player import Player
from extensions import db


def get_random_player():
    """
    Busca um jogador aleatório do banco de dados.
    
    Returns:
        Player: Objeto Player aleatório ou None se não houver jogadores
    """
    players = Player.query.all()
    if not players:
        return None
    return random.choice(players)


def get_player_by_name(name):
    """
    Busca um jogador pelo nome (case-insensitive).
    
    Args:
        name (str): Nome do jogador
        
    Returns:
        Player: Objeto Player ou None se não encontrado
    """
    return Player.query.filter(Player.name.ilike(name.strip())).first()


def get_player_name(player):
    """
    Retorna o nome do jogador em maiúsculas.
    
    Args:
        player: Objeto Player ou string
        
    Returns:
        str: Nome do jogador em maiúsculas
    """
    if isinstance(player, Player):
        return player.name.upper()
    return str(player).upper()


def check_guess(guess, answer):
    """
    Verifica o palpite do usuário comparando com a resposta.
    Retorna um array com as cores correspondentes a cada letra.
    
    Algoritmo seguindo o padrão Wordle:
    - Verde: letra correta na posição correta
    - Amarelo: letra existe na palavra mas em posição diferente
    - Cinza: letra não existe na palavra
    
    Args:
        guess (str): Palpite do usuário
        answer (str): Resposta correta
        
    Returns:
        list: Lista de dicionários com 'letter' e 'color' para cada letra
        Exemplo: [{'letter': 'M', 'color': 'green'}, {'letter': 'E', 'color': 'yellow'}, ...]
    """
    guess = guess.upper().strip()
    answer = answer.upper().strip()
    
    result = [None] * len(guess)  # Inicializa com None para cada posição
    answer_chars = list(answer)  # Lista mutável para rastrear letras usadas
    used_indices = set()  # Índices já marcados como verde
    
    # Primeira passagem: marca letras corretas na posição correta (verde)
    for i, letter in enumerate(guess):
        if i < len(answer) and letter == answer[i]:
            result[i] = {'letter': letter, 'color': 'green'}
            used_indices.add(i)
            answer_chars[i] = None  # Marca como usada
    
    # Segunda passagem: marca letras presentes mas em posição errada (amarelo)
    for i, letter in enumerate(guess):
        if result[i] is not None:
            continue  # Já foi marcado como verde
        
        # Verifica se a letra existe na resposta e não foi toda usada
        if letter in answer_chars:
            # Procura uma ocorrência disponível na resposta
            found = False
            for j, char in enumerate(answer):
                if char == letter and j not in used_indices and answer_chars[j] is not None:
                    result[i] = {'letter': letter, 'color': 'yellow'}
                    used_indices.add(j)
                    answer_chars[j] = None  # Marca como usada
                    found = True
                    break
            
            if not found:
                result[i] = {'letter': letter, 'color': 'gray'}
        else:
            result[i] = {'letter': letter, 'color': 'gray'}
    
    return result


def is_guess_correct(guess, answer):
    """
    Verifica se o palpite está completamente correto.
    
    Args:
        guess (str): Palpite do usuário
        answer (str): Resposta correta
        
    Returns:
        bool: True se o palpite estiver correto, False caso contrário
    """
    return guess.upper().strip() == answer.upper().strip()


def is_game_over(attempt, max_attempts, won):
    """
    Verifica se o jogo terminou.
    
    Args:
        attempt (int): Número da tentativa atual (0-indexed)
        max_attempts (int): Número máximo de tentativas
        won (bool): Se o jogador ganhou
        
    Returns:
        bool: True se o jogo terminou, False caso contrário
    """
    return won or attempt >= (max_attempts - 1)

