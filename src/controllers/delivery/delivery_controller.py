from flask import Blueprint, render_template
from src.services.delivery.delivery_service import DeliveryService

delivery_bp = Blueprint('delivery', __name__, url_prefix='/demos/delivery')

@delivery_bp.route('/')
def index():
    DeliveryService.init_defaults()
    categorias = DeliveryService.listar_por_categoria()
    return render_template('delivery/menu.html', categorias=categorias)
