#!/usr/bin/env python3
# Set up imports and paths
bufferpath = "../../dataAcq/buffer/python"
sigProcPath = "../signalProc"
import pygame, sys
from pygame.locals import *
from time import sleep, time
import os
import matplotlib
import numpy as np
matplotlib.rcParams['toolbar']='None'
from psychopy import visual, core
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),bufferpath))
import FieldTrip
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),sigProcPath))

## CONFIGURABLE VARIABLES
# Connection options of fieldtrip, hostname and port of the computer running the fieldtrip buffer.
hostname='localhost'
port=1972

## init connection to the buffer
timeout=5000
ftc = FieldTrip.Client()
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

class GOL(object):

    def __init__(self, x):
        self.gridsize_=int(x)
        self.god = 0.001
        gridsize_=self.gridsize_
        gol=np.zeros((gridsize_**2),dtype='float32')
        num_start_clusters = int(np.round(gridsize_ / 5.))
        clustersize = int(np.round(gridsize_ / 10.))
        clustercomplexity = 0.1

        c1 = [[0, 0, 0], [1, 1, 1], [2, 2, 2]], [[0, 1, 2], [0, 1, 2], [0, 1, 2]]
        c2 = [[1], [1]]

        offsets = np.ravel_multi_index(c1, dims=(gridsize_, gridsize_), order='F') - np.ravel_multi_index(c2, dims=(
            gridsize_, gridsize_), order='F')

        for i in range(num_start_clusters):
            tmp=int(np.ceil((np.round(np.random.rand() * clustersize + 1))))
            randclust = np.zeros(tmp**2,dtype='float32')
            randclust[np.where(np.random.rand(np.size(randclust)) > clustercomplexity)] = 1
            size_clust = tmp
            randloc = (np.round(np.random.rand(1,2) * (gridsize_ - size_clust - 2)) + 1).astype('int16')[0]

            col_=np.repeat(range(randloc[0],randloc[0] + size_clust), size_clust, 0)
            row_ = np.repeat(np.reshape(range(randloc[1], randloc[1] + size_clust),(1,size_clust)), size_clust, 0).reshape(tmp**2,1).reshape(1,tmp**2)

            randindclust = np.ravel_multi_index([col_,row_], dims=(gridsize_,gridsize_), order='F')
            gol[randindclust[0]] = randclust

        self.gol_old=gol+0
        self.offsets=offsets.reshape(1,9)


    def __call__(self):
        if self.gol_old.sum()<1:
            self.god = 0.001
            gridsize_ = self.gridsize_
            gol = np.zeros((gridsize_ ** 2))
            num_start_clusters = np.round(gridsize_ / 5)
            clustersize = np.round(gridsize_ / 10)
            clustercomplexity = 0.1

            c1 = [[0, 0, 0], [1, 1, 1], [2, 2, 2]], [[0, 1, 2], [0, 1, 2], [0, 1, 2]]
            c2 = [[1], [1]]

            offsets = np.ravel_multi_index(c1, dims=(gridsize_, gridsize_), order='F') - np.ravel_multi_index(c2, dims=(
                gridsize_, gridsize_), order='F')

            for i in range(num_start_clusters):
                tmp = int(np.ceil((np.round(np.random.rand() * clustersize + 1))))
                randclust = np.zeros(tmp ** 2)
                randclust[np.where(np.random.rand(np.size(randclust)) > clustercomplexity)] = 1
                size_clust = tmp
                randloc = (np.round(np.random.rand(1, 2) * (gridsize_ - size_clust - 2)) + 1).astype('int64')[0]

                col_ = np.repeat(range(randloc[0], randloc[0] + size_clust), size_clust, 0)
                row_ = np.repeat(np.reshape(range(randloc[1], randloc[1] + size_clust), (1, size_clust)), size_clust,
                                 0).reshape(tmp ** 2, 1).reshape(1, tmp ** 2)

                randindclust = np.ravel_multi_index([col_, row_], dims=(gridsize_, gridsize_), order='F')
                gol[randindclust[0]] = randclust

            gol = gol.reshape(gridsize_, gridsize_)
            self.gol_old = gol.reshape(1, gridsize_ ** 2)[0] + 0
            self.offsets = offsets.reshape(1, 9)

        gol = self.gol_old+0
        offsets=self.offsets+0
        livingidx=np.where(gol==1)[0]
        size_idx=len(livingidx)
        neigharrayidx=np.tile(livingidx, (9, 1)).transpose()+np.tile(offsets[0], (size_idx, 1))
        neigharrayidx[neigharrayidx < 0] = 0
        neigharrayidx[neigharrayidx >= (self.gridsize_**2)] = 0

        neigharray=gol[neigharrayidx]
        killidx=(neigharray.sum(1)<3) | (neigharray.sum(1)>4)
        randkillidx=np.random.rand(size_idx)<self.god

        offspridx=np.tile(livingidx, (9, 1)).transpose()[:,range(4)+range(5,9)]+np.tile(offsets[0][range(4)+range(5,9)], (size_idx, 1))
        offspridx=offspridx.flatten()
        offspridx[offspridx < 0] = 0
        offspridx[offspridx >= (self.gridsize_ ** 2)] = 0

        size_idx = len(offspridx)

        neigharrayidx = np.tile(offspridx, (9, 1)).transpose() + np.tile(offsets[0], (size_idx, 1))
        neigharrayidx[neigharrayidx < 0]=0
        neigharrayidx[neigharrayidx >= (self.gridsize_**2)] = 0

        neigharray = gol[neigharrayidx]

        aliveidx = (neigharray.sum(1) == 3)
        randaliveidx = np.random.rand(size_idx) < self.god

        gol[livingidx[killidx+randkillidx]] = 0
        gol[offspridx[aliveidx+randaliveidx]] = 1

        self.gol_old=gol+0
        return self.gol_old


