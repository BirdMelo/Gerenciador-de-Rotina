from flask import request, render_template, redirect, url_for, session

from src.models import ActionsType, HistoryActions, User
from src.extentions import db
from . import bp

#CREATE
@bp.route('/register', methods=['GET', 'POST'])
def register():
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
    if request.method == 'POST':
        nome_digitado = request.form.get('name')
        user = User.query.filter_by(name=nome_digitado).first()
        if user and user.is_active:
            session['user_id'] = user.id
            return redirect(url_for('user.dashboard'))
        elif user and not user.is_active:
            
            return 'Esse usuário está inativo. Por favor, entre em contato com o suporte.'
        else:
            return 'Usuário não encontrado. Por favor, verifique o nome e tente novamente.'
    return render_template('user/login.html')

#UPDATE
@bp.route('/update/<int:user_id>', methods=['POST', 'GET']) #Permitir GET para facilitar testes, mas será modificado para só POST updates futuros
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        new_name = request.form.get('name')
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
@bp.route('/delete/<int:user_id>', methods=['POST', 'GET']) #Permitir GET para facilitar testes, mas será modificado para só POST updates futuros
def delete_user(user_id):
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
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    user = User.query.get_or_404(session['user_id'])
    return render_template('user/dashboard.html', user=user, rotinas=user.rotinas)

@bp.route('/logout')
def logout():
    # Remove o ID do usuário da sessão do navegador
    session.pop('user_id', None)
    
    # Redireciona ele de volta para a página inicial
    return redirect(url_for('home.index'))