#!/usr/bin/env bash
set -euo pipefail

# Crear .env si no existe
if [ ! -f .env ]; then
  cat > .env <<'ENV'
DEBUG=True
SECRET_KEY=dev-secret
ALLOWED_HOSTS=*

POSTGRES_DB=books
POSTGRES_USER=books
POSTGRES_PASSWORD=books
POSTGRES_HOST=db
POSTGRES_PORT=5432

DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=admin123
ENV
fi

echo "Construyendo e iniciando contenedores..."
docker compose up -d --build


echo "Admin:   http://localhost:8000/admin/"
echo "API:     http://localhost:8000/api/"
echo "Swagger: http://localhost:8000/swagger/"
