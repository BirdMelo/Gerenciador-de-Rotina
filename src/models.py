#Modelos do banco de dados

from .extentions import db
from sqlalchemy.sql import func
from enum import Enum

class ActionsType(Enum):
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'

class User(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

class Task(db.Model):
    __tablename__ = 'rotina'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    startTime = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    deadLine = db.Column(db.DateTIme(timezone=True), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    # Foreign key para o usuário que criou a rotina
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('rotinas', lazy=True))

class Executions(db.Model):
    __tablename__ = 'execucoes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Foreign key para a rotina associada à execução
    rotina_id = db.Column(db.Integer, db.ForeignKey('rotina.id'), nullable=False)
    rotina = db.relationship('Rotina', backref=db.backref('execucoes', lazy=True))

    __table_args__ = (
        db.UniqueConstraint('rotina_id', 'date', name='uk_rotina_date_idx'),
    )

class HistoryActions(db.Model):
    __tablename__ = 'historico_acoes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    actionsType = db.Column(db.Enum(ActionsType), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    # Foreign key para o usuário que realizou a ação
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('historico_acoes', lazy=True))

    # Foreign key para a rotina associada à ação (pode ser nulo se a ação não estiver relacionada a uma rotina específica)
    rotina_id = db.Column(db.Integer, db.ForeignKey('rotina.id'), nullable=True)
    rotina = db.relationship('Rotina', backref=db.backref('historico_acoes', lazy=True))