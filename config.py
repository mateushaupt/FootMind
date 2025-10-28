import os
from datetime import timedelta

# Define o diretório base do projeto
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Chave Secreta para segurança (Sessões, CSRF, etc.)
    # ATENÇÃO: Use uma chave mais robusta em produção!
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua_chave_super_secreta_e_forte_aqui'

    # ==========================================================
    # Configuração do Banco de Dados (SQLAlchemy com SQLite)
    # ==========================================================
    
    # Define a URI do banco de dados SQLite
    # 'sqlite:///' + caminho completo do arquivo footmind.db
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database', 'footmind.db')
    
    # Desabilita o rastreamento de modificações do SQLAlchemy (boa prática e evita warnings)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configurações de Sessão (Opcional, mas recomendado)
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    
    # Configurações do ambiente de desenvolvimento
    FLASK_ENV = 'development'
    DEBUG = True


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    # No ambiente real, a chave secreta deve ser carregada de uma variável de ambiente segura
    # SECRET_KEY = os.environ.get('SECRET_KEY')