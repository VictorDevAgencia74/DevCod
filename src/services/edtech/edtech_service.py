from src.database import db
from src.models.edtech.models import Curso, Modulo, Aula

class EdTechService:
    @staticmethod
    def init_defaults():
        if Curso.query.count() == 0:
            # Curso 1: Python Fullstack
            curso1 = Curso(
                titulo="Python Fullstack Masterclass",
                descricao="Domine o desenvolvimento web com Python, Flask e Django do zero ao deploy.",
                thumbnail_url="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
                instrutor="Victor Xavier",
                preco=497.00
            )
            db.session.add(curso1)
            db.session.commit() # Commit para gerar ID
            
            mod1 = Modulo(curso_id=curso1.id, titulo="Introdução ao Python", ordem=1)
            mod2 = Modulo(curso_id=curso1.id, titulo="Web com Flask", ordem=2)
            db.session.add_all([mod1, mod2])
            db.session.commit()
            
            aulas = [
                Aula(modulo_id=mod1.id, titulo="Configurando o Ambiente", video_url="https://www.youtube.com/embed/dQw4w9WgXcQ", duracao="10:00", ordem=1),
                Aula(modulo_id=mod1.id, titulo="Variáveis e Tipos de Dados", video_url="https://www.youtube.com/embed/dQw4w9WgXcQ", duracao="15:30", ordem=2),
                Aula(modulo_id=mod2.id, titulo="Rotas e Views", video_url="https://www.youtube.com/embed/dQw4w9WgXcQ", duracao="20:00", ordem=1),
            ]
            db.session.add_all(aulas)

            # Curso 2: Marketing Digital
            curso2 = Curso(
                titulo="Marketing para Devs",
                descricao="Aprenda a vender seus serviços de software e criar sua marca pessoal.",
                thumbnail_url="https://images.unsplash.com/photo-1533750516457-a7f992034fec?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
                instrutor="Ana Silva",
                preco=297.00
            )
            db.session.add(curso2)
            db.session.commit()

    @staticmethod
    def listar_cursos():
        return Curso.query.all()

    @staticmethod
    def get_curso(id):
        return Curso.query.get(id)
    
    @staticmethod
    def get_aula(id):
        return Aula.query.get(id)

    @staticmethod
    def get_navegacao_aulas(aula_atual):
        if not aula_atual:
            return None, None
            
        curso_id = aula_atual.modulo.curso_id
        
        # Busca todas as aulas do curso ordenadas por módulo e ordem da aula
        todas_aulas = db.session.query(Aula)\
            .join(Modulo)\
            .filter(Modulo.curso_id == curso_id)\
            .order_by(Modulo.ordem, Aula.ordem)\
            .all()
            
        try:
            idx = todas_aulas.index(aula_atual)
            prev_aula = todas_aulas[idx - 1] if idx > 0 else None
            next_aula = todas_aulas[idx + 1] if idx < len(todas_aulas) - 1 else None
            return prev_aula, next_aula
        except ValueError:
            return None, None
