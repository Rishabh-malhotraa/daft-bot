import sys
from daftlistings import Listing


def load_cache(cache_file="listings.txt"):
    # load cache if exists
    print("[*] Loading Cache.")
    cache = {}
    try:
        f = open(cache_file, 'r')
        for i in f.readlines():
            cache[i.strip()] = ""
        f.close()
    except:
        print("[W] Unable to read cache file. Don't worry if you start from scretch.")
    return cache


def save_images(listings: list[Listing], images_file="images.txt"):
    try:
        f = open(images_file, 'a')
        for l in listings:
            f.write("\n%s\n%s\n%s\n\n" %
                    (('=' * 50), l.title,  l.daft_link))

            for i in l.images:
                image_link = i["size720x480"] if (
                    "size720x480" in i.keys()) else ""
                f.write("%s\n" % image_link)
        f.close()
        print("[*] Images Saved.")
    except Exception as e:
        print(e)
        print("[E] Unable to Save Images.")


def update_cache(cache: dict, cache_file="listings.txt"):
    try:
        f = open(cache_file, 'w')
        for i in cache.keys():
            f.write("%s\n" % i)
        f.close()
        print("[*] Cache updated.")
    except:
        print("[E] Unable to write cache file.")
        sys.exit(-1)
