#!/bin/bash

echo Activating Virtual Environment...
source venv/bin/activate
echo

echo Starting Telegram Daemon...
chmod +x ./interface/telegram_daemon.py
./interface/telegram_daemon.py

deactivate