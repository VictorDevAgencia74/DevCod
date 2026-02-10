# Guia de Modularização e Arquitetura - DevCod

Este documento explica a arquitetura atual do projeto e como você pode extrair módulos (como o Agendamento ou RPA) para transformá-los em produtos independentes ou microserviços.

## Arquitetura Atual: Monólito Modular
O projeto utiliza o padrão de **Application Factory** com **Blueprints**.
Isso significa que o código já está logicamente separado, mas roda no mesmo processo.

### Estrutura de Pastas
```
src/
├── controllers/          # Onde vivem os módulos (Blueprints)
│   ├── booking/          # Módulo de Agendamento (Lógica, Rotas)
│   ├── rpa/              # Módulo de Automação
│   ├── delivery/         # Módulo de Delivery
│   └── home_controller.py
├── services/             # Regras de Negócio (Reutilizáveis)
├── models/               # Tabelas do Banco de Dados
└── templates/            # Telas HTML (separadas por módulo)
```

---

## Como Extrair um Módulo (Ex: Agenda)
Imagine que o sistema de **Agendamento (`booking`)** cresceu e você quer vendê-lo como um SaaS separado ou rodá-lo em um servidor exclusivo.

### Passo 1: Isolar o Código
1.  Crie um novo repositório git: `flask-booking-service`.
2.  Copie a pasta `src/controllers/booking` para este novo repo.
3.  Copie os templates relacionados (`templates/booking`).
4.  Copie os modelos de banco de dados usados pelo booking (`src/models/booking_model.py`).

### Passo 2: Criar a Estrutura do Novo Projeto
No novo repositório, crie uma estrutura Flask básica para "receber" o módulo:

```
flask-booking-service/
├── app.py                # Novo ponto de entrada
├── booking/              # O código que você copiou (antigo controller)
│   ├── __init__.py       # Onde define o Blueprint
│   └── routes.py
├── templates/
│   └── booking/
└── requirements.txt
```

### Passo 3: Transformar em Pacote (Opcional - Para Reuso)
Se você quiser usar o `booking` em VÁRIOS projetos sem duplicar código, transforme-o em uma biblioteca Python instalável.

1.  Adicione um arquivo `setup.py` na raiz do novo repo:
    ```python
    from setuptools import setup, find_packages

    setup(
        name='my-booking-lib',
        version='1.0.0',
        packages=find_packages(),
        include_package_data=True,
        install_requires=[
            'Flask',
            'SQLAlchemy'
        ],
    )
    ```
2.  No projeto principal (DevCod), remova o código da pasta e instale via pip:
    ```bash
    pip install git+https://github.com/seu-usuario/flask-booking-service.git
    ```
3.  No `app.py` do DevCod, importe do pacote:
    ```python
    from my_booking_lib import booking_bp
    app.register_blueprint(booking_bp)
    ```

---

## Quando migrar para Microserviços?
Não faça isso prematuramente. Mantenha a estrutura atual (Monólito Modular) até ter um destes problemas:

1.  **Escala Diferenciada:** O módulo de RPA consome 100% da CPU processando bots, deixando o site de Delivery lento.
    *   *Solução:* Mova o RPA para um servidor separado (Microserviço).
2.  **Tecnologia Diferente:** Você quer reescrever o módulo de Delivery em Node.js ou Go.
    *   *Solução:* Separe o Delivery em uma API independente.
3.  **Times Diferentes:** Há 5 devs cuidando só do ERP e 3 cuidando só do EdTech, e eles vivem tendo conflito de merge.

### Como seria a comunicação?
Se você separar, os sistemas não podem mais importar funções Python um do outro. Eles devem se falar via **API REST**:

*   **Antes (Monólito):**
    ```python
    # No controller de Vendas
    from src.controllers.booking import verificar_disponibilidade
    if verificar_disponibilidade(data):
        ...
    ```

*   **Depois (Microserviço):**
    ```python
    # No controller de Vendas
    import requests
    resp = requests.get('https://api-booking.com/check', json={'data': data})
    if resp.json()['disponivel']:
        ...
    ```
