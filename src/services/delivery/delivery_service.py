from src.database import db
from src.models.delivery.models import ItemCardapio

class DeliveryService:
    @staticmethod
    def init_defaults():
        if ItemCardapio.query.count() == 0:
            itens = [
                ItemCardapio(
                    nome="X-Fuosteck Burger", 
                    descricao="Pão brioche, burger 180g, queijo cheddar, bacon e molho especial.", 
                    preco=32.90, 
                    categoria="Lanches",
                    imagem_url="https://placehold.co/400x300/1e293b/00d2ff?text=Burger"
                ),
                ItemCardapio(
                    nome="Smash Duplo", 
                    descricao="Dois burgers 90g, queijo prato, cebola caramelizada.", 
                    preco=28.50, 
                    categoria="Lanches",
                    imagem_url="https://placehold.co/400x300/1e293b/00d2ff?text=Smash"
                ),
                ItemCardapio(
                    nome="Batata Rústica", 
                    descricao="Batatas cortadas a mão com alecrim e páprica.", 
                    preco=18.00, 
                    categoria="Acompanhamentos",
                    imagem_url="https://placehold.co/400x300/1e293b/00d2ff?text=Fritas"
                ),
                ItemCardapio(
                    nome="Coca-Cola Lata", 
                    descricao="Lata 350ml gelada.", 
                    preco=6.00, 
                    categoria="Bebidas",
                    imagem_url="https://placehold.co/400x300/1e293b/00d2ff?text=Refri"
                )
            ]
            db.session.add_all(itens)
            db.session.commit()

    @staticmethod
    def listar_itens():
        return ItemCardapio.query.all()

    @staticmethod
    def listar_por_categoria():
        itens = ItemCardapio.query.all()
        categorias = {}
        for item in itens:
            if item.categoria not in categorias:
                categorias[item.categoria] = []
            categorias[item.categoria].append(item)
        return categorias
