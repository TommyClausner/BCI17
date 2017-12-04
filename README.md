# BCI17 

### MATLAB part

There are two relevant MATLAB files: calib_sig.m used to record data and train the classifier and feedback_sig.m / SS_feedback_sig.m for doing the online classification when running the game in BCI mode.

### Python part
There are two relevant Python files: calib_stim.py providing the stimulus material for training the classifier and brainflyTest.py / SS_Game_BCI.py containing the actual game.

### Terminal wrapper
There are two wrapper functions (unix only :/ ) called run_calibration.sh and run_game.sh
Both functions initialise a MATLAB instance without any MATLAB GUI functions and run the respective script for the analysis. After a delay of 10s the actual Python stimulation will start. For the calibration phase the display handler is kept, so that the classifier result is presented in MATLAB figure windows.
Using those functions works as follows: sh run_calibration.sh <matlabroot> <scriptpath> <pythonroot> <scriptpath>

### Further notes
brainflyTest.py provides a basic version of the original brainfly-game and can be run with additional stimulation (e.g. steady state stimulation) or without.

SS_Game_BCI.py provides a very sophisticated version employing original space invaders graphics and further eyecandy! (Thanks to Steven!!) 

### Using the GUI
The GUI is still under development and currently only runs on Unix (at least I assume without having tested a Windows version :D ). Unix only: In order to use it define your MATLAB and python root in the config.txt file and run start_brainflyGUI_debug.py

The Windows version uses the Python MATLAB engine to do the job.

Note that it does not work using an actual EEG system yet.

- Switch keyboard mode using 'k'
- Switch EEG mode using 'e'
- Switch music on/off using 'm'
- use arrow keys to navigate
- hit 'return' to select
- during the calibration hit 'esc' to exit
- during the game hithit 'esc' (basic version) of close window (Steven's version) to exit

### Known Bugs
- calling the EEG viewer yields a problem when closing it... the GUI window becomes unresponsive and has to be force killed. However this is only the case for the EEG viewer and does not affect other functions. The problem seems to be that after closing the figure window, MATLAB is still activated... if someone knows how to fix that, let me know ;) SOLVED
