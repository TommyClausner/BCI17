#!/usr/bin/env python3
# Set up imports and paths
bufferpath = "../../dataAcq/buffer/python"
sigProcPath = "../signalProc"

import sys,os
from time import sleep
import matplotlib
import numpy as np
matplotlib.rcParams['toolbar']='None'
from psychopy import visual, core,event
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

def processBufferEvents():
    global running
    events = ftc.getEvents()
    events=events[-1]
    if events.type == 'classifier.prediction':
        pred = events.value
        game.ship.direction=pred+0
        sendEvent('stim.target', 1)
    else:
        game.ship.direction = 0


grid_size=100
window_size=800

numtrials_per_cond=20

mywin=visual.Window([window_size,window_size*0.75],color=(-1,-1,-1),units='pix',monitor='testMonitor',winType="pygame")

class stimuli_(object):
        def __init__(self,mywin):
            self.mywin=mywin
            win_s = self.mywin.size

            self.pattern2 = visual.Circle(win=self.mywin, pos=[win_s[0] / 2 - win_s[0] / 10 + 10, -win_s[1] / 2 + win_s[1] / 10],
                                     radius=win_s[0] / 16, edges=32, fillColor=[1, -1, -1], lineColor=[-1, -1, -1],
                                     units='pix')
            self.pattern3 = visual.Circle(win=self.mywin, pos=[-win_s[0] / 2 + win_s[0] / 10 - 10, -win_s[1] / 2 + win_s[1] / 10],
                                     radius=win_s[0] / 16, edges=32, fillColor=[-1, -1, 1], lineColor=[-1, -1, -1],
                                     units='pix')
            self.pattern4 = visual.ShapeStim(win=self.mywin, vertices=(
            [-win_s[0] / 2, -(win_s[1] / 2 - win_s[1] / 5 - 10)], [-win_s[0] / 2, -(win_s[1] / 2 - win_s[1] / 5 - 9)],
            [win_s[0] / 2, -(win_s[1] / 2 - win_s[1] / 5 - 9)], [win_s[0] / 2, -(win_s[1] / 2 - win_s[1] / 5 - 10)]),
                                        lineColor=[1, 1, 1], units='pix')

            self.Trialclock = core.Clock()

            self.start_time1 = self.Trialclock.getTime()
            self.start_time2 = self.Trialclock.getTime()
            self.start_time3 = self.Trialclock.getTime()
            self.start_time4 = self.Trialclock.getTime()

            self.pattern2.setAutoDraw(True)
            self.pattern3.setAutoDraw(True)
            self.pattern4.setAutoDraw(True)


        def __call__(self,mywin,freq = 15,freq2 = 10):
            self.mywin=mywin
            dur = 1. / freq
            dur2 = 1. / freq2

            if ((self.Trialclock.getTime() - self.start_time1) > (dur * 0.45)):
                if (dur * 0.45 - (self.Trialclock.getTime() - self.start_time1)) > 0:
                    core.wait(dur * 0.49 - (self.Trialclock.getTime() - self.start_time1))
                self.pattern3.setAutoDraw(True)

            if ((self.Trialclock.getTime() - self.start_time2) > (dur2 * 0.45)):
                if (dur2 * 0.45 - (self.Trialclock.getTime() - self.start_time2)) > 0:
                    core.wait(dur2 * 0.49 - (self.Trialclock.getTime() - self.start_time2))
                self.pattern2.setAutoDraw(True)

            if ((self.Trialclock.getTime() - self.start_time1) > (dur * 0.95)):

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
            return self.mywin

