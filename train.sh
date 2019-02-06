#!/bin/bash

echo Activating Virtual Environment...
source venv/bin/activate
echo

echo Booting MEERA...
chmod +x ./nlp/training/trainer.py
./nlp/training/trainer.py

deactivate