#!/usr/bin/env python3
# Set up imports and paths
__file__="__file__"
bufferpath = "../../dataAcq/buffer/python"
sigProcPath = "../signalProc"
import pygame, sys
import pygame.locals
from pygame.locals import *
from time import sleep, time
import os
import matplotlib
matplotlib.rcParams['toolbar']='None'
from psychopy import visual, core
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),bufferpath))
import FieldTrip
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),sigProcPath))
import time
import numpy as np


class Alien(object):
    def __init__(self, screen, x, alienColor):
        '''
        Alien
        '''
        self._x = x
        self._y = int(screen.get_size()[0] * 0.06)
        self._y_now = self._y + 0  # Moving y
        self.size = int(round(screen.get_size()[0] * 0.05)) # Ball radius
        self.R_init = self.size + 0
        self.color = alienColor
        self.start_time = time.time() + 0
        self.screen = screen
        self.speed = int(screen.get_size()[1] * 0.16)  # Pixels per seconds.
        self.sprite =pygame.draw.circle(self.screen, self.color, (self._x, self._y_now), self.size)
        self.destroy = False
        self.Growth = 0.25 # Growth per second


    def move(self):
        '''
        Alien move down
        '''
        # Timing of movement
        time_passed = (time.time() - self.start_time)
        self._y_now = int(round(self._y + self.speed*time_passed))
        if self._y_now > screen.get_size()[1]:
            self.destroy = True

        # Growth alien
        self.size = int(self.R_init + time_passed*self.R_init*self.Growth)
        self.sprite = pygame.draw.circle(self.screen, self.color, (self._x, self._y_now), self.size)
        pass

class Cannonball(object):
    def __init__(self, screen, x, y):
        '''
        Constructor for cannonball.
        '''
        self._x = x
        self._y = y
        self._y_now = y + 0  # Moving y
        self.size = int(round(screen.get_size()[0] * 0.01)) # Ball radius
        self.color = (255, 255, 255)
        self.start_time = time.time() + 0
        self.screen = screen
        self.speed = int(round(screen.get_size()[1] * 0.25))  # Pixels per seconds. 16% of height
        self.sprite =[]
        self.destroy = False

    def move(self):
        '''
        initiates the cannonball to move until its past the screen
        '''
        time_passed = (time.time() - self.start_time)

        self._y_now = int(round(self._y - self.speed*time_passed))
        if self._y_now < 0:
            self.destroy = True


        self.sprite = pygame.draw.circle(self.screen, self.color, (self._x, self._y_now), self.size)
        pass

def hit_alien(Alien, Ball):
    """Checks Euclidean distance between alien and ball"""
    x_squared = (Alien._x - Ball._x) ** 2
    y_sqaured = (Alien._y_now - Ball._y_now) ** 2
    L2 = np.sqrt(x_squared + y_sqaured)
    hit = (L2 - Alien.size) <= 0
    return hit

def hit_forcefield(Alien, Ball):
    """Check if balls hit the forcefield of alien"""
    hit = Alien._y_now >= (Ball._y_now - Ball.size)
    return hit


# Initialize screen
ScreenWidth = 800
ScreenHeight = 500
pygame.init()
screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
clock = pygame.time.Clock()

# Init cannon
square_side = int(round(0.08 * ScreenHeight)) # Length of one side of square cannon
x = ScreenWidth /2 - square_side# Start position cannon
y = ScreenHeight - square_side # Static height cannon
colorCannon = (255, 255, 255)
MoveSpeed = 0.00625 # Move with speed % pixels of ScreenWdith

# Inits balls
balls=[]
ball_time = time.time()
space_tmp  = 0 # Space bar hasn't been pushed yet

# Inits aliens
leftAliens=[]
rightAliens=[]
alien_time = time.time()
alien_secs = 3 # 1 alien per 3 sec
alien_start = 1 # For fist alien
alienColorRight = (0, 0, 255)
alienColorLeft = (255, 0, 0)

# Alien frequencies
left_hz = 16
right_hz = 8

left_time = time.time()
right_time = time.time()


