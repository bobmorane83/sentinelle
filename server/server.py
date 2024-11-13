from flask import Flask, request, render_template_string
from io import BytesIO
import base64
import time

app = Flask(__name__)

# Variables pour stocker l'image en mémoire et l'horodatage
last_image = None
last_image_time = 0

# Template HTML avec Bootstrap pour une interface moderne
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dernière Image Reçue</title>
    <!-- Lien vers Bootstrap CSS -->
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <script type="text/javascript">
        // Rafraîchit la page toutes les secondes
        setInterval(function() {
            window.location.reload();
        }, 1000);
    </script>
    <style>
        body { background-color: #f8f9fa; }
        .container { max-width: 600px; margin-top: 50px; }
        .img-container { text-align: center; margin-top: 20px; }
        .img-container img { width: 100%; max-width: 400px; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center">Dernière Image Reçue</h1>
        
        <div class="img-container">
            {% if image %}
                <img src="{{ image }}" alt="Image">
            {% else %}
                <p class="text-muted">Aucune image n'a été reçue pour le moment.</p>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/upload', methods=['POST'])
def upload_image():
    global last_image, last_image_time
    if 'image' not in request.files:
        return "", 400
    file = request.files['image']
    if file.filename == '':
        return "", 400

    # Stocker l'image en mémoire et mettre à jour l'horodatage
    image_stream = BytesIO()
    file.save(image_stream)
    image_stream.seek(0)
    last_image = image_stream
    last_image_time = time.time()  # Enregistrer l'heure de réception de l'image

    return "", 201

@app.route('/')
def show_image():
    global last_image, last_image_time
    # Vérifier si l'image a plus de 10 secondes
    image_data = None
    if last_image and (time.time() - last_image_time <= 10):
        # Si l'image a moins de 10 secondes, la convertir en base64 pour l'afficher
        image_data = f"data:image/png;base64,{base64.b64encode(last_image.getvalue()).decode()}"
    return render_template_string(html_template, image=image_data)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
