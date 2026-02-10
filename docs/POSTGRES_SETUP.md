# Guia de Configuração do PostgreSQL para Projetos Flask + SQLAlchemy

Este guia mostra, passo a passo, como instalar, configurar e integrar o PostgreSQL a projetos Flask com SQLAlchemy, usando variáveis de ambiente (.env) e boas práticas de segurança.

## 1. Pré-requisitos

- Windows com PostgreSQL 18+ e pgAdmin 4 instalados
- Python 3.x e virtualenv (venv)
- Projeto Flask com SQLAlchemy e dotenv

Dependências mínimas (requirements.txt):

```
Flask
Flask-SQLAlchemy
python-dotenv
psycopg2-binary
```

## 2. Instalação e porta do servidor

- Instale o PostgreSQL normalmente pelo instalador oficial.
- Opcional: use uma porta diferente da padrão (5432), como 5433.
- Iniciar/Parar no Windows (PowerShell):

```
"C:\Program Files\PostgreSQL\18\bin\pg_ctl.exe" -D "D:/_projetos/postgres-data" start -o "-p 5433"
"C:\Program Files\PostgreSQL\18\bin\pg_ctl.exe" -D "D:/_projetos/postgres-data" stop -m fast
```

## 3. Recuperar/Definir senha do usuário postgres (se necessário)

Se esqueceu a senha, altere temporariamente o `pg_hba.conf` para `trust`, defina uma nova senha e volte para `md5`:

1) Pare o servidor.
2) Edite `pg_hba.conf` e substitua `md5` por `trust` nas entradas locais (local/host).
3) Inicie o servidor.
4) No `psql`, defina a nova senha:

```
"C:\Program Files\PostgreSQL\18\bin\psql.exe" -p 5433 -U postgres
ALTER USER postgres WITH PASSWORD 'NovaSenhaForte!';
```

5) Volte o `pg_hba.conf` para `md5` e reinicie o servidor.

## 4. Criar usuário e banco da aplicação
 
 O ideal é ter um usuário próprio do app (sem superprivilégios) e um banco pertencente a esse usuário.
 
 ### 4.1 Via pgAdmin (GUI)
 
 1) Conecte como `postgres` (ou outro admin) no servidor.
 2) Crie o usuário (Login Role):
    - Menu: Object → Create → Login/Group Role
    - Aba General: Name = devuser
    - Aba Definition: Password = SenhaForte123!
    - Aba Privileges: marque LOGIN
    - Save
 3) Crie o database do app:
    - Menu: Object → Create → Database
    - Database: meuapp
    - Owner: devuser
    - Save
 
 ### 4.2 Via CLI (PowerShell no Windows)
 
 ```
 "C:\Program Files\PostgreSQL\18\bin\psql.exe" -p 5433 -U postgres -c "CREATE ROLE devuser LOGIN PASSWORD 'SenhaForte123!';"
 "C:\Program Files\PostgreSQL\18\bin\psql.exe" -p 5433 -U postgres -c "CREATE DATABASE meuapp OWNER devuser;"
 ```
 
 ### 4.3 Testar login do usuário da aplicação
 
 ```
 "C:\Program Files\PostgreSQL\18\bin\psql.exe" -p 5433 -U devuser -d meuapp -c "\dt"
 ```
 
 Se listar tabelas (ou “No relations found” em banco vazio), o login está OK.

## 5. Conceder privilégios no schema public

Se as tabelas foram criadas por outro usuário (ex.: postgres), conceda privilégios ao usuário do app e defina privilégios padrão:

```
"C:\Program Files\PostgreSQL\18\bin\psql.exe" -p 5433 -U postgres -d meuapp -c "GRANT USAGE ON SCHEMA public TO devuser;"
"C:\Program Files\PostgreSQL\18\bin\psql.exe" -p 5433 -U postgres -d meuapp -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO devuser;"
"C:\Program Files\PostgreSQL\18\bin\psql.exe" -p 5433 -U postgres -d meuapp -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO devuser;"

"C:\Program Files\PostgreSQL\18\bin\psql.exe" -p 5433 -U postgres -d meuapp -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO devuser;"
"C:\Program Files\PostgreSQL\18\bin\psql.exe" -p 5433 -U postgres -d meuapp -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO devuser;"
```

## 6. Configurar variáveis de ambiente (.env)

No arquivo `.env` do projeto, defina a URL de conexão do SQLAlchemy:

```
SECRET_KEY=uma_secret_key_segura
DATABASE_URL=postgresql+psycopg2://devuser:SenhaForte123!@localhost:5433/meuapp
```

- Se usar a porta padrão, troque `5433` por `5432`.
- Nunca versionar senhas; use `.env` e mantenha fora do repositório público.

## 7. Criar e ativar o ambiente virtual

```
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
```

Inclua no `requirements.txt` outras dependências que seu projeto precise (ex.: Flask-Caching, reportlab, etc).

## 8. Integrar no app Flask (SQLAlchemy)

Exemplo de configuração no seu `app.py`:

```
from dotenv import load_dotenv
load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()
```

## 9. Criar as tabelas e validar

- Inicie o app: `python app.py`
- A primeira execução com `db.create_all()` cria as tabelas baseadas nos modelos (`db.Model`).
- Verifique no pgAdmin: `Servers → Databases → meuapp → Schemas → public → Tables`.

## 10. Erros comuns e soluções rápidas

- Timeout ao conectar (pgAdmin tenta 5432): verifique a porta (`5433` vs `5432`) e o `postgresql.conf`.
- `InsufficientPrivilege` ao consultar: execute os `GRANT` e `ALTER DEFAULT PRIVILEGES` do passo 5.
- `authentication failed`: confira o `pg_hba.conf` (modo `md5`), usuário, senha e host.
- Erros de pool/timeout do SQLAlchemy sob carga: ajuste `pool_size`, `max_overflow` e `pool_timeout` no `create_engine` (veja documentação do SQLAlchemy).

## 11. Boas práticas

- Use um usuário dedicado para o app (sem superprivilégios).
- Não deixe `pg_hba.conf` em `trust` em produção; use `md5`/`scram-sha-256`.
- Centralize segredos em `.env` e em variáveis de ambiente no servidor.
- Faça backup regular do banco e teste restaurações.
- Considere migrações com Alembic em projetos que evoluem o esquema com frequência.

---

Checklist rápido para novos projetos:

1) Criar usuário e banco (`CREATE ROLE` / `CREATE DATABASE`)  
2) Conceder privilégios e defaults (GRANT / ALTER DEFAULT PRIVILEGES)  
3) Configurar `.env` com `DATABASE_URL`  
4) Criar venv e instalar dependências  
5) Iniciar app e validar criação de tabelas no pgAdmin  
