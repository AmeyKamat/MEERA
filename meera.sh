#!/bin/bash

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
'help')			 ./scripts/help.sh;;
*)				 echo "$invalid_command_message";;

esac