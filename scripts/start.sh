#!/bin/bash

x-terminal-emulator -e scripts/deploy.sh
sleep 5
x-terminal-emulator -e scripts/telegram.sh