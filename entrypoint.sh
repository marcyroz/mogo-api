#!/bin/bash
set -e

echo "Aguardando PostgreSQL..."

# Esperar o banco estar disponível
until nc -z db 5432; do
  echo "Aguardando banco..."
  sleep 2
done

echo "PostgreSQL pronto!"

echo "Aplicando migrações..."
python manage.py migrate --noinput

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "Iniciando servidor..."

# Executar o comando passado como argumento (CMD)
exec "$@"