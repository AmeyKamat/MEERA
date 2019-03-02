#!/bin/bash

usage_message="
Usage: ./meera.sh [command]

Supported commands:

clean				: cleans the project directory
install				: installs project
lint				: checks for compile time errors
train [iterations]	: trains ML models. Optional parameter: number of iterations. Default value is 50
evaluate			: evaluates ML models
test				: runs tests
start				: starts the deployment
help				: help on supported commands
"

iterations=50

invalid_command_message="Invalid Command: '$1'
Try \"./meera.sh help\" to list all supported commands.
"

no_command_message="No command found.
Try \"./meera.sh help\" to list all supported commands.
"

if [ $# -eq 0 ]; then
	echo "$no_command_message"
	exit 1
fi


if [ $# -eq 2 ]; then
	echo $2
	iterations=$2
fi

case $1 in

'clean')		./scripts/clean.sh;;
'install')		./scripts/install.sh;;
'lint')			pylint **/*.py --disable=C,R,W;;
'train')		./scripts/train.sh "$iterations";;
'evaluate')		./scripts/evaluate.sh;;
'test')			./scripts/test.sh;;
'start')		./scripts/start.sh;;
'help')			echo "$usage_message";;
*)				echo "$invalid_command_message";;

esac