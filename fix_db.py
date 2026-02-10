import sqlite3

def adicionar_coluna_telefone():
    try:
        conn = sqlite3.connect('instance/dev.db')
        cursor = conn.cursor()
        
        # Verificar se a coluna já existe para evitar erro
        cursor.execute("PRAGMA table_info(agendamentos)")
        colunas = [info[1] for info in cursor.fetchall()]
        
        if 'cliente_telefone' not in colunas:
            print("Adicionando coluna 'cliente_telefone'...")
            cursor.execute("ALTER TABLE agendamentos ADD COLUMN cliente_telefone TEXT")
            conn.commit()
            print("Coluna adicionada com sucesso!")
        else:
            print("A coluna 'cliente_telefone' já existe.")
            
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    adicionar_coluna_telefone()
