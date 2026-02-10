from src.database import db

class ItemCardapio(db.Model):
    __tablename__ = 'itens_cardapio'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200))
    preco = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False) # Lanches, Bebidas, Sobremesas
    imagem_url = db.Column(db.String(200)) # URL da imagem

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': self.preco,
            'categoria': self.categoria,
            'imagem_url': self.imagem_url
        }
