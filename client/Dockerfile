# Dockerfile.client
FROM python:3.9-slim

# Installer les dépendances
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN apt-get update && \
    pip install --no-cache-dir -r requirements.txt

# Copier le script de capture
COPY yolo_client.py /app/yolo_client.py
COPY yolov4-tiny.cfg /app/yolov4-tiny.cfg 
COPY yolov4-tiny.weights /app/yolov4-tiny.weights
COPY classes.txt /app/classes.txt

# Exécuter l'application
CMD ["python", "yolo_client.py"]
