"""
Controller do Game Duel
Contém apenas as rotas e lógica de HTTP/Flask
Toda a lógica de negócio está em model.py
"""
from flask import Blueprint, render_template, session, redirect, url_for
from games.gameDuel.model import prepare_round, check_answer, ESTATISTICAS
from history.model import (
    get_or_create_history_game,
    save_game_result,
    has_user_played_today,
    get_today_date_string
)
from models.HistoryGame import HistoryGame
from models.UserGame import UserGame
import hashlib

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
    Verifica se o usuário já jogou o jogo do dia.
    """
    # Para Duel, a configuração do dia é simples (apenas a data)
    # Todos jogam o mesmo jogo no mesmo dia
    today = get_today_date_string()
    config_data = {'date': today}
    
    # Verifica se o usuário já jogou hoje (se estiver logado)
    if 'user_id' in session:
        has_played, user_game = has_user_played_today(
            session['user_id'],
            'duel',
            config_data
        )
        
        if has_played:
            # Usuário já jogou - mostra resultado
            history_game = HistoryGame.query.get(user_game.gameId)
            return render_template(
                'games/game_result.html',
                game_type='duel',
                game_type_display='Game Duel',
                won=user_game.result == 1,
                date=history_game.dateCreated if history_game else today
            )
    
    # Inicializa o jogo se necessário
    if 'pontos' not in session:
        iniciar_jogo()
    
    # Verifica se o jogo terminou (derrota)
    if session.get('vidas', INITIAL_LIVES) <= 0:
        session['game_over'] = True
        pontos_obtidos = session.get('pontos', 0)
        # Salva resultado se o usuário estiver logado
        if 'user_id' in session and not session.get('duel_result_saved', False):
            try:
                save_game_result(
                    user_id=session['user_id'],
                    game_type='duel',
                    config_data=config_data,
                    won=False,
                    points=pontos_obtidos
                )
                session['duel_result_saved'] = True
                # Limpa a sessão do jogo
                session.pop('pontos', None)
                session.pop('vidas', None)
                session.pop('resposta_correta', None)
                session.pop('game_over', None)
                session.pop('vitoria', None)
            except Exception as e:
                print(f"Erro ao salvar histórico: {e}")
        
        # Se o usuário está logado, sempre verifica e mostra resultado
        if 'user_id' in session:
            has_played, user_game = has_user_played_today(
                session['user_id'],
                'duel',
                config_data
            )
            if has_played:
                history_game = HistoryGame.query.get(user_game.gameId)
                return render_template(
                    'games/game_result.html',
                    game_type='duel',
                    game_type_display='Game Duel',
                    won=False,
                    date=history_game.dateCreated if history_game else today,
                    points=pontos_obtidos
                )
        
        return render_template('games/game_duel.html')
    
    # Verifica se o jogador venceu
    if session.get('pontos', 0) >= MAX_POINTS:
        session['vitoria'] = True
        pontos_obtidos = session.get('pontos', 0)
        # Salva resultado se o usuário estiver logado
        if 'user_id' in session and not session.get('duel_result_saved', False):
            try:
                save_game_result(
                    user_id=session['user_id'],
                    game_type='duel',
                    config_data=config_data,
                    won=True,
                    points=pontos_obtidos
                )
                session['duel_result_saved'] = True
                # Limpa a sessão do jogo
                session.pop('pontos', None)
                session.pop('vidas', None)
                session.pop('resposta_correta', None)
                session.pop('game_over', None)
                session.pop('vitoria', None)
            except Exception as e:
                print(f"Erro ao salvar histórico: {e}")
        
        # Se o usuário está logado, sempre verifica e mostra resultado
        if 'user_id' in session:
            has_played, user_game = has_user_played_today(
                session['user_id'],
                'duel',
                config_data
            )
            if has_played:
                history_game = HistoryGame.query.get(user_game.gameId)
                return render_template(
                    'games/game_result.html',
                    game_type='duel',
                    game_type_display='Game Duel',
                    won=True,
                    date=history_game.dateCreated if history_game else today,
                    points=pontos_obtidos
                )
        
        return render_template('games/game_duel.html')
    
    # Verifica novamente se já jogou (pode ter mudado desde o início)
    # Isso garante que mesmo se o resultado foi salvo em outra requisição, ainda bloqueia
    if 'user_id' in session:
        has_played, user_game = has_user_played_today(
            session['user_id'],
            'duel',
            config_data
        )
        
        if has_played:
            # Usuário já jogou - mostra resultado
            history_game = HistoryGame.query.get(user_game.gameId)
            return render_template(
                'games/game_result.html',
                game_type='duel',
                game_type_display='Game Duel',
                won=user_game.result == 1,
                date=history_game.dateCreated if history_game else today
            )
    
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
    # Verifica se o usuário já jogou hoje (se estiver logado)
    if 'user_id' in session:
        today = get_today_date_string()
        config_data = {'date': today}
        has_played, _ = has_user_played_today(
            session['user_id'],
            'duel',
            config_data
        )
        if has_played:
            return redirect(url_for('game_duel.home'))
    
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
    # Não permite reiniciar se já jogou hoje
    if 'user_id' in session:
        today = get_today_date_string()
        config_data = {'date': today}
        has_played, _ = has_user_played_today(
            session['user_id'],
            'duel',
            config_data
        )
        if has_played:
            return redirect(url_for('game_duel.home'))
    
    iniciar_jogo()
    session.pop('duel_result_saved', None)
    return redirect(url_for('game_duel.home'))

