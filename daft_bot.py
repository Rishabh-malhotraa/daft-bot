from daftlistings import Daft, Location, SearchType
from dotenv import load_dotenv
from email_notification import notify
from selenium_bot import send_automated_response
from daft_bot_utils import load_cache, update_cache
from datetime import datetime, timedelta
import os

load_dotenv()

# Get Daft Seach Instance with relevant filters


def daft_with_filters():
    daft = Daft()
    daft.set_location(Location.DUBLIN)
    daft.set_min_beds(2)
    daft.set_max_beds(2)
    daft.set_search_type(SearchType.RESIDENTIAL_RENT)
    daft.set_max_price(3000)
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
    print("=====START=====")

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
