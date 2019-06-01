#!/bin/bash

invalid_command_message="Invalid Command: '$1'
Try \"./meera.sh help\" to list all supported commands.
"

application="all"

if [ $# = 1 ]; then
	application=$1
fi

echo Activating Virtual Environment...
source venv/bin/activate
echo

echo "Waking MEERA up!"

case $application in

'server')				python3.6 ./src/index.py > ./log/server.out.log 2> ./log/server.err.log;;
'telegram-client')		python3.6 ./src/interface/telegram_bot/daemon.py > ./log/client.out.log 2> ./log/client.err.log;;
'all')					./scripts/start.sh;;
*)						echo "$invalid_command_message";;

esac

deactivate