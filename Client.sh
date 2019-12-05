#!/bin/bash

# export WORKON_HOME=$HOME/.virtualenvs
# export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh
source ~/.profile

workon cv
python ~/Desktop/CITE301/Client_Main.py

