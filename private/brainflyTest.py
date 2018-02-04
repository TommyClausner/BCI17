"""
  ____            _       ______ _         ____   _____ _____
 |  _ \          (_)     |  ____| |       |  _ \ / ____|_   _|
 | |_) |_ __ __ _ _ _ __ | |__  | |_   _  | |_) | |      | |
 |  _ <| '__/ _` | | '_ \|  __| | | | | | |  _ <| |      | |
 | |_) | | | (_| | | | | | |    | | |_| | | |_) | |____ _| |_
 |____/|_|  \__,_|_|_| |_|_|    |_|\__, | |____/ \_____|_____|
                                    __/ |
                                   |___/

"""

# This function is basic implementation of the BrainFly game. It can be played with and without keyboard control (EEG mode)
# In the appendix of the report a users manual is provided.

# import all necessary libraries
import pygame.locals
import sys,os
from time import sleep
import time # NEW
import matplotlib
matplotlib.rcParams['toolbar']='None'
from psychopy import visual, core
import pygame

# enable if you want animated explosions
enable_explosions=1

# enable if you want steady state stimulation
enable_stimuli=1

# fire rate of the ship in Hz
cannonfirerate=5

# spawn time of aliens in seconds
timeBeforeNextAlien= 3

# game duration in seconds
max_game_dur=90

# window size
window_size=800
deaths=0
hits=0

pygame.init()

matplotlib.rcParams['toolbar']='None'

# parent path from where the script was run
main_path=os.path.dirname(os.path.abspath(__file__))+os.sep+'..'+os.sep

# sets up all path dependencies needed for the function to run
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

# if using real EEG as input
# In that case the FieldTrip buffer and bufhelp is imported and the respective paths are set
# Further the function connects to the buffer
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

# setup video drivers
if platform.system() == 'Windows':
    os.environ['SDL_VIDEODRIVER'] = 'directx'
else:
    os.environ['SDL_VIDEODRIVER'] = 'quartz'
# stimuli
if enable_stimuli:
    mywin=visual.Window([window_size,window_size*0.75],color=(-1,-1,-1),units='pix',monitor='testMonitor',winType="pygame")
    class stimuli_(object):
        def __init__(self, mywin, color):
            self.mywin = mywin
            win_s = self.mywin.size

            # depending on color choice in the main menu, the colors will be set to red and blue or both white
            if color:
                blue = [-1, -1, 1]
                red = [1, -1, -1]
            else:
                blue = [1, 1, 1]
                red = [1, 1, 1]

            # right circle
            self.pattern2 = visual.Circle(win=self.mywin,
                                          pos=[win_s[0] / 2 - win_s[0] / 10 + 10, -win_s[1] / 2 + win_s[1] / 10],
                                          radius=win_s[0] / 16, edges=32, fillColor=blue, lineColor=[-1, -1, -1],
                                          units='pix')
            # left circle
            self.pattern3 = visual.Circle(win=self.mywin,
                                          pos=[-win_s[0] / 2 + win_s[0] / 10 - 10, -win_s[1] / 2 + win_s[1] / 10],
                                          radius=win_s[0] / 16, edges=32, fillColor=red, lineColor=[-1, -1, -1],
                                          units='pix')
            # split line circle
            self.pattern4 = visual.ShapeStim(win=self.mywin, vertices=(
                [-win_s[0] / 2, -(win_s[1] / 2 - win_s[1] / 5 - 10)],
                [-win_s[0] / 2, -(win_s[1] / 2 - win_s[1] / 5 - 9)],
                [win_s[0] / 2, -(win_s[1] / 2 - win_s[1] / 5 - 9)],
                [win_s[0] / 2, -(win_s[1] / 2 - win_s[1] / 5 - 10)]),
                                             lineColor=[1, 1, 1], units='pix')

            # set timers for stimulation
            self.Trialclock = core.Clock()

            self.start_time1 = self.Trialclock.getTime()
            self.start_time2 = self.Trialclock.getTime()
            self.start_time3 = self.Trialclock.getTime()
            self.start_time4 = self.Trialclock.getTime()

            # set screen components to draw
            self.pattern2.setAutoDraw(True)
            self.pattern3.setAutoDraw(True)
            self.pattern4.setAutoDraw(True)

        def __call__(self, freq=15, freq2=10):
            # set frequencies for SSVEPs. Note, that it is advisable to chose frquencies that are not first order harmonics
            # and are in accordance with the refresh rate of your screen
            dur = 1. / freq
            dur2 = 1. / freq2

            # enable stimulus (half cycle + some buffer time, hence the 0.45)
            if ((self.Trialclock.getTime() - self.start_time1) > (dur * 0.45)):
                # correct for buffer time
                if (dur * 0.45 - (self.Trialclock.getTime() - self.start_time1)) > 0:
                    core.wait(dur * 0.49 - (self.Trialclock.getTime() - self.start_time1))
                self.pattern3.setAutoDraw(True)

            if ((self.Trialclock.getTime() - self.start_time2) > (dur2 * 0.45)):
                if (dur2 * 0.45 - (self.Trialclock.getTime() - self.start_time2)) > 0:
                    core.wait(dur2 * 0.49 - (self.Trialclock.getTime() - self.start_time2))
                self.pattern2.setAutoDraw(True)

            # disable stimulus (half cycle + half cycle enable + some buffer time, hence the 0.95)
            if ((self.Trialclock.getTime() - self.start_time1) > (dur * 0.95)):
                # correct for buffer time
                if (dur * 0.95 - (self.Trialclock.getTime() - self.start_time1)) > 0:
                    print(self.Trialclock.getTime() - self.start_time1)
                    core.wait(dur * 0.99 - (self.Trialclock.getTime() - self.start_time1))
                self.start_time1 = self.Trialclock.getTime()
                self.pattern3.setAutoDraw(False)

            if ((self.Trialclock.getTime() - self.start_time2) > (dur2 * 0.95)):
                if (dur2 * 0.95 - (self.Trialclock.getTime() - self.start_time2)) > 0:
                    core.wait(dur2 * 0.99 - (self.Trialclock.getTime() - self.start_time2))
                self.start_time2 = self.Trialclock.getTime()
                self.pattern2.setAutoDraw(False)

    pos_corr=0
    stim = stimuli_(mywin, color)
