#!/bin/zsh
cd -- "${0:A:h}" || exit 1
./venv/bin/python server.py --setup-telegram
echo
read 'reply?Press Enter to close this window.'
