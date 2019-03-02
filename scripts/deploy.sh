#!/bin/bash

echo Activating Virtual Environment...
source venv/bin/activate
echo

echo Booting MEERA...
chmod +x index.py
python3.6 ./index.py

deactivate