#!/bin/env python

cd /root/daft-bot
python3 daft_bot.py 2 >> output.log

# Use the following Script if you want to simultaneously search for 2BHK 3BHK and 4BHK accomodations
# python3 daft_bot.py 2 >> output.log && python3 daft_bot.py 3 >> output.log && python3 daft_bot.py 4 >> output.log 
