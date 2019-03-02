#!/bin/bash

echo Activating Virtual Environment...
source venv/bin/activate
echo

echo Evaluating models...
chmod +x ./nlp/training/evaluator.py
./nlp/training/evaluator.py

deactivate