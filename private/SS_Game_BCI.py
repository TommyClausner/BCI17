import pygame, sys
import pygame.locals
from pygame.locals import *
from time import sleep, time
import os
import matplotlib

matplotlib.rcParams['toolbar']='None'

main_path=os.path.dirname(os.path.abspath(__file__))+os.sep+'..'+os.sep


BCI_buff_path="external"+os.sep
bufferpath = BCI_buff_path+"dataAcq"+os.sep+"buffer"+os.sep+"python"
sigProcPath = BCI_buff_path+"python"+os.sep+"signalProc"
assetpath="assets"+os.sep+"GUI_grafix"
functionspath="private"+os.sep

# add paths
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),main_path+bufferpath))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),main_path+sigProcPath))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),main_path+assetpath))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),main_path+functionspath))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),main_path+BCI_buff_path))


import time
import numpy as np
import platform
from PIL import Image

##### BCI enable #######
if __name__ == "__main__":
    if len(sys.argv) > 1:
        braincontrol = int(sys.argv[1])
        color = int(sys.argv[2])
    else:
        braincontrol = 0
        color = 1
else:
    braincontrol = 0
    color = 1
print(braincontrol)
print(color)
if braincontrol:
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),bufferpath))
    import FieldTrip
    import bufhelp
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),sigProcPath))

    ## CONFIGURABLE VARIABLES
    # Connection options of fieldtrip, hostname and port of the computer running the fieldtrip buffer.
    hostname='localhost'
    port=1972

    ## init connection to the buffer
    timeout=5000
    (ftc,hdr) = bufhelp.connect(hostname,port)

    # Wait until the buffer connects correctly and returns a valid header
    hdr = None
    while hdr is None :
        print(('Trying to connect to buffer on %s:%i ...'%(hostname,port)))
        try:
            ftc.connect(hostname, port)
            print('\nConnected - trying to read header...')
            hdr = ftc.getHeader()
        except IOError:
            pass

        if hdr is None:
            print('Invalid Header... waiting')
            sleep(1)
        else:
            print(hdr)
            print((hdr.labels))
    fSample = hdr.fSample

    def sendEvent(event_type, event_value=1, sample=-1):
        e = FieldTrip.Event()
        e.type=event_type
        e.value=event_value
        e.sample=sample
        ftc.putEvents(e)
#######################

BCI_buff_path="external"+os.sep
bufferpath = BCI_buff_path+"dataAcq"+os.sep+"buffer"+os.sep+"python"
sigProcPath = BCI_buff_path+"python"+os.sep+"signalProc"
assetpath=main_path+"assets"+os.sep

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),bufferpath))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),sigProcPath))

class Alien(object):
    def __init__(self, screen, x, alienColor, hz, image):
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
        self.Force = pygame.draw.line(self.screen, (255, 0, 0), (0, self._y_now), (screen.get_size()[0], self._y_now), 1)
        self.destroy = False
        self.Growth = 0.25 # Growth per second

        self.hz = hz
        self.image = image
        self.sprite = self.screen.blit(self.image, (self._x - self.image.get_rect()[2]/2, self._y_now -  self.image.get_rect()[3]/2))
        self.time_hz = time.time()


    def move(self):
        '''
        Alien move down
        '''
        # Timing of movement
        time_passed = (time.time() - self.start_time)


        self._y_now = int(round(self._y + self.speed*time_passed))
        if self._y_now > screen.get_size()[1]*0.9:
            self.destroy = True

        # Growth alien
        self.size = int(self.R_init + time_passed*self.R_init*self.Growth)

        self.image = pygame.transform.scale(self.image, (int(self.screen.get_size()[0] *0.001 + self.size *2), int(self.screen.get_size()[1]*0.001 + self.size*2)))

        # self.Force = pygame.draw.line(self.screen, (255, 0, 0), (0, self._y_now), (screen.get_size()[0], self._y_now), 1)
        pygame.draw.line(screen, (255, 0, 0), (0, self._y_now),(self._x - self.size, self._y_now), 1)
        pygame.draw.line(screen, (255, 0, 0), (self._x + self.size, self._y_now),(self.screen.get_size()[0], self._y_now), 1)

        if (time.time() - self.time_hz) >= (1.0 / self.hz):
            # self.sprite = pygame.draw.circle(self.screen, self.color, (self._x, self._y_now), self.size)
            self.screen.blit(self.image, (self._x - self.image.get_rect()[2]/2, self._y_now -  self.image.get_rect()[3]/2))
            self.time_hz = time.time()
        pass

