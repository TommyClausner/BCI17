#!/bin/bash
/Applications/MATLAB_R2015a.app/bin/matlab -nodisplay -nodesktop -r "run('/Users/Tommy/Github_repositories/BCI17/feedback_sig.m')" &
sleep 10s
/Users/Tommy/anaconda/bin/ipython brainflyTest.py
