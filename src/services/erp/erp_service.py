from src.models.erp.models import db, Produto, Venda
from sqlalchemy import func

class DashboardService:
    @staticmethod
    def get_kpis():
        total_vendas = db.session.query(func.sum(Venda.valor_total)).scalar() or 0
        total_pedidos = db.session.query(func.count(Venda.id)).scalar() or 0
        produtos_baixo_estoque = db.session.query(func.count(Produto.id)).filter(Produto.estoque < 10).scalar() or 0
        
        return {
            'faturamento': total_vendas,
            'pedidos': total_pedidos,
            'alertas': produtos_baixo_estoque
        }

    @staticmethod
    def get_vendas_mensais():
        # Simulação de dados para o gráfico (em produção faríamos uma query complexa)
        return {
            'labels': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
            'data': [12000, 19000, 3000, 5000, 2000, 30000]
        }

class ProdutoService:
    @staticmethod
    def listar_todos():
        return Produto.query.all()

    @staticmethod
    def criar_produto(dados):
        novo_produto = Produto(
            nome=dados['nome'],
            categoria=dados['categoria'],
            preco=float(dados['preco']),
            estoque=int(dados['estoque'])
        )
        db.session.add(novo_produto)
        db.session.commit()
        return novo_produto
