import sqlite3

# 1. Conectar ao arquivo do banco de dados
# O 'instance/dev.db' é o caminho onde o arquivo está salvo
conexao = sqlite3.connect('instance/dev.db')

# 2. Criar um cursor (o objeto que executa comandos SQL)
cursor = conexao.cursor()

def listar_tabelas():
    print("\n=== 📂 Tabelas no Banco ===")
    # Consulta para listar todas as tabelas criadas pelo sistema
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = cursor.fetchall()
    for tabela in tabelas:
        print(f"- {tabela[0]}")

def ver_produtos():
    print("\n=== 📦 Produtos (Tabela 'produtos') ===")
    try:
        # SELECT * significa "Selecione TODAS as colunas"
        cursor.execute("SELECT id, nome, preco, estoque FROM produtos")
        produtos = cursor.fetchall()
        
        if not produtos:
            print("Nenhum produto encontrado.")
        
        # Iterar sobre cada linha encontrada
        for p in produtos:
            print(f"ID: {p[0]} | Nome: {p[1]:<20} | Preço: R$ {p[2]:<8} | Estoque: {p[3]}")
            
    except Exception as e:
        print(f"Erro ao ler produtos: {e}")

# Executando as funções
listar_tabelas()
ver_produtos()

# 3. Fechar a conexão (Sempre importante!)
conexao.close()
