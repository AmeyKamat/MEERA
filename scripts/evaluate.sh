#!/bin/bash

echo Activating Virtual Environment...
source venv/bin/activate
echo

echo Evaluating models...
chmod +x ./meera/evaluator.py
./meera/evaluator.py

deactivate