class brainfly(object):
    class enemy(object):
        def __init__(self,mywin):
            self.mywin=mywin


            self.enemy_one_line=visual.Line(win=self.mywin, start=(-400, 250), end=(400, 250),lineColor='red')
            self.enemy_one_line.setAutoDraw(True)
            self.enemy_one = visual.Circle(win=self.mywin,
                                           pos=[np.random.randint(600) - 300, 250],
                                           radius=40, edges=32, fillColor=[-1, 1, -1],
                                           units='pix')
            self.enemy_one.setAutoDraw(True)
        def __call__(self,mywin,stepsize=5,radincrease=1):
            self.mywin = mywin
            self.enemy_one.setPos([self.enemy_one.pos[0],self.enemy_one.pos[1]-stepsize])
            self.enemy_one_line.setPos([self.enemy_one_line.pos[0], self.enemy_one_line.pos[1] - stepsize])

            if self.enemy_one.pos[1]<-150:
                collision_=1
                self.enemy_one.setAutoDraw(False)
                self.enemy_one_line.setAutoDraw(False)
            else:
                collision_=0
                self.enemy_one.radius=self.enemy_one.radius+radincrease
                self.enemy_one.setAutoDraw(True)
                self.enemy_one_line.setAutoDraw(True)

            return self.mywin,collision_

    class spaceship(object):

        def __init__(self, mywin):
            self.mywin=mywin
            self.ship = visual.Rect(win=self.mywin,pos=[0, -150],
                                           width=40, height=32, fillColor=[1, 1, 1],
                                           units='pix')
            self.ship.setAutoDraw(True)
            self.direction=1

        def __call__(self, mywin,stepsize=50):

            self.ship.setPos([self.ship.pos[0] -self.direction* stepsize, self.ship.pos[1]])

            if self.ship.pos[0]<-350:
                self.ship.setPos([-350, self.ship.pos[1]])

            if self.ship.pos[0]>350:
                self.ship.setPos([350, self.ship.pos[1]])

            return self.mywin

    class cannonball(object):

        def __init__(self, mywin,shippos):
            self.mywin=mywin
            self.ball = visual.Circle(win=self.mywin, pos=shippos,
                                     radius=15, edges=32, fillColor=[1, 1, 1], lineColor=[-1, -1, -1],
                                     units='pix')
            self.ball.setAutoDraw(False)

        def __call__(self, mywin,shippos,stepsize=10):
            self.ball.setPos([self.ball.pos[0],self.ball.pos[1]+stepsize])
            if self.ball.pos[1]>350:
                self.ball.setPos(shippos)
            return self.mywin

    def __init__(self, mywin):
        self.mywin = mywin
        win_s = self.mywin.size
        self.enemy1=brainfly.enemy(self.mywin)
        self.enemy2 = brainfly.enemy(self.mywin)
        self.enemy2.enemy_one.setAutoDraw(False)
        self.enemy2.enemy_one_line.setAutoDraw(False)
        self.enemyclock = core.Clock()
        self.start_ememy1=self.enemyclock.getTime()

        self.ship=brainfly.spaceship(self.mywin)
        self.cannons=list()
        for n in range(11):
            self.cannons.append(brainfly.cannonball(self.mywin,self.ship.ship.pos))

        self.initval=1

    def __call__(self, mywin):
        self.mywin = mywin
        self.mywin,collision_=self.enemy1(self.mywin)
        if collision_:
            self.enemy1 = brainfly.enemy(self.mywin)

        if self.enemy1.enemy_one.pos[1]<50:
            self.initval=0
            self.enemy2.enemy_one_line.setAutoDraw(True)
            self.enemy2.enemy_one.setAutoDraw(True)

        if not self.initval:
            self.mywin, collision_ = self.enemy2(self.mywin)

        if collision_ and self.enemy1.enemy_one.pos[1]<50:
            self.enemy2 = brainfly.enemy(self.mywin)

        for n in range(len(self.cannons)-1):
            if n==0 or abs(self.cannons[n].ball.pos[1]-self.cannons[n+1].ball.pos[1])>50:
                self.mywin = self.cannons[n+1](self.mywin,self.ship.ship.pos)
                self.cannons[n+1].ball.setAutoDraw(True)

        self.mywin=self.ship(self.mywin)

        return self.mywin

frametime=1/60.

numtrials_per_cond_act=np.atleast_2d(np.zeros(2))

stim=stimuli_(mywin)
game=brainfly(mywin)
sendEvent('stim.target', 1)

while True:
    mywin=stim(mywin)
    mywin.flip()
    mywin = game(mywin)
    mywin.flip()

    processBufferEvents()