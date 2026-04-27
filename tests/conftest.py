"""
Conftest.py é um arquivo de configuração para os testes do projeto.
Ele utiliza o framework pytest para criar fixtures que serão usadas nos testes.
A fixture "app" cria uma instância da aplicação Flask configurada para testes,
utilizando um banco de dados SQLite em memória.
A fixture "client" fornece um cliente de teste para fazer requisições
à aplicação durante os testes.
Essas fixtures garantem que cada teste seja executado em um ambiente isolado,
com um banco de dados limpo e sem interferências entre os testes.
"""

import sys
import os
import pytest
from src import create_app
from src.extentions import db

sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Desativa o aviso de redefinição de nome, pois o Pytest exige isso nas fixtures
# pylint: disable=redefined-outer-name

@pytest.fixture
def app():
    """
    Fornece uma instância da aplicação Flask configurada para testes.
    Ele utiliza um banco de dados SQLite em memória para garantir
    que os testes sejam executados em um ambiente isolado.
    A fixture cria o banco de dados, executa os testes e depois limpa o banco de
    dados para garantir que não haja interferências entre os testes.
    """
    config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    }
    app = create_app(config)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
@pytest.fixture
def client(app):
    """
    Fornce um cliente de teste para a aplicação Flask.
    Ele é usado para fazer requisições à aplicação durante os testes.
    """
    return app.test_client()
