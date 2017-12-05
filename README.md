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
~/path_to_MATLAB/bin/matlab -nosplash -nodesktop -r "try;run('myscript.m');end"
~/path_to_iPython/ipython myscript.py

Example (Windows case):
MATLABroot = C:\path_to_MATLAB\matlab.exe -nosplash -nodesktop -r
Pythonroot = C:\path_to_MATLAB\python.exe

The GUI internally would interpret the above commands as follows:
C:\path_to_MATLAB\matlab.exe -nosplash -nodesktop -r "try;run('myscript.m');end"
C:\path_to_MATLAB\python.exe myscript.py

Note that the relative paths to the respective scripts are set internally.

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
- calling the EEG viewer yields a problem when closing it... the GUI window becomes unresponsive and has to be force killed. However this is only the case for the EEG viewer and does not affect other functions. The problem seems to be that after closing the figure window, MATLAB is still activated... if someone knows how to fix that, let me know ;) SOLVED

- sometimes the buffer is not initialised properly. In order to cope with that switching EEG mode on and off again works in most cases.
