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


def update_user_nickname(user_id, new_nickname):
    """
    Atualiza o nickname de um usuário.
    
    Args:
        user_id (int): ID do usuário
        new_nickname (str): Novo nickname
        
    Returns:
        tuple: (User, error_message) - User atualizado ou None e mensagem de erro
    """
    user = get_user_by_id(user_id)
    if not user:
        return None, 'Usuário não encontrado'
    
    new_nickname = new_nickname.strip()
    
    # Validação
    if not new_nickname:
        return None, 'Nickname não pode estar vazio'
    
    if len(new_nickname) < 3:
        return None, 'Nickname deve ter pelo menos 3 caracteres'
    
    # Verifica se o novo nickname já está em uso por outro usuário
    existing_user = User.query.filter_by(nickname=new_nickname).first()
    if existing_user and existing_user.id != user_id:
        return None, 'Este nickname já está em uso'
    
    # Atualiza o nickname
    user.nickname = new_nickname
    db.session.commit()
    
    return user, None


def update_user_password(user_id, current_password, new_password):
    """
    Atualiza a senha de um usuário.
    
    Args:
        user_id (int): ID do usuário
        current_password (str): Senha atual
        new_password (str): Nova senha
        
    Returns:
        tuple: (success, error_message) - True se sucesso, False e mensagem de erro caso contrário
    """
    user = get_user_by_id(user_id)
    if not user:
        return False, 'Usuário não encontrado'
    
    # Verifica a senha atual
    if not verify_password(user.password, current_password):
        return False, 'Senha atual incorreta'
    
    # Validação da nova senha
    if not new_password:
        return False, 'Nova senha não pode estar vazia'
    
    if len(new_password) < 6:
        return False, 'Nova senha deve ter pelo menos 6 caracteres'
    
    # Atualiza a senha
    user.password = hash_password(new_password)
    db.session.commit()
    
    return True, None

