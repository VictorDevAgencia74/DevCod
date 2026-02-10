from flask import Blueprint, render_template, jsonify, request
from src.services.rpa.rpa_service import RPAService

rpa_bp = Blueprint('rpa', __name__, url_prefix='/demos/rpa')

@rpa_bp.route('/')
def dashboard():
    RPAService.init_defaults()
    tasks = RPAService.listar_tasks()
    return render_template('rpa/dashboard.html', tasks=tasks)

@rpa_bp.route('/start/<int:id>', methods=['POST'])
def start_bot(id):
    # Pega URL do corpo da requisição JSON (se houver)
    data = request.get_json()
    target_url = data.get('url') if data else None
    
    RPAService.simular_execucao(id, target_url)
    return jsonify({'success': True, 'status': 'executando'})

@rpa_bp.route('/finish/<int:id>', methods=['POST'])
def finish_bot(id):
    # Rota auxiliar para simular o fim do processamento pelo front
    RPAService.finalizar_simulacao(id)
    return jsonify({'success': True, 'status': 'concluido'})

@rpa_bp.route('/status/<int:id>')
def check_status(id):
    task = RPAService.get_task(id)
    if task:
        return jsonify(task.to_dict())
    return jsonify({'error': 'Task not found'}), 404
