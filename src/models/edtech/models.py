from src.database import db

class Curso(db.Model):
    __tablename__ = 'cursos'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    thumbnail_url = db.Column(db.String(200))
    instrutor = db.Column(db.String(100))
    preco = db.Column(db.Float)
    
    modulos = db.relationship('Modulo', backref='curso', lazy=True)

class Modulo(db.Model):
    __tablename__ = 'modulos'
    
    id = db.Column(db.Integer, primary_key=True)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    ordem = db.Column(db.Integer)
    
    aulas = db.relationship('Aula', backref='modulo', lazy=True)

class Aula(db.Model):
    __tablename__ = 'aulas'
    
    id = db.Column(db.Integer, primary_key=True)
    modulo_id = db.Column(db.Integer, db.ForeignKey('modulos.id'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    video_url = db.Column(db.String(200)) # Vimeo/YouTube embed
    duracao = db.Column(db.String(20)) # ex: "10:30"
    ordem = db.Column(db.Integer)
