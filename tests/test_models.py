"""
Test_models.py é um arquivo de teste que contém testes para os modelos do projeto.
Ele utiliza o framework pytest para criar testes automatizados que verificam
a funcionalidade dos modelos de dados definidos em src/models.py.
Esses testes são essenciais para garantir
a integridade dos dados e o correto funcionamento da aplicação.
"""
from src.extentions import db
from src.models import User

def test_create_user(app):
    """
    O teste create_test_user verifica se um usuário pode ser criado e
    salvo corretamente no banco de dados,
    garantindo que os campos sejam preenchidos conforme esperado.
    """
    with app.app_context():
        new_user = User(name = "Bob")
        db.session.add(new_user)
        db.session.commit()

        salved_user = User.query.filter_by(name="Bob").first()
        assert salved_user is not None
        assert salved_user.name == "Bob"
        assert salved_user.id is not None
