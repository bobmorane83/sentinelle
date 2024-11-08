from flask import Flask, request, redirect, url_for, render_template_string, send_from_directory
from collections import deque
import os
# from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)

# Configuration pour le stockage des images
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# File de taille fixe pour stocker les 10 dernières images
image_queue = deque(maxlen=3)

# Template HTML pour afficher les images
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dernières Images Téléchargées</title>
</head>
<body>
    <h1>Dernières Images Téléchargées</h1>
    
    {% if images %}
        {% for image in images %}
            <div style="margin-bottom: 20px;">
                <img src="{{ url_for('uploaded_file', filename=image) }}" alt="Image" style="width:300px;">
            </div>
        {% endfor %}
    {% else %}
        <p>Aucune image n'a été téléchargée pour le moment.</p>
    {% endif %}
</body>
</html>
"""

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return "", 400
    file = request.files['image']
    if file.filename == '':
        return "", 400

    if file:
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # Ajout de l'image à la file de 10 images max
        image_queue.append(unique_filename)
    return "", 201

@app.route('/')
def show_images():
    return render_template_string(html_template, images=list(image_queue))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
