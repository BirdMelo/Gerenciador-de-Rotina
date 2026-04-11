"""
Esse arquivo é o ponto de entrada para a aplicação Flask.
Ele carrega as variáveis de ambiente, cria a aplicação e a executa.
"""
from dotenv import load_dotenv
from src import create_app

load_dotenv()


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)