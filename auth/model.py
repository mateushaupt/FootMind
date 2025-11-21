"""
Model de Autenticação
Contém funções para hash de senhas e verificação de credenciais
"""
from werkzeug.security import generate_password_hash, check_password_hash
from models.User import User
from models.UserGame import UserGame  # Import necessário para o relacionamento funcionar
from extensions import db


def hash_password(password):
    """
    Gera um hash seguro da senha usando werkzeug.
    
    Args:
        password (str): Senha em texto plano
        
    Returns:
        str: Hash da senha
    """
    return generate_password_hash(password)


def verify_password(password_hash, password):
    """
    Verifica se a senha corresponde ao hash.
    
    Args:
        password_hash (str): Hash armazenado no banco
        password (str): Senha em texto plano fornecida pelo usuário
        
    Returns:
        bool: True se a senha corresponde, False caso contrário
    """
    return check_password_hash(password_hash, password)


def create_user(nickname, password):
    """
    Cria um novo usuário no banco de dados.
    
    Args:
        nickname (str): Nome de usuário
        password (str): Senha em texto plano
        
    Returns:
        User: Objeto User criado ou None se o nickname já existe
    """
    # Verifica se o usuário já existe
    existing_user = User.query.filter_by(nickname=nickname).first()
    if existing_user:
        return None
    
    # Cria novo usuário
    hashed_password = hash_password(password)
    new_user = User(nickname=nickname, password=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return new_user


def authenticate_user(nickname, password):
    """
    Autentica um usuário verificando nickname e senha.
    
    Args:
        nickname (str): Nome de usuário
        password (str): Senha em texto plano
        
    Returns:
        User: Objeto User se autenticação bem-sucedida, None caso contrário
    """
    user = User.query.filter_by(nickname=nickname).first()
    
    if user and verify_password(user.password, password):
        return user
    
    return None


def get_user_by_id(user_id):
    """
    Busca um usuário pelo ID.
    
    Args:
        user_id (int): ID do usuário
        
    Returns:
        User: Objeto User ou None se não encontrado
    """
    return User.query.get(user_id)

