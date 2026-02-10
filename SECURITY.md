# Política de Segurança e Controle de Acesso (RBAC)

Este documento detalha a arquitetura de segurança implementada no SIGF-Const, focando na proteção de dados e segregação de funções.

## 1. Visão Geral

O sistema utiliza o padrão **JWT (JSON Web Token)** para autenticação stateless. Isso significa que o servidor não guarda sessão; cada requisição do cliente deve enviar um token válido no cabeçalho `Authorization`.

### Níveis de Acesso (Roles)

| Cargo | Código (Role) | Permissões |
| :--- | :--- | :--- |
| **Administrador** | `admin` | Acesso total. Pode editar, excluir, exportar dados e gerenciar usuários. |
| **Gestor** | `manager` | Acesso similar ao Admin, focado na operação (Ver/Editar), mas sem gerenciar usuários. |
| **Motorista** | `driver` | Acesso restrito. Pode apenas enviar novos checklists e ver seu próprio histórico. |

## 2. Proteção de Rotas (Backend)

O backend FastAPI valida o token em cada endpoint crítico usando a dependência `get_current_user`.

| Método | Rota | Nível Exigido | Ação em caso de Falha |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/submit` | Público (ou Auth) | Permite envio (offline support). |
| `GET` | `/api/checklists` | `auth` | 401 Unauthorized. |
| `PUT` | `/api/checklists/{id}` | `admin`, `manager` | 403 Forbidden. |
| `DELETE` | `/api/checklists/{id}` | `admin`, `manager` | 403 Forbidden. |
| `GET` | `/api/export/excel` | `admin`, `manager` | 403 Forbidden. |

## 3. Proteção de Interface (Frontend)

Embora a segurança real esteja no backend, o frontend implementa "Guardas" para melhorar a UX:

*   **Redirecionamento de Login:** Se não houver token no `localStorage`, o usuário é enviado para `/login.html` imediatamente ao tentar abrir o App.
*   **Bloqueio de Admin:** Se um usuário com role `driver` tentar acessar `/admin.html`, um script verifica o payload do JWT e o redireciona de volta para `/index.html` com um alerta de "Acesso Negado".

## 4. Gerenciamento de Senhas

*   As senhas **NUNCA** são salvas em texto puro.
*   Utilizamos o algoritmo **Argon2** (padrão vencedor da competição de hashing de senhas) para hash e sal.
*   Bibliotecas: `passlib` + `argon2-cffi`.

## 5. Procedimento para Novos Usuários

Para adicionar novos funcionários, o administrador deve utilizar a API (futuro painel de gestão de usuários) ou o script de seed inicial:

```bash
python setup_users.py
```
