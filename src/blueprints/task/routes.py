from datetime import datetime

from flask import session, redirect, render_template, url_for, request
from src.models import Task, HistoryActions, ActionsType, User
from src.extentions import db
from . import bp

#CREATE
@bp.route('/create', methods=['GET', 'POST'])
def create_task():
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    if request.method == "POST":
        user = User.query.get(session['user_id'])
        name = request.form.get('name')
        description = request.form.get('description')
        deadline = request.form.get('deadLine')

        user_id = session['user_id']
        deadline_date = None
        if deadline:
            # Converte a string de data para um objeto DateTime do Python
            deadline_date = datetime.strptime(deadline, '%Y-%m-%dT%H:%M')
        
        new_task = Task(
            name=name, 
            description=description, 
            deadLine=deadline_date, 
            user_id=user_id
        )
        db.session.add(new_task)
        db.session.flush()  # Garante que o ID da tarefa seja gerado antes de criar o histórico

        # Cria um registro de histórico para a criação da tarefa
        history_entry = HistoryActions(
            actionsType=ActionsType.CREATE,
            description=f'Task "{name}" created for user {user.name}.',
            user_id=user_id,
            rotina_id=new_task.id
        )
        db.session.add(history_entry)
        db.session.commit()
        return redirect(url_for('user.dashboard'))
    return render_template('task/register.html')

#UPDATE
@bp.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    task = Task.query.get_or_404(task_id)
    if request.method == "POST":
        user = User.query.get(session['user_id'])
        # Novos dados da tarefa
        new_name = request.form.get('name')
        new_description = request.form.get('description')
        new_deadline = request.form.get('deadLine')
        deadline_date = None
        if new_deadline:
            deadline_date = datetime.strptime(new_deadline, '%Y-%m-%dT%H:%M')
        
        # Atualiza os campos da tarefa
        task.name = new_name
        task.description = new_description
        task.deadLine = deadline_date
        db.session.add(task)
        db.session.commit()

        # Cria um registro de histórico para a atualização da tarefa
        history_entry = HistoryActions(
            actionsType=ActionsType.UPDATE,
            description=f'Task "{new_name}" updated for user {user.name}.',
            user_id=session['user_id'],
            rotina_id=task.id
        )

        db.session.add(history_entry)
        db.session.commit()
        return redirect(url_for('user.dashboard'))
    return render_template('task/edit.html', task=task)

#DELETE
@bp.route('/delete/<int:task_id>', methods=['POST', 'GET'])
def delete_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    user = User.query.get(session['user_id'])
    task = Task.query.get_or_404(task_id)
    task.is_active = False  # Marcar a tarefa como inativa em vez de deletar
    db.session.add(task)
    # Cria um registro de histórico para a exclusão da tarefa
    history_entry = HistoryActions(
        actionsType=ActionsType.DELETE,
        description=f'Task "{task.name}" deleted for user {user.name}.',
        user_id=session['user_id'],
        rotina_id=task.id
    )
    db.session.add(history_entry)
    db.session.commit()
    return redirect(url_for('user.dashboard'))