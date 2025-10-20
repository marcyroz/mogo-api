# MOGO API 🚀

API Django com GeoDjango, PostgreSQL/PostGIS e JWT Authentication.

## 📋 Pré-requisitos

- Docker Desktop instalado e rodando
- Git

## 🔧 Instalação

1. **Clone o repositório:**
   ```bash
   git clone <seu-repositorio>
   cd mogo-api
   ```

2. **Configure as variáveis de ambiente:**
   ```bash
   # Windows
   copy .env.example .env

   # Linux/Mac
   cp .env.example .env
   ```

3. **Suba os containers:**
   ```bash
   docker-compose up -d --build
   ```

4. **Aguarde as migrações (primeira vez pode demorar ~2 minutos):**
   ```bash
   docker-compose logs -f api
   ```

   Você verá:
   ```
   Aguardando PostgreSQL...
   PostgreSQL pronto!
   Aplicando migrações...
   Coletando arquivos estáticos...
   Iniciando servidor...
   ```

5. **Acesse a API:**
   - API: http://localhost:8000
   - Admin: http://localhost:8000/admin

## 🛠️ Comandos úteis

```bash
# Ver logs
docker-compose logs -f

# Parar containers
docker-compose down

# Parar e limpar volumes (reseta banco)
docker-compose down -v

# Criar superusuário
docker-compose exec api python manage.py createsuperuser

# Rodar migrações manualmente
docker-compose exec api python manage.py migrate

# Entrar no container
docker-compose exec api bash
```

## 📁 Estrutura do Projeto

```
mogo-api/
├── docker-compose.yml    # Orquestração dos containers
├── Dockerfile            # Imagem da API
├── entrypoint.sh         # Script de inicialização
├── requirements.txt      # Dependências Python
├── .env.example          # Exemplo de variáveis de ambiente
└── mogo/                 # Código Django
    ├── manage.py
    ├── mogo/             # Settings
    ├── usuarios/         # App de usuários
    ├── navigation/       # App de navegação
    └── social/           # App social
```

## 🧪 Testar API

### Register (criar usuário):
```bash
curl -X POST http://localhost:8000/usuarios/usuario/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Maria",
    "sobrenome": "Silva",
    "email": "maria@email.com",
    "email_confirmation": "maria@email.com",
    "password": "Senha123!",
    "password_confirmation": "Senha123!",
    "aceita_termos": true,
    "aceita_privacidade": true
  }'
```

### Login:
```bash
curl -X POST http://localhost:8000/usuarios/usuario/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "maria@email.com",
    "password": "Senha123!"
  }'
```

## 🐛 Troubleshooting

### Container não inicia:
```bash
# Ver logs detalhados
docker-compose logs api

# Rebuild completo
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### Erro de conexão com banco:
```bash
# Verificar se o banco está rodando
docker-compose ps

# Deve mostrar "healthy" no container db
```

### Erro "permission denied" no entrypoint.sh:
```bash
# Garantir que tem permissão de execução
docker-compose exec api chmod +x /entrypoint.sh
```

## 👥 Equipe

- Vinicius 
- Johny
- Marcelly