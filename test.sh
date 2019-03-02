#!/bin/bash

echo Activating Virtual Environment...
source venv/bin/activate
echo

echo $(/usr/bin/env)

echo Running tests...
python3.6 -m pytest -s tests/

deactivate