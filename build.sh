#!/bin/bash
# Script de build para Render

# Instala dependências
pip install -r requirements.txt

# Inicializa o banco de dados se DATABASE_URL estiver configurado
if [ ! -z "$DATABASE_URL" ]; then
    echo "🗄️ Inicializando banco de dados..."
    python -c "from app import app; app.cli.commands['init_db'].invoke({})"
fi

echo "✅ Build concluído!"
