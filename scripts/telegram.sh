#!/bin/bash

echo Activating Virtual Environment...
source venv/bin/activate
echo

echo Starting Telegram Daemon...
python3.6 ./src/interface/telegram_bot/daemon.py

deactivate