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

# This function is used during the calibration phase. SSVEPs are created and paired with the selected background.
# In the appendix of the report a users manual is provided.

# import all necessary libraries
import sys
from time import sleep
import os
import matplotlib
import numpy as np
from threading import Timer

from psychopy import visual, core,event

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

import platform

##### BCI enable #######
if __name__ == "__main__":
    braincontrol = 1#int(sys.argv[1])
    ##### BCI enable #######
    if len(sys.argv) > 1:
        color = int(sys.argv[1])
        use_gol = int(sys.argv[2])
    else:
        color = 1
        use_gol = 1
else:
    braincontrol=0
    color = 1
    use_gol = 1

print(braincontrol)
print(color)
print(use_gol)

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

    # send start even value
    def sendEvent(event_type, event_value=1, sample=-1):
        e = FieldTrip.Event()
        e.type=event_type
        e.value=event_value
        e.sample=sample
        ftc.putEvents(e)

BCI_buff_path="external"+os.sep
bufferpath = BCI_buff_path+"dataAcq"+os.sep+"buffer"+os.sep+"python"
sigProcPath = BCI_buff_path+"python"+os.sep+"signalProc"
assetpath="assets"+os.sep

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),bufferpath))

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),sigProcPath))

# setup video drivers
if platform.system() == 'Windows':
    os.environ['SDL_VIDEODRIVER'] = 'directx'
else:
    os.environ['SDL_VIDEODRIVER'] = 'quartz'

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

# setup Game of Life
class GOL(object):

    def __init__(self, x):
        self.gridsize_=int(x)
        self.god = 0.001
        gridsize_=self.gridsize_
        gol=np.zeros((gridsize_**2),dtype='float32')
        num_start_clusters = int(np.round(gridsize_ / 5.))
        clustersize = int(np.round(gridsize_ / 10.))
        clustercomplexity = 0.1

        # define grid structure
        c1 = [[0, 0, 0], [1, 1, 1], [2, 2, 2]], [[0, 1, 2], [0, 1, 2], [0, 1, 2]]
        c2 = [[1], [1]]

        offsets = np.ravel_multi_index(c1, dims=(gridsize_, gridsize_), order='F') - np.ravel_multi_index(c2, dims=(
            gridsize_, gridsize_), order='F')

        # initialize starting clusers randomly given a certain size and complexity (added noise)
        for i in range(num_start_clusters):
            tmp=int(np.ceil((np.round(np.random.rand() * clustersize + 1))))
            randclust = np.zeros(tmp**2,dtype='float32')
            randclust[np.where(np.random.rand(np.size(randclust)) > clustercomplexity)] = 1
            size_clust = tmp
            randloc = (np.round(np.random.rand(1,2) * (gridsize_ - size_clust - 2)) + 1).astype('int16')[0]

            col_=np.repeat(range(randloc[0],randloc[0] + size_clust), size_clust, 0)
            row_ = np.repeat(np.reshape(range(randloc[1], randloc[1] + size_clust),(1,size_clust)), size_clust, 0).reshape(tmp**2,1).reshape(1,tmp**2)
            # get indices of cluster and update the new arrangement
            randindclust = np.ravel_multi_index([col_,row_], dims=(gridsize_,gridsize_), order='F')
            gol[randindclust[0]] = randclust

        self.gol_old=gol+0
        self.offsets=offsets.reshape(1,9)


    def __call__(self):
        # if all cells are dead, re-initialize display (like __init__)
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

        # find neighbouring cells for evaluation of the rules
        gol = self.gol_old+0
        offsets=self.offsets+0
        livingidx=np.where(gol==1)[0]
        size_idx=len(livingidx)
        neigharrayidx=np.tile(livingidx, (9, 1)).transpose()+np.tile(offsets[0], (size_idx, 1))
        neigharrayidx[neigharrayidx < 0] = 0
        neigharrayidx[neigharrayidx >= (self.gridsize_**2)] = 0

        # those that have less than 3 or more than 4 neighbours die of starvation or overpopulation
        # furthermore a random fraction is killed anyways by "God"
        neigharray=gol[neigharrayidx]
        killidx=(neigharray.sum(1)<3) | (neigharray.sum(1)>4)
        randkillidx=np.random.rand(size_idx)<self.god

        # evaluating offspring
        offspridx=np.tile(livingidx, (9, 1)).transpose()[:,range(4)+range(5,9)]+np.tile(offsets[0][range(4)+range(5,9)], (size_idx, 1))
        offspridx=offspridx.flatten()
        offspridx[offspridx < 0] = 0
        offspridx[offspridx >= (self.gridsize_ ** 2)] = 0

        size_idx = len(offspridx)

        neigharrayidx = np.tile(offspridx, (9, 1)).transpose() + np.tile(offsets[0], (size_idx, 1))
        neigharrayidx[neigharrayidx < 0]=0
        neigharrayidx[neigharrayidx >= (self.gridsize_**2)] = 0

        neigharray = gol[neigharrayidx]

        # dead cells with exactly 3 living neighbours become alive
        # furthermore a random fraction re-born by "God"
        aliveidx = (neigharray.sum(1) == 3)
        randaliveidx = np.random.rand(size_idx) < self.god

        # update current state
        gol[livingidx[killidx+randkillidx]] = 0
        gol[offspridx[aliveidx+randaliveidx]] = 1

        self.gol_old=gol+0
        return self.gol_old

