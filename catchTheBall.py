#Import
import random
import pygame
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

#Initialize
pygame.init()

#Create Window/Display
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Catch the Ball")

#Initialize
fps = 30
clock = pygame.time.Clock()

#song
pygame.mixer.init()


#Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  #width
cap.set(4, 720)  #height

#Images
imgBalloon = pygame.image.load('./Resources/redBall.png').convert_alpha()
rectBalloon = imgBalloon.get_rect()



#Variables
speed = 6
score = 0
fingerIndex = False
fingerMiddle = False
flag = 0

#rectangle
rect_width = 200
rect_height = 50
rect_x = (width - rect_width) // 2
rect_y = height - rect_height
speed_rect = 50

#Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)


#main music
pygame.mixer.Channel(0).play(pygame.mixer.Sound('./Resources/drum_beat_1.mp3'), loops=-1)

def resetBalloon():
    rectBalloon.x = random.randint(100, img.shape[1]-100)
    rectBalloon.y = img.shape[0] - height + 50


#Main loop
start = True

while start:
    
    #Get Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    #Apply Logic
    window.fill((255, 0, 255))

    #OpenCV
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        n_fingers = detector.fingersUp(hands[0])
        # print(f'Fingers: {n_fingers}')
    
        # Example: Check if the index finger is up
        if n_fingers[1] == 1 and n_fingers[2] == 1 and rect_x < width-rect_width+10:
            print("Index finger is up")
            rect_x += speed_rect
        elif n_fingers[1] == 1 and rect_x > 0:
            print("Index finger is down")
            rect_x -= speed_rect
        elif n_fingers[1] == 0:
            rect_x += 0

    rectBalloon.y += speed

    print(f'rectBalloon.y: {rectBalloon.y}, rectBalloon.x: {rectBalloon.x}')
    print(f'rect_x: {rect_x}, rect_y: {rect_y}, rect_width: {rect_width}')

    #Collision logic
    if flag == 0 and rectBalloon.y <= rect_y+50 and rectBalloon.y >= rect_y - 5 and rectBalloon.x >= rect_x and rectBalloon.x < rect_x + rect_width:
        print("Collision detected")
        score+=1
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('./Resources/score_increase.mp3'))
        speed+=1
        flag = 1
    
    #Not collision logic
    if rectBalloon.y > height:
        flag = 0
        resetBalloon()
        speed+=1
        

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB = np.rot90(imgRGB)
    frame = pygame.surfarray.make_surface(imgRGB).convert()
    frame = pygame.transform.flip(frame, True, False)
    window.blit(frame, (0, 0))

    window.blit(imgBalloon, rectBalloon)
    pygame.draw.rect(window, (0, 0, 0), (rect_x, rect_y, rect_width, rect_height))

    font = pygame.font.Font(None, 50)
    text_score = font.render(str(score), True, (50, 50, 50))
    window.blit(text_score, (20, 20))
    
    #Update Display
    pygame.display.update()

    #Set FPS
    clock.tick(fps)
