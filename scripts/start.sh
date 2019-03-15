#!/bin/bash

x-terminal-emulator -e scripts/deploy.sh server
sleep 5
x-terminal-emulator -e scripts/deploy.sh telegram-client