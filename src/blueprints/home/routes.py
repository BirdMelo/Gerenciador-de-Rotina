"""
Módulo para execultar as rotas relacionadas à página inicial do aplicativo.
Contém a rota para a página inicial (home) do aplicativo,
que serve como ponto de entrada para os usuários.
A rota verifica se o usuário está logado e, se estiver, redireciona para a dashboard do usuário.
Caso contrário, renderiza a página de boas-vindas.
"""
from flask import render_template
from . import bp


@bp.route('/')
def index():
    """
    Rota para a página inicial do aplicativo. Verifica se o usuário está logado e,
    se estiver, redireciona para a dashboard do usuário.
    Caso contrário, renderiza a página de boas-vindas.
    """
    return render_template('home/home.html')
