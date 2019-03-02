#!/bin/bash

echo Activating Virtual Environment...
source venv/bin/activate
echo

echo Running tests...
chmod +x ./tests/*
pytest -s tests/

deactivate