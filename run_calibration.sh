#!/bin/bash
/Applications/MATLAB_R2015a.app/bin/matlab -nodesktop -r "run('/Users/Tommy/Github_repositories/BCI17/calib_sig.m')" &
sleep 10s
/Users/Tommy/anaconda/bin/ipython calib_stim.py
