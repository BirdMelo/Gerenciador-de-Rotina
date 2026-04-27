# Sistema de Gerenciamento de Rotinas Pessoais

## Descrição do Sistema

### Problema real
Na sociedade atual, o excesso de informações e de responsabilidades diárias torna extremamente difícil manter a consistência em hábitos e metas de longo prazo (como rotinas de estudo, leitura ou exercícios físicos). Para tentar se organizar, as pessoas costumam depender apenas da memória, de alarmes soltos no celular ou de anotações desestruturadas em papel.

Isso gera três consequências graves:

* **Sobrecarga Cognitiva**: O estresse e a ansiedade constantes de ter que se lembrar ativamente de tudo o que precisa ser feito no dia.

* **Falta de Visibilidade**: Sem um histórico registrado, o indivíduo perde a noção do próprio progresso (não sabe se estudou 2 ou 5 vezes na semana passada).

### Proposta
Este projeto consiste em uma aplicação backend desenvolvida para o gerenciamento de rotinas pessoais. O sistema permite que os usuários se cadastrem na plataforma e registrem suas atividades recorrentes diárias, como momentos de estudo, práticas de exercícios físicos, entre outras. 
### Funcionalidades
A aplicação oferece as seguintes funcionalidades principais:
* **Gestão de Rotinas:** Criação, listagem e alternância de status (ativação e desativação) das rotinas cadastradas.
* **Registro de Execução:** Acompanhamento e registro diário da execução de cada rotina do usuário.
* **Trilha de Auditoria (Logs):** Registro de todas as ações relevantes realizadas no sistema, incluindo a criação de novas rotinas, marcação de execuções e alterações de status das atividades.

O foco central da aplicação é garantir a consistência dos dados do usuário por meio de validações rigorosas que controlam o estado atual das rotinas e a frequência de seus registros diários.

### Tecnologias utilizadas

#### Backend & Framework

* **Python (3.8+)**: Linguagem de programação pricipal do projeto;
* **Flask**: Microframework web utilizado para construir a aplicação, gerenciar as rotas e a lógica do servidor;
* **JinJa2 & Werkzeug**: Motores base do Flask utilizados para renderizar as páginas HTML de forma dinâmica.

#### Banco de Dados & ORM
* **MySQL**: Banco de dados relacional principal da aplicação;
* **PyMySQL**: Driver de conexão que permite o Python se comunicar com o MySQL;
* **Flask-SQLAlchemy**: Ferramenta de ORM (Object-Relational Mapping) para interagir com o banco de dados usando código Python em vez de comandos SQL puros;
* **Flask-Migrate/Alembic**: Gerenciadores de migração para manter o histórico de alterações das tabelas do banco de dados;
* **SQLite**: Utilizado em memória (`:memory:`) exclusivamente para rodar os testes automatizados.

#### Segurança & Configuração
* **Cryptography**: Biblioteca de segurança utilizada para gerar os hashes e proteger as senhas dos usuários;
* **Python-detenv**: Gerenciador de variáveis de ambiente para esconder dados sensíveis (como senhas do banco de dados) no arquivo `.env`.

#### Qualidade de Código & Testes
* **Pylint**: Ferramentas de análise estática (Linter) para garantir que o código siga as boas práticas e o padrão internacional PEP 8;
* **Pytest**: Framework utilizado para a criação e execução dos testes automatizados (Testes de Unidade e Integração).

#### DevOps & Infraestrutura
* **Github Action**: Plataforma de CI/CD configurada para rodar a esteira de Integração Contínua (instalação, linting e testes) a cada novo push ou pull request;
* **Setuptools & Pip**: Ferramentas de empacotamento e gerenciamento de dependências (`pyproject.toml` e `requirements.txt`).

#### Frontend
* **HTML/CSS**: Estruturação e estilização das telas do sistema, [/templates](/src/templates/) e [/static](/src/static/)

## Explicação das Tabelas

O banco de dados (`db_rotinas`) foi modelado de forma relacional e simples, composto por 4 tabelas principais:

* **usuario:** Armazena os dados básicos de quem usa o sistema (`idusuario`, `nome`, `criado_em`). Como é um sistema simplificado, não exige senha.
* **rotina:** Guarda as atividades criadas pelo usuário. Possui um vínculo direto com o criador (`usuario_idusuario`), o nome da atividade e um indicador (`ativa`) para saber se a rotina está em andamento ou pausada.
* **execucoes:** Registra cada vez que uma rotina é concluída no dia. Vincula-se à rotina executada (`rotina_idrotina`) e guarda a data exata da execução (`data_execucao`). 
* **historico_acoes:** Tabela de log e auditoria. Salva o histórico de eventos importantes (`tipo_acao`), vinculando a ação ao usuário e à rotina correspondente, além do momento exato do ocorrido.

arquivo para montagem do banco de dados no **`MySQL`** foi disponibilizado [aqui](/document/dbScripts/db_create.sql).

### Modelo conceitual de Banco de Dados

para a visualização do modelo conceitual na IDE VS Code, é recomendado baixar a extenção **`Markdown Preview Mermaid Support`**

