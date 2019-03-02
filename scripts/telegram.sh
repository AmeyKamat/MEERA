#!/bin/bash

echo Activating Virtual Environment...
source venv/bin/activate
echo

echo Starting Telegram Daemon...
chmod +x ./interface/telegram_bot/daemon.py
python3.6 ./interface/telegram_bot/daemon.py

deactivate