from flask import Blueprint, render_template, redirect, url_for
from src.services.edtech.edtech_service import EdTechService

edtech_bp = Blueprint('edtech', __name__, url_prefix='/demos/edtech')

@edtech_bp.route('/')
def index():
    EdTechService.init_defaults()
    cursos = EdTechService.listar_cursos()
    return render_template('edtech/index.html', cursos=cursos)

@edtech_bp.route('/curso/<int:id>')
def course_player(id):
    curso = EdTechService.get_curso(id)
    if not curso:
        return redirect(url_for('edtech.index'))
    
    # Pega a primeira aula do primeiro módulo como padrão se não especificado
    aula_atual = None
    if curso.modulos and curso.modulos[0].aulas:
        aula_atual = curso.modulos[0].aulas[0]
    
    prev_aula, next_aula = EdTechService.get_navegacao_aulas(aula_atual)
        
    return render_template('edtech/course.html', curso=curso, aula_atual=aula_atual, prev_aula=prev_aula, next_aula=next_aula)

@edtech_bp.route('/aula/<int:id>')
def watch_lesson(id):
    aula = EdTechService.get_aula(id)
    if not aula:
        return redirect(url_for('edtech.index'))
    
    curso = aula.modulo.curso
    prev_aula, next_aula = EdTechService.get_navegacao_aulas(aula)
    
    return render_template('edtech/course.html', curso=curso, aula_atual=aula, prev_aula=prev_aula, next_aula=next_aula)
