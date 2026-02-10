from src.database import db
from src.models.booking.models import Servico, Agendamento, Prontuario
from datetime import datetime, timedelta

class BookingService:
    @staticmethod
    def init_defaults():
        if Servico.query.count() == 0:
            servicos = [
                Servico(nome="Consulta Médica", duracao=60, preco=350.00),
                Servico(nome="Sessão de Fisioterapia", duracao=45, preco=150.00),
                Servico(nome="Avaliação Odontológica", duracao=30, preco=100.00),
                Servico(nome="Terapia Psicológica", duracao=50, preco=200.00)
            ]
            db.session.add_all(servicos)
            db.session.commit()

    @staticmethod
    def listar_servicos():
        return Servico.query.all()

    @staticmethod
    def criar_agendamento(dados):
        inicio = datetime.strptime(dados['data_hora'], '%Y-%m-%dT%H:%M')
        servico = Servico.query.get(dados['servico_id'])
        fim = inicio + timedelta(minutes=servico.duracao)
        
        novo_agendamento = Agendamento(
            cliente_nome=dados['nome'],
            cliente_email=dados['email'],
            cliente_telefone=dados.get('telefone'), # Pegando telefone do form
            servico_id=dados['servico_id'],
            inicio=inicio,
            fim=fim
        )
        db.session.add(novo_agendamento)
        db.session.commit()
        return novo_agendamento

    @staticmethod
    def listar_eventos():
        agendamentos = Agendamento.query.all()
        return [a.to_dict() for a in agendamentos]
    
    @staticmethod
    def salvar_prontuario(agendamento_id, dados):
        prontuario = Prontuario.query.filter_by(agendamento_id=agendamento_id).first()
        if not prontuario:
            prontuario = Prontuario(agendamento_id=agendamento_id)
            
        prontuario.queixa_principal = dados.get('queixa')
        prontuario.historico = dados.get('historico')
        prontuario.observacoes = dados.get('observacoes')
        
        db.session.add(prontuario)
        db.session.commit()
        return prontuario
    
    @staticmethod
    def get_prontuario(agendamento_id):
        return Prontuario.query.filter_by(agendamento_id=agendamento_id).first()