class BonusAlien(object):
    def __init__(self, screen, x, y, image):
        '''
        Bonus Alien
        '''
        self._x = x
        self._y = y
        self._y_now = y
        self.size = int(round(screen.get_size()[0] * 0.05)) # Ball radius
        self.R_init = self.size + 0
        self.color = (0,255,0)
        self.start_time = time.time() + 0
        self.screen = screen
        self.image = image
        self.sprite = self.screen.blit(self.image, (self._x - self.image.get_rect()[2] / 2, self._y_now - self.image.get_rect()[3] / 2))
        self.destroy = False




    def update(self):
        '''
        Alien move down
        '''
        # Timing of movement
        time_passed = (time.time() - self.start_time)

        if time_passed >= 3:
            self.destroy = True

        # self.sprite = pygame.draw.circle(self.screen, self.color, (self._x, self._y), self.size)
        self.screen.blit(self.image, (self._x - self.image.get_rect()[2] / 2, self._y_now - self.image.get_rect()[3] / 2))
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


def extractFrames(inGif, outFolder):
    frame = Image.open(inGif)
    nframes = 0
    while frame:
        frame.save( '%s/%s-%s.gif' % (outFolder, os.path.basename(inGif), nframes ) , 'GIF')
        nframes += 1
        try:
            frame.seek( nframes )
        except EOFError:
            break;
    return True

class explosionanim(object):
    def __init__(self, screen,explosion_gif,exppos):
        self.screen = screen
        self.pos = exppos
        self.gif=explosion_gif
        self.frame_counter=0
        self.frameorder = range(7, 17) + range(6)


    def __call__(self):
        self.screen.blit(self.gif[self.frameorder[self.frame_counter]], self.pos)
        self.frame_counter += 1
    pass

# GIF Explosion parser
# Loading gif from seperated images
gif_direct = assetpath
# gif_direct = "D:\OneDrive\RU\Master Artificial Intelligence\courses\BCI Practical\Project\Tests\GIftests"
extractFrames(assetpath+"explosion2.gif", gif_direct)
explosion_gif =[]


# OS
if platform.system() == 'Windows':
    os.environ['SDL_VIDEODRIVER'] = 'directx'
else:
    os.environ['SDL_VIDEODRIVER'] = 'quartz'

# Music
pygame.mixer.pre_init(44100, 16, 2, 4096)

# Initialize screen
ScreenWidth = 800
ScreenHeight = int(0.625 * ScreenWidth)
pygame.init()

if platform.system() == 'Windows':
    screen = pygame.display.set_mode((ScreenWidth, ScreenHeight), pygame.HWSURFACE | pygame.DOUBLEBUF)
else:
    screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))


clock = pygame.time.Clock()
# screen.set_alpha(None)

# GIF
for i in list(range(17)):
    file = gif_direct + os.sep+"explosion2.gif" + "-" + str(i) + ".gif"
    loaded = pygame.image.load(file).convert_alpha()
    explosion_gif.append(loaded)

explosions=[]
show_explosion = 0


# Background
background = pygame.image.load(assetpath+"space_background.png")
background = pygame.transform.scale(background, (ScreenWidth, ScreenHeight))

# Images
if color:
    alien_red = pygame.image.load(assetpath+"alien_red.png").convert_alpha()
    alien_blue = pygame.image.load(assetpath+"alien_blue.png").convert_alpha()
else:
    alien_red = pygame.image.load(assetpath+"alien_red_white.png").convert_alpha()
    alien_blue = pygame.image.load(assetpath+"alien_blue_white.png").convert_alpha()

alien_red = pygame.transform.scale(alien_red, (int(ScreenWidth * 0.15), int(ScreenHeight * 0.15)))
alien_blue = pygame.transform.scale(alien_blue, (int(ScreenWidth * 0.15), int(ScreenHeight * 0.15)))

alien_red_static = pygame.transform.scale(alien_red, (int(ScreenWidth * 0.13), int(ScreenHeight * 0.13)))
alien_blue_static = pygame.transform.scale(alien_blue, (int(ScreenWidth * 0.13), int(ScreenHeight * 0.13)))

alien_bonus = pygame.image.load(assetpath+"alien_green.png").convert_alpha()
alien_bonus = pygame.transform.scale(alien_bonus, (int(ScreenWidth * 0.1), int(ScreenHeight * 0.1)))