else: # if stimuli are disabled, set up a blank screen
    pos_corr = (window_size*0.625-window_size*0.75)/2.
    mywin=visual.Window([window_size,window_size*0.625],color=(-1,-1,-1),units='pix',monitor='testMonitor',winType="pygame")

# setup enemies
class enemy(object):
    def __init__(self,mywin):
        self.mywin=mywin

        # Alien stimuli
        self.enemy_line=visual.Line(win=self.mywin, start=(-self.mywin.size[0]/2, self.mywin.size[1]/2+pos_corr), end=(self.mywin.size[0]/2, self.mywin.size[1]/2+pos_corr),lineColor='red')
        self.enemy_line.setAutoDraw(True)
        self.enemy = visual.Circle(win=self.mywin,
                                       pos=[np.random.randint(self.mywin.size[0]*0.75) - self.mywin.size[0]*0.375, self.mywin.size[1]/2+pos_corr],
                                       radius=self.mywin.size[0]/20, edges=32, fillColor=[-1, 1, -1],
                                       units='pix')
        self.enemy.setAutoDraw(True)

    # move along the y-axis according to 'stepsize' per update
    # increase the radius of the alien by 'radincrease' per update
    def __call__(self,stepsize=1.25,radincrease=0.3):
        self.enemy.setPos([self.enemy.pos[0],self.enemy.pos[1]-stepsize])
        self.enemy_line.setPos([self.enemy_line.pos[0], self.enemy_line.pos[1] - stepsize])
        self.enemy.radius = self.enemy.radius + radincrease
        pass

# setup ship
class spaceship(object):

    def __init__(self, mywin,braincontrol=0):
        self.mywin=mywin
        self.braincontrol=braincontrol
        self.ship = visual.Rect(win=self.mywin,pos=[0, -self.mywin.size[1]/4.+pos_corr*2.],
                                       width=self.mywin.size[0]/20, height=self.mywin.size[0]/25, fillColor=[1, 1, 1],
                                       units='pix')
        self.ship.setAutoDraw(True)
        self.direction=0

    def __call__(self):
        stepsize=self.mywin.size[0]/80
        # if brain control accept classifier predictions as input
        if self.braincontrol:
            stepsize = self.mywin.size[0] / 16
            events = ftc.getEvents()
            events = events[-1]
            if events.type == 'classifier.prediction':
                pred = events.value
                self.direction = pred
                sendEvent('stim.target', 1)
            else:
                self.direction = 0
        else:

            if pygame.key.get_pressed()[pygame.K_LEFT]:
                self.direction=-1
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.direction = 1
            else:
                self.direction = 0
        self.ship.setPos([self.ship.pos[0] +self.direction* stepsize, self.ship.pos[1]])
        # the output of the direction choice is a -1 or 1. This is used to change the direction along the x-axis of the ship
        # the ship will move according to 'stepsize' per update

        # statements below ensure that the sip cannot move outside the screen
        if self.ship.pos[0]<-0.4375*self.mywin.size[0]:
            self.ship.setPos([-0.4375*self.mywin.size[0], self.ship.pos[1]])

        if self.ship.pos[0]>0.4375*self.mywin.size[0]:
            self.ship.setPos([0.4375*self.mywin.size[0], self.ship.pos[1]])

        pass

# setup cannonballs
class cannonball(object):

        def __init__(self, mywin,shippos):
            self.mywin=mywin
            self.ball = visual.Circle(win=self.mywin, pos=shippos,
                                     radius=self.mywin.size[0]/53.334, edges=32, fillColor=[1, 1, 1], lineColor=[-1, -1, -1],
                                     units='pix')
            self.ball.setAutoDraw(True)

        def __call__(self):
            stepsize = self.mywin.size[0] / 80
            self.ball.setPos([self.ball.pos[0],self.ball.pos[1]+stepsize])
            pass

