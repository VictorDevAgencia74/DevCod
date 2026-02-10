from flask import Blueprint, render_template, request, jsonify
from src.extensions import cache
import urllib.parse
import os

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
# @cache.cached(timeout=60) # Desabilitando cache para garantir atualização imediata
def index():
    return render_template('index.html')

@home_bp.route('/landing')
# @cache.cached(timeout=60)
def landing():
    return render_template('landing.html')

@home_bp.route('/send-message', methods=['POST'])
def send_message():
    nome = request.form.get('nome')
    email = request.form.get('email')
    mensagem = request.form.get('mensagem')
    
    # Gerar Link WhatsApp
    texto_whatsapp = f"*Novo Contato via Site Fuosteck* 🚀\n\n" \
                     f"👤 *Nome:* {nome}\n" \
                     f"📧 *Email:* {email}\n" \
                     f"📝 *Mensagem:* {mensagem}\n\n" \
                     f"--- Fim da mensagem ---"
    
    encoded_text = urllib.parse.quote(texto_whatsapp)
    whatsapp_link = f"https://wa.me/5573981747651?text={encoded_text}"
    
    return jsonify({
        'success': True,
        'whatsapp_link': whatsapp_link,
        'message': f"Obrigado, {nome}! Sua mensagem foi preparada. Clique em OK para enviar via WhatsApp."
    })
