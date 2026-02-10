import sqlite3
import os

# Caminho do banco de dados
db_path = os.path.join('instance', 'dev.db')

def inspect_db():
    if not os.path.exists(db_path):
        print(f"❌ Erro: Banco de dados não encontrado em {db_path}")
        return

    print(f"🔍 Inspecionando Banco de Dados: {db_path}\n")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Listar todas as tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    if not tables:
        print("O banco de dados está vazio (nenhuma tabela encontrada).")
        return

    for table_name in tables:
        table = table_name[0]
        # Ignorar tabelas internas do SQLite ou do Alembic (migrações) se houver
        if table in ['sqlite_sequence', 'alembic_version']: 
            continue 

        print(f"{'='*40}")
        print(f"📋 Tabela: {table}")
        print(f"{'='*40}")
        
        # Obter nomes das colunas
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [col[1] for col in cursor.fetchall()]
        print(f"Colunas: { ' | '.join(columns) }")
        print("-" * 40)

        # Obter dados
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        
        if not rows:
            print("  (Tabela vazia)")
        else:
            for row in rows:
                # Converter cada item para string para facilitar visualização
                print(f"  {row}")
        print("\n")

    conn.close()

if __name__ == "__main__":
    inspect_db()
