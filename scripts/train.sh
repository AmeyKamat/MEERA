#!/bin/bash

echo Activating Virtual Environment...
source venv/bin/activate
echo

echo Training models...
chmod +x ./nlp/training/trainer.py
python3.6 ./nlp/training/trainer.py  $1

deactivate