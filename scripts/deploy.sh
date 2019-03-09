#!/bin/bash

echo Activating Virtual Environment...
source venv/bin/activate
echo

echo Booting MEERA...
chmod +x ./meera/index.py
python3.6 ./meera/index.py

deactivate