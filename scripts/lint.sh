#!/bin/bash

echo Activating Virtual Environment...
source venv/bin/activate
echo

echo Linting the project...
cd meera
pylint **/*.py --disable=C,duplicate-code,too-few-public-methods
cd ..
echo

deactivate
