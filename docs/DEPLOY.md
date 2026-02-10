# Guia de Deploy - DevCod

Este documento explica como colocar a aplicação Flask `DevCod` em produção.

## Pré-requisitos Gerais
1.  **Repositório Git:** O código deve estar em um repositório (GitHub, GitLab, etc).
2.  **Requirements:** O arquivo `requirements.txt` deve estar atualizado (incluindo `gunicorn` e `whitenoise`).
3.  **Variáveis de Ambiente:** Em produção, nunca "chumbe" senhas no código. Use variáveis de ambiente (`SECRET_KEY`, `DATABASE_URL`).

---

## Opção 1: Render (Recomendado - Moderno e Fácil)
O Render é uma plataforma PaaS (Platform as a Service) excelente para Flask.

### Passos:
1.  Crie uma conta em [render.com](https://render.com).
2.  Clique em **New +** e selecione **Web Service**.
3.  Conecte seu repositório GitHub.
4.  Configure o serviço:
    *   **Name:** `devcod-portfolio`
    *   **Runtime:** `Python 3`
    *   **Build Command:** `pip install -r requirements.txt`
    *   **Start Command:** `gunicorn app:app`
5.  **Environment Variables (Advanced):**
    *   Adicione `SECRET_KEY` = `(gere uma string aleatória)`
    *   Adicione `DATABASE_URL` = `(sua string de conexão Postgres/Supabase)`
6.  Clique em **Create Web Service**.

**Vantagem:** O HTTPS é configurado automaticamente e o deploy é contínuo (push no git = deploy novo).

---

## Opção 2: PythonAnywhere (Tradicional)
Ideal para projetos menores ou se você prefere uma abordagem mais manual via painel.

### Passos:
1.  Crie conta em [pythonanywhere.com](https://www.pythonanywhere.com/).
2.  Vá em **Web** -> **Add a new web app**.
3.  Escolha **Manual Configuration** (Python 3.10).
4.  Abra o **Console Bash** e configure o projeto:
    ```bash
    git clone https://github.com/seu-usuario/devcod.git
    cd devcod
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
5.  Volte na aba **Web** e configure:
    *   **Virtualenv:** `/home/seuusuario/devcod/venv`
    *   **WSGI Configuration File:** Clique para editar e deixe assim:
        ```python
        import sys
        import os
        from dotenv import load_dotenv

        path = '/home/seuusuario/devcod'
        if path not in sys.path:
            sys.path.append(path)

        project_folder = os.path.expanduser('~/devcod')
        load_dotenv(os.path.join(project_folder, '.env'))

        from app import create_app
        application = create_app()
        ```
6.  Clique em **Reload**.

---

## Opção 3: VPS (DigitalOcean / AWS - Avançado)
Para controle total do servidor (Linux Ubuntu).

### 1. Preparar Servidor
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx git
```

### 2. Configurar Aplicação
```bash
cd /var/www
git clone https://github.com/seu-usuario/devcod.git
cd devcod
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Criar Serviço Gunicorn
Crie o arquivo `/etc/systemd/system/devcod.service`:
```ini
[Unit]
Description=Gunicorn instance to serve DevCod
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/devcod
Environment="PATH=/var/www/devcod/venv/bin"
EnvironmentFile=/var/www/devcod/.env
ExecStart=/var/www/devcod/venv/bin/gunicorn --workers 3 --bind unix:devcod.sock -m 007 app:app

[Install]
WantedBy=multi-user.target
```
Ative: `sudo systemctl start devcod && sudo systemctl enable devcod`

### 4. Configurar Nginx (Proxy Reverso)
Crie `/etc/nginx/sites-available/devcod`:
```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/devcod/devcod.sock;
    }

    # Servir estáticos diretamente (mais rápido)
    location /assets {
        alias /var/www/devcod/assets;
    }
}
```
Ative:
```bash
sudo ln -s /etc/nginx/sites-available/devcod /etc/nginx/sites-enabled
sudo systemctl restart nginx
```

### 5. SSL (HTTPS)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d seu-dominio.com
```
