import cv2
import face_recognition
import os
import numpy as np
# from gpiozero import LED
from time import sleep
# Import libraries
import RPi.GPIO as GPIO
import time

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

camera_ip = 'http://192.168.12.59:8080/video'
cv2.imread('ImageBase')
path = 'ImageBase'
cap = cv2.VideoCapture(camera_ip)
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

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

names()
encodeListKnown = findEncodings(images)
f = open("face_enc.txt", "wb")
f.write(pickle.dumps(data))
f.close()
print("Encoding Complete")
print(encodeListKnown)
