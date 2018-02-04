import sys,os,time
import subprocess
import signal
import pygame
from psychopy import visual, core,event
import platform
from PIL import Image
import gc
import pdb

def initModules():
    # presetting for some modules
    gc.collect()
    pygame.init()
    pygame.display.init()

#pdb.set_trace()
initModules()

def initPaths():

    # setup relative directories
    main_path=os.path.dirname(os.path.abspath(__file__))+os.sep


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

    pathsettings=open(main_path+"config.txt","r").read().split("\n")

    idx_MATLAB=int([i for i, e in enumerate([str.find(path_,"MATLABroot") for path_ in pathsettings]) if e == 0][0])
    idx_Python=int([i for i, e in enumerate([str.find(path_,"Pythonroot") for path_ in pathsettings]) if e == 0][0])
    idx_debug = int([i for i, e in enumerate([str.find(path_, "debug") for path_ in pathsettings]) if e == 0][0])

    # setup roots
    MATLABrootpath=pathsettings[idx_MATLAB][str.find(pathsettings[idx_MATLAB],'=')+1:]
    Pythonrootpath=pathsettings[idx_Python][str.find(pathsettings[idx_Python],'=')+1:]
    initdebug=bool(int((pathsettings[idx_debug][str.find(pathsettings[idx_debug], '=') + 1:]).replace(' ', '')))
    print(initdebug)
    return MATLABrootpath,Pythonrootpath,main_path,BCI_buff_path,bufferpath,sigProcPath,assetpath,functionspath,initdebug

MATLABrootpath,Pythonrootpath,main_path,BCI_buff_path,bufferpath,sigProcPath,assetpath,functionspath,initdebug=initPaths()


def setupOS():
    # setup video drivers
    if platform.system() == 'Windows':
        os.environ['SDL_VIDEODRIVER'] = 'windib'#'directx'
        sleep_timer=0.09
    else:
        sleep_timer=0.09
        os.environ['SDL_VIDEODRIVER'] = 'quartz'
    return sleep_timer

def killbuff(BCI_buff_path_int=BCI_buff_path):

    if platform.system() == 'Windows':
        try:
            PID=open(main_path+BCI_buff_path_int+"pids.txt")
            PID=PID.read()[:-1]
            os.system("start cmd /c taskkill /PID "+PID)
            print('killed those processes: '+PID)
        except:
            pass
    else:
        killthose_pids = []
        try:
            with open(main_path+BCI_buff_path_int+"pids.txt", 'r') as pids:
                for line in pids:
                    for pid_ in line.split():
                        killthose_pids.append(pid_)

            for kill_pid in killthose_pids:
                try: os.kill(int(kill_pid), signal.SIGTERM)
                except: pass
            print('killed those processes: ')
            print(killthose_pids)
        except: pass



def debug_mode(isdebug=False):

    killbuff()

    # run buffer components
    if isdebug:
        if platform.system() == 'Windows':
            os.chdir(main_path + BCI_buff_path)
            subprocess.Popen('start debug_quickstart.bat %', shell=True)
        else:
            subprocess.Popen(main_path+BCI_buff_path+'debug_quickstart.sh &', shell=True)
    else:
        if platform.system() == 'Windows':
            os.chdir(main_path + BCI_buff_path)
            subprocess.Popen('start eeg_quickstart.bat %', shell=True)
        else:
            subprocess.Popen(main_path + BCI_buff_path + 'eeg_quickstart.sh &', shell=True)

