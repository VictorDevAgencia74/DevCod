# SIGF-Const: Sistema Integrado de Gestão de Frota (Offline-First)

## 📌 Sobre o Projeto

O **SIGF-Const** é uma solução tecnológica desenvolvida para resolver o desafio de gestão de ativos em canteiros de obras com conectividade intermitente. 

O sistema opera com uma arquitetura **Offline-First**, permitindo que motoristas e operadores preencham checklists, registrem abastecimentos e ocorrências diretamente em seus dispositivos (Tablets/Celulares) sem depender de internet. Os dados são armazenados localmente e, futuramente, serão sincronizados com a nuvem quando houver conexão.

## 🚀 Funcionalidades Principais (MVP Atual)

*   **App PWA (Progressive Web App):** Instalável no celular, leve e funciona offline.
*   **Formulários Dinâmicos:** Checklists (Veículos Leves, Pesados, Máquinas) gerados automaticamente a partir de arquivos JSON. Flexibilidade total para criar novos modelos sem alterar código.
*   **Backend Robusto:** API em Python (FastAPI) pronta para escalar.
*   **Persistência Local:** Banco de dados SQLite embarcado para garantir que nenhum dado se perca no campo.

## 🛠️ Stack Tecnológica

*   **Backend:** Python 3.x, FastAPI, SQLAlchemy, Pydantic.
*   **Frontend:** HTML5, CSS3 (Bootstrap 5), JavaScript (Vanilla).
*   **Banco de Dados:** SQLite (Local) -> *Preparado para PostgreSQL/Supabase*.
*   **Infra:** Service Workers para cache e funcionamento offline.

## 📂 Estrutura do Projeto

```text
/backend      -> Código da API Python (main.py, models).
/frontend     -> Interface do usuário (HTML, JS, Service Worker).
/data         -> Banco de dados SQLite (sigf_local.db).
/schemas      -> Configurações JSON dos formulários (checklists.json).
/documentacao -> Manuais de processos, relatórios e visão técnica.
```

## ▶️ Como Rodar o Projeto

1.  **Configurar Ambiente Python:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    ```

2.  **Executar o Servidor:**
    ```bash
    python backend/main.py
    ```

3.  **Acessar:**
    Abra o navegador em `http://localhost:8000`.

4.  **Configuração Inicial de Usuários:**
    Para acessar o sistema (que agora é protegido), você precisa criar os usuários padrão:
    ```bash
    python setup_users.py
    ```
    Isso criará:
    *   **Admin:** Usuário `admin` / Senha `admin123`
    *   **Motorista:** Usuário `motorista1` / Senha `moto123`

## 🔮 Roadmap e Futuras Melhorias (Banco de Ideias)

Para garantir a evolução contínua e escalabilidade do SIGF-Const, os seguintes passos foram mapeados:

### FASE 1: Consolidação (Imediato)
- [ ] **CRUD Administrativo:** Interface Web para gestores editarem/excluírem registros lançados errados.
- [ ] **Exportação Excel:** Endpoint para baixar todos os checklists em formato `.xlsx` para análise financeira.
- [ ] **Visualização de Histórico:** Permitir que o motorista veja seus últimos envios no próprio App.

### FASE 2: Conectividade e Nuvem (Curto Prazo)
- [ ] **Sincronização Bidirecional:** Script de background para enviar dados do SQLite local para o Supabase (PostgreSQL) assim que detectar internet.
- [ ] **Autenticação:** Sistema de Login (JWT) para diferenciar Motorista, Mecânico e Gestor.
- [ ] **Tratamento de Conflitos:** Lógica para resolver edições simultâneas (local vs nuvem).

### FASE 3: Inteligência e IoT (Médio/Longo Prazo)
- [ ] **Dashboards BI:** Painéis gráficos de consumo de combustível e disponibilidade de frota.
- [ ] **Manutenção Preditiva:** Alertas automáticos baseados no horímetro/KM informado (ex: "Troca de óleo em 50h").
- [ ] **Integração IoT:** Captura automática de dados de rastreadores (Sascar/Omnilink) para auditar o input manual.

## 📚 Documentação Detalhada

Para detalhes profundos sobre processos e arquitetura, consulte os arquivos na raiz do projeto:
*   `documentacao.md`: Visão de Negócio, Processos (POPs), KPIs e Modelos de Documentos.
*   `documentacao_sistema.md`: Visão Técnica, Arquitetura de Software e Plano de Escalabilidade.
