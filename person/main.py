import cv2
import imutils
import numpy as np
import argparse

def detect(frame):
    bounding_box_cordinates, weights =  HOGCV.detectMultiScale(frame, winStride = (4, 4), padding = (8, 8), scale = 1.03)
    
    person = 1
    for x,y,w,h in bounding_box_cordinates:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(frame, f'person {person}', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
        person += 1
    
    cv2.putText(frame, 'Status : Detecting ', (40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
    cv2.putText(frame, f'Total Persons : {person-1}', (40,70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)

    print("Person :", person)
#    cv2.imshow('output', frame)

    return frame


def detectByCamera():
    video = cv2.VideoCapture(0)
    print('Detecting people...')

    n = 0
    digit = len(str(int(video.get(cv2.CAP_PROP_FRAME_COUNT))))
    ext = 'jpg'

    for i in range(20):
        check, frame = video.read()

        frame = detect(frame)
        cv2.imwrite('{}_{}.{}'.format('image', str(n).zfill(digit), ext), frame)
        n += 1

    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    HOGCV = cv2.HOGDescriptor()
    HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    detectByCamera()

