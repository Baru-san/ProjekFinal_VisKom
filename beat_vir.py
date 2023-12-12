import cv2
from cvzone.HandTrackingModule import HandDetector
import os
import random
import schedule
import time

class Button:
    def __init__(self, pos, radius, maxRadius, idle):

        self.pos = pos
        self.radius = radius
        self.visible = True
        self.maxRadius = maxRadius
        self.idle = idle

    def draw(self, img, color):
            cv2.circle(img, self.pos, (max(self.radius, self.maxRadius)), 
                        color, cv2.FILLED)
            cv2.circle(img, self.pos, (max(self.radius, self.maxRadius)), 
                        (50, 50, 50), 3)
        

        
    def clicked(self, x, y):
        if self.visible:
            if self.pos[0] - max(self.radius, self.maxRadius) < x < self.pos[0] + max(self.radius, self.maxRadius) and \
                self.pos[1] - max(self.radius, self.maxRadius) < y < self.pos[1] + max(self.radius, self.maxRadius):
                cv2.circle(img, self.pos, (max(self.radius+10, self.maxRadius+10)), 
                        (255, 255, 255), cv2.FILLED)
                cv2.circle(img, self.pos, (max(self.radius+10, self.maxRadius+10)), 
                            (50, 50, 50), 3)
                
                return True
            else:
                return False
        else:
            return False
        

    

def create_button():
        x = random.randint(0, 2)
        y = random.randint(0, 2)
        xpos = x * random.randint(300, 400) + random.randint(150, 250)
        ypos = y * random.randint(200, 250) + random.randint(75, 100)
        buttonList.append(Button((xpos, ypos), radius, maxRadius, buttonIdle))

#webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280) #width
cap.set(4, 720) #height
detector = HandDetector(detectionCon=0.8, maxHands=1)

#creating buttons

radius = 50
maxRadius = 100
maxDot = 0
buttonList = []
heatlh = 3


#variables
myEquation = ''
delayCounter = 0
dotCounter = 1
loop = True
skor = 0
buttonIdle = 1


#loop
while loop:
    #get image from webcam
    success, img = cap.read()
    img = cv2.flip(img, 1)

    #Detect Hand
    hands, img = detector.findHands(img, flipType=False)

    if heatlh > 0:
        if maxDot <= 3 and dotCounter % 15 == 0:
            create_button()
            maxDot += 1
        elif maxDot > 3:
            dotCounter = 1

        if dotCounter != 0:
            dotCounter += 1


        #draw all buttons
        for button in buttonList:
            if button.visible:
                if button.maxRadius >= button.radius:
                    button.maxRadius -= 1

                if button.maxRadius <= 50:
                    button.idle += 1

                if button.idle >= 20 and button.idle < 80: 
                    button.draw(img, (0, 0, 0))
                elif button.idle >= 80:
                    button.draw(img, (0, 0, 255))
                else:
                    button.draw(img, (225, 225, 225))

                if button.idle % 100 == 0:
                    heatlh -= 1
                    buttonList.clear()
                    maxDot = 0
                    

                

        for button in buttonList:
            if button.visible != True:
                buttonList.remove(button)
                
        

        #check for hand
        if hands:
            lmList = hands[0]['lmList']
            length, _, img = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
            x, y = lmList[8][:2]
            if length<=60:

                for i, button in enumerate(buttonList):
                    if button.clicked(x, y) and delayCounter == 0 :
                        button.visible = False
                        delayCounter = 1
                        maxDot -= 1
                        skor += 1

        

        cv2.rectangle(img, (40, 120), (200, 30),
                    (255, 255, 255), cv2.FILLED)
        cv2.rectangle(img, (40, 120), (200, 30),
                    (50, 50, 50), 3)
        
        cv2.putText(img, 'skor : ', (45, 65), cv2.FONT_HERSHEY_PLAIN, 2,
                    (200, 50, 50), 2)
        cv2.putText(img, str(skor), (150, 65), cv2.FONT_HERSHEY_PLAIN, 2,
                    (200, 50, 50), 2)
        
        cv2.putText(img, 'HP : ', (45, 100), cv2.FONT_HERSHEY_PLAIN, 2,
                    (200, 50, 50), 2)
        cv2.putText(img, str(heatlh), (150      , 100), cv2.FONT_HERSHEY_PLAIN, 2,
                        (200, 50, 50), 2)

        #avoid duplicates
        if delayCounter != 0:
            delayCounter += 1
            if delayCounter > 10:
                delayCounter = 0
    else:
        cv2.rectangle(img, (int(1280/3), int(720/4)), (800, 400),
                    (255, 255, 255), cv2.FILLED)
        cv2.rectangle(img, (int(1280/3), int(720/4)), (800, 400),
                    (0, 0, 0), 3)
        cv2.putText(img, 'Game berakhir ', (500, 220), cv2.FONT_HERSHEY_PLAIN, 2,
                    (200, 50, 50), 2)
        cv2.putText(img, str(skor), (600, 350), cv2.FONT_HERSHEY_PLAIN, 4,
                    (200, 50, 50), 4)

    #Display result

    #Display image
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord('c'):
        myEquation = ''
    elif key == ord('q'):
        loop = False