```mermaid
erDiagram
    USUARIO ||--o{ ROTINA : "cadastra"
    USUARIO ||--o{ HISTORICO_ACOES : "realiza"
    ROTINA ||--o{ EXECUCOES : "possui"
    ROTINA ||--o{ HISTORICO_ACOES : "gera"

    USUARIO {
        int id PK
        string name UK
        timestamp created_at
        boolean is_active
    }

    ROTINA {
        int id PK
        string name
        string description
        time startTime
        time endTime
        enum weakday
        boolean is_active
        int user_id FK
    }

    EXECUCOES {
        int id PK
        date date
        int rotina_id FK
    }

    HISTORICO_ACOES {
        int id PK
        enum actionsType
        string description
        timestamp created_at
        int user_id FK
        int rotina_id FK
    }
```

## Lista de Rotas
* **home (/)**: página inicial para registrar usuário ou fazer login
### Usuário
* **register (/user/register)**: página para fazer cadastro do usuário
* **login (/user/login)**: página pra entrar com uma conta já existente
* **update (/user/update)**: página para alterar os dados do usuário
* **delete (/user/delete/{int:user_id})**: página para deletar o usuário
* **dashboard (/user/dashboard/{int:user_id})**: página para gerenciamento de informações e rotinas do usuário
### Rotina
* **create (/task/create)**: página para fazer cadastro da rotina
* **update (/task/update)**: página para editar a rotina
* **delete (/task/delete/{int:task_id})**: página para deletar rotina
## Explicação das Regras de Negócio

O sistema foi desenhado para garantir a consistência no acompanhamento das rotinas e manter um registro confiável de auditoria. As principais regras de negócio implementadas são:

1. **Unicidade de Execução Diária:** * Uma rotina só pode ser registrada como "concluída" ou "executada" uma única vez por dia.
   * O banco de dados garante essa integridade através de uma restrição única (`UniqueConstraint`) cruzando o ID da rotina e a data da execução. Tentativas de registrar a mesma rotina duas vezes no mesmo dia serão bloqueadas.

2. **Validação de Status da Rotina (Ativa/Inativa):**
   * Apenas rotinas com o status "ativo" (`is_active = True`) podem receber novos registros de execução.
   * Rotinas desativadas ou pausadas servem apenas para consulta de histórico, evitando inconsistências nos dados de progresso atual do usuário.

3. **Auditoria Contínua (Trilha de Logs):**
   * Nenhuma alteração crítica pode passar despercebida. Todas as ações do tipo `CREATE` (Criação), `UPDATE` (Atualização) e `DELETE` (Remoção) realizadas no sistema devem obrigatoriamente gerar um registro imutável na tabela `historico_acoes`.
   * Esse registro guarda o autor da ação, qual rotina foi afetada (se aplicável), a descrição do evento e o carimbo exato de data e hora (`created_at`).

4. **Integridade Relacional (Exclusão Segura):**
   * Para evitar registros "órfãos" no banco de dados, a exclusão de um usuário não pode ser feita de forma arbitrária.
   * Ao deletar um usuário, o sistema deve garantir que o histórico de ações atrelado a ele seja devidamente tratado ou limpo primeiro, respeitando as chaves estrangeiras (Foreign Keys).
## Issue de feriados
Atualização da aplicação para ter uma API que fornece todos os feriados e pontos facutativos do Brasil, utilizando a api [invertexto](https://api.invertexto.com/).
A API fornece os dias e nomes dos feriados/facutativos que serão utilizados para mudar a aparência do dia para indicar que é um dia com feriado.
## Instruções para Execução do Projeto
### Preparação de Ambiente
Para a preparação do ambiente, copie os códigos abaixo no terminal da IDE:
```
python -m venv venv_desenvolvimento
```
```
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```
```
.\venv_desenvolvimento\Scripts\activate
```


### Criação do arquivo `.env`
É necessario a criação de um arquivo `.env` para configuração do banco de dados.
Crie uma um arquivo com o nome `.env` e coloquei as seguintes variáveis:
* DB_USER = {nome_do_perfil_do_usuário}
* DB_PASSWORD = {senha_de_acesso}
* DB_HOST = localhost
* DB_PORT = 3306 (ou outra porta configurada)
* DB_NAME = {nome_do_db}
* SECRET_KEY = {chave_secreta}

### Bibliotecas a serem baixadas
As bibliotecas que serão baixadas no projeto estarão disponíveis no arquivo [requirement.txt](/requirements.txt)

Copie o codigo abaixo no terminal, dentro do ambiente `(venv_desenvolvimento)`:
```
pip install -r requirements.txt
```
### Execução do programa
Para executar o programa só precisa clicar no botão de **run** no arquivo [run.py](/run.py)

Ou executar no terminal, dentro do ambiente `(venv_desenvolvimento)` o comando abaixo:
```
python run.py
```
---
**Versão Atual**: 2.1.2

**Autores**: João Pedro de Melo Naves, Vítor Camargo

**Link do Repositório**: [Sistema de Gerenciamento de Rotinas Pessoais](https://github.com/BirdMelo/CEUB-DevWeb-Avaliacao)