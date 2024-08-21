import random
import pygame
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# Initialize Pygame
pygame.init()

# Create Window/Display
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Catch the Ball")

# Initialize
fps = 30
clock = pygame.time.Clock()

# Load Background Image
background_image = pygame.image.load('./Resources/background.jpg').convert()
background_image = pygame.transform.scale(background_image, (width, height))

# Load and Resize Ball Image
imgBalloon = pygame.image.load('./Resources/redBall.png').convert_alpha()
imgBalloon = pygame.transform.scale(imgBalloon, (60, 60))  # Smaller ball size

# Get the rect for the resized image
rectBalloon = imgBalloon.get_rect()

# Variables
speed = 6
score = 0
rect_width = 200
rect_height = 50
rect_x = (width - rect_width) // 2
rect_y = height - rect_height
speed_rect = 20  # Slower catcher movement (reduce from 50 to 20)
flag = 0

# Load and Play Background Music
pygame.mixer.init()
pygame.mixer.Channel(0).play(pygame.mixer.Sound('./Resources/drum_beat_1.mp3'), loops=-1)

# Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)  # height

def resetBalloon():
    rectBalloon.x = random.randint(100, width - 100)
    rectBalloon.y = -50  # Start above the screen

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

# Start Menu
show_start_menu()

# Main Game Loop
start = True
while start:
    # Get Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    # Draw Background
    window.blit(background_image, (0, 0))

    # Capture and Process Frame
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    # Hand Detection Logic
    if hands:
        hand_type = hands[0]["type"]
        if hand_type == "Right" and rect_x < width - rect_width:
            rect_x += speed_rect  # Slower movement to the right
        elif hand_type == "Left" and rect_x > 0:
            rect_x -= speed_rect  # Slower movement to the left

    rectBalloon.y += speed

    # Collision Detection
    if flag == 0 and rectBalloon.y <= rect_y + 50 and rectBalloon.y >= rect_y - 5 and rectBalloon.x >= rect_x and rectBalloon.x < rect_x + rect_width:
        score += 1
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('./Resources/score_increase.mp3'))
        speed += 1  # Speed only increases when the score increases
        flag = 1
    
    if rectBalloon.y > height:
        flag = 0
        resetBalloon()

    # Draw Game Elements (Without Showing Camera Feed)
    window.blit(imgBalloon, rectBalloon)
    pygame.draw.rect(window, (0, 0, 0), (rect_x, rect_y, rect_width, rect_height))

    # Display Score
    font = pygame.font.Font(None, 50)
    text_score = font.render(str(score), True, (50, 50, 50))
    window.blit(text_score, (20, 20))

    # Update Display
    pygame.display.update()

    # Set FPS
    clock.tick(fps)
