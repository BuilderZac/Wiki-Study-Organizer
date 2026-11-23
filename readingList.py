import os

def queryAndMakeList(zim_file):
    # Variables that will prob be customizable later
    output_length = 10
    output_page_number = 1

    # List setup
    cache = createCache()
    orderedKeys = rank(cache.keys())

    return

def list_menu(zim_file):
    while True:
        print(f"\n=== {zim_file.name} ===")
        print("1. Bookmark/Unbookmark")
        print("2. Mark as Read/Unread")
        print("3. Next Page")
        print("4. Previous Page")
        print("b. Back")

        choice = input("\nChoose an option: ").strip().lower()

        if choice == "1":
            choice2 = input("\nPlease provide URL to bookmark: ").strip()
            bookmark(choice2)
        elif choice == "2":
            choice2 = input("\nPlease provide URL to mark as read: ").strip()
            finishedPage(choice2)
        elif choice == "3":
            nextPage()
        elif choice == "4":
            prevPage()
        elif choice == "b":
            return
        else:
            print("Invalid option.")

def nextPage():
    pass

def prevPage():
    pass

def getReadPages(): # return dict of page urls
    return readEntries("finished.txt")

def getBookmarkedPages(): # return dict of page urls
    return readEntries("bookmarks.txt")

def addRead(url):
    return addEntry(url, "finished.txt")

def removeRead(url):
    return removeEntry(url, "finished.txt")

def finishedPage(url):
    readPages = getReadPages()
    for page in readPages:
        if page is url: 
            if removeRead(url) == 1:
                print("Successfully removed read marker")
                return 1
            else:
                print("ERROR: removeEntry could not find text")
                return -1
    if addRead(url) is 1:
        print("Successfully added read marker")
        return 1
    else:
        print("ERROR: addEntry detected bookmark!")
        return -1

def bookmark(url):
    bookmarks = getBookmarkedPages()
    for bookmark in bookmarks:
        if bookmark is url: 
            if removeBookmark(url) == 1:
                print("Successfully removed bookmark")
                return 1
            else:
                print("ERROR: removeEntry could not find text")
                return -1
    if addBookmark(url) is 1:
        print("Successfully added bookmark")
        return 1
    else:
        print("ERROR: addEntry detected bookmark!")
        return -1
            
    

def addBookmark(url):
    return addEntry(url, "bookmarks.txt")

def removeBookmark(url):
    return removeEntry(url, "bookmarks.txt")

def readEntries(file):
    outputDict = dict()
    
    with open(file,"r") as targetFile:
        lines = targetFile.readlines()
    
    for i, line in enumerate(lines):
        outputDict.update({line.strip("\n"): i})

    return outputDict

def addEntry(url, file):
    with open(file, "a") as targetFile:
        lines = targetFile.readlines()

        for line in lines:
            if line.strip("\n") is url: return -1
        
        print(url)
        return 1

def removeEntry(url, file):
    targetExists = False

    with open(file, "r") as targetFile:
        lines = targetFile.readlines()

    with open(file,"w") as targetFile:
        for line in lines:
            if line.strip("\n") is url:
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
        if readPages.get(x.url):
            results.pop(x)
        else:
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


