#!/bin/bash
# finds Python instance to use by reading the respective line in the config.txt
# uses this instance to launch the actual graphical user interface
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python_=$(grep -w  "^Pythonroot" $DIR/config.txt | cut -d '=' -f2)
$python_ $DIR/brainflyGUI.py
