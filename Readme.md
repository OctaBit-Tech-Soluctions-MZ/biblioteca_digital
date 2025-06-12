# Biblioteca Virtual 📚

Projeto desenvolvido em Django para gerenciar uma biblioteca virtual, com controle de usuários e permissões por grupos.

## Funcionalidades

- Cadastro e autenticação de usuários (bibliotecários, docentes, estudantes)
- Upload e visualização de documentos
- Registo de cursos
- Registro de histórico de pedidos
- Sistema de permissões por grupo
- Painel de administração customizado

## Tecnologias

- Python 3.13
- Django 5.2
- Bootstrap 5
- SQLite / PostgreSQL/MySQL
- HTML + CSS + JS

## Como rodar localmente

1. Clone o repositório:

git clone https://github.com/seu-usuario/biblioteca-virtual.git](https://github.com/OctaBit-Tech-Soluctions-MZ/biblioteca_digital.git
cd biblioteca-virtual

## Crie e ative o ambiente virtual:

python -m venv venv
source venv/bin/activate  # no Windows: venv\Scripts\activate

## Instale as dependências:

pip install -r requirements.txt

## Execute as migrações:

python manage.py migrate

## Rode o servidor:

python manage.py runserver

Acesse http://127.0.0.1:8000/
