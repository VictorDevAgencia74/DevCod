# Fuosteck Portfolio & SaaS Demos

Este repositório contém o portfólio profissional da **Fuosteck**, desenvolvido com uma arquitetura modular em Python (Flask), focado em alta performance e escalabilidade. O projeto inclui não apenas a landing page, mas também demonstrações funcionais de sistemas (SaaS) integrados.

##  Tecnologias

*   **Backend:** Python 3.12, Flask, SQLAlchemy.
*   **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript (Vanilla).
*   **Banco de Dados:** SQLite (Dev) / PostgreSQL (Prod - Supabase Ready).
*   **Visualização de Dados:** Chart.js, FullCalendar.js.

##  Estrutura do Projeto

`
/
 assets/             # Arquivos estáticos (CSS, JS, Imagens)
 src/
    config/         # Configurações do App
    controllers/    # Rotas e Lógica de Controle (Blueprints)
    models/         # Modelos de Banco de Dados (ORM)
    services/       # Regras de Negócio
    database.py     # Instância compartilhada do DB
 templates/          # Arquivos HTML (Jinja2)
 app.py              # Entry Point da aplicação
 requirements.txt    # Dependências
`

##  Instalação e Execução

1.  **Clone o repositório:**
    `ash
    git clone https://github.com/seu-usuario/fuosteck-portfolio.git
    cd fuosteck-portfolio
    `

2.  **Crie o ambiente virtual:**
    `ash
    python -m venv venv
    # Windows
    .\venv\Scripts\Activate
    # Linux/Mac
    source venv/bin/activate
    `

3.  **Instale as dependências:**
    `ash
    pip install -r requirements.txt
    `

4.  **Execute a aplicação:**
    `ash
    python app.py
    `
    Acesse: http://127.0.0.1:5000

##  Demos Incluídos

1.  **Sistema ERP (Gestão Empresarial):** Dashboard administrativo com gráficos de vendas e gestão de estoque.
    *   *URL:* /demos/erp
2.  **Agendamento Online (Booking SaaS):** Sistema de reservas com calendário interativo para clínicas/consultorias.
    *   *URL:* /demos/booking

##  Relatório Estratégico

Consulte o arquivo RELATORIO_ESTRATEGICO.md na raiz para uma análise detalhada de nichos de mercado e oportunidades de negócio mapeadas para a Fuosteck.

---
Desenvolvido por **Fuosteck** - Soluções Digitais.
