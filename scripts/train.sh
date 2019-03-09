#!/bin/bash

echo Activating Virtual Environment...
source venv/bin/activate
echo

echo Training models...
chmod +x ./meera/trainer.py
python3.6 ./meera/trainer.py  $1

deactivate