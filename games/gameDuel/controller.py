"""
Controller do Game Duel
Contém apenas as rotas e lógica de HTTP/Flask
Toda a lógica de negócio está em model.py
"""
from flask import Blueprint, render_template, session, redirect, url_for
from games.gameDuel.model import prepare_round, check_answer, ESTATISTICAS

game_duel_bp = Blueprint(
    'game_duel',
    __name__,
    template_folder='../../templates/games'
)

# Configurações do jogo
MAX_POINTS = 20
INITIAL_LIVES = 3


def iniciar_jogo():
    """Reinicia o estado do jogo na sessão."""
    session['vidas'] = INITIAL_LIVES
    session['pontos'] = 0
    session['game_over'] = False
    session['vitoria'] = False


@game_duel_bp.route('/')
def home():
    """
    Rota principal do jogo Game Duel.
    Inicializa o jogo ou prepara uma nova rodada.
    """
    # Inicializa o jogo se necessário
    if 'pontos' not in session:
        iniciar_jogo()
    
    # Verifica se o jogo terminou
    if session.get('vidas', INITIAL_LIVES) <= 0:
        session['game_over'] = True
        return render_template('games/game_duel.html')
    
    # Verifica se o jogador venceu
    if session.get('pontos', 0) >= MAX_POINTS:
        session['vitoria'] = True
        return render_template('games/game_duel.html')
    
    # Prepara uma nova rodada
    dados_rodada = prepare_round()
    
    if not dados_rodada:
        return render_template(
            'games/game_duel.html',
            error="Não há jogadores suficientes no banco de dados ou não há estatísticas disponíveis."
        )
    
    # Armazena a resposta correta na sessão
    session['resposta_correta'] = dados_rodada['resposta_correta']
    
    # Prepara os dados para o template
    return render_template(
        'games/game_duel.html',
        jogador1=dados_rodada['jogador1'],
        jogador2=dados_rodada['jogador2'],
        stat_nome=dados_rodada['stat_nome']
    )


@game_duel_bp.route('/checar/<escolha>')
def checar_resposta(escolha):
    """
    Verifica se a escolha do usuário está correta.
    
    Args:
        escolha (str): 'jogador1' ou 'jogador2'
    """
    # Verifica se o jogo está ativo
    if session.get('game_over', False) or session.get('vitoria', False):
        return redirect(url_for('game_duel.home'))
    
    # Verifica se há uma resposta correta na sessão
    resposta_correta = session.get('resposta_correta')
    if not resposta_correta:
        return redirect(url_for('game_duel.home'))
    
    # Valida a escolha
    if escolha not in ['jogador1', 'jogador2']:
        return redirect(url_for('game_duel.home'))
    
    # Verifica se a resposta está correta
    if check_answer(escolha, resposta_correta):
        session['pontos'] = session.get('pontos', 0) + 1
    else:
        session['vidas'] = session.get('vidas', INITIAL_LIVES) - 1
    
    # Limpa a resposta da sessão para preparar próxima rodada
    session.pop('resposta_correta', None)
    
    return redirect(url_for('game_duel.home'))


@game_duel_bp.route('/reiniciar')
def reiniciar():
    """Rota para reiniciar o jogo."""
    iniciar_jogo()
    return redirect(url_for('game_duel.home'))

