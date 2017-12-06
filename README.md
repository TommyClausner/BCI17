# BCI17 

### MATLAB part

There are two relevant MATLAB files: calib_sig.m used to record data and train the classifier and feedback_sig.m / SS_feedback_sig.m for doing the online classification when running the game in BCI mode.

### Python part
There are two relevant Python files: calib_stim.py providing the stimulus material for training the classifier and brainflyTest.py / SS_Game_BCI.py containing the actual game.

### Further notes
brainflyTest.py provides a basic version of the original brainfly-game and can be run with additional stimulation (e.g. steady state stimulation) or without.

SS_Game_BCI.py provides a very sophisticated version employing original space invaders graphics and further eyecandy! (Thanks to Steven!!) 

### Using the GUI

In order to use the GUI define your matlab and python instances in the config.txt
The GUI will call this file and looking for MATLABroot and Pythonroot. Both have to be defined in a way that some could plug in a script right behind the root and it would run.

Example (Unix case):
MATLABroot = ~/path_to_MATLAB/bin/matlab -nosplash -nodesktop -r
Pythonroot = ~/path_to_iPython/ipython

The GUI internally would interpret the above commands as follows:
~/path_to_MATLAB/bin/matlab -nosplash -nodesktop -r "try;run('myscript.m');exit;end;exit"
~/path_to_iPython/ipython myscript.py

Example (Windows case):
MATLABroot = matlab -nosplash -nodesktop -r
Pythonroot = cmd /c  py -2.7

The GUI internally would interpret the above commands as follows:
matlab -nosplash -nodesktop -r "try;run('myscript.m');end"
cmd /c  py -2.7 myscript.py

Note that the relative paths to the respective scripts are set internally.

if debug = 1 then the GUI will run in debugmode -> set to 0 if real EEG use is intended

START THE GUI BY DOUBLE CLICKING THE RESPECTIVE "START_for_Windows/unix.bat/.sh"

Further note:
eeg_quickstart.sh/.bat and debug_quickstart.sh/.bat were modified in order to output PIDs to pids.txt
This file is used to kill the respective processes within the GUI

Commands:
- Switch keyboard mode using 'k'
- Switch EEG mode using 'e'
- Switch music on/off using 'm'
- Switch game mode using 'g'
- use arrow keys to navigate 'up' and 'down'
- hit 'return' to select
- during the calibration hit 'esc' to exit
- during the game hit 'esc' (basic version) or close window (Steven's version) to exit

When Keyboard mode is selected, the feedback_sig.m will not be called. Hence the game window opens much faster.

Further exit commands were added at the end of each MATLAB script to kill the respective instance. When doing the calibration, the exit command will be sent after closing the figure windows.

Aborting the calibration (hitting 'esc') will cause the classifier to be trained on all available data so far.

### Known Bugs
- in eeg_quickstart.sh/.bat the file startMobita.sh/.bat crashes -> can't find /dataAcq/buffer/bin/startMobita.sh./.bat
