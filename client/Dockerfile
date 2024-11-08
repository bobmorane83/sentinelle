# Dockerfile.client
FROM python:3.9-slim

# Installer les dépendances
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN apt-get update && \
    pip install --no-cache-dir -r requirements.txt

# Copier le script de capture
COPY client.py /app/client.py

# Exécuter l'application
CMD ["python", "client.py"]