# Emergency looks
left_time_IC = time.time()
right_time_IC = time.time()
right_IC_color = alienColorRight
left_IC_color = alienColorLeft
IC_side = int(round(0.1 * ScreenHeight))

# Count inits
start_time = time.time()
shots_fired = 0
hit_score = 0

# Text inits
if 'font' not in locals():
    font = pygame.font.Font(None, int(ScreenHeight * 0.03)) # Python crashes if SysFont is called > 1 XOR specified font
text_y = int(round(ScreenHeight * 0.01))
x_time = int(round(ScreenWidth * 0.025))
x_static = int(round(ScreenWidth * 0.16))
x_shots = int(round(ScreenWidth * 0.17))
x_static2 = int(round(ScreenWidth * 0.27))
x_score = int(round(ScreenWidth * 0.29))
x_static3 = int(round(ScreenWidth * 0.365))
x_accuracy = int(round(ScreenWidth * 0.37))

textColor = (150, 150, 150) # So the bullet over it don't hide the text

# Autofire
fire_hz = 5
fire_last = time.time()

## Game loop
done = False


# pygame.draw.line(screen, (255, 0, 0), (0, rightAliens[0]._x), (screen.get_size()[0], rightAliens[0]._y_now), 1)


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.quit() # Close window

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        if (x <= 0): x -= 0 # If window limit left reached, dont do squat.
        else: x -= int(round(ScreenWidth * MoveSpeed))

    if pressed[pygame.K_RIGHT]:
        if (x >= ScreenWidth - square_side): x +=0 # If window limit right reached, don't do squat.
        else: x += int(round(ScreenWidth * MoveSpeed))
    # Check for shots
    if pressed[pygame.K_SPACE] and (space_tmp==0): space_tmp=1 # Now you can check for release space

    if (event.type == pygame.KEYUP and event.key == pygame.K_SPACE) and space_tmp: # If space pushed and released
        balls.append(Cannonball(screen, x + square_side/2, y + square_side/2))
        space_tmp = 0 # Now don't check for release anymore
        shots_fired += 1

    if (time.time() - fire_last) >= (1.0/fire_hz):
        balls.append(Cannonball(screen, x + square_side/2, y + square_side/2))
        space_tmp = 0 # Now don't check for release anymore
        shots_fired += 1
        fire_last = time.time()

    # Set screen dark for update
    screen.fill((0, 0, 0))

    # Draw constant emergency SSVEP's
    if ((time.time() - left_time_IC) >= (1.0 / left_hz)):
        pygame.draw.rect(screen, left_IC_color, pygame.Rect(0, ScreenHeight - IC_side, IC_side, IC_side))  # Square cannon
        left_time_IC = time.time()

    if ((time.time() - right_time_IC) >= (1.0 / right_hz)):
        pygame.draw.rect(screen, right_IC_color, pygame.Rect(ScreenWidth - IC_side, ScreenHeight-IC_side, IC_side, IC_side))  # Square cannon
        right_time_IC = time.time()


    # Draw the cannon position
    pygame.draw.rect(screen, colorCannon, pygame.Rect(x, y, square_side, square_side)) # Square cannon
    pygame.draw.circle(screen, (0,0,0), (x+square_side/2, y), square_side/3) # Fake inside gun


    # Create aliens
    if ((time.time() - alien_time) >= 3) or alien_start:
        x_position = np.random.randint(0, ScreenWidth)
        if x_position >= (ScreenWidth/2.0): # Create right aliens:
            rightAliens.append(Alien(screen, x_position, alienColorRight))
            alien_time = time.time()
            alien_start = 0
        else: # Create left aliens
            leftAliens.append(Alien(screen, x_position, alienColorLeft))
            alien_time = time.time()
            alien_start = 0

    # Force field line loop - so that forcefield is not in transparant alien
    if len(rightAliens)>0:
        for i in list(reversed(range(len(rightAliens)))):
            pygame.draw.line(screen, (255, 0, 0), (0, rightAliens[i]._y_now), (rightAliens[i]._x - rightAliens[i].size, rightAliens[i]._y_now), 1)
            pygame.draw.line(screen, (255, 0, 0), (rightAliens[i]._x + rightAliens[i].size, rightAliens[i]._y_now),(screen.get_size()[0], rightAliens[i]._y_now), 1)

    if len(leftAliens) > 0:
        for i in list(reversed(range(len(leftAliens)))):
            pygame.draw.line(screen, (255, 0, 0), (0, leftAliens[i]._y_now), (leftAliens[i]._x - leftAliens[i].size, leftAliens[i]._y_now), 1)
            pygame.draw.line(screen, (255, 0, 0), (leftAliens[i]._x + leftAliens[i].size, leftAliens[i]._y_now),(screen.get_size()[0], leftAliens[i]._y_now), 1)


    # LEFTIES Move aliens and remove if hit or out of range
    if (time.time() - left_time) >= (1.0 / left_hz):

        if len(leftAliens)>0:
            for i in list(reversed(range(len(leftAliens)))):
                leftAliens[i].move()

                if leftAliens[i].destroy:
                    leftAliens.remove(leftAliens[i])


            if len(balls) > 0:
                for i in list(reversed(range(len(balls)))):
                    if len(leftAliens)>0:
                        if hit_alien(leftAliens[0],balls[i]):
                            leftAliens.remove(leftAliens[0])
                            balls.remove(balls[i])
                            hit_score += 1
            left_time = time.time()


    # RIGHTIES Move aliens and remove if hit or out of range
    if (time.time() - right_time) >= (1.0 / right_hz):
        if len(rightAliens) > 0:
            for i in list(reversed(range(len(rightAliens)))):
                rightAliens[i].move()

                if rightAliens[i].destroy:
                    rightAliens.remove(rightAliens[i])

            if len(balls) > 0:
                for i in list(reversed(range(len(balls)))):
                    if len(rightAliens) > 0:
                        if hit_alien(rightAliens[0], balls[i]):
                            rightAliens.remove(rightAliens[0])
                            balls.remove(balls[i])
                            hit_score += 1
            right_time = time.time()


    # Update balls position and delete if hit forcefield or out of FOV
    if len(balls)>0:
        for i in list(reversed(range(len(balls)))):  # Reversed because if 1 is del, index out of range..
            balls[i].move()

            if balls[i].destroy:
                balls.remove(balls[i])

            if len(leftAliens)> 0 and len(balls)>0:
                if hit_forcefield(leftAliens[0], balls[i]):
                    balls.remove(balls[i])

            if len(rightAliens)>0 and len(balls)>0:
                if hit_forcefield(rightAliens[0], balls[i]):
                    balls.remove(balls[i])



    # Text time on screen
    now_time = time.time()
    time_played = round(now_time - start_time, 2)
    text_time = 'Time played: ' + str(time_played) + 's'
    text = font.render(text_time, True, textColor)
    screen.blit(text, (x_time, text_y))

    # Text shots on screen
    text_shots = 'Shots fired: ' + str(shots_fired)
    text = font.render(text_shots, True, textColor)
    screen.blit(text, (x_shots, text_y))

    # Text score
    text_hits = 'Hits: ' + str(hit_score)
    text = font.render(text_hits, True, textColor)
    screen.blit(text, (x_score, text_y))

    # Text accuracy
    text_acc = 'Accuracy: ' + str(round(hit_score/(shots_fired +0.000001),1)) + '%'
    text = font.render(text_acc, True, textColor)
    screen.blit(text, (x_accuracy, text_y))

    # Text statics
    text_static = '|'
    text = font.render(text_static, True, textColor)
    screen.blit(text, (x_static, text_y))

    text_static = '|'
    text = font.render(text_static, True, textColor)
    screen.blit(text, (x_static2, text_y))

    text_static = '|'
    text = font.render(text_static, True, textColor)
    screen.blit(text, (x_static3, text_y))


    # Update screen
    pygame.display.flip() # Update screen
    clock.tick(60) # Set response pygame rate fo 60fps




# pygame.quit()
