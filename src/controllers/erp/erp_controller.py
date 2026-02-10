from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from src.services.erp.erp_service import DashboardService, ProdutoService
from src.database import db

erp_bp = Blueprint('erp', __name__, url_prefix='/demos/erp')

@erp_bp.route('/')
def index():
    kpis = DashboardService.get_kpis()
    produtos = ProdutoService.listar_todos()
    return render_template('erp/dashboard.html', kpis=kpis, produtos=produtos)

@erp_bp.route('/api/chart-data')
def chart_data():
    data = DashboardService.get_vendas_mensais()
    return jsonify(data)

@erp_bp.route('/produtos/novo', methods=['POST'])
def novo_produto():
    dados = request.form
    ProdutoService.criar_produto(dados)
    return redirect(url_for('erp.index'))
