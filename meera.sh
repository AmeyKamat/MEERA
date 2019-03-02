#!/bin/bash

usage_message="
Usage: ./meera.sh [command]

Supported commands:

clean		: cleans the project directory
install		: installs project
lint		: checks for compile time errors
train		: trains ML models
evaluate	: evaluates ML models
test		: runs tests
start		: starts the deployment 
"

error_message="Invalid Command: '$1'
Try \"./meera.sh help\" to list all supported commands.
"



case $1 in

'clean')		./scripts/clean.sh;;
'install')		./scripts/install.sh;;
'lint')			pylint **/*.py --disable=C,R,W;;
'train')		./scripts/train.sh;;
'evaluate')		./scripts/evaluate.sh;;
'test')			./scripts/test.sh;;
'start')		./scripts/start.sh;;
'help')			echo "$usage_message";;
*)				echo "$error_message";;

esac