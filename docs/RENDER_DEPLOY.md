# 🚀 Guia de Deploy no Render

## Pré-requisitos

- Projeto conectado ao GitHub
- Conta no [Render.com](https://render.com)
- (Opcional) Banco PostgreSQL no Supabase/Render

---

## ⚙️ Variáveis de Ambiente no Render

No dashboard do Render, configure as seguintes variáveis de ambiente:

### Obrigatórias
```
SECRET_KEY=sua_chave_secreta_muito_segura_aqui
DATABASE_URL=postgresql://usuario:senha@host:porta/banco_dados
```

### Opcionais
```
GA_MEASUREMENT_ID=seu_google_analytics_id
```

---

## 🗄️ Configurando o Banco de Dados

### Opção 1: PostgreSQL no Render (Recomendado)

1. No dashboard do Render, clique em **New +** → **PostgreSQL**
2. Configure o banco:
   - **Name**: `fuosteck-db`
   - **Region**: Mesmo da sua aplicação (ex: São Paulo)
   - Crie o banco

3. Após criar, pegue a **Internal Database URL** e configure como `DATABASE_URL` na sua web service

4. Aguarde ~5 minutos até o banco estar pronto

### Opção 2: PostgreSQL no Supabase

1. Acesse [supabase.com](https://supabase.com)
2. Crie um novo projeto
3. Vá para **Settings** → **Database** → copie a "Connection String"
4. Configure como `DATABASE_URL` no Render (substitua `[YOUR-PASSWORD]`)

### Opção 3: SQLite (Apenas Desenvolvimento)

- Se não configurar `DATABASE_URL`, usa `sqlite:///dev.db` (local)
- ⚠️ Em produção, não recomendado pois dados se perdem entre deploys

---

## 🔄 Processo de Deploy

1. **Push do código para GitHub**
   ```bash
   git add .
   git commit -m "Configuração de deploy"
   git push origin main
   ```

2. **Conectar no Render**
   - Clique em **New +** → **Web Service**
   - Conecte seu repositório GitHub
   - Configure:
     - **Name**: `fuosteck-app`
     - **Runtime**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`

3. **Adicione as Environment Variables** (conforme seção anterior)

4. **Deploy**
   - Clique em **Create Web Service**
   - Aguarde o deploy completar

---

## ✅ Inicializar o Banco de Dados

Se o deploy falhar no primeiro upload (esperado se o banco está lento):

### Opção 1: Comando CLI (Recomendado)

Na console do Render (durante/após deploy):
```bash
flask init-db
```

Ou via web service shell:
```bash
python -c "from app import app; app.app_context().push(); from src.database import db; db.create_all(); print('✅ OK')"
```

### Opção 2: Redeploy

Se o banco agora está pronto, faça um redeploy:
- Acesse o serviço no Render
- Clique em **Manual Deploy** → **Latest Commit**

---

## 🔍 Troubleshooting

### Erro: `connection to server at "localhost"...`

**Causa**: Variável `DATABASE_URL` apontando para localhost

**Solução**:
1. Verifique se `DATABASE_URL` está configurada corretamente no Render
2. Se usar PostgreSQL local, deve estar acessível pela internet (raramente funciona)
3. Use um banco gerenciado (Render PostgreSQL ou Supabase)

### Erro: `psycopg2.OperationalError`

**Causa**: Banco PostgreSQL não está pronto ainda

**Solução**:
1. Aguarde 5-10 minutos
2. Faça um redeploy
3. Se persistir, verifique credenciais de conexão

### Erro: `SQLALCHEMY_DATABASE_URI`

**Causa**: Banco não configurado

**Solução**: Adicione `DATABASE_URL` nas variáveis de ambiente do Render

---

## 🎯 Verificar o Deploy

1. Acesse a URL da aplicação (ex: `https://fuosteck-app.onrender.com`)
2. Verifique os logs no Render:
   - Console → **Logs** → veja output da aplicação
3. Teste endpoints:
   - `GET /` → Home page
   - `GET /demos/erp` → ERP demo
   - `GET /demos/booking` → Booking demo

---

## 📝 Notas Importantes

- **SQLite não é recomendado em produção** (dados se perdem em redeploy)
- **Backup do banco**: Configure backups automáticos no Render/Supabase
- **Environment Variables são case-sensitive**
- **Não commite arquivos `.env`** no git (use `.env.example`)
- Render desliza aplicações inativos, use **cron jobs** para keep-alive

---

## ❓ Dúvidas?

Consulte:
- [Documentação Render](https://render.com/docs)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Supabase Docs](https://supabase.com/docs)
