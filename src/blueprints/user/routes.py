"""
Módulo de rotas para o blueprint de usuário, contendo as operações CRUD e a dashboard do usuário.
As rotas implementam as seguintes funcionalidades:
- Registro de novos usuários (CREATE)
- Login de usuários existentes (READ)
- Atualização de informações do usuário (UPDATE)
- Desativação de usuários (DELETE)
- Dashboard do usuário para acessar suas rotinas e informações pessoais
"""
from flask import request, render_template, redirect, url_for, session, flash

from src.models import ActionsType, HistoryActions, User
from src.extentions import db
from . import bp

#CREATE
@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Rota para registrar um novo usuário. No método POST, recebe o nome do usuário,
    cria um novo registro na tabela de usuários e registra a ação de criação no histórico.
    No método GET, renderiza o formulário de registro.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.flush()  # Flush para obter o ID do novo usuário

        # Registrar a ação de criação do usuário
        action = HistoryActions(
            actionsType = ActionsType.CREATE,
            description = f'User {name} registered.',
            user_id = new_user.id
        )
        db.session.add(action)

        db.session.commit()
        return 'Registration successful!'
    return render_template('user/register.html')
#READ
@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Rota para login de usuários. No método POST, recebe o nome do usuário,
    verifica se ele existe e está ativo, e, se for o caso,
    armazena o ID do usuário na sessão para manter o estado
    de login. No método GET, renderiza o formulário de login.
    """
    if request.method == 'POST':
        nome_digitado = request.form.get('name')  
        # Verifica se o usuário existe e está ativo
        if not nome_digitado:
            flash('Por favor, insira um nome de usuário.', 'error')
            return redirect(url_for('user.login'))

        user = User.query.filter_by(name=nome_digitado).first()
        if user and user.is_active:
            session['user_id'] = user.id
            return redirect(url_for('user.dashboard'))
        elif user and not user.is_active:
            flash('Sua conta está desativada. Por favor, entre em contato com o suporte.', 'error')
            return redirect(url_for('user.login'))

        else:
            flash('Usuário não encontrado. Por favor, tente novamente.', 'error')
            return redirect(url_for('user.login'))
    return render_template('user/login.html')

#UPDATE
@bp.route('/update/<int:user_id>', methods=['POST', 'GET'])
def update_user(user_id):
    """
    Rota para atualizar as informações de um usuário. No método POST, recebe o novo nome do usuário,
    atualiza o registro do usuário no banco de dados e registra a ação de atualização no histórico.
    No método GET, renderiza o formulário de atualização com as informações atuais do usuário.
    """
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        new_name = request.form.get('name')

        # Verifica se o campo de nome foi preenchido
        if not new_name:
            flash('O nome do usuário não pode ser vazio.', 'error')
            return redirect(url_for('user.update_user', user_id=user_id))
        user.name = new_name
        action = HistoryActions(
            actionsType = ActionsType.UPDATE,
            description = f'User {user_id} updated name to {new_name}.',
            user_id = user.id
        )
        db.session.add(action)
        db.session.commit()
        return 'User updated successfully!'
    return render_template('user/update.html', user=user)

#DELETE
@bp.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """
    Rota para desativar um usuário. Recebe o ID do usuário,
    marca o usuário como inativo no banco de dados
    e registra a ação de desativação no histórico.
    O usuário desativado não poderá mais fazer login,
    mas seus dados permanecerão no banco para fins de histórico e auditoria.
    """
    user = User.query.get_or_404(user_id)
    user.is_active = False  # Marcar o usuário como inativo em vez de deletar
    action = HistoryActions(
        actionsType = ActionsType.DELETE,
        description = f'User {user_id} marked as inactive.',
        user_id = user.id
    )
    db.session.add(action)
    db.session.commit()
    return f"Usuário {user.name} desativado com sucesso! Ele não pode mais fazer login."

# ESPAÇO DO USUÁRIO (DASHBOARD)

@bp.route('/dashboard')
def dashboard():
    """
    Rota para a dashboard do usuário, onde ele pode acessar suas rotinas e informações pessoais.
    Verifica se o usuário está logado (presença do ID do usuário na sessão) e, se estiver,
    busca as informações do usuário no banco de dados para renderizar a dashboard.
    Se o usuário não estiver logado, redireciona para a página de login.
    """
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    user = User.query.get_or_404(session['user_id'])
    return render_template('user/dashboard.html', user=user, rotinas=user.rotinas)

@bp.route('/logout')
def logout():
    """
    Rota para logout do usuário. Remove o ID do usuário da sessão do navegador,
    efetivamente encerrando a sessão de login,
    e redireciona o usuário de volta para a página inicial.
    """
    # Remove o ID do usuário da sessão do navegador
    session.pop('user_id', None)
    # Redireciona ele de volta para a página inicial
    return redirect(url_for('home.index'))
