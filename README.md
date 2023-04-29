# Como instalar a Recipes API
## Pré-requisitos
- [Python 3.11.2](https://www.python.org/downloads/release/python-385/)
- [Pip](https://pip.pypa.io/en/stable/installing/)
- [venv](https://docs.python.org/3/library/venv.html)

## Como instalar
1. Clone o repositório
2. Crie um ambiente virtual
    ```bash
    python3 -m venv venv
    ```

3. Ative o ambiente virtual
    - Windows
        ```bash
       source venv\Scripts\activate
        ```
    - Linux
        ```bash
        source venv/bin/activate
        ```
    - MacOS
        ```bash
        source venv/bin/activate
        ```
4. Instale as dependências
    ```bash
    pip install -r requirements.txt
    ```
    
5. Rode o main.py
    ```bash
    python main.py
    ```
6. Acesse a API em http://localhost:8000/


## Descrição do projeto
- A Recipes API é uma API que permite o cadastro de receitas, ingredientes e passos, além de permitir a busca de receitas por título.
- O projeto foi desenvolvido utilizando o framework [FastAPI](https://fastapi.tiangolo.com/). Ele permite a criação de documentação automática e interativa, além de ser fácil de usar e rápido.
- O banco de dados utilizado foi o [SQLite](https://www.sqlite.org/index.html), que é um banco de dados leve e rápido, ideal para projetos pequenos.
- O ORM utilizado foi o [SQLAlchemy](https://www.sqlalchemy.org/), que permite a criação de classes que representam tabelas do banco de dados, além de facilitar a criação de queries.
