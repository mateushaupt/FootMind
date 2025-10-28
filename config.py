import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # A URL para o SQLAlchemy usar o SQLite
    # 'sqlite:///' + caminho completo do arquivo
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database', 'footmind.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Boa prática para evitar warnings