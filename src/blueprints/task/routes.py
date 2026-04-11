"""
Define as rotas para o gerenciamento de rotinas.
Contém a lógica de requisição e resposta (GET, POST) para
criar, excluir e marcar rotina como concluída,
além de registrar as ações no histórico.
Conectando o banco de dados às páginas HTML
para permitir a interação do usuário com suas rotinas.
"""
from datetime import datetime, date

from flask import session, redirect, render_template, url_for, request, flash
from sqlalchemy.exc import SQLAlchemyError
from src.models import Task, HistoryActions, ActionsType, User, Executions
from src.extentions import db
from . import bp

#CREATE
@bp.route('/create', methods=['GET', 'POST'])
def create_task():
    """
    Rota para criar uma nova rotina. No método POST, recebe os dados da rotina,
    valida os campos obrigatórios, cria um novo registro na tabela de rotinas e
    registra a ação de criação no histórico.
    No método GET, renderiza o formulário de criação de rotina.
    """
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    if request.method == "POST":
        user = User.query.get(session['user_id'])
        name = request.form.get('name')
        description = request.form.get('description')
        endtime = request.form.get('endTime')
        start_time: str | None = request.form.get('startTime')
        weakday = request.form.get('weakday')

        # Verifica se os campos obrigatórios estão preenchidos
        if not name or not endtime or not start_time or not weakday:
            flash('Precisa preencher todos os campos obrigatórios.', 'error')
            return redirect(url_for('task.create_task'))

        user_id = session['user_id']
        endtime_date = None
        if endtime:
            # Converte a string de data para um objeto DateTime do Python
            endtime_date = datetime.strptime(endtime, '%H:%M').time()
        start_time_date = None
        if start_time:
            # Converte a string de data para um objeto DateTime do Python
            start_time_date = datetime.strptime(start_time, '%H:%M').time()
        new_task = Task(
            name=name,
            description=description,
            endTime=endtime_date,
            startTime=start_time_date,
            weakday=weakday,
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
    """
    Rota para atualizar uma rotina existente. No método POST, recebe os novos dados da rotina,
    valida os campos obrigatórios, atualiza o registro da rotina no banco de dados e
    registra a ação de atualização no histórico. No método GET, renderiza o formulário de edição
    com as informações atuais da rotina para que o usuário possa editá-las.
    """
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    task = Task.query.get_or_404(task_id)
    if request.method == "POST":
        user = User.query.get(session['user_id'])
        # Novos dados da tarefa
        new_name = request.form.get('name')
        new_description = request.form.get('description')
        new_end_time = request.form.get('endTime')
        new_start_time = request.form.get('startTime')
        new_weakday = request.form.get('weakday')

        # Verifica se os campos obrigatórios estão preenchidos
        if not new_name or not new_end_time or not new_start_time or not new_weakday:
            flash('Precisa preencher todos os campos obrigatórios.', 'error')
            return redirect(url_for('task.update_task', task_id=task_id))

        end_time_date = None
        if new_end_time:
            end_time_date = datetime.strptime(new_end_time, '%H:%M').time()
        start_time_date = None
        if new_start_time:
            start_time_date = datetime.strptime(new_start_time, '%H:%M').time()

        # Atualiza os campos da tarefa
        task.name = new_name
        task.description = new_description
        task.endTime = end_time_date
        task.startTime = start_time_date
        task.weakday = new_weakday
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
    """
    Rota para excluir uma rotina.
    Recebe o ID da rotina, marca a rotina como inativa no banco de dados
    e registra a ação de exclusão no histórico.
    A rotina marcada como inativa não será exibida na dashboard do usuário,
    mas seus dados permanecerão no banco para fins de histórico e auditoria.
    """
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

#CONCLUIR
@bp.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    """
    Rota para marcar uma rotina como concluída.
    Recebe o ID da rotina, verifica se a rotina está ativa
    e se já foi concluída no dia atual.
    Se a rotina estiver ativa e ainda não tiver sido concluída hoje,
    cria um novo registro na tabela de execuções para marcar a rotina como concluída
    """
    if 'user_id' not in session:
        return redirect(url_for('user.dashboard'))
    task = Task.query.get_or_404(task_id)
    user_id = task.user_id
    user = User.query.get(user_id)

    if not task.is_active:
        flash('Não é possível concluir uma tarefa inativa.', 'error')
        return redirect(url_for('user.dashboard'))
    today = date.today()
    execution_conflict = Executions.query.filter_by(rotina_id=task_id, date=today).first()
    if execution_conflict:
        flash('Esta tarefa já foi concluída hoje.', 'error')
        return redirect(url_for('user.dashboard'))
    try:
        new_execution = Executions(rotina_id=task_id, date=today)
        db.session.add(new_execution)
        action = HistoryActions(
            actionsType=ActionsType.UPDATE,
            description=f'Task "{task.name}" marked as completed for user {user.name}.',
            user_id=user.id,
            rotina_id=task.id
        )
        db.session.add(action)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        flash('Ocorreu um erro ao concluir a tarefa. Tente novamente.', 'error')
        return redirect(url_for('user.dashboard'))
    return redirect(url_for('user.dashboard'))
