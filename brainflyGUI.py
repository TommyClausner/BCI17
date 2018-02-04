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

# This is the actual main window from where everything is administered
# In the appendix of the report a users manual is provided.

# import all necessary libraries
import sys,os,time
import subprocess
import signal
import pygame
from psychopy import visual, core,event
import platform
from PIL import Image
import gc
import pdb

# initializes PyGame window
def initModules():
    # presetting for some modules
    gc.collect()
    pygame.init()
    pygame.display.init()

#pdb.set_trace()
initModules()

# sets up all path dependencies needed for the GUI to run
def initPaths():

    # own path from where the script was run
    main_path=os.path.dirname(os.path.abspath(__file__))+os.sep

    # setup relative sub-directories for each component
    BCI_buff_path="external"+os.sep
    bufferpath = BCI_buff_path+"dataAcq"+os.sep+"buffer"+os.sep+"python"
    sigProcPath = BCI_buff_path+"python"+os.sep+"signalProc"
    assetpath="assets"+os.sep+"GUI_grafix"
    functionspath="private"+os.sep

    # add respective paths
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),main_path+bufferpath))
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),main_path+sigProcPath))
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),main_path+assetpath))
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),main_path+functionspath))
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),main_path+BCI_buff_path))

    # get MATLAB and Python root paths from the config.txt file (Additionally the initial configuration for debug mode is read)
    pathsettings=open(main_path+"config.txt","r").read().split("\n")

    idx_MATLAB=int([i for i, e in enumerate([str.find(path_,"MATLABroot") for path_ in pathsettings]) if e == 0][0])
    idx_Python=int([i for i, e in enumerate([str.find(path_,"Pythonroot") for path_ in pathsettings]) if e == 0][0])
    idx_debug = int([i for i, e in enumerate([str.find(path_, "debug") for path_ in pathsettings]) if e == 0][0])

    # setup roots
    MATLABrootpath=pathsettings[idx_MATLAB][str.find(pathsettings[idx_MATLAB],'=')+1:]
    Pythonrootpath=pathsettings[idx_Python][str.find(pathsettings[idx_Python],'=')+1:]

    # define initial debug mode
    initdebug=bool(int((pathsettings[idx_debug][str.find(pathsettings[idx_debug], '=') + 1:]).replace(' ', '')))
    print(initdebug)
    return MATLABrootpath,Pythonrootpath,main_path,BCI_buff_path,bufferpath,sigProcPath,assetpath,functionspath,initdebug

# calling the function below sets up all folder dependencies necessary for the GUI to run
MATLABrootpath,Pythonrootpath,main_path,BCI_buff_path,bufferpath,sigProcPath,assetpath,functionspath,initdebug=initPaths()

# setting OS specific driver information. Due to various problems with display drivers and the resulting output,
# it is highly recommended to keep the settings as they are
def setupOS():
    # setup video drivers
    if platform.system() == 'Windows':
        os.environ['SDL_VIDEODRIVER'] = 'windib'#'directx'
        # sleep timer is used to limit the number of button press responses to certain maximum (e.g. min 0.09 ~ 11Hz)
        sleep_timer=0.09
    else:
        sleep_timer=0.09
        os.environ['SDL_VIDEODRIVER'] = 'quartz'
    return sleep_timer

# This function is used to kill background processes that are started by the GUI. Within "pids.txt" process IDs are stored,
# as processes are created. Those IDs will be read and killed. Since this works different on Unix and Windows, the
# respective implementation varies slightly
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


# This function is used to switch between real EEG and debug mode
def debug_mode(isdebug=False):

    # Kills all buffer related processes in order to build up the new architecture corresponding to the respective choice
    killbuff()

    # run buffer components
    if isdebug:
        # debug_quickstart.*
        if platform.system() == 'Windows':
            os.chdir(main_path + BCI_buff_path)
            subprocess.Popen('start debug_quickstart.bat %', shell=True)
        else:
            subprocess.Popen(main_path+BCI_buff_path+'debug_quickstart.sh &', shell=True)
    else:
        # eeg_quickstart.*
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
    #   (3): Calibration Stimulus (Python)              default: /private/calib_stim.py
    #   (4): Feedback Stimulus (Python)                 default: /private/brainflyTest.py
    #   (5): Feedback Stimulus v2 (Python)              default: /private/SS_Game_BCI.py

    # The scripts are called within the key listener object (class below):
    # depending on the operating system a suffix will be appended in order to make the system command not wait (% or &)
    # Further a boolean indicating keyboard control will be used in Feedback Stimuli

    # the lines below might seem odd, but what actually happens is that a command is created and send to the default
    # command line tool in the respective language (Batch or Bash). The command is composed by the respective call
    # function for the interpreter instance (MATLAB or Python) followed by the command to open the respective script.
    # In the MATLAB case the script is not called directly but wrapped inside a command. This is due to the fact that
    # the command line Version of MATLAB does not accept script input, but only command input. For this reason the script
    # was wrapped inside a "try" statement

    scripts_=[]
    scripts_.append(MATLABrootpath+' '+'"'"try;run('"+main_path+functionspath+"sigViewer_wrapper.m""');exit;end;exit"'"')
    scripts_.append(MATLABrootpath+' '+'"'"try;run('"+main_path+functionspath+"calib_sig.m""');exit;end;exit"'"')
    scripts_.append(MATLABrootpath+' '+'"'"try;run('"+main_path+functionspath+"feedback_sig.m"+"');exit;end;exit"'"')
    scripts_.append(Pythonrootpath+' '+'"'+main_path+functionspath+"calib_stim.py"+'"')
    scripts_.append(Pythonrootpath+' '+'"'+main_path+functionspath+"brainflyTest.py"+'"')
    scripts_.append(Pythonrootpath+' '+'"'+main_path+functionspath+"SS_Game_BCI.py"+'"')
    return scripts_

