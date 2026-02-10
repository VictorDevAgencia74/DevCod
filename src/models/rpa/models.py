from src.database import db
from datetime import datetime

class BotTask(db.Model):
    __tablename__ = 'bot_tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200))
    status = db.Column(db.String(20), default='parado') # parado, executando, concluido, erro
    last_run = db.Column(db.DateTime)
    logs = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'status': self.status,
            'last_run': self.last_run.strftime('%d/%m/%Y %H:%M:%S') if self.last_run else '-',
            'logs': self.logs
        }
