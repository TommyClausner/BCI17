#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python_=$(grep -w  "^Pythonroot" $DIR/config.txt | cut -d '=' -f2)
$python_ $DIR/brainflyGUI.py
