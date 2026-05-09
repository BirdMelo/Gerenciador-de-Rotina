"""
Esse arquivo é o ponto de entrada para a aplicação Flask.
Ele carrega as variáveis de ambiente, cria a aplicação e a executa.
"""
import locale
from dotenv import load_dotenv
from src import create_app

try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') #Linux/Mac
except locale.Error:
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252') #Windowns

load_dotenv()


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
