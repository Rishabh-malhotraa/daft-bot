from daftlistings import Daft, Location, SearchType, Distance
from dotenv import load_dotenv
from email_notification import notify
from selenium_bot import send_automated_response
from daft_bot_utils import load_cache, update_cache
from datetime import datetime, timedelta
import os
import sys


def load_environment():
    load_dotenv(os.path.join(os.getcwd(), '.env'))

    ENV = sys.argv[1] if len(sys.argv) > 1 else '2'

    if ENV == '2':
        load_dotenv(os.path.join(os.getcwd(), '.2bhk.env'))
    elif ENV == '3':
        load_dotenv(os.path.join(os.getcwd(), '.3bhk.env'))
    elif ENV == '4':
        load_dotenv(os.path.join(os.getcwd(), '.4bhk.env'))
    return ENV


def daft_with_filters():
    daft = Daft()
    # daft.set_location(Location.DUBLIN)
    daft.set_location(Location.RANELAGH_DUBLIN, Distance.KM3)
    daft.set_min_beds(os.getenv('rent_min_bedroom'))
    daft.set_max_beds(os.getenv('rent_max_bedroom'))
    daft.set_search_type(SearchType.RESIDENTIAL_RENT)
    daft.set_max_price(os.getenv('rent_max_price'))
    return daft

# search listings on daft and update cache


def get_new_listings(daft, cache):
    new_listings = []
    listings = daft.search()
    for l in listings:
        if l.daft_link in cache:
            continue
        new_listings.append(l)
        cache[l.daft_link] = ''
    print("[*] %d new listing(s) found." % len(new_listings))
    return new_listings


def main():
    ENV = load_environment()
    print("=====START", ENV,  "=====")
    IndianTime = datetime.utcnow() + timedelta(hours=5, minutes=30)
    print(IndianTime.strftime("%m/%d/%Y, %H:%M:%S"))

    daft = daft_with_filters()
    cache = load_cache(os.getenv("cache_file"))

    new_listings = get_new_listings(daft, cache)

    notify(new_listings)
    send_automated_response(new_listings)

    update_cache(cache, os.getenv("cache_file"))
    print("Finished :) \n====END======")


if __name__ == '__main__':
    main()
