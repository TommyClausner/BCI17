import sys
from time import sleep
import os
import matplotlib
import numpy as np

from psychopy import visual, core,event


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

import platform

##### BCI enable #######
if __name__ == "__main__":
    braincontrol = 1#int(sys.argv[1])
else:
    braincontrol=0
print(braincontrol)
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

# setup stimuli
class stimuli_(object):
        def __init__(self, mywin):
            self.mywin = mywin
            win_s = self.mywin.size
            self.pattern1 = visual.ImageStim(win=mywin, name='pattern1', units='pix',
                                        size=[win_s[0], win_s[1] - win_s[0] / 8], pos=(0, win_s[0] / 8))

            self.pattern2 = visual.Circle(win=self.mywin,
                                          pos=[win_s[0] / 2 - win_s[0] / 10 + 10, -win_s[1] / 2 + win_s[1] / 10],
                                          radius=win_s[0] / 16, edges=32, fillColor=[1, -1, -1], lineColor=[-1, -1, -1],
                                          units='pix')
            self.pattern3 = visual.Circle(win=self.mywin,
                                          pos=[-win_s[0] / 2 + win_s[0] / 10 - 10, -win_s[1] / 2 + win_s[1] / 10],
                                          radius=win_s[0] / 16, edges=32, fillColor=[-1, -1, 1], lineColor=[-1, -1, -1],
                                          units='pix')
            self.pattern4 = visual.ShapeStim(win=self.mywin, vertices=(
                [-win_s[0] / 2, -(win_s[1] / 2 - win_s[1] / 5 - 10)],
                [-win_s[0] / 2, -(win_s[1] / 2 - win_s[1] / 5 - 9)],
                [win_s[0] / 2, -(win_s[1] / 2 - win_s[1] / 5 - 9)],
                [win_s[0] / 2, -(win_s[1] / 2 - win_s[1] / 5 - 10)]),
                                             lineColor=[1, 1, 1], units='pix')
            self.pattern5 = visual.TextStim(win=mywin, pos=(0, -(win_s[1] / 2 - win_s[1] / 10 - 10)), text='+',
                                       color=[1, 1, 1], units='pix', height=win_s[0] / 8)
            self.pattern6 = visual.TextStim(win=mywin, pos=(0, -(win_s[1] / 2 - win_s[1] / 10 - 10)), text='',
                                       color=[1, 1, 1], units='pix', height=win_s[0] / 8)
            self.pattern7 = visual.TextStim(win=mywin, pos=(0, -(win_s[1] / 2 - win_s[1] / 10 - 10)), text='',
                                       color=[1, 1, 1], units='pix', height=win_s[0] / 8)

            self.Trialclock = core.Clock()

            self.start_time1 = self.Trialclock.getTime()
            self.start_time2 = self.Trialclock.getTime()
            self.start_time3 = self.Trialclock.getTime()
            self.start_time4 = self.Trialclock.getTime()

            self.pattern1.setAutoDraw(True)
            self.pattern2.setAutoDraw(True)
            self.pattern3.setAutoDraw(True)
            self.pattern4.setAutoDraw(True)
            self.pattern5.setAutoDraw(True)
            self.pattern6.setAutoDraw(True)
            self.pattern7.setAutoDraw(True)

            self.instructions=['<','>']

        def __call__(self, numtrials_per_cond_act,freq=15, freq2=10):
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

            if ((Trialclock.getTime() - self.start_time3) > trialtime):
                self.start_time3 = Trialclock.getTime()
                values_ = ['1 LH','2 RH']
                idx = np.random.randint(2)
                sendEvent('stim.target', values_[idx])

                numtrials_per_cond_act[0][idx] += 1
                self.pattern5.setPos(self.pattern2.pos)
                self.pattern5.setText(self.instructions[idx])

                self.pattern6.setPos(self.pattern3.pos)
                self.pattern6.setText(self.instructions[idx])

                self.pattern7.setText(self.instructions[idx])
            return numtrials_per_cond_act

grid_size=100
window_size=800

trialtime=4.5 # time per trial
numtrials_per_cond=20

#### Using PsychoPy and pygame ####
mywin=visual.Window([window_size,window_size*0.75],color=(-1,-1,-1),units='pix',monitor='testMonitor',winType="pygame")
stim = stimuli_(mywin)

Trialclock = core.Clock()

numtrials_per_cond_act=np.atleast_2d(np.zeros(2))

gol=GOL(grid_size)
sendEvent('stimulus.training','start')
done=False

# run calibration
while (numtrials_per_cond_act.sum(0)<numtrials_per_cond).any()==True & (not done):


    data_ = gol().reshape(grid_size, grid_size) + 0
    data_[data_ == 0] = -1
    stim.pattern1.setImage(data_)
    numtrials_per_cond_act=stim(numtrials_per_cond_act)
    mywin.flip()
    ev_ = event.getKeys()
    if len(ev_)>0:
        ev_=ev_[-1]
        if ev_ == 'escape':
            sendEvent('stim.tartget', 0)
            done = True

sendEvent('stim.training','end')
stim.pattern5.setText('end')
mywin.flip()
core.quit()