grid_size=100
window_size=800

freq=15 # (note 30Hz = hardware max, because: turn pixel on / off = 1 frame -> 30Hz flicker needs 60 frames/s)
freq2=10

trialtime=4.5 # time per trial
numtrials_per_cond=20

instructions=['<','>']

#instructions=['<','+','>']

#values_=['2 RH','99 Rest','1 LH']
values_=['2 RH','1 LH']

#### Using PsychoPy and pygame ####

mywin=visual.Window([window_size,window_size*0.75],color=(-1,-1,-1),units='pix',monitor='testMonitor',winType="pygame")

win_s=mywin.size

pattern1 = visual.ImageStim(win=mywin, name='pattern1',units='pix',size=[win_s[0],win_s[1]-win_s[0]/8],pos=(0,win_s[0]/8))
pattern2 = visual.Circle(win=mywin,pos=[win_s[0]/2-win_s[0]/10+10,-win_s[1]/2+win_s[1]/10],radius=win_s[0]/16, edges=32,fillColor=[1,-1,-1],lineColor=[-1,-1,-1],units='pix')
pattern3 = visual.Circle(win=mywin,pos=[-win_s[0]/2+win_s[0]/10-10,-win_s[1]/2+win_s[1]/10],radius=win_s[0]/16, edges=32,fillColor=[-1,-1,1],lineColor=[-1,-1,-1],units='pix')
pattern4 = visual.ShapeStim(win=mywin,vertices=([-win_s[0]/2, -(win_s[1]/2-win_s[1]/5-10)], [-win_s[0]/2, -(win_s[1]/2-win_s[1]/5-9)],[win_s[0]/2, -(win_s[1]/2-win_s[1]/5-9)], [win_s[0]/2, -(win_s[1]/2-win_s[1]/5-10)] ),lineColor=[1,1,1],units='pix')

pattern5 = visual.TextStim(win=mywin,pos=(0,-(win_s[1]/2-win_s[1]/10-10)),text='+',color=[1, 1, 1],units='pix',height=win_s[0]/8)
pattern6 = visual.TextStim(win=mywin,pos=(0,-(win_s[1]/2-win_s[1]/10-10)),text='',color=[1, 1, 1],units='pix',height=win_s[0]/8)
pattern7 = visual.TextStim(win=mywin,pos=(0,-(win_s[1]/2-win_s[1]/10-10)),text='',color=[1, 1, 1],units='pix',height=win_s[0]/8)


Trialclock = core.Clock()

start_time1=Trialclock.getTime()
start_time2=Trialclock.getTime()
start_time3=Trialclock.getTime()
start_time4=Trialclock.getTime()

idx=np.random.randint(2)

pattern1.setAutoDraw(True)
pattern4.setAutoDraw(True)
pattern5.setAutoDraw(True)
pattern6.setAutoDraw(True)
pattern7.setAutoDraw(True)

frametime=1/60.

dur=1./freq
dur2=1./freq2

numtrials_per_cond_act=np.atleast_2d(np.zeros(2))

gol=GOL(grid_size)

sendEvent('stimulus.training','start')

while (numtrials_per_cond_act.sum(0)<numtrials_per_cond).any()==True:

    if ((Trialclock.getTime() - start_time1) > (dur * 0.45)):
        if (dur*0.45-(Trialclock.getTime()-start_time1))>0:
            core.wait(dur*0.49-(Trialclock.getTime()-start_time1))
        pattern3.setAutoDraw(True)

    if ((Trialclock.getTime() - start_time2) > (dur2 * 0.45)):
        if (dur2*0.45-(Trialclock.getTime()-start_time2))>0:
            core.wait(dur2*0.49-(Trialclock.getTime()-start_time2))
        pattern2.setAutoDraw(True)

    if ((Trialclock.getTime() - start_time1) > (dur * 0.95)):
        if (dur*0.95-(Trialclock.getTime()-start_time1))>0:
            core.wait(dur*0.99-(Trialclock.getTime()-start_time1))
        start_time1 = Trialclock.getTime()
        pattern3.setAutoDraw(False)

    if ((Trialclock.getTime() - start_time2) > (dur2 * 0.95)):
        if (dur2*0.95-(Trialclock.getTime()-start_time2))>0:
            core.wait(dur2*0.99-(Trialclock.getTime()-start_time2))
        start_time2 = Trialclock.getTime()
        pattern2.setAutoDraw(False)

    if ((Trialclock.getTime() - start_time3) > trialtime):
        start_time3 = Trialclock.getTime()
        idx=np.random.randint(2)

        sendEvent('stim.target',values_[idx])

        numtrials_per_cond_act[0][idx]+=1
        pattern5.setPos(pattern2.pos)
        pattern5.setText(instructions[idx])

        pattern6.setPos(pattern3.pos)
        pattern6.setText(instructions[idx])

        pattern7.setText(instructions[idx])

    data_ = gol().reshape(grid_size, grid_size) + 0
    data_[data_ == 0] = -1
    pattern1.setImage(data_)
    mywin.flip()

sendEvent('stim.training','end')
pattern5.setText('end')
mywin.flip()