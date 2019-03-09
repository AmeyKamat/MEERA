#!/bin/bash

echo Activating Virtual Environment...
source venv/bin/activate
echo

echo Training models...
python3.6 ./meera/trainer.py  $1

deactivate