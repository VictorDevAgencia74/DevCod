# Changelog

Todas as alterações notáveis no projeto SIGF-Const serão documentadas neste arquivo.

## [v0.4.0] - 2026-01-29 (Fase 4 - Hardening de Segurança)
### Adicionado
- **Controle de Acesso Baseado em Função (RBAC):** Implementação rigorosa de distinção entre `admin` e `driver`.
- **Frontend Guards:** Scripts em `index.html` e `admin.html` que verificam a existência e validade do Token JWT antes de renderizar a tela.
- **Redirecionamento Automático:** Usuários não autenticados são enviados para o login; Usuários sem permissão (ex: motorista tentando acessar admin) são redirecionados para a home.
- **Segurança de API:** Todos os endpoints críticos (`GET /checklists`, `PUT`, `DELETE`, `Export`) agora exigem cabeçalho `Authorization: Bearer <token>`.
- **Script de Setup:** Novo utilitário `setup_users.py` para criar usuários padrão (`admin` e `motorista1`).

## [v0.3.0] - 2026-01-29 (Fase 3 - Inteligência)
### Adicionado
- **Módulo de Manutenção:** Novo endpoint `/api/maintenance/alerts` que analisa automaticamente os checklists enviados.
- **Regras de Alerta:**
  - Detecta pneus com status "CRÍTICO".
  - Alerta sobre revisões vencidas (ex: KM > 10.000).
- **Dashboard Admin:** Cards visuais no topo da tela de administração mostrando:
  - Total de Envios.
  - Pendências de Sincronização.
  - Alertas de Problemas (Pneus/Manutenção).

## [v0.2.0] - 2026-01-29 (Fase 2 - Segurança e Nuvem)
### Adicionado
- **Autenticação:** Sistema de Login com JWT (JSON Web Token).
- **Proteção de Rotas:** Endpoints de administração (`PUT`, `DELETE`, `Excel`) agora exigem token de 'manager' ou 'admin'.
- **Histórico:** Tela "Meus Envios" no App PWA para o motorista consultar o status.
- **Sincronização:** Script `sync_service.py` para enviar dados ao Supabase (PostgreSQL).

## [v0.1.0] - 2026-01-29 (MVP Inicial)
### Adicionado
- **App PWA:** Interface Offline-First com Bootstrap 5.
- **Backend:** API FastAPI com SQLite.
- **Formulários Dinâmicos:** Geração de checklists via `schemas/checklists.json`.
- **Exportação Excel:** Geração de relatórios `.xlsx` via Pandas.
