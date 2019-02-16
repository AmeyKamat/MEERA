#!/bin/bash

echo Activating Virtual Environment...
source venv/bin/activate
echo

echo Booting MEERA...
mkdir log
chmod +w log
chmod +x index.py
./index.py

deactivate