space_ship = pygame.image.load(assetpath+"space_ship.png").convert_alpha()
space_ship = pygame.transform.scale(space_ship, (int(ScreenWidth * 0.1), int(ScreenHeight * 0.1)))

# Init cannon
square_side = int(round(0.08 * ScreenHeight)) # Length of one side of square cannon
x = ScreenWidth /2 - square_side# Start position cannon
y = ScreenHeight - square_side # Static height cannon
colorCannon = (255, 255, 255)
MoveSpeed = 0.01 # Move with speed % pixels of ScreenWdith

# Inits balls
balls=[]
ball_time = time.time()
space_tmp  = 0 # Space bar hasn't been pushed yet

# Inits aliens
aliens=[]
alien_time = time.time()
alien_secs = 3 # 1 alien per 3 sec
alien_start = 1 # For fist alien

if color:
    alienColorRight = (0, 0, 255)
    alienColorLeft = (255, 0, 0)
else:
    alienColorRight = (255, 255, 255)
    alienColorLeft = (255, 255, 255)

# Inits bonus aliens
bonusaliens = []
bonus_time = time.time()
bonus_prob = 0.05
bonus_secs = 8 # Per second there is a bonus_prob of a bonus alien

# Count inits
start_time = time.time()
shots_fired = 0
hit_score = 0
aliens_total = 0

# Frequencies
left_hz = 15 #16
right_hz = 10 #8
clock_FPS = 43 #35 # FPS 43 works!

# Emergency looks
left_time_IC = time.time()
right_time_IC = time.time()
right_IC_color = alienColorRight
left_IC_color = alienColorLeft
IC_side = int(round(0.1 * ScreenHeight))

