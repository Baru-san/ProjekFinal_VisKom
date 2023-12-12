import cv2
from cvzone.HandTrackingModule import HandDetector
import os
# import math
import re

class Button:
    def __init__(self, pos, width, height, value):

        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), 
                    (225, 225, 225), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), 
                    (50, 50, 50), 3)
        
        cv2.putText(img, self.value, (self.pos[0] + 40, self.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN, 2,
                    (50, 50, 50), 2)
        
    def clicked(self, x, y):

        if self.pos[0] < x < self.pos[0] + self.width and \
            self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), 
                    (255, 255, 255), cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), 
                        (50, 50, 50), 3)
            
            cv2.putText(img, self.value, (self.pos[0] + 25, self.pos[1] + 80), cv2.FONT_HERSHEY_PLAIN, 2,
                        (0, 0, 0), 5)
            return True
        else:
            return False

#webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280) #width
cap.set(4, 720) #height
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Get the center position of the screen
screen_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
screen_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
center_x = screen_width / 2
center_y = screen_height / 2

#creating buttons

buttonListValues = [
    ['7', '8', '9', '*'],
    ['4', '5', '6', '-'],
    ['1', '2', '3', '+'],
    ['0', '/', '.', '='],
    ['**', 'C'] # Clear button
]

# ...

buttonList = []
for i, value in enumerate(buttonListValues):
   for j, buttonValue in enumerate(value):
       xpos = int(center_x + i * 100 - 400) # Subtract 400 to center the buttons
       ypos = int(center_y + j * 100 - 350) # Subtract 350 to center the buttons
       buttonList.append(Button((xpos, ypos), 100, 100, buttonValue))
      
#variables
myEquation = ''
delayCounter = 0
loop = True
temp = ''
tes = ''

#loop
while loop:
    #get image from webcam
    success, img = cap.read()
    img = cv2.flip(img, 1)

    #Detect Hand
    hands, img = detector.findHands(img, flipType=False)

    #draw all buttons
    cv2.rectangle(img, (800, 50), (800 + 400, 70 + 100), 
                    (225, 225, 225), cv2.FILLED)
    cv2.rectangle(img, (800, 50), (800 + 400, 70 + 100), 
                    (50, 50, 50), 3)
    for button in buttonList:
        button.draw(img)
    #check for hand
    if hands:
        lmList = hands[0]['lmList']
        length, _, img = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
        x, y = lmList[8][:2]
        if length <= 60:
            for i, button in enumerate(buttonList):
                # print(f"i: {i}, len(buttonList): {len(buttonList)}, len(buttonListValues): {len(buttonListValues)}")
                if button.clicked(x, y) and delayCounter == 0:
                    print(button.value)
                    myValue = button.value
                    
                    # if myValue in ['sin', 'cos', 'tan', 'log']:
                    #     temp = myValue
                        
                    
                    if myValue == "=" and temp == '':
                        # Check if myEquation contains both a number and an operator
                        if re.search(r'\d', myEquation) and re.search(r'[+\-*/]', myEquation):
                            myEquation = str(eval(myEquation))
                        else:
                            print("Invalid equation. Please enter a number and an operator.")
                        
                    # elif temp in ['sin', 'cos', 'tan', 'log'] and myValue.isdigit():
                    #     if temp == 'sin':
                    #         tes += myValue
                    #         result = format(math.sin(float(tes)), '.10f')
                    #         myEquation += temp + '(' + myValue + ')'
                    #         myEquation = result
                    #     elif temp == 'cos':
                    #         result = format(math.cos(float(myValue)), '.10f')
                    #         myEquation += temp + '(' + myValue + ')'
                    #         myEquation = result
                    #     elif temp == 'tan':
                    #         result = format(math.tan(float(myValue)), '.10f')
                    #         myEquation += temp + '(' + myValue + ')'
                    #         myEquation = result
                    #     # elif temp == 'log':
                    #     #     if float(myValue) <= 0:
                    #     #         print("Cannot compute the logarithm of zero or a negative number")
                    #     #     else:
                    #     #         result = format(math.log10(float(myValue)), '.10f')
                    #     #         myEquation += temp + '(' + myValue + ')'
                    #     #         myEquation = result
                 
                    elif myValue == 'C':
                        myEquation = ''  # Clear the equation
                        myValue = ''
                        temp = ''
                    else:
                        myEquation += myValue
                


                    delayCounter = 1

    #avoid duplicates
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0

    if myEquation.isdigit() or myEquation.replace('.', '', 1).isdigit():
        cv2.putText(img, format(float(myEquation), '.9f'), (810, 117), cv2.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 3)
    else:
        cv2.putText(img, myEquation, (810, 117), cv2.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 3)

    #Display image
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord('c'):
        myEquation = ''
    elif key == ord('q'):
        loop = False