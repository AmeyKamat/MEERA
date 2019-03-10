#!/bin/bash

echo Activating Virtual Environment...
source venv/bin/activate
echo

echo Linting the code...
cd src
find . -iname "*.py" | xargs pylint --disable=duplicate-code,too-few-public-methods,missing-docstring
cd ..
echo

echo Linting the tests...
cd tests
find . -iname "*.py" | xargs pylint --disable=duplicate-code,too-few-public-methods,missing-docstring
cd ..
echo

deactivate
