from flask import Blueprint, render_template, request, jsonify, url_for, redirect
from src.services.booking.booking_service import BookingService
from src.extensions import cache

booking_bp = Blueprint('booking', __name__, url_prefix='/demos/booking')

@booking_bp.route('/')
def index():
    BookingService.init_defaults()
    servicos = BookingService.listar_servicos()
    return render_template('booking/calendar.html', servicos=servicos)

@booking_bp.route('/api/events')
@cache.cached(timeout=10, query_string=True) # Cache curto (10s) para eventos, variando com query params
def get_events():
    events = BookingService.listar_eventos()
    return jsonify(events)

@booking_bp.route('/new', methods=['POST'])
def new_booking():
    BookingService.criar_agendamento(request.form)
    # Limpar cache de eventos ao criar novo
    cache.delete_memoized(get_events)
    return redirect(url_for('booking.index'))

# Novas Rotas para Prontuário
@booking_bp.route('/prontuario/<int:agendamento_id>', methods=['GET'])
def get_prontuario(agendamento_id):
    prontuario = BookingService.get_prontuario(agendamento_id)
    if prontuario:
        return jsonify({
            'queixa': prontuario.queixa_principal,
            'historico': prontuario.historico,
            'observacoes': prontuario.observacoes
        })
    return jsonify({})

@booking_bp.route('/prontuario/<int:agendamento_id>', methods=['POST'])
def save_prontuario(agendamento_id):
    BookingService.salvar_prontuario(agendamento_id, request.form)
    return jsonify({'success': True})

# Simulação de Envio de WhatsApp
@booking_bp.route('/whatsapp/send/<int:agendamento_id>', methods=['POST'])
def send_whatsapp(agendamento_id):
    return jsonify({'success': True, 'message': 'Lembrete enviado com sucesso via WhatsApp API!'})
