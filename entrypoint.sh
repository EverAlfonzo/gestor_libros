#!/bin/bash
set -euo pipefail

# Cargar .env para comandos standalone (en compose ya se inyecta)
if [ -f .env ]; then
  set -o allexport; source .env; set +o allexport
fi

python manage.py migrate --noinput

# Crear superusuario si no existe
python - <<'PY'
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','core.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
u = os.getenv('DJANGO_SUPERUSER_USERNAME','admin')
e = os.getenv('DJANGO_SUPERUSER_EMAIL','admin@example.com')
p = os.getenv('DJANGO_SUPERUSER_PASSWORD','admin123')
if not User.objects.filter(username=u).exists():
    User.objects.create_superuser(username=u, email=e, password=p)
    print("Superusuario creado:", u)
else:
    print("Superusuario ya existe:", u)
PY


# Levantar dev server
python manage.py runserver 0.0.0.0:8000
