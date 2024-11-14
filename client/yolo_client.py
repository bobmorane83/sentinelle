import cv2
import requests
import time
import os
import signal
import sys

# Obtenir l'URL de l'API depuis les variables d'environnement
API_URL = os.getenv('API_URL', 'http://poc.faf.dev.gcp.renault.com:10002/upload')

# Prepare Yolo NN
Conf_threshold = 0.4
NMS_threshold = 0.4
COLORS = [(0, 255, 0), (0, 0, 255), (255, 0, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

class_name = []
with open('classes.txt', 'r') as f:
    class_name = [cname.strip() for cname in f.readlines()]

net = cv2.dnn.readNet('yolov4-tiny.weights', 'yolov4-tiny.cfg')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

starting_time = time.time()
frame_counter = 0
running = True  # Variable pour contrôler la boucle

def capture_image():
    global frame_counter
    cap = cv2.VideoCapture(2)

    if not cap.isOpened():
        print("Erreur: Impossible d'ouvrir la caméra.")
        return None

    ret, frame = cap.read()
    frame_counter += 1
    cap.release()

    classes, scores, boxes = model.detect(frame, Conf_threshold, NMS_threshold)
    for (classid, score, box) in zip(classes, scores, boxes):
        color = COLORS[int(classid) % len(COLORS)]
        label = "%s : %f" % (class_name[classid], score)
        cv2.rectangle(frame, box, color, 1)
        cv2.putText(frame, label, (box[0], box[1]-10),
                   cv2.FONT_HERSHEY_COMPLEX, 0.3, color, 1)
    endingTime = time.time() - starting_time
    fps = frame_counter / endingTime
    cv2.putText(frame, f'FPS: {fps}', (20, 50),
               cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

    if ret:
        image_path = 'captured_image.jpg'
        cv2.imwrite(image_path, frame)
        return image_path
    else:
        print("Erreur: Impossible de capturer l'image.")
        return None

def upload_image(image_path):
    with open(image_path, 'rb') as img:
        files = {'image': img}
        response = requests.post(API_URL, files=files)
    print(response)

def signal_handler(sig, frame):
    global running
    print("Signal d'arrêt reçu. Fermeture du programme...")
    running = False

if __name__ == '__main__':
    # Associer le gestionnaire de signal pour SIGINT et SIGTERM
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while running:
        image_path = capture_image()
        if image_path:
            upload_image(image_path)

    print("Nettoyage des ressources et sortie.")
