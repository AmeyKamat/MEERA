#!/bin/bash

echo Activating Virtual Environment...
source venv/bin/activate
echo

echo $(which python3.6)

echo Running tests...
pytest -s tests/

deactivate