def setupScripts():
    # setup scripts
    # That part is important: it uses the interpreters set in config.txt to call the respective scripts
    # the general syntax is: your_interpreter your_script

    # the order of the scripts is:
    #   (0): Signal Viewer (MATLAB)                     default: /private/sigViewer_wrapper.m
    #   (1): Calibration Signal (MATLAB)                default: /private/calib_sig.m
    #   (2): Feedback Signal (MATLAB)                   default: /private/feedback_sig.m
    #   (3): Calibration Stimulus (Python)              default: /private/calib_stimpy
    #   (4): Feedback Stimulus (Python)                 default: /private/brainflyTest.py
    #   (5): Feedback Stimulus v2 (Python)              default: /private/SS_Game_BCI.py

    # The scripts are called in within the key listener object (class below):
    # depending on the operating system a suffix will be appended in order to make the system command not wait (% or &)
    # Further a boolean indicating keyboard control will be used in Feedback Stimuli

    scripts_=[]
    scripts_.append(MATLABrootpath+' '+'"'"try;run('"+main_path+functionspath+"sigViewer_wrapper.m""');exit;end;exit"'"')
    scripts_.append(MATLABrootpath+' '+'"'"try;run('"+main_path+functionspath+"calib_sig.m""');exit;end;exit"'"')
    scripts_.append(MATLABrootpath+' '+'"'"try;run('"+main_path+functionspath+"feedback_sig.m"+"');exit;end;exit"'"')
    scripts_.append(Pythonrootpath+' '+'"'+main_path+functionspath+"calib_stim.py"+'"')
    scripts_.append(Pythonrootpath+' '+'"'+main_path+functionspath+"brainflyTest.py"+'"')
    scripts_.append(Pythonrootpath+' '+'"'+main_path+functionspath+"SS_Game_BCI.py"+'"')
    return scripts_

def setupMainwindow(winsize=[800,600]):

    # load assets
    icons=[]
    icons.append(Image.open(main_path+assetpath+os.sep+"EEG_off_icon.png"))
    icons.append(Image.open(main_path+assetpath+os.sep+"EEG_on_icon.png"))
    icons.append(Image.open(main_path+assetpath+os.sep+"set_False_icon.png"))
    icons.append(Image.open(main_path+assetpath+os.sep+"set_True_icon.png"))
    icons.append(Image.open(main_path+assetpath+os.sep+"keyboard_icon.png"))
    icons.append(Image.open(main_path + assetpath + os.sep + "high_res_off.png"))
    icons.append(Image.open(main_path + assetpath + os.sep + "high_res_on.png"))
    icons.append(Image.open(main_path+assetpath+os.sep+"GOL_on_icon.png"))
    icons.append(Image.open(main_path+assetpath+os.sep+"GOL_off_icon.png"))
    icons.append(Image.open(main_path+assetpath+os.sep+"color_on_icon.png"))
    icons.append(Image.open(main_path+assetpath+os.sep+"color_off_icon.png"))
    icons.append(Image.open(main_path+assetpath+os.sep+"time_on.png"))
    icons.append(Image.open(main_path+assetpath+os.sep+"time_off.png"))


    # setup GUI
    mywin=visual.Window(winsize,units='pix',monitor='testMonitor',winType="pygame")

    # background
    BG_=visual.ImageStim(mywin,image=Image.open(main_path+assetpath+os.sep+"GUI_background.png"))
    BG_.setAutoDraw(True)

    # EEG indicator
    EEG_indicator=visual.ImageStim(mywin,image=icons[int(not initdebug)],pos=[-300,250],units='pix')
    EEG_indicator.setAutoDraw(True)
    EEG_indicator_text=visual.TextStim(mywin,text='EEG mode',font='Futura',pos=[-300,210],units='pix',height=30)
    EEG_indicator_text.setAutoDraw(True)

    
    # GOL indicator
    GOL_indicator=visual.ImageStim(mywin,image=icons[7],pos=[-300,150],units='pix', size=(75,75))
    GOL_indicator.setAutoDraw(True)

    # Color indicator
    Color_indicator=visual.ImageStim(mywin,image=icons[9],pos=[-300,75],units='pix', size=(75,75))
    Color_indicator.setAutoDraw(True)

    # Time indicator
    Time_indicator=visual.ImageStim(mywin,image=icons[12],pos=[325,-150],units='pix', size=(75,75))
    Time_indicator.setAutoDraw(True)

    # Keyboard indicator
    Keyboard_=visual.ImageStim(mywin,image=icons[4],pos=[-300,-250])
    Keyboard_.setAutoDraw(True)
    Keyboard_indicator=visual.ImageStim(mywin,image=icons[3],pos=[-200,-250])
    Keyboard_indicator.setAutoDraw(True)

    # High res indicator
    high_res_indicator = visual.ImageStim(mywin, image=icons[6], pos=[325, -250])
    high_res_indicator.setAutoDraw(True)

    # main menu
    main_menu=[]
    main_menu.append(visual.TextStim(mywin,text='EEG Viewer',font='Helvetica',pos=[0,-50],units='pix',height=36))
    main_menu[0].setAutoDraw(True)

    main_menu.append(visual.TextStim(mywin,text='Calibration',font='Helvetica',pos=[0,-100],units='pix',height=36))
    main_menu[1].setAutoDraw(True)

    main_menu.append(visual.TextStim(mywin,text='Play Game',font='Helvetica',pos=[0,-150],units='pix',height=48))
    main_menu[2].setAutoDraw(True)

    main_menu.append(visual.TextStim(mywin,text='exit',font='Helvetica',pos=[0,-200],units='pix',height=36))
    main_menu[3].setAutoDraw(True)

    main_menu.append(visual.Line(mywin, start=((main_menu[2].pos[0]-main_menu[2].width/2),(main_menu[2].pos[1]-main_menu[2].height/2)),
                              end=((main_menu[2].pos[0]+main_menu[2].width/2), (main_menu[2].pos[1]-main_menu[2].height/2)),units='pix'))
    main_menu[4].setAutoDraw(True)

    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.mixer.init(44100, -16,2,2048)

    pygame.mixer.music.load(main_path+assetpath+os.sep+'backgroundmusic.wav')
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)
    return mywin,main_menu,EEG_indicator,GOL_indicator,Color_indicator, Time_indicator, Keyboard_indicator,high_res_indicator,icons

def updateMenu():
    main_menu[4].start = ((main_menu[curr_menu_idx].pos[0] - main_menu[curr_menu_idx].width / 2),
                          (main_menu[curr_menu_idx].pos[1] - main_menu[curr_menu_idx].height / 2))

    main_menu[4].end = ((main_menu[curr_menu_idx].pos[0] + main_menu[curr_menu_idx].width / 2),
                        (main_menu[curr_menu_idx].pos[1] - main_menu[curr_menu_idx].height / 2))
    mywin.flip()
    return 0

def splashscreen_():
    #pdb.set_trace()
    mywin_splash = visual.Window([400,300], units='pix', monitor='testMonitor', winType="pygame")
    BG_ = visual.ImageStim(mywin_splash, image=Image.open(main_path + assetpath + os.sep + "splashscreen.jpg"))
    BG_.setAutoDraw(True)
    mywin_splash.flip()
    return mywin_splash

class keylistener_(object):

    def __init__(self):
        # predefinition of all sorts of stuff

        self.curr_menu_idx = 2 # selection initially on "Play Game"
        self.EEG_is_on = not initdebug
        self.Keyboard_is_on = True
        self.braincontrol=' '+str(int(not self.Keyboard_is_on))
        self.update_menu = 1 # to draw the main window for the first time
        self.done = False # for the while loop that executes the GUI
        self.music=True
        self.Stevens_version=True # set to False if you prefer the default brainFly version
        self.color_mode = True # set to False for non-color stimuli
        self.use_gol = True # set to False for calibration without the game of life
        self.use_timer = False # set to True to set time limit in game to 90 seconds

        if platform.system() == 'Windows':
            self.skip_suffix = ' %'
        else:
            self.skip_suffix = ' &'

    def __call__(self, ev_):
        if len(ev_) > 0: # ensure that keyboard events exist

            #ev_ = ev_[-1]  # use lates event

            # navigation in main window
            if ev_ == 'up' or ev_[pygame.K_UP]:
                self.curr_menu_idx -= 1
                self.update_menu = 1

            if ev_ == 'down' or ev_[pygame.K_DOWN]:
                self.curr_menu_idx += 1
                self.update_menu = 1

            # switching game mode
            if ev_ == 'g' or ev_[pygame.K_g]:
                self.Stevens_version=not self.Stevens_version
                high_res_indicator.image = icons[int(self.Stevens_version)+5]
                self.update_menu = 1

            # switching eeg mode
            if ev_ == 'e' or ev_[pygame.K_e]:
                self.EEG_is_on = not self.EEG_is_on
                EEG_indicator.image = icons[int(self.EEG_is_on)]
                self.update_menu = 1
                debug_mode(not self.EEG_is_on)

            # switching music on/off
            if ev_ == 'm' or ev_[pygame.K_m]:
                self.music = not self.music
                pygame.mixer.music.set_volume(int(self.music))

            # switching keyboard on/off
            if ev_ == 'k' or ev_[pygame.K_k]:
                self.Keyboard_is_on = not self.Keyboard_is_on
                Keyboard_indicator.image = icons[int(self.Keyboard_is_on) + 2]
                self.braincontrol=' '+str(int(not self.Keyboard_is_on))
                self.update_menu = 1

            # switching color mode    
            if ev_ == 'c' or ev_[pygame.K_c]:
                self.color_mode = not self.color_mode
                Color_indicator.image = icons[int(not self.color_mode)+9]
                self.update_menu = 1        

            # switching game of life   
            if ev_ == 'u' or ev_[pygame.K_u]:
                self.use_gol = not self.use_gol
                GOL_indicator.image = icons[int(not self.use_gol) + 7]
                self.update_menu = 1  

            # switching time limit in game 
            if ev_ == 't' or ev_[pygame.K_t]:
                self.use_timer = not self.use_timer
                Time_indicator.image = icons[int(not self.use_timer) + 11]
                self.update_menu = 1        

        # loop the menu
        if self.curr_menu_idx < 0:
            self.curr_menu_idx = 3

        if self.curr_menu_idx > 3:
            self.curr_menu_idx = 0

        # check selection
        if ev_ == 'return' or ev_[pygame.K_ESCAPE] or ev_[pygame.K_RETURN]:

            # 'exit' was selected
            if self.curr_menu_idx == 3:
                self.done = True

            else:
                # turn off music when necessary
                if self.curr_menu_idx != 0:
                    self.music = not self.music
                    pygame.mixer.music.set_volume(0)

                # call signal Viewer
                if self.curr_menu_idx == 0:
                    try: subprocess.Popen(scripts_[0]+self.skip_suffix,shell=True);print(scripts_[0]+self.skip_suffix)
                    except: pass

                # call calibration
                if self.curr_menu_idx == 1:
                    try: subprocess.Popen(scripts_[1]+self.skip_suffix,shell=True);print(scripts_[1]+self.skip_suffix);time.sleep(15)
                    except: pass
                    try: subprocess.Popen(scripts_[3]+' '+str(int(self.color_mode))+' '+str(int(self.use_gol))+self.skip_suffix, shell=True);print(scripts_[3]+ ' ' + str(int(self.color_mode)) +' '+str(int(self.use_gol)) + self.skip_suffix)
                    except: pass

                # call Game
                if self.curr_menu_idx == 2:
                    if not self.Keyboard_is_on:
                        try: subprocess.Popen(scripts_[2]+self.skip_suffix, shell=True);print(scripts_[2]+self.skip_suffix);time.sleep(15)
                        except: pass
                    try: subprocess.Popen(scripts_[4+int(self.Stevens_version)]+self.braincontrol + ' ' + str(int(self.color_mode)) + ' ' + str(int(self.use_timer)) + self.skip_suffix, shell=True);print(scripts_[4+int(self.Stevens_version)]+self.braincontrol+ ' ' + str(int(self.color_mode)) + ' ' + str(int(self.use_timer))+self.skip_suffix)
                    except: pass

        return self.curr_menu_idx, self.update_menu, self.done

mywin_splash=splashscreen_()

sleep_timer=setupOS()
# initial EEG mode setting -> EEG: set to False
debug_mode(initdebug)

# prepare sub-scripts
scripts_=setupScripts()

time.sleep(10)
mywin_splash.close()

# create screen
mywin,main_menu,EEG_indicator,GOL_indicator,Color_indicator, Time_indicator, Keyboard_indicator,high_res_indicator,icons=setupMainwindow()

# create key-listener
get_keys=keylistener_()

# run GUI
done=False
while not done:
    #ev_=event.getKeys()
    ev_ =  pygame.key.get_pressed()
    curr_menu_idx,update_menu,done=get_keys(ev_)
    if update_menu: update_menu=updateMenu()
    time.sleep(sleep_timer)
# clear screen + kill buffers
mywin.close()
if platform.system() == 'Windows':
    os.system("start cmd /c taskkill /IM cmd.exe")
killbuff()
try: os.remove(main_path+BCI_buff_path+"pids.txt")
except: pass
core.quit()