# setup stimuli for SSVEP stimulation
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

            # background
            self.pattern1 = visual.ImageStim(win=mywin, name='pattern1', units='pix',
                                        size=[win_s[0], win_s[1] - win_s[0] / 8], pos=(0, win_s[0] / 8))
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
            # screen line
            self.pattern4 = visual.ShapeStim(win=self.mywin, vertices=(
                [-win_s[0] / 2, -(win_s[1] / 2 - win_s[1] / 5 - 10)],
                [-win_s[0] / 2, -(win_s[1] / 2 - win_s[1] / 5 - 9)],
                [win_s[0] / 2, -(win_s[1] / 2 - win_s[1] / 5 - 9)],
                [win_s[0] / 2, -(win_s[1] / 2 - win_s[1] / 5 - 10)]),
                                             lineColor=[1, 1, 1], units='pix')
            # stimulation text (side indicators and fixation cross)
            self.pattern5 = visual.TextStim(win=mywin, pos=(0, -(win_s[1] / 2 - win_s[1] / 10 - 10)), text='+',
                                       color=[1, 1, 1], units='pix', height=win_s[0] / 8)
            self.pattern6 = visual.TextStim(win=mywin, pos=(0, -(win_s[1] / 2 - win_s[1] / 10 - 10)), text='',
                                       color=[1, 1, 1], units='pix', height=win_s[0] / 8)
            self.pattern7 = visual.TextStim(win=mywin, pos=(0, -(win_s[1] / 2 - win_s[1] / 10 - 10)), text='',
                                       color=[1, 1, 1], units='pix', height=win_s[0] / 8)

            # set timers for stimulation
            self.Trialclock = core.Clock()

            self.start_time1 = self.Trialclock.getTime()
            self.start_time2 = self.Trialclock.getTime()
            self.start_time3 = self.Trialclock.getTime()
            self.start_time4 = self.Trialclock.getTime()

            # set screen components to draw
            self.pattern1.setAutoDraw(True)
            self.pattern2.setAutoDraw(True)
            self.pattern3.setAutoDraw(True)
            self.pattern4.setAutoDraw(True)
            self.pattern5.setAutoDraw(True)
            self.pattern6.setAutoDraw(True)
            self.pattern7.setAutoDraw(True)

            self.instructions=['<','>']

        # screen update
        def __call__(self, numtrials_per_cond_act,freq=15, freq2=10):
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

            # update trial according to trial length
            if ((Trialclock.getTime() - self.start_time3) > trialtime):
                self.start_time3 = Trialclock.getTime()
                values_ = ['1 LH','2 RH']
                idx = np.random.randint(2)
                t = Timer(rec_wait_time, sendEvent, ['stim.target', values_[idx]])

                numtrials_per_cond_act[0][idx] += 1
                self.pattern5.setPos(self.pattern2.pos)
                self.pattern5.setText(self.instructions[idx])

                self.pattern6.setPos(self.pattern3.pos)
                self.pattern6.setText(self.instructions[idx])

                self.pattern7.setText(self.instructions[idx])
                t.start()
            # return current trial count per condition
            return numtrials_per_cond_act

# Game of life presetting of the squared grid
grid_size=100
# Stimulation window size at a ratio of 4:3
window_size=800

trialtime = 2.5 # time per trial
rec_wait_time = 0.5 # wait 0.5s until target event is sent to only record last second
numtrials_per_cond=80

#### Using PsychoPy and pygame ####
mywin=visual.Window([window_size,window_size*0.75],color=(-1,-1,-1),units='pix',monitor='testMonitor',winType="pygame")
stim = stimuli_(mywin, color)

Trialclock = core.Clock()

numtrials_per_cond_act=np.atleast_2d(np.zeros(2))
gol=GOL(grid_size)

# sending start event that can be read by the data collector
sendEvent('stimulus.training','start')
done=False

# run calibration
while (numtrials_per_cond_act.sum(0)<numtrials_per_cond).any()==True & (not done):

    if use_gol: # obtain latest gol frame
        data_ = gol().reshape(grid_size, grid_size) + 0
        data_[data_ == 0] = -1
    else: # background is black screen
        data_ = -np.ones((grid_size, grid_size),dtype='float32')

    stim.pattern1.setImage(data_)
    numtrials_per_cond_act=stim(numtrials_per_cond_act)
    mywin.flip() # update screen
    ev_ = event.getKeys()
    if len(ev_)>0:
        ev_=ev_[-1]
        if ev_ == 'escape':
            done = True
# if calibration ends, exit screen
sendEvent('stim.training','end')
stim.pattern5.setText('end')
mywin.flip()
core.quit()