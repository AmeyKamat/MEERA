#!/bin/bash

echo Installing MEERA...
echo

echo Checking Requirements...
echo python: `python3.6 --version 2>&1`
echo pip: `pip --version`
echo

echo Installing virtualenv...
python3.6 -m pip install virtualenv
echo

echo virtualenv: `virtualenv --version`
echo

echo Creating Virtual Environment...
echo pwd: `pwd`
virtualenv -p /usr/bin/python3.6 venv
echo

echo Activating Virtual Environment...
source venv/bin/activate
echo Virtual Environment Activated.
echo

echo Installing Dependencies...
python3.6 -m pip install -r requirements.txt
echo

chmod +x deploy.sh
./deploy.sh
echo