# Sets up the main window of the GUI
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


    # setup display
    mywin=visual.Window(winsize,units='pix',monitor='testMonitor',winType="pygame")

    # define background
    BG_=visual.ImageStim(mywin,image=Image.open(main_path+assetpath+os.sep+"GUI_background.png"))
    BG_.setAutoDraw(True)

    # EEG indicator logo
    EEG_indicator=visual.ImageStim(mywin,image=icons[int(not initdebug)],pos=[-300,250],units='pix')
    EEG_indicator.setAutoDraw(True)
    EEG_indicator_text=visual.TextStim(mywin,text='EEG mode',font='Futura',pos=[-300,210],units='pix',height=30)
    EEG_indicator_text.setAutoDraw(True)

    
    # GOL indicator logo
    GOL_indicator=visual.ImageStim(mywin,image=icons[7],pos=[-300,150],units='pix', size=(75,75))
    GOL_indicator.setAutoDraw(True)

    # Color indicator logo
    Color_indicator=visual.ImageStim(mywin,image=icons[9],pos=[-300,75],units='pix', size=(75,75))
    Color_indicator.setAutoDraw(True)

    # Time indicator logo
    Time_indicator=visual.ImageStim(mywin,image=icons[12],pos=[325,-150],units='pix', size=(75,75))
    Time_indicator.setAutoDraw(True)

    # Keyboard indicator logo
    Keyboard_=visual.ImageStim(mywin,image=icons[4],pos=[-300,-250])
    Keyboard_.setAutoDraw(True)
    Keyboard_indicator=visual.ImageStim(mywin,image=icons[3],pos=[-200,-250])
    Keyboard_indicator.setAutoDraw(True)

    # eye-candy indicator logo
    high_res_indicator = visual.ImageStim(mywin, image=icons[6], pos=[325, -250])
    high_res_indicator.setAutoDraw(True)

    # main menu - All Text based main choices within the GUI are defined here
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

    # pre-initialize audio
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.mixer.init(44100, -16,2,2048)

    # initialize background music
    pygame.mixer.music.load(main_path+assetpath+os.sep+'backgroundmusic.wav')
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)
    return mywin,main_menu,EEG_indicator,GOL_indicator,Color_indicator, Time_indicator, Keyboard_indicator,high_res_indicator,icons

# update line under the respective menu option of choice
def updateMenu():
    main_menu[4].start = ((main_menu[curr_menu_idx].pos[0] - main_menu[curr_menu_idx].width / 2),
                          (main_menu[curr_menu_idx].pos[1] - main_menu[curr_menu_idx].height / 2))

    main_menu[4].end = ((main_menu[curr_menu_idx].pos[0] + main_menu[curr_menu_idx].width / 2),
                        (main_menu[curr_menu_idx].pos[1] - main_menu[curr_menu_idx].height / 2))
    mywin.flip()
    return 0

# splash screen that is displayed when starting the GUI, while buffer functions are initialized in the background
# This was done to ensure that everything is loaded / initialized properly before any of the critical functions are called.
# This way crashes could mostly be avoided
def splashscreen_():
    #pdb.set_trace()
    mywin_splash = visual.Window([400,300], units='pix', monitor='testMonitor', winType="pygame")
    BG_ = visual.ImageStim(mywin_splash, image=Image.open(main_path + assetpath + os.sep + "splashscreen.jpg"))
    BG_.setAutoDraw(True)
    mywin_splash.flip()
    return mywin_splash

# PyGame Key-listener
# Processes all input from the user in the main window. After changing a respective setting, processes and commands
# that the actual change applies to will be selected. When then using one of the main GUI functions the respective
# settings apply to the respective choices.
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

# show splash screen
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
