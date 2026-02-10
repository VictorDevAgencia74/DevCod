from flask_caching import Cache

# Inicializa o cache separadamente para evitar importação circular
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
