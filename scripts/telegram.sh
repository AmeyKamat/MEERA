#!/bin/bash

echo Activating Virtual Environment...
source venv/bin/activate
echo

echo Starting Telegram Daemon...
chmod +x ./meera/interface/telegram_bot/daemon.py
python3.6 ./meera/interface/telegram_bot/daemon.py

deactivate