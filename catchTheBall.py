import random
import pygame
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time

pygame.init()

width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Catch the Ball")

fps = 30
clock = pygame.time.Clock()

background_image = pygame.image.load('./Resources/background.jpg').convert()
background_image = pygame.transform.scale(background_image, (width, height))

imgBalloon = pygame.image.load('./Resources/redBall.png').convert_alpha()
imgBalloon = pygame.transform.scale(imgBalloon, (75, 75))
rectBalloon = imgBalloon.get_rect()

imgHoop = pygame.image.load('./Resources/hoop2.png').convert_alpha()
imgHoop = pygame.transform.scale(imgHoop, (150, 125))
rectHoop = imgHoop.get_rect()

rectHoop.y = height - rectHoop.height

society_logo = pygame.image.load('./Resources/ACM logo.png').convert_alpha()
society_logo = pygame.transform.scale(society_logo, (200, 100))
logo_padding = 10
logo_rect = society_logo.get_rect(topright=(width - logo_padding, logo_padding))

speed = 6
score = 0
speed_hoop = 20
acceleration = 2
max_speed = 40
flag = 0

hoop_direction = None
hoop_move_start_time = 0

detector = HandDetector(detectionCon=0.8, maxHands=1)

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
        window.blit(society_logo, logo_rect) 

        font = pygame.font.Font(None, 100)
        title = font.render('Catch the Ball', True, (255, 255, 255))
        window.blit(title, (width//2 - title.get_width()//2, height//4))
        
        font = pygame.font.Font(None, 50)
        start_button_color = (255, 255, 255)
        mouse_pos = pygame.mouse.get_pos()
        start_button_rect = pygame.Rect(width//2 - 100, height//2 - 25, 200, 50)

        if start_button_rect.collidepoint(mouse_pos):
            start_button_color = (0, 0, 0) 
        
        start_button = font.render('Start Game', True, start_button_color)
        window.blit(start_button, (width//2 - start_button.get_width()//2, height//2))
        
        pygame.display.update()
        clock.tick(fps)

show_start_menu()

def show_end_menu(final_score):
    pygame.mixer.Channel(0).stop()
    end = True
    while end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button_rect.collidepoint(mouse_pos):
                    end = False
                    main_game_loop()

        window.blit(background_image, (0, 0))
        window.blit(society_logo, logo_rect)

        font = pygame.font.Font(None, 100)
        text_score = font.render(f'Your score: {str(final_score)}', True, (255, 255, 255))
        window.blit(text_score, (width//2 - text_score.get_width()//2, height//3))

        font = pygame.font.Font(None, 50)
        restart_button_color = (255, 255, 255)
        mouse_pos = pygame.mouse.get_pos()
        restart_button_rect = pygame.Rect(width//2 - 100, height//2 - 25, 200, 50)

        if restart_button_rect.collidepoint(mouse_pos):
            restart_button_color = (0, 0, 0)

        restart_button = font.render('Restart', True, restart_button_color)
        window.blit(restart_button, (width//2 - restart_button.get_width()//2, height//2))

        pygame.display.update()
        clock.tick(fps)

def main_game_loop():
    global score, speed, speed_hoop, flag, hoop_direction, hoop_move_start_time
    
    score = 0
    speed = 6
    speed_hoop = 20
    flag = 0
    hoop_direction = None
    hoop_move_start_time = 0

    pygame.mixer.Channel(0).play(pygame.mixer.Sound('./Resources/drum_beat_1.mp3'), loops=-1)

    start_time = time.time()
    initial_time = 45
    
    while True:
        remaining_time = int(initial_time - (time.time() - start_time))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        window.blit(background_image, (0, 0))
        window.blit(society_logo, logo_rect)  

        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)

        if hands:
            hand_type = hands[0]["type"]
            current_move_time = time.time()

            if hand_type == "Right":
                if hoop_direction == "Right":
                    time_held = current_move_time - hoop_move_start_time
                    speed_hoop = min(20 + acceleration * time_held, max_speed)
                else:
                    hoop_direction = "Right"
                    hoop_move_start_time = current_move_time
                    speed_hoop = 20
                
                if rectHoop.x < width - rectHoop.width:
                    rectHoop.x += speed_hoop  
            elif hand_type == "Left":
                if hoop_direction == "Left":
                    time_held = current_move_time - hoop_move_start_time
                    speed_hoop = min(20 + acceleration * time_held, max_speed)
                else:
                    hoop_direction = "Left"
                    hoop_move_start_time = current_move_time
                    speed_hoop = 20
                
                if rectHoop.x > 0:
                    rectHoop.x -= speed_hoop  

        rectBalloon.y += speed

        if flag == 0 and rectBalloon.colliderect(rectHoop):
            score += 1
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('./Resources/score_increase.mp3'))
            speed += 1  
            flag = 1
        
        if rectBalloon.y > height:
            flag = 0
            resetBalloon()

        window.blit(imgBalloon, rectBalloon)
        window.blit(imgHoop, rectHoop)  

        font = pygame.font.Font(None, 50)
        text_score = font.render(str(score), True, (50, 50, 50))
        window.blit(text_score, (20, 20))
        
        text_timer = font.render(f'Time Remaining: {str(remaining_time)}', True, (50, 50, 50))
        window.blit(text_timer, (475, 30))

        if remaining_time <= 0:
            show_end_menu(score)

        pygame.display.update()
        clock.tick(fps)

try:
    main_game_loop()

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    pygame.quit()
