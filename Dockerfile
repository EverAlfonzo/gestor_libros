# Etapa 1: Etapa de construcción base
FROM python:3.10-slim AS builder

# Crear el directorio de la aplicación
RUN mkdir /app

# Establecer el directorio de trabajo
WORKDIR /app

# Establecer variables de entorno para optimizar Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Actualizar pip e instalar dependencias
RUN pip install --upgrade pip

# Copiar el archivo de requerimientos primero (mejor caché)
COPY requirements.txt /app/

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Etapa 2: Etapa de producción 
FROM python:3.10-slim

RUN useradd -m -r appuser && \
   mkdir /app && \
   chown -R appuser /app

# Copiar las dependencias de Python desde la etapa de construcción
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Establecer el directorio de trabajo
WORKDIR /app



# Copiar el código de la aplicación
COPY --chown=appuser:appuser . .
RUN mkdir -p /app/staticfiles
RUN chown -R appuser:appuser /app/staticfiles
RUN chmod +x /app/entrypoint.sh
# Establecer variables de entorno para optimizar Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Ensure access.log exists and is writable by appuser
RUN touch /app/access.log && chown appuser:appuser /app/access.log

# Cambiar a usuario no root
USER appuser
