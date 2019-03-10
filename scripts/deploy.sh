#!/bin/bash

echo Activating Virtual Environment...
source venv/bin/activate
echo

echo Booting MEERA...
python3.6 ./src/index.py

deactivate