# setup explosion animation
class explosionanim(object):
    def __init__(self, mywin,explosion,exppos):
        self.mywin = mywin
        self.gif=explosion
        self.expl = visual.ImageStim(self.mywin,pos=exppos)
        self.expl.setAutoDraw(False)
        self.frame_counter=0
        self.frameorder=range(7,17)+range(6)

    def __call__(self):
        self.expl.setAutoDraw(False)
        self.gif.seek(self.frameorder[self.frame_counter])
        self.expl.setImage(self.gif)
        self.expl.setAutoDraw(True)
        self.frame_counter += 1
    pass

enemies=[]
balls=[]


# create all objects
ship=spaceship(mywin,braincontrol)
enemies.append(enemy(mywin))

Timerobj=core.Clock()
enemtimer=Timerobj.getTime()
canontimer=Timerobj.getTime()

gamedur=Timerobj.getTime()
fpstimer=Timerobj.getTime()

# setup HUD
hud_string='Time played: '+str(round(Timerobj.getTime()-gamedur,1))+' | hits: '+str(hits)+' | deaths: '+str(deaths)

HUD_ = visual.TextStim(win=mywin,pos=[-mywin.size[0]/2,mywin.size[1]/2],text=hud_string,color=[1, 1, 1],units='pix',height=20,alignVert='top',alignHoriz='left')
HUD_.setAutoDraw(True)

FPS_ = visual.TextStim(win=mywin,pos=[mywin.size[0]/2,mywin.size[1]/2],text='0',color=[0, 1, 1],units='pix',height=40,alignVert='top',alignHoriz='right')
FPS_.setAutoDraw(True)

fps_timer_col=[]

if enable_explosions:
    explosiongif = Image.open(assetpath+"explosion2.gif")
    explo = explosionanim(mywin, explosiongif, [0,0])
    explosions=[]
    show_explosion = 0

if braincontrol:
    sendEvent('stim.target', 1)
pygame.display.init()

# run Game
while Timerobj.getTime() - gamedur<=max_game_dur:
    time.sleep(1.0/100)
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        if braincontrol:
            sendEvent('stim.target', 0)
        core.quit()

    # create enemies
    if Timerobj.getTime()-enemtimer>timeBeforeNextAlien:
        enemtimer = Timerobj.getTime()
        enemies.append(enemy(mywin))

    # update enemy pos
    if len(enemies)>0:
        for enem in enemies:
            enem()
            if enem.enemy.pos[1]<ship.ship.pos[1]:
                enem.enemy.setAutoDraw(False)
                enem.enemy_line.setAutoDraw(False)
                enemies.remove(enem)
                deaths+=1

    # update ship pos
    ship()

    # create cannonballs
    if Timerobj.getTime() - canontimer > 1./cannonfirerate:
        canontimer = Timerobj.getTime()
        balls.append(cannonball(mywin, ship.ship.pos))

    # update cannonballs pos
    if len(balls) > 0:
        for ball in balls:

            if len(enemies) > 0:
                for enem in enemies:
                    # detect hit
                    if np.sqrt((ball.ball.pos[0] - enem.enemy.pos[0]) ** 2 + (
                                ball.ball.pos[1] - enem.enemy.pos[1]) ** 2) < enem.enemy.radius:
                        ball.ball.setAutoDraw(False)
                        balls.remove(ball)
                        if enable_explosions:
                            show_explosion = 1
                            explosion_pos=enem.enemy.pos
                        enem.enemy.setAutoDraw(False)
                        enem.enemy_line.setAutoDraw(False)
                        enemies.remove(enem)
                        hits+=1

                    else:
                        if ball.ball.pos[1] > enem.enemy.pos[1]:
                            ball.ball.setAutoDraw(False)
                            balls.remove(ball)
                        else:
                            if ball.ball.pos[1] > mywin.size[0]/2:
                                ball.ball.setAutoDraw(False)
                                balls.remove(ball)
            ball()

    # update stimuli pos
    if enable_stimuli:
        stim()

    # update explosion anim
    if enable_explosions:
        if show_explosion:
            explosions.append(explosionanim(mywin, explosiongif, explosion_pos))
            show_explosion=0

        for exp_ in explosions:
            if exp_.frame_counter>15:
                exp_.expl.setAutoDraw(False)
                explosions.remove(exp_)
            else:
                exp_()

    # update HUD
    hud_string = 'Time played: ' + str(round(Timerobj.getTime() - gamedur, 1)) + ' | hits: ' + str(
        hits) + ' | deaths: ' + str(deaths)
    HUD_.setText(hud_string)
    fps_timer_col.append(1. / (Timerobj.getTime() - fpstimer))
    FPS_.setText(str(int(np.round(np.mean(fps_timer_col)))))
    if len(fps_timer_col)>120:
        del fps_timer_col[0]
    fpstimer = Timerobj.getTime()

    mywin.flip()
if braincontrol:
    sendEvent('stim.target', 0)

core.quit()