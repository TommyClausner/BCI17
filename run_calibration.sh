#!/bin/bash

#use: sh run_game.sh <matlabroot path> <path to script to execute> <python interpreter path> <python script path>

#example: sh run_game.sh /Applications/MATLAB_Release.app /Users/User/scripts/MATLABscript.m  /usr/bin/ipython /Users/User/scripts/Pythonscript.py

$1/bin/matlab -nodesktop -r "run('$2')" &
sleep 10s
$3 $4

