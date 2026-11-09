#!/bin/zsh
cd -- "${0:A:h}" || exit 1
echo 'If the simulation server is still running, stop it with Ctrl+C in its terminal first.'
read 'reply?Press Enter when ready to start the Pico with Telegram: '
./venv/bin/python server.py --port /dev/cu.usbmodem21201 --telegram-token-prompt
echo
read 'reply?Press Enter to close this window.'
