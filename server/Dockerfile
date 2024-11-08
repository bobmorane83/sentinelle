# Dockerfile.flask
FROM python:3.9-slim

# Installer les dépendances
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier l'application Flask
COPY server.py /app/server.py

# Créer le dossier de stockage des images
RUN mkdir /app/uploads

# Exposer le port Flask
EXPOSE 5000

# Démarrer l'application Flask
CMD ["python", "server.py"]