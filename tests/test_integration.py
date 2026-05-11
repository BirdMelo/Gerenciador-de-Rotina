"""
test_integration.py - Testes de integração entre a API de feriados e o sistema.
Verifica se a rota /task/feriados retorna os dados corretamente,
simulando a resposta da API externa com mock para garantir
que os testes sejam independentes de conectividade.
"""
from unittest.mock import patch, Mock
from src.models import User

FERIADOS_MOCK = [
    {
        "date": "2026-01-01",
        "name": "Confraternização Universal",
        "type": "feriado",
        "level": "nacional"
    },
    {
        "date": "2026-04-21",
        "name": "Tiradentes",
        "type": "feriado",
        "level": "nacional"
    },
    {
        "date": "2026-12-25",
        "name": "Natal",
        "type": "feriado",
        "level": "nacional"
    }
]

def test_feriados_retorna_lista(client, app):
    """
    Verifica se a rota /task/feriados retorna uma lista de feriados com sucesso
    """
    with app.app_context():
        from src.extentions import db # pylint: disable=import-outside-toplevel
        # Criar um usuário para autenticação
        user = User(name="Test User")
        db.session.add(user)
        db.session.commit()
        user_id = user.id
    with client.session_transaction() as sess:
        sess['user_id'] = user_id

    mock_response = Mock()
    mock_response.json.return_value = FERIADOS_MOCK
    with patch('src.blueprints.task.routes.http_request.get', return_value=mock_response):
        response = client.get('/task/feriados?year=2026')
    data = response.get_json()
    campos_esperados = {"date", "name", "type", "level"}
    for feriado in data:
        assert campos_esperados.issubset(feriado.keys())

def test_feriados_sem_login_retorna_401(client):
    """
    Verifica se a rota retorna 401 quando o usuário não está logado
    """
    response = client.get('/task/feriados?year=2026')
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data

def test_feriados_ano_parametro(client, app):
    """
    Verifica se o parâmetro 'year' é passado corretamente para a API externa
    """
    with app.app_context():
        from src.extentions import db # pylint: disable=import-outside-toplevel
        user = User(name= "Test User Ano")
        db.session.add(user)
        db.session.commit()
        user_id = user.id
    with client.session_transaction() as sess:
        sess['user_id'] = user_id
        mock_response = Mock()
        mock_response.json.return_value = FERIADOS_MOCK
    with patch('src.blueprints.task.routes.http_request.get',
               return_value=mock_response) as mock_get:
        client.get('/task/feriados?year=2026')
        args, _ = mock_get.call_args
        assert '2026' in args[0] # Verifica se o ano está presente na URL da requisição externa
