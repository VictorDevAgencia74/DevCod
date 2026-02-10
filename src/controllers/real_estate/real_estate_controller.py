from flask import Blueprint, render_template, request, send_file, redirect, url_for, flash
from src.services.real_estate.real_estate_service import RealEstateService

real_estate_bp = Blueprint('real_estate', __name__, url_prefix='/demos/real-estate')

@real_estate_bp.route('/')
def index():
    RealEstateService.init_defaults()
    imoveis = RealEstateService.listar_imoveis()
    return render_template('real_estate/index.html', imoveis=imoveis)

@real_estate_bp.route('/imovel/<int:id>')
def details(id):
    imovel = RealEstateService.get_imovel(id)
    if not imovel:
        return redirect(url_for('real_estate.index'))
    return render_template('real_estate/details.html', imovel=imovel)

@real_estate_bp.route('/gerar-proposta', methods=['POST'])
def gerar_proposta():
    imovel_id = request.form.get('imovel_id')
    cliente_nome = request.form.get('nome')
    cliente_email = request.form.get('email')
    valor_proposta = request.form.get('valor')
    
    pdf_buffer = RealEstateService.gerar_pdf_proposta(imovel_id, cliente_nome, cliente_email, valor_proposta)
    
    if pdf_buffer:
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f'proposta_imovel_{imovel_id}.pdf',
            mimetype='application/pdf'
        )
    
    return redirect(url_for('real_estate.index'))