# Music
pygame.mixer.init(44100, -16,2,2048)
pygame.mixer.music.load(assetpath+"space.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

# Text inits
if 'font' not in locals():
    font = pygame.font.Font(None, int(ScreenHeight * 0.04)) # Python crashes if SysFont is called > 1 XOR specified font
    font_FPS = pygame.font.Font(None, int(ScreenHeight * 0.1))

text_y = int(round(ScreenHeight * 0.01))
x_time = int(round(ScreenWidth * 0.025))
x_static = int(round(ScreenWidth * 0.2))
x_shots = int(round(ScreenWidth * 0.21))
x_static2 = int(round(ScreenWidth * 0.35))
x_score = int(round(ScreenWidth * 0.36))
x_static3 = int(round(ScreenWidth * 0.43))
x_accuracy = int(round(ScreenWidth * 0.44))

textColor = (150, 150, 150) # So the bullet over it don't hide the text

# Autofire
fire_hz = 5
fire_last = time.time()

# For FPS testing
test_timing = time.time()
times= []
now_FPS = 0
x_FPS = int(round(ScreenWidth * 0.94))
fps_timer = time.time()

##### BCI - Start game sign
if braincontrol:
    sendEvent('stim.target', 1)

direction=[]

## Game loop
done = False

while not done:

    for event in pygame.event.get():
        pass

    # BCI events
    if braincontrol:
        events = ftc.getEvents()
        events = events[-1]
        if events.type == 'classifier.prediction':
            pred = events.value
            direction = pred
            sendEvent('stim.target', 1)
        
            

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT] or (direction == -1):
        if (x <= 0): x -= 0 # If window limit left reached, dont do squat.
        else: x -= int(round(ScreenWidth * MoveSpeed))

    if pressed[pygame.K_RIGHT] or (direction == 1):
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
    screen.blit(background, (0, 0))

    # Draw constant emergency SSVEP's
    if ((time.time() - left_time_IC) >= (1.0 / left_hz)):
        screen.blit(alien_red_static, (0, ScreenHeight - alien_red_static.get_rect()[3]))
        left_time_IC = time.time()

    if ((time.time() - right_time_IC) >= (1.0 / right_hz)):
        screen.blit(alien_blue_static, (ScreenWidth - alien_blue_static.get_rect()[2], ScreenHeight - alien_blue_static.get_rect()[3]))

        right_time_IC = time.time()


    # Draw the cannon position
    screen.blit(space_ship,(int(x - space_ship.get_rect()[2]/3.5), y))


    # Create aliens
    if ((time.time() - alien_time) >= 3) or alien_start:
        x_position = np.random.randint(0, ScreenWidth)
        aliens_total += 1 # For accuracy!
        if x_position >= (ScreenWidth/2.0):
            aliens.append(Alien(screen, x_position, alienColorRight, right_hz, alien_blue))
            alien_time = time.time()
            alien_start = 0
        else:
            aliens.append(Alien(screen, x_position, alienColorLeft, left_hz, alien_red))
            alien_time = time.time()
            alien_start = 0


    # Create Bonus Alien
    if ((time.time() - bonus_time) >= bonus_secs) and (float(np.random.uniform(0, 1, 1)) <= bonus_prob):
        aliens_total += 1 # For accuracy!
        x_position = np.random.randint(0, ScreenWidth)
        y_position = np.random.randint(0, int(ScreenHeight * 0.8))
        bonusaliens.append(BonusAlien(screen, x_position, y_position, alien_bonus))
        bonus_time = time.time()

    # Update balls position and delete if hit forcefield or out of FOV
    if len(balls)>0:
        for i in list(reversed(range(len(balls)))):  # Reversed because if 1 is del, index out of range..
            balls[i].move()

            if balls[i].destroy:
                del balls[i]

            if len(aliens)> 0:
                if hit_forcefield(aliens[0], balls[i]):
                    del balls[i]

    # Draw Bonus Alien and remove if hit
    if len(bonusaliens) > 0:
        for i in list(reversed(range(len(bonusaliens)))):
            bonusaliens[i].update()

            if bonusaliens[i].destroy:
                del bonusaliens[i]

        if (len(balls) > 0) and (len(bonusaliens) > 0):  # Looks for a hit by ball
            for i in list(reversed(range(len(bonusaliens)))):
                if len(balls) > 0:
                    for u in list(reversed(range(len(balls)))):
                        if len(bonusaliens) > 0 and len(balls) > 0:
                            if hit_alien(bonusaliens[i], balls[u]):
                                explosion_pos = (bonusaliens[i]._x - bonusaliens[i].size*2, bonusaliens[i]._y_now - bonusaliens[i].size*3)
                                show_explosion = 1
                                del bonusaliens[i]
                                del balls[u]
                                hit_score += 1

    # Move aliens and remove if hit or out of range
    if len(aliens) > 0:
        for i in list(reversed(range(len(aliens)))):
            aliens[i].move()

            if aliens[i].destroy:
                del aliens[i]

        if len(balls) > 0:  # Remove alien if hit
            for i in list(reversed(range(len(balls)))):
                if len(aliens) > 0:
                    if hit_alien(aliens[0], balls[i]):
                        explosion_pos = (aliens[0]._x - aliens[0].size, int(aliens[0]._y_now - aliens[0].size*1.5))
                        show_explosion = 1
                        del aliens[0]
                        del balls[i]
                        hit_score += 1

    # Explosion
    if show_explosion:
        explosions.append(explosionanim(screen, explosion_gif, explosion_pos))
        show_explosion = 0

    for exp_ in explosions:
        if exp_.frame_counter > 15:
            explosions.remove(exp_)
        else:
            exp_()

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
    text_acc = 'Accuracy: ' + str(round(100 * hit_score/(aliens_total +0.000001),1)) + '%' # aliens_total used to be shots_fired!
    text = font.render(text_acc, True, textColor)
    screen.blit(text, (x_accuracy, text_y))


    # Text FPS
    text_fps = str(now_FPS)
    text = font_FPS.render(text_fps, True, (255,255,0))
    screen.blit(text, (x_FPS, text_y))


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


    # Update screen + check FPS
    pygame.display.flip() # Update screen
    onewhile = time.time() - test_timing
    times.append(onewhile)
    if (time.time() - fps_timer) >= 0.5:
        now_FPS = int(1.0 / onewhile)
        fps_timer = time.time()
    test_timing = time.time()
    clock.tick(clock_FPS) # Set response pygame rate fo 60fps

    # Quit without error (if this loop is at the beginning, pygame finishes the loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if braincontrol:
                sendEvent('stim.target', 0)
            done = True
pygame.quit() # Close window

### BCI End game sign
if braincontrol:
    sendEvent('stim.target', 0)


# Just checking FPS
FPS = [1/float(i) for i in times]
sumFPS =0
for i in range(len(FPS)):
    sumFPS += FPS[i]
meanFPS = sumFPS / len(FPS)
print("Mean FPS: " + str(meanFPS))


