#!/bin/bash

# Change to script directory
cd "$(dirname "$0")"

# Run the bot for 2BHK (logs to daft_bot_2bhk.log)
poetry run daft-bot --override .2bhk.env

# Uncomment below to search for multiple configurations:
# Each will have its own log file (daft_bot_2bhk.log, daft_bot_3bhk.log, etc.)
#
# poetry run daft-bot --override .2bhk.env
# poetry run daft-bot --override .3bhk.env
# poetry run daft-bot --override .4bhk.env
