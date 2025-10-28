import sys
import os

# Adiciona o diretório raiz do projeto ao path
# Garante que 'app' e 'models' possam ser importados corretamente
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 1. Importar o Factory e o objeto db
from app import create_app
from extensions import db

# 2. Importar TODAS as classes Model
# É essencial que o SQLAlchemy "conheça" todas as classes antes de criar as tabelas
from models.Player import Player
from models.User import User
from models.HistoryGame import HistoryGame
from models.UserGame import UserGame 

def initialize_database():
    """
    Inicializa o banco de dados criando as tabelas
    a partir das classes Model, usando o Application Factory.
    """
    
    # Cria uma instância da aplicação (com a config padrão/desenvolvimento)
    app = create_app()
    
    # 3. Usa o contexto da aplicação Flask para rodar db.create_all()
    with app.app_context():
        # Você pode rodar db.drop_all() se precisar começar do zero
        # db.drop_all() 
        
        # Cria todas as tabelas no arquivo footmind.db
        db.create_all()
        print("✅ Banco de dados FootMind inicializado com sucesso!")
        print(f"Tabelas criadas: {', '.join(db.metadata.tables.keys())}")
        
        # Opcional: Adicionar lógica de preenchimento inicial aqui

if __name__ == '__main__':
    initialize_database()