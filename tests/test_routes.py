"""
Esse modulo serve para testar automaticamente criações de rotinas no sistema
Testando a conectividade com o banco de dados
"""
from src.models import Task, User

def test_create_task_route_get(client):
    """Verifica se a página de criação de rotina carrega o formulário corretamente"""
    # Simulando um utilizador logado na sessão
    with client.session_transaction() as sess:
        sess['user_id'] = 1
    response = client.get('task/create')
    assert response.status_code == 200
    # Verifica se os elementos do seu register.html estão a ser renderizados
    assert b"Nome da Rotina*:" in response.data 
    assert b"Guardar Rotina" in response.data

def test_create_task_post_success(client, app):
    """Testa a criação de uma nova tarefa via POST usando os dados reais do HTML"""
    # 1. Criar um utilizador no banco de dados de teste
    with app.app_context():
        # pylint: disable=import-outside-toplevel
        from src.extentions import db
        user = User(name="Test User")
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    # 2. Simular login colocando o ID na sessão
    with client.session_transaction() as sess:
        sess['user_id'] = user_id

    # 3. Enviar os dados do formulário EXATAMENTE como o HTML envia
    data = {
        'name': 'Fazer Exercício',            # Corresponde ao input id="name"
        'description': 'Corrida no parque',   # Corresponde ao textarea id="description"
        'startTime': '07:00',                 # Corresponde ao input id="startTime"
        'endTime': '08:00',                   # Corresponde ao input id="endTime"
        'weakday': 'MONDAY'                   # Corresponde ao option value="MONDAY" do select
    }
    # Faz o POST para a rota
    response = client.post('task/create', data=data, follow_redirects=True)

    # 4. Verificações
    assert response.status_code == 200
    with app.app_context():
        # Verifica se a rotina foi realmente guardada na base de dados
        task = Task.query.filter_by(name='Fazer Exercício').first()
        assert task is not None
        assert task.user_id == user_id
        assert task.weakday.value == 'MONDAY'
