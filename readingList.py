import os

def queryAndMakeList():
    # Variables that will prob be customizable later
    output_length = 10
    output_page_number = 1

    # List setup
    cache = createCache()
    orderedKeys = rank(cache.keys())

    return

def getBookmarkedPages(): # return dict of page urls
    pass

def getReadPages(): # return dict of page urls
    pass

def bookmark(page):
    with open("bookmarks.txt", a) as bookmarkFile:
        bookmarks = bookmarkFile.readlines()

        for bookmark in bookmarks:
            if bookmark is page.url: return -1
        
        print(page.url)
        return 1

def removeBookmark(page):
    bookmarkExists = False

    with open("bookmarks.txt", "r") as bookmarkFile:
        bookmarks = bookmarkFile.readlines()

    with open("bookmarks.txt","w") as bookmarkFile:
        for bookmark in bookmarks:
            if bookmark.strip("\n") is page.url:
                bookmarkExists = True
            else: 
                bookmarkFile.write(bookmark)

        return 1
    

def rank(cache):
    results = sorted(cache.values(), key=lambda x: cache.get(x).ref_count, reverse=True)
    readPages = getReadPages()

    # Ranks which pages to read while ignoring already read pages
    i = 1
    for x in results:
        if not readPages.get(x.url):
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


