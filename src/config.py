"""
config.py - Este arquivo é responsável por carregar as variáveis de ambiente
e configurar a aplicação Flask, especialmente a conexão com o banco de dados.
Ele utiliza a biblioteca python-dotenv para carregar as variáveis de ambiente
definidas no arquivo .env, e define a classe Config que é usada para configurar a aplicação Flask.
"""

import os
from dotenv import load_dotenv
load_dotenv( interpolate= True )

# pylint: disable=too-few-public-methods
class Config:
    """
    A classe Config define a URI de conexão com o banco de dados MySQL
    usando as variáveis de ambiente,
    além de outras configurações como a chave secreta e
    o rastreamento de modificações do SQLAlchemy.
    """
    _user = os.getenv("DB_USER")
    _password = os.getenv("DB_PASSWORD")
    _host = os.getenv("DB_HOST")
    _port = os.getenv("DB_PORT", "3306")
    _db = os.getenv("DB_NAME")

    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{_user}:{_password}@{_host}:{_port}/{_db}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    print("DATABASE_URL:", SQLALCHEMY_DATABASE_URI)
