"""
models.py - Este arquivo define os modelos de dados para a aplicação Flask usando SQLAlchemy.
Ele inclui as classes User, Task, Executions e HistoryActions, que representam as tabelas
do banco de dados. Cada classe define os campos e relacionamentos necessários para a aplicação,
além de usar enums para tipos específicos como ActionsType e WeakDay.
"""
from enum import Enum
from sqlalchemy.sql import func
from .extentions import db

# pylint: disable=not-callable
# pylint: disable=too-few-public-methods

class ActionsType(Enum):
    """
    ActionsType é um enum que define
    os tipos de ações que podem ser registradas no histórico de ações.
    Ele inclui as ações de criação, atualização e exclusão.
    """
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'

class WeakDay(Enum):
    """
    WeakDay é um enum que define os dias da semana.
    Ele é usado para indicar em quais dias da semana uma tarefa deve ser executada.
    """
    SUNDAY = 'SUNDAY'
    MONDAY = 'MONDAY'
    TUESDAY = 'TUESDAY'
    WEDNESDAY = 'WEDNESDAY'
    THURSDAY = 'THURSDAY'
    FRIDAY = 'FRIDAY'
    SATURDAY = 'SATURDAY'

class User(db.Model):
    """
    User é um modelo que representa a tabela de usuários no banco de dados.
    Ele inclui campos para id, name, is_active e created_at, além de um relacionamento
    """
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

class Task(db.Model):
    """
    Task é um modelo que representa a tabela de tarefas (rotinas) no banco de dados.
    Ele inclui campos para id, name, description, startTime, endTime, weakday,
    is_active e created_at, além de um relacionamento com o modelo User para indicar
    """
    __tablename__ = 'rotina'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    startTime = db.Column(db.Time, nullable=False)
    endTime = db.Column(db.Time, nullable=False)
    weakday = db.Column(db.Enum(WeakDay), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    # Foreign key para o usuário que criou a rotina
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('rotinas', lazy=True))

class Executions(db.Model):
    """
    Executions é um modelo que representa a tabela de execuções de tarefas no banco de dados.
    Ele inclui campos para id, date, created_at, além de um relacionamento com o modelo
    Task para indicar a qual rotina a execução está associada.
    Ele também define uma restrição de unicidade para garantir
    que não haja mais de uma execução para a mesma rotina em um mesmo dia.
    """
    __tablename__ = 'execucoes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Foreign key para a rotina associada à execução
    rotina_id = db.Column(db.Integer, db.ForeignKey('rotina.id'), nullable=False)
    rotina = db.relationship('Task', backref=db.backref('execucoes', lazy=True))

    __table_args__ = (
        db.UniqueConstraint('rotina_id', 'date', name='uk_rotina_date_idx'),
    )

class HistoryActions(db.Model):
    """
    HistoryActions é um modelo que representa a tabela de histórico de ações no banco de dados.
    Ele inclui campos para id, actionsType, created_at, description, além de relacionamentos
    com os modelos User e Task para indicar
    o usuário que realizou a ação e a rotina associada à ação (se houver).
    Ele também define uma enum ActionsType para indicar
    o tipo de ação realizada (criação, atualização ou exclusão).
    """
    __tablename__ = 'historico_acoes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    actionsType = db.Column(db.Enum(ActionsType), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    # Foreign key para o usuário que realizou a ação
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('historico_acoes', lazy=True))

    # Foreign key para a rotina associada à ação
    # (pode ser nulo se a ação não estiver relacionada a uma rotina específica)
    rotina_id = db.Column(db.Integer, db.ForeignKey('rotina.id'), nullable=True)
    rotina = db.relationship('Task', backref=db.backref('historico_acoes', lazy=True))
