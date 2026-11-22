import os

def queryAndMakeList():
    cache = createCache()
    orderedKeys = rank(cache.keys())
    return

def bookmark(page):
    pass

def rank(cache):
    results = sorted(cache.keys(), key=lambda x: cache.get(x).ref_count, reverse=True)
    i = 1
    for x in results:
        cache.get(x).rank = i
        i += 1
    
    print(results) #TODO: remove, used for debug
    return results

# TODO: Check if redundant
def readFile(filename):
    if not os.path.exists(filename): 
        print("Error: Cache file not found")
        return
    
    with open(filename, "r") as cache:
        pages = cache.readlines()
        return pages


