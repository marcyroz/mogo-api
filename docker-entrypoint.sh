#!/bin/bash

# Exit on error
set -e

echo "🔍 Aguardando PostgreSQL estar pronto..."

# Esperar o banco estar disponível
until nc -z db 5432; do
  echo "⏳ PostgreSQL ainda não está pronto - aguardando..."
  sleep 2
done

echo "✅ PostgreSQL está pronto!"

echo "🔄 Aplicando migrações..."
python manage.py migrate --noinput

echo "📦 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "🚀 Iniciando servidor..."
exec "$@"