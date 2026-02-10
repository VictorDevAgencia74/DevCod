# Documentação de Testes - SIGF-Const

Este documento descreve a estratégia de testes e como executar a suíte de validação automatizada do projeto.

## 🛠️ Tecnologias de Teste

*   **Framework:** `pytest` (Padrão de indústria para Python).
*   **Cliente HTTP:** `TestClient` (do FastAPI/Starlette) para simular requisições sem subir o servidor.
*   **Banco de Dados:** SQLite em Memória (`sqlite://`) para garantir que os testes não afetem os dados reais de produção.

## 🧪 O que está sendo testado?

O arquivo `tests/test_main.py` cobre os seguintes cenários críticos:

1.  **Configuração (Schema):** Verifica se o JSON de configuração dos checklists é servido corretamente.
2.  **Autenticação (Auth):**
    *   Criação de usuários.
    *   Login bem-sucedido (Geração de Token JWT).
3.  **Fluxo de Envio (Submit):**
    *   Simula um motorista enviando um checklist preenchido.
    *   Verifica se o backend salva e retorna ID.
4.  **Segurança (RBAC - Role Based Access Control):**
    *   Garante que usuários anônimos **não acessem** rotas administrativas.
    *   Garante que motoristas (`driver`) **não consigam** exportar Excel ou deletar dados.
    *   Verifica se administradores (`admin`) têm acesso liberado.

## ▶️ Como Executar os Testes

Com o ambiente virtual ativado, execute o comando abaixo na raiz do projeto:

```bash
pytest
```

### Saída Esperada

Se tudo estiver correto, você verá algo como:

```text
tests/test_main.py .....                                                     [100%]

============================== 5 passed in 0.45s ===============================
```

*   **. (ponto):** Significa que o teste passou.
*   **F (Fail):** Significa que falhou (o log mostrará o motivo).

## 📝 Adicionando Novos Testes

Ao criar novas funcionalidades no `backend/main.py`:
1.  Crie uma nova função em `tests/test_main.py` começando com `test_`.
2.  Use `client.get()`, `client.post()`, etc.
3.  Use `assert` para validar o `status_code` e o JSON de resposta.
