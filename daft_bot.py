from email.message import EmailMessage
from daftlistings import Daft, Location, SearchType
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from email_notification import notify
from selenium_bot import send_automated_response
from daft_bot_utils import load_cache, update_cache
from datetime import datetime


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
    print("\n\n==========\n\n")
    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
    daft = daft_with_filters()
    cache = load_cache()
    new_listings = get_new_listings(daft, cache)

    notify(new_listings)

    send_automated_response(new_listings)

    update_cache(cache)
    print("Finished :) \n\n==========\n\n")


if __name__ == '__main__':
    main()
