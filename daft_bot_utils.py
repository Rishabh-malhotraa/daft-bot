import sys


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


def update_cache(cache, cache_file="listings.txt"):
    try:
        f = open(cache_file, 'w')
        for i in cache.keys():
            f.write("%s\n" % i)
        f.close()
        print("[*] Cache updated.")
    except:
        print("[E] Unable to write cache file.")
        sys.exit(-1)
