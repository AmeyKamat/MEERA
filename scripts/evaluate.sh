#!/bin/bash

echo Activating Virtual Environment...
source venv/bin/activate
echo

echo Evaluating models...
python3.6 ./src/evaluator.py

deactivate