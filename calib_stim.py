import matplotlib
import numpy as np
matplotlib.rcParams['toolbar']='None'
import matplotlib.pyplot as plt
from psychopy import visual, core, event

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
        alifeind=np.where(gol==1)[0]
        size_idx=len(alifeind)
        neigharrayidx=np.tile(alifeind, (9, 1)).transpose()+np.tile(offsets[0], (size_idx, 1))
        neigharrayidx[neigharrayidx < 0] = 0
        neigharrayidx[neigharrayidx >= (self.gridsize_**2)] = 0

        neigharray=gol[neigharrayidx]
        killidx=(neigharray.sum(1)<3) | (neigharray.sum(1)>4)
        randkillidx=np.random.rand(size_idx)<self.god

        offspridx=np.tile(alifeind, (9, 1)).transpose()[:,range(4)+range(5,9)]+np.tile(offsets[0][range(4)+range(5,9)], (size_idx, 1))
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

        gol[alifeind[killidx+randkillidx]] = 0
        gol[offspridx[aliveidx+randaliveidx]] = 1

        self.gol_old=gol+0
        return self.gol_old


grid_size=100
gol=GOL(grid_size)


#### Using matplotlib ####

# data_=gol().reshape(grid_size,grid_size)+0
#
# arrow_size=round(grid_size/6)
#
# offset_X=np.round(grid_size*0.25)+1
# offset_Y=-grid_size*0.2
#
# fig, ax = plt.subplots()
# LA=ax.arrow(offset_X, offset_Y, -0.00001, 0, head_width=arrow_size, head_length=arrow_size, fc='b', ec='b')
# RA=ax.arrow(offset_X+grid_size/2-np.round(grid_size/16), offset_Y, 0.00001, 0, head_width=arrow_size, head_length=arrow_size, fc='r', ec='r')
# plt.set_cmap('gray')
# fig.set_facecolor('k')
# ax.set_facecolor('k')
# plt.xlim((0,grid_size-1))
# plt.ylim((-grid_size*0.2-arrow_size,grid_size-1))
# ax.get_xaxis().set_visible(False)
# ax.get_yaxis().set_visible(False)
# line = ax.imshow(data_)
# freq=8
#
# dur=1./freq/2.
# start_time1 = time.time()
# start_time2 = time.time()
# start_time3 = time.time()
# n=1
# fig.tight_layout()
# plt.draw()
# plt.show(block=False)
# plt.pause(1)
#
# axbackground = fig.canvas.copy_from_bbox(ax.bbox)
#
# while True:
#
#     line.set_array(gol().reshape(grid_size, grid_size).astype('int') + 0)
#
#     if ((time.time()-start_time1)>(dur*0.4)):
#
#         if (dur*0.5-(time.time()-start_time1))>0:
#             time.sleep(dur*0.5-(time.time()-start_time1))
#         start_time1 = time.time()
#         print(time.time() - start_time3-dur/2.)
#         start_time3 = time.time()
#         RA.set_visible(not RA.get_visible())
#
#     if ((time.time()-start_time2)>(dur*0.9)):
#
#         if (dur-(time.time()-start_time2))>0:
#             time.sleep(dur-(time.time()-start_time2))
#         start_time2 = time.time()
#         LA.set_visible(not LA.get_visible())
#
#     fig.canvas.restore_region(axbackground)
#     ax.draw_artist(LA)
#     ax.draw_artist(RA)
#     ax.draw_artist(line)
#     fig.canvas.blit(ax.bbox)
#     plt.pause(0.000000000001)


#### Using PsychoPy ####

mywin=visual.Window(fullscr=False, monitor='testMonitor', units='deg',color=(-1,-1,-1),size=[800,600])

pattern1 = visual.ImageStim(win=mywin, name='pattern1',units='pix',size=[800,500],pos=(0,100))
pattern2 = visual.ShapeStim(win=mywin,vertices=([300, -280], [300, -180], [400, -230]),fillColor=[-1,-1,1],lineColor=[-1,-1,-1],units='pix')
pattern3 = visual.ShapeStim(win=mywin,vertices=([-300, -280], [-300, -180], [-400, -230]),fillColor=[1,-1,-1],lineColor=[-1,-1,-1],units='pix')
pattern4 = visual.ShapeStim(win=mywin,vertices=([-400, -170], [-400, -171],[400, -171], [400, -170] ),lineColor=[1,1,1],units='pix')
pattern5 = visual.TextStim(win=mywin,pos=(0,-230),text='test',color=[1, 1, 1],units='pix')

instructions=['<','+','>']
Trialclock = core.Clock()


freq=20 # (note 30Hz = hardware max, because: turn pixel on / off = 1 frame -> 30Hz flicker needs 60 frames/s)

dur=1./freq

trialtime=4

start_time1=Trialclock.getTime()
start_time2=Trialclock.getTime()
start_time3=Trialclock.getTime()

pattern1.setAutoDraw(True)
pattern4.setAutoDraw(True)
pattern5.setAutoDraw(True)
pattern5.setText(instructions[np.random.randint(3)])

while True:
    if ((Trialclock.getTime() - start_time1) > (dur * 0.45)):
        if (dur*0.49-(Trialclock.getTime()-start_time1))>0:
            core.wait(dur*0.5-(Trialclock.getTime()-start_time1))
        start_time1 = Trialclock.getTime()
        pattern3.setAutoDraw(not pattern3.autoDraw)

    if ((Trialclock.getTime() - start_time2) > (dur * 0.95)):
        if (dur*0.99-(Trialclock.getTime()-start_time2))>0:
            core.wait(dur-(Trialclock.getTime()-start_time2))
        start_time2 = Trialclock.getTime()
        pattern2.setAutoDraw(not pattern2.autoDraw)

    if ((Trialclock.getTime() - start_time3) > trialtime*0.99):
        if (trialtime*0.99-(Trialclock.getTime()-start_time3))>0:
            core.wait(trialtime-(Trialclock.getTime()-start_time3))
        start_time3 = Trialclock.getTime()
        idx=np.random.randint(3)
        #sendEvent
        pattern5.setText(instructions[idx])

    data_ = gol().reshape(grid_size, grid_size) + 0
    data_[data_ == 0] = -1
    pattern1.setImage(data_)
    mywin.flip()
    #core.wait(1/60.)