from src.database import db
from datetime import datetime

class Servico(db.Model):
    __tablename__ = 'servicos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    duracao = db.Column(db.Integer, nullable=False) # em minutos
    preco = db.Column(db.Float, nullable=False)

class Agendamento(db.Model):
    __tablename__ = 'agendamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_nome = db.Column(db.String(100), nullable=False)
    cliente_email = db.Column(db.String(100))
    cliente_telefone = db.Column(db.String(20))
    servico_id = db.Column(db.Integer, db.ForeignKey('servicos.id'), nullable=False)
    inicio = db.Column(db.DateTime, nullable=False)
    fim = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='confirmado')
    
    servico = db.relationship('Servico', backref='agendamentos')

    def to_dict(self):
        return {
            'id': self.id,
            'title': f'{self.cliente_nome} - {self.servico.nome}',
            'start': self.inicio.isoformat(),
            'end': self.fim.isoformat(),
            'backgroundColor': '#00d2ff',
            'borderColor': '#00d2ff',
            'extendedProps': {
                'telefone': self.cliente_telefone,
                'email': self.cliente_email,
                'servico': self.servico.nome,
                'preco': self.servico.preco
            }
        }

class Prontuario(db.Model):
    __tablename__ = 'prontuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    agendamento_id = db.Column(db.Integer, db.ForeignKey('agendamentos.id'), nullable=False)
    queixa_principal = db.Column(db.Text)
    historico = db.Column(db.Text)
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    agendamento = db.relationship('Agendamento', backref=db.backref('prontuario', uselist=False))
