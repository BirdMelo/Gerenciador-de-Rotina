"""
Módulo para gerenciar as rotas relacionadas às páginas de rotina do aplicativo.
Contém a lógica básica para renderizar
as rotas de criação, edição, exclusão e conclusão de rotinas.
"""
from flask import Blueprint
bp = Blueprint('task', __name__)
# pylint: disable=wrong-import-position
from .import routes
