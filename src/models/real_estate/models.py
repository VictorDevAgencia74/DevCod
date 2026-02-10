from src.database import db

class Imovel(db.Model):
    __tablename__ = 'imoveis'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(50)) # Apartamento, Casa, Sala Comercial
    area = db.Column(db.Float) # m²
    quartos = db.Column(db.Integer)
    banheiros = db.Column(db.Integer)
    vagas = db.Column(db.Integer)
    endereco = db.Column(db.String(200))
    imagem_url = db.Column(db.String(200)) # URL de imagem principal
    status = db.Column(db.String(20), default='disponivel') # disponivel, vendido, alugado
    
    imagens = db.relationship('ImagemImovel', backref='imovel', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'preco': self.preco,
            'tipo': self.tipo,
            'area': self.area,
            'endereco': self.endereco,
            'imagem_url': self.imagem_url
        }

class ImagemImovel(db.Model):
    __tablename__ = 'imagens_imoveis'
    
    id = db.Column(db.Integer, primary_key=True)
    imovel_id = db.Column(db.Integer, db.ForeignKey('imoveis.id'), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.String(100)) # ex: "Sala de Estar", "Cozinha"
