import cv2
import face_recognition
import os
import numpy as np
# from gpiozero import LED
from time import sleep
# Import libraries
import RPi.GPIO as GPIO
import time
from imutils import paths
import pickle


# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Set pin 11 as an output, and define as servo1 as PWM pin
GPIO.setup(22,GPIO.OUT)
servo1 = GPIO.PWM(22,50) # pin 11 for servo1, pulse 50Hz

# Start PWM running, with value of 0 (pulse off)
servo1.start(0)


def gate(status):
    if (status == 0) :
       servo1.ChangeDutyCycle(2+(0/18))
       time.sleep(0.4)
       servo1.ChangeDutyCycle(0)
    else :
        servo1.ChangeDutyCycle(2+(180/18))
        time.sleep(0.5)
        servo1.ChangeDutyCycle(0)
# gate(0)

a = 0

#camera_ip = 'http://192.168.12.59:8080/video'
cv2.imread('ImageBase')
path = 'ImageBase'
cap = cv2.VideoCapture(0)
images = []
image_name = []



def names():
    images_list = os.listdir(path)
    print(images_list)
    for cl in images_list:
        curImage = cv2.imread(f'{path}/{cl}') 
        images.append(curImage)
        image_name.append(os.path.splitext(cl)[0])
        print(image_name)

# not its disabled code
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

names()
encodeListKnown = pickle.loads(open('face_enc.txt', "rb").read())
# encodeListKnown = findEncodings(images)


print("Encoding Complete")
print(encodeListKnown)

count = 0
while a==0:
    count += 1
    success, img = cap.read()
    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, face_loc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace, tolerance=0.5)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
    
        print(faceDis)

        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = image_name[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = face_loc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img,(x1, y1), (x2, y2), (0, 255, 0), 2)
            #cv2.rectangle(img, (x1, y2-35), (y2, y2),(0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            gate(1)
            a = 1
            break
        else :    
            name = image_name[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = face_loc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img,(x1, y1), (x2, y2), (0, 255, 0), 2)
            #cv2.rectangle(img, (x1, y2-35), (y2, y2),(0, 255, 0), cv2.FILLED)
            cv2.putText(img, "unknown", (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            # gate(0)
            break

    
    cv2.imshow("Webcam", img)

    if a==1:
        time.sleep(5)
        gate(0)
        #Clean things up at the end
        servo1.stop()
        GPIO.cleanup()
        print("Servo Stop")

    if cv2.waitKey(25) & 0xFF == ord('q'):
        a = 1
        # print(count)
        
    cv2.waitKey(1)


