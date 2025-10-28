import os
from flask import Flask, render_template

# 1. Importar as configurações e o objeto de extensão (db)
from config import Config
from extensions import db

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
    
    # Registro do Blueprint do Jogo 1
    # O prefixo /jogadores/ significa que todas as rotas em game1_bp terão este prefixo
    # app.register_blueprint(game1_bp, url_prefix='/jogadores')
    
    # Registro de futuros jogos
    # app.register_blueprint(game2_bp, url_prefix='/times') 
    # app.register_blueprint(game3_bp, url_prefix='/grade') 

    # Rota Raiz (Página Inicial/Seleção de Jogos)
    # @app.route('/')
    # def index():
    #     # Você pode listar os jogos disponíveis aqui
    #     return render_template('index.html', games=[
    #         {'name': 'FootWordle (Jogadores)', 'url': '/jogadores'},
    #         # {'name': 'FootContext (Times)', 'url': '/times'},
    #         # {'name': 'FootGrade (Imaculado)', 'url': '/grade'},
    #     ])

    return app

# Se for rodar via 'python app.py' (mas flask run é o recomendado)
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)