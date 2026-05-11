"""
config.py - Este arquivo é responsável por carregar as variáveis de ambiente
e configurar a aplicação Flask, separando os ambientes de Desenvolvimento (MySQL)
e Produção (PostgreSQL no Supabase).
"""

import os
from dotenv import load_dotenv
load_dotenv( interpolate= True )

# pylint: disable=too-few-public-methods
class Config:
    """
    Configurações bases compartilhadas entre todos os ambientes.
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    TOKEN_FERIADO = os.getenv("TOKEN_FERIADO")

class DevelopmentConfig(Config):
    """
    Configurações específicas para o ambiente de desenvolvimento.
    """
    _user = os.getenv("DB_USER")
    _password = os.getenv("DB_PASSWORD")
    _host = os.getenv("DB_HOST")
    _port = os.getenv("DB_PORT", "3306")
    _db = os.getenv("DB_NAME")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{_user}:{_password}@{_host}:{_port}/{_db}"

class ProductionConfig(Config):
    """
    Configurações específicas para o ambiente de produção.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    if(SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://")):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI or "sqlite:///:memory:"

config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
