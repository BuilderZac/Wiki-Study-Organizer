import os

def queryAndMakeList():
    # Variables that will prob be customizable later
    output_length = 10
    output_page_number = 1

    # List setup
    cache = createCache()
    orderedKeys = rank(cache.keys())

    return

def getReadPages(): # return dict of page urls
    return readEntries("finished.txt")

def getBookmarkedPages(): # return dict of page urls
    return readEntries("bookmarks.txt")

def addRead(page):
    return addEntry(page, "finished.txt")

def removeRead(page):
    return removeEntry(page, "finished.txt")

def bookmark(page):
    return addEntry(page, "bookmarks.txt")

def removeBookmark(page):
    return removeEntry(page, "bookmarks.txt")

def readEntries(file):
    outputDict = dict()
    
    with open(file,"r") as targetFile:
        lines = targetFile.readlines()
    
    for i, line in enumerate(lines):
        outputDict.update({line.strip("\n"): i})

    return outputDict

def addEntry(page, file):
    with open(file, "a") as targetFile:
        lines = targetFile.readlines()

        for line in lines:
            if line.strip("\n") is page.url: return -1
        
        print(page.url)
        return 1

def removeEntry(page, file):
    targetExists = False

    with open(file, "r") as targetFile:
        lines = targetFile.readlines()

    with open(file,"w") as targetFile:
        for line in lines:
            if line.strip("\n") is page.url:
                targetExists = True
            else: 
                targetFile.write(line)
        if targetExists: return 1
        else: return -1

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


