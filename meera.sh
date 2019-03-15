#!/bin/bash

usage_message="
./meera.sh [command [optional parameters...]]

Supported commands:

clean                                : cleans the project directory
pre-install                          : installs python, pip and other required binaries for installation
install                              : installs project
install-model                        : installs model from download folder
lint                                 : checks for compile time errors
train [iterations]                   : trains ML models. Optional parameter: # of iterations. Default value is 50. Trained models are zipped and placed in `download` folder
evaluate                             : evaluates ML models
test                                 : runs tests
deploy [server|telegram-client|all]  : deploys specified component. Optional parameter: application. Default value is 'all'
help                                 : help on supported commands                                : help on supported commands
"

iterations=50
application=

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


if [ $# = 2 ] && [ "$1" = 'train' ]; then
	iterations=$2
	echo $iterations
fi

if [ $# = 2 ] && [ "$1" = 'deploy' ]; then
	application=$2
fi

chmod +x scripts/*.sh

# Activating Environment Variables
set -a
. .env
set +a

case $1 in

'clean')		 ./scripts/clean.sh;;
'pre-install')   ./scripts/pre-install.sh;;
'install')		 ./scripts/install.sh;;
'lint')			 ./scripts/lint.sh;;
'train')		 ./scripts/train.sh "$iterations";;
'install-model') ./scripts/install-model.sh;;
'evaluate')		 ./scripts/evaluate.sh;;
'test')			 ./scripts/test.sh;;
'deploy')        ./scripts/deploy.sh "$application";;
'help')			 echo "$usage_message";;
*)				 echo "$invalid_command_message";;

esac