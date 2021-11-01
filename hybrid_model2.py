import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import urllib.request
import pyttsx3


engine = pyttsx3.init()

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)
human = cv2.CascadeClassifier("gesture_automation/Resources/haarcascade_frontalface_default.xml")
i = 0
cap.set(10,50)
c1, c2, c3, c4 = 0, 0, 0, 0
led1_on = "http://192.168.43.88/H"
led2_on = "http://192.168.43.88/O"
led1_off = "http://192.168.43.88/L"
led2_off = "http://192.168.43.88/F"
while True:
    success, img = cap.read()
    
    hands, img = detector.findHands(img)
    iGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face = human.detectMultiScale(iGray, 1.1, 4)

    for (x, y, w, h) in face:
            #cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            i = 0
    i +=1
    
    if i == 100 :
        print("no one in the room...")
        engine.say("no one in room...")
        urllib.request.urlopen(led1_off)
        urllib.request.urlopen(led2_off)

    if hands:
        hand1 = hands[0]
        finger = detector.fingersUp(hand1)
        if finger == [0, 1, 0, 0, 0]:
            c2, c3, c4 = 0, 0, 0
            print("process",c1,"%")
            c1 +=5
        elif finger == [1, 1, 1, 1, 1]:
            c1, c3, c4 = 0, 0, 0
            print("process",c2,"%")
            c2 +=5
        elif finger == [1, 0, 0, 0, 0]:
            c1, c2, c4 = 0, 0, 0
            print("process",c3,"%")
            c3 +=5
        elif finger == [1, 1, 0, 0, 0]:
            c1, c2, c3 = 0, 0, 0
            print("process",c4,"%")
            c4 += 5


        if c1 == 50 :
            print("first led...")
            engine.say("L E D is on  ")
            urllib.request.urlopen(led1_on)
            urllib.request.urlopen(led2_off)
            c1, c2, c3, c4 = 0, 0, 0, 0
            time.sleep(2) 
        elif c2 == 50 :
            print("off all led...")
            engine.say("turn off all L E D")
            urllib.request.urlopen(led1_off)
            urllib.request.urlopen(led2_off)
            c1, c2, c3, c4 = 0, 0, 0, 0
            time.sleep(2)
        elif c3 == 50 :
            print("second led...")
            engine.say("L E D is on")
            urllib.request.urlopen(led2_on)
            urllib.request.urlopen(led1_off)
            c1, c2, c3, c4 = 0, 0, 0, 0
            time.sleep(2)
        elif c4 == 50 :
            print("both led ...")
            engine.say("turn on all L E D")
            urllib.request.urlopen(led1_on)
            urllib.request.urlopen(led2_on)
            c1, c2, c3, c4 = 0, 0, 0, 0
            time.sleep(2)

    
    engine.runAndWait()
    cv2.imshow("camera", img)
    if cv2.waitKey(10)& 0xFF ==ord(' '):
        break