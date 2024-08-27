import random
import pygame
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

pygame.init()

width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Catch the Ball")

fps = 30
clock = pygame.time.Clock()

background_image = pygame.image.load('./Resources/background.jpg').convert()
background_image = pygame.transform.scale(background_image, (width, height))

imgBalloon = pygame.image.load('./Resources/redBall.png').convert_alpha()
imgBalloon = pygame.transform.scale(imgBalloon, (75, 75))  # Smaller ball size
rectBalloon = imgBalloon.get_rect()

imgHoop = pygame.image.load('./Resources/hoop2.png').convert_alpha()
imgHoop = pygame.transform.scale(imgHoop, (160, 137.14))
rectHoop = imgHoop.get_rect()

# Set the hoop position at the bottom of the screen
rectHoop.y = height - rectHoop.height

speed = 6
score = 0
speed_hoop = 20
flag = 0

pygame.mixer.init()
pygame.mixer.Channel(0).play(pygame.mixer.Sound('./Resources/drum_beat_1.mp3'), loops=-1)

# Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

def resetBalloon():
    rectBalloon.x = random.randint(100, width - 100)
    rectBalloon.y = -50

def show_start_menu():
    start = True
    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                start = False
        
        window.blit(background_image, (0, 0))
        font = pygame.font.Font(None, 100)
        title = font.render('Catch the Ball', True, (255, 255, 255))
        window.blit(title, (width//2 - title.get_width()//2, height//4))
        
        font = pygame.font.Font(None, 50)
        start_button = font.render('Start Game', True, (255, 255, 255))
        window.blit(start_button, (width//2 - start_button.get_width()//2, height//2))
        
        pygame.display.update()
        clock.tick(fps)

show_start_menu()

start = True
while start:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    window.blit(background_image, (0, 0))

    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        hand_type = hands[0]["type"]
        if hand_type == "Right" and rectHoop.x < width - rectHoop.width:
            rectHoop.x += speed_hoop  # Move the hoop to the right
        elif hand_type == "Left" and rectHoop.x > 0:
            rectHoop.x -= speed_hoop  # Move the hoop to the left

    rectBalloon.y += speed

    if flag == 0 and rectBalloon.colliderect(rectHoop):
        score += 1
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('./Resources/score_increase.mp3'))
        speed += 1  # Increase the balloon speed as the score increases
        flag = 1
    
    if rectBalloon.y > height:
        flag = 0
        resetBalloon()

    window.blit(imgBalloon, rectBalloon)
    window.blit(imgHoop, rectHoop)  # Draw the hoop at the bottom of the screen

    font = pygame.font.Font(None, 50)
    text_score = font.render(str(score), True, (50, 50, 50))
    window.blit(text_score, (20, 20))

    pygame.display.update()

    clock.tick(fps)
