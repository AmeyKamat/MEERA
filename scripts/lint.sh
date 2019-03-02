#!/bin/bash

echo Activating Virtual Environment...
source venv/bin/activate
echo

echo Linting the project...
pylint **/*.py --disable=C,R,W
echo

deactivate
