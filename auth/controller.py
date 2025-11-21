"""
Controller de Autenticação
Contém apenas as rotas e lógica de HTTP/Flask
Toda a lógica de negócio está em model.py
"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from auth.model import create_user, authenticate_user, get_user_by_id

auth_bp = Blueprint('auth', __name__, template_folder='../../templates')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Rota para login de usuário.
    GET: Exibe formulário de login
    POST: Processa login
    """
    if request.method == 'GET':
        # Se já estiver logado, redireciona para home
        if 'user_id' in session:
            return redirect(url_for('index'))
        return render_template('auth/login.html')
    
    # POST: Processa login
    data = request.get_json() if request.is_json else request.form
    nickname = data.get('nickname', '').strip()
    password = data.get('password', '')
    
    # Validação básica
    if not nickname or not password:
        if request.is_json:
            return jsonify({'success': False, 'message': 'Nickname e senha são obrigatórios!'}), 400
        flash('Nickname e senha são obrigatórios!', 'error')
        return render_template('auth/login.html')
    
    # Autentica usuário
    user = authenticate_user(nickname, password)
    
    if user:
        # Login bem-sucedido
        session['user_id'] = user.id
        session['user_nickname'] = user.nickname
        session.permanent = True
        
        if request.is_json:
            return jsonify({
                'success': True,
                'message': 'Login realizado com sucesso!',
                'user': {
                    'id': user.id,
                    'nickname': user.nickname
                }
            })
        
        flash('Login realizado com sucesso!', 'success')
        return redirect(url_for('index'))
    else:
        # Credenciais inválidas
        if request.is_json:
            return jsonify({'success': False, 'message': 'Nickname ou senha incorretos!'}), 401
        
        flash('Nickname ou senha incorretos!', 'error')
        return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Rota para registro de novo usuário.
    GET: Exibe formulário de registro
    POST: Processa registro
    """
    if request.method == 'GET':
        # Se já estiver logado, redireciona para home
        if 'user_id' in session:
            return redirect(url_for('index'))
        return render_template('auth/register.html')
    
    # POST: Processa registro
    data = request.get_json() if request.is_json else request.form
    nickname = data.get('nickname', '').strip()
    password = data.get('password', '')
    confirm_password = data.get('confirm_password', '')
    
    # Validação básica
    if not nickname or not password:
        if request.is_json:
            return jsonify({'success': False, 'message': 'Nickname e senha são obrigatórios!'}), 400
        flash('Nickname e senha são obrigatórios!', 'error')
        return render_template('auth/register.html')
    
    if len(nickname) < 3:
        if request.is_json:
            return jsonify({'success': False, 'message': 'Nickname deve ter pelo menos 3 caracteres!'}), 400
        flash('Nickname deve ter pelo menos 3 caracteres!', 'error')
        return render_template('auth/register.html')
    
    if len(password) < 6:
        if request.is_json:
            return jsonify({'success': False, 'message': 'Senha deve ter pelo menos 6 caracteres!'}), 400
        flash('Senha deve ter pelo menos 6 caracteres!', 'error')
        return render_template('auth/register.html')
    
    if password != confirm_password:
        if request.is_json:
            return jsonify({'success': False, 'message': 'As senhas não coincidem!'}), 400
        flash('As senhas não coincidem!', 'error')
        return render_template('auth/register.html')
    
    # Cria usuário
    user = create_user(nickname, password)
    
    if user:
        # Registro bem-sucedido - faz login automático
        session['user_id'] = user.id
        session['user_nickname'] = user.nickname
        session.permanent = True
        
        if request.is_json:
            return jsonify({
                'success': True,
                'message': 'Conta criada com sucesso!',
                'user': {
                    'id': user.id,
                    'nickname': user.nickname
                }
            }), 201
        
        flash('Conta criada com sucesso!', 'success')
        return redirect(url_for('index'))
    else:
        # Nickname já existe
        if request.is_json:
            return jsonify({'success': False, 'message': 'Este nickname já está em uso!'}), 409
        
        flash('Este nickname já está em uso!', 'error')
        return render_template('auth/register.html')


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    Rota para logout de usuário.
    """
    session.clear()
    
    if request.is_json:
        return jsonify({'success': True, 'message': 'Logout realizado com sucesso!'})
    
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('index'))


@auth_bp.route('/check-auth', methods=['GET'])
def check_auth():
    """
    Verifica se o usuário está autenticado.
    Retorna informações do usuário se logado.
    """
    if 'user_id' in session:
        user = get_user_by_id(session['user_id'])
        if user:
            return jsonify({
                'authenticated': True,
                'user': {
                    'id': user.id,
                    'nickname': user.nickname
                }
            })
    
    return jsonify({'authenticated': False})

