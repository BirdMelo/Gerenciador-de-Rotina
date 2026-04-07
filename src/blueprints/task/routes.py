from flask import session, redirect, render_template, url_for, request
from src.models import Task, HistoryActions, ActionsType
from . import bp

@bp.route('/create', methods=['GET', 'POST'])
def create_task():
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    if request.method == "POST":
        task_name = request.form.get('name')
        login_user_id = session['user.id']