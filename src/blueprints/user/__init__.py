"""
Módulo para gerenciar as rotas relacionadas às páginas de usuário do aplicativo.
Contém a lógica básica para renderizar
as rotas de criação, edição, exclusão de usuários,
página de login e logout de usuário e a página de dashboard do usuário.
"""
from flask import Blueprint
bp = Blueprint('user', __name__)
# pylint: disable=wrong-import-position
from . import routes
