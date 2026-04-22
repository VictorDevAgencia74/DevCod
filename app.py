from flask import Flask, render_template
from flask_talisman import Talisman
from whitenoise import WhiteNoise
from src.extensions import cache
from src.controllers.home_controller import home_bp
from src.controllers.erp.erp_controller import erp_bp
from src.controllers.booking.booking_controller import booking_bp
from src.controllers.delivery.delivery_controller import delivery_bp
from src.controllers.real_estate.real_estate_controller import real_estate_bp
from src.controllers.edtech.edtech_controller import edtech_bp
from src.controllers.rpa.rpa_controller import rpa_bp
from src.database import db
import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

def create_app():
    app = Flask(__name__, static_folder='assets', template_folder='templates')
    
    # Configurar WhiteNoise para servir arquivos estáticos em produção
    app.wsgi_app = WhiteNoise(app.wsgi_app, root='assets/', prefix='assets/')
    
    # Configuração básica
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///dev.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['GA_MEASUREMENT_ID'] = os.environ.get('GA_MEASUREMENT_ID')

    # Inicializar Extensões
    db.init_app(app)
    cache.init_app(app)
    
    @app.context_processor
    def inject_globals():
        return {
            'ga_id': app.config.get('GA_MEASUREMENT_ID'),
            'is_prod': not app.debug
        }
    
    # Segurança (Talisman): Força HTTPS e Headers Seguros
    # Ajuste na CSP para permitir CDNs (Bootstrap, FontAwesome, etc)
    if not app.debug:
        csp = {
            'default-src': ["'self'", 'https://cdn.jsdelivr.net', 'https://cdnjs.cloudflare.com'],
            'script-src': ["'self'", "'unsafe-inline'", 'https://cdn.jsdelivr.net', 'https://www.googletagmanager.com'],
            'style-src': ["'self'", "'unsafe-inline'", 'https://cdn.jsdelivr.net', 'https://cdnjs.cloudflare.com', 'https://fonts.googleapis.com'],
            'img-src': ["'self'", 'data:', 'https:', '*'],
            'font-src': ["'self'", 'https://cdnjs.cloudflare.com', 'https://fonts.gstatic.com'],
            'frame-src': ["'self'", 'https://www.youtube.com'],
            'connect-src': ["'self'", 'https://www.google-analytics.com', 'https://cdn.jsdelivr.net']
        }
        Talisman(app, content_security_policy=csp)
    
    # Registrar Blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(erp_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(delivery_bp)
    app.register_blueprint(real_estate_bp)
    app.register_blueprint(edtech_bp)
    app.register_blueprint(rpa_bp)
    
    # CLI command para inicializar o banco de dados
    @app.cli.command()
    def init_db():
        """Inicializa o banco de dados."""
        with app.app_context():
            db.create_all()
            print("✅ Banco de dados inicializado!")
    
    # Criar tabelas automaticamente se estiver em desenvolvimento e banco não existir
    if app.debug and 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
        with app.app_context():
            db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
