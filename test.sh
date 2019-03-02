#!/bin/bash

echo Activating Virtual Environment...
source venv/bin/activate
echo

echo $(/usr/bin/env)

echo Running tests...
pytest -s tests/

deactivate