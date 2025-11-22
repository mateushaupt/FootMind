import os
from flask import Flask, render_template
from games.gameWordle.controller import game_wordle_bp
from games.gameBingo.controller import game_bingo_bp
from games.gameDuel.controller import game_duel_bp
from auth.controller import auth_bp
from history.controller import history_bp

# 1. Importar as configurações e o objeto de extensão (db)
from config import Config
from extensions import db

# Importar todos os modelos para garantir que os relacionamentos funcionem
# Isso é necessário para que o SQLAlchemy possa resolver os relacionamentos
from models.User import User
from models.UserGame import UserGame
from models.Player import Player
from models.HistoryGame import HistoryGame

# 2. Importar os Blueprints (Controladores)
# Assumindo que você tem 3 jogos, vamos importar os Blueprints definidos nos __init__.py de cada pasta 'game'
# from games.gameWordle import bp as game_bp
# from games.game2_context import bp as game2_bp  # (Futuro)
# from games.game3_imaculado import bp as game3_bp # (Futuro)

def create_app(config_class=Config):
    """Factory de aplicação para criar a instância Flask."""
    app = Flask(__name__)
    
    # Carrega a configuração (Configuração do DB, SECRET_KEY, etc.)
    app.config.from_object(config_class)

    # ==========================================================
    # 3. Inicializar Extensões
    # ==========================================================
    db.init_app(app) # Associa o SQLAlchemy à instância 'app'

    # ==========================================================
    # 4. Registro de Blueprints (Rotas/Controladores)
    # ==========================================================
    
    # Registro do Blueprint de Autenticação
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Registro do Blueprint de Histórico e Ranking
    app.register_blueprint(history_bp, url_prefix='')
    
    # Registro do Blueprint do Jogo 1: FootWordle
    app.register_blueprint(game_wordle_bp, url_prefix='/game-wordle')
    
    # Registro do Blueprint do Jogo 2: Football Bingo
    app.register_blueprint(game_bingo_bp, url_prefix='/game-bingo')
    
    # Registro do Blueprint do Jogo 3: Game Duel
    app.register_blueprint(game_duel_bp, url_prefix='/game-duel')
    
    # Registro de futuros jogos
    # app.register_blueprint(game2_bp, url_prefix='/times') 
    # app.register_blueprint(game3_bp, url_prefix='/grade') 

    # ==========================================================
    # 5. Rotas Principais
    # ==========================================================
    
    @app.route('/')
    def index():
        """Página inicial com lista de jogos disponíveis."""
        return render_template('index.html')

    return app

# Se for rodar via 'python app.py' (mas flask run é o recomendado)
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
    

