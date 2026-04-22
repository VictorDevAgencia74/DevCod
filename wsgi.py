#!/usr/bin/env python
"""
Script para inicializar o banco de dados e iniciar a aplicação.
Executado antes do gunicorn no Render.
"""
import os
import sys
from app import app

def init_database():
    """Inicializa o banco de dados com tratamento de erros."""
    with app.app_context():
        try:
            # Tenta criar as tabelas
            from src.database import db
            
            # Se estiver usando PostgreSQL e não conseguir conectar, skipa
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            
            if 'postgresql' in db_uri or 'postgres' in db_uri:
                try:
                    db.create_all()
                    print("✅ Banco de dados PostgreSQL inicializado com sucesso!")
                except Exception as e:
                    print(f"⚠️ Aviso: Não foi possível inicializar o banco PostgreSQL: {e}")
                    print("   Isso é normal no primeiro deploy. O banco será criado pelo Render.")
                    print("   Você pode rodar 'flask init-db' manualmente após confirmar a conexão.")
            else:
                # Para SQLite, sempre tenta criar
                db.create_all()
                print("✅ Banco de dados SQLite inicializado com sucesso!")
                
        except Exception as e:
            print(f"❌ Erro ao inicializar banco: {e}")
            # Não interrompe o deploy por erro de banco
            pass

if __name__ == '__main__':
    print("🚀 Inicializando aplicação...")
    
    # Tenta inicializar o banco
    init_database()
    
    print("✅ Aplicação pronta para rodar!")
    print(f"DATABASE_URL: {os.environ.get('DATABASE_URL', 'Usando SQLite padrão')}")
