"""
Módulo para gerenciar as rotas relacionadas à página inicial do aplicativo.
Contém a lógica básica para renderizar a página de boas-vindas (home),
servindo como ponto de entrada e apresentação do sistema para os usuários.
"""

from flask import Blueprint
bp = Blueprint('home', __name__)
# pylint: disable=wrong-import-position
from . import routes
