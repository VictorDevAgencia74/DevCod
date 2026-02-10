import sqlite3
import json
import os

# Caminho para o banco de dados
DB_PATH = os.path.join("data", "sigf_local.db")

def inspect_db():
    if not os.path.exists(DB_PATH):
        print(f"Erro: Banco de dados não encontrado em {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Listar todas as tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("\n=== TABELAS ENCONTRADAS ===")
        for table in tables:
            print(f"- {table[0]}")

        # Ler dados da tabela checklist_responses
        print("\n=== DADOS SALVOS (checklist_responses) ===")
        cursor.execute("SELECT * FROM checklist_responses")
        rows = cursor.fetchall()

        if not rows:
            print("Nenhum registro encontrado.")
        else:
            for row in rows:
                id, checklist_id, data, created_at, synced = row
                print(f"ID: {id}")
                print(f"Tipo: {checklist_id}")
                print(f"Data Criação: {created_at}")
                print(f"Sincronizado: {'Sim' if synced else 'Não'}")
                print(f"Conteúdo: {json.loads(data) if isinstance(data, str) else data}") # Tenta formatar JSON
                print("-" * 30)

    except sqlite3.Error as e:
        print(f"Erro ao ler banco: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    inspect_db()
