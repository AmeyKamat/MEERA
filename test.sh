#!/bin/bash

echo Activating Virtual Environment...
source venv/bin/activate
echo

echo Running tests...
pytest -s tests/

deactivate