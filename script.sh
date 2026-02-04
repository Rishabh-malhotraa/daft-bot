#!/bin/bash

# Change to script directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

# Run the bot for 2BHK (logs to daft_bot_2bhk.log)
python -m daft_bot --override .2bhk.env

# Uncomment below to search for multiple configurations:
# Each will have its own log file (daft_bot_2bhk.log, daft_bot_3bhk.log, etc.)
#
# python -m daft_bot --override .2bhk.env
# python -m daft_bot --override .3bhk.env
# python -m daft_bot --override .4bhk.env
