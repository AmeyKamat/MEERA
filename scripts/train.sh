#!/bin/bash

echo Activating Virtual Environment...
source venv/bin/activate
echo

echo Training models...
python3.6 ./src/trainer.py  $1
./scripts/evaluate.sh

deactivate