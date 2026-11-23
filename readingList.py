import os
import cachePages
from pathlib import Path

def queryAndMakeList(zim_file):
    # Variables that will prob be customizable later
    output_length = 10

    # List setup
    cache = cachePages.createCache(Path("library/" + zim_file.name))
    orderedKeys = rank(cache.pages)

    list_menu(zim_file, orderedKeys, output_length)
    return

def list_menu(zim_file, orderedKeys, output_length):
    pageNum = 1
    maxPages = 1 + len(orderedKeys)//output_length
    currentDisplay = "pages"
    bookmarkedPages = []
    readPages = []

    while True:
        print(f"\n=== {zim_file.name} ===")
        print("1. Previous Page")
        print("2. Next Page")
        print("3. View Bookmarks")
        print("4. View Read History")
        print("5. Bookmark/Unbookmark")
        print("6. Mark as Read/Unread")
        print("b. Back")
        print()

        if currentDisplay == "pages":
            print("Pages to Read:")
            for n in range(min(len(orderedKeys) - (output_length*(pageNum-1)), output_length)):
                currentPage = orderedKeys[(output_length*(pageNum-1)) + n + 1]
                print(f"{n+1+(output_length*(pageNum-1))}. {currentPage.name} -- {currentPage.url}")
            print(f"====== {pageNum}/{maxPages} ======")

        elif currentDisplay == "bookmarks":
            print("Bookmarks:")
            for n in range(min(len(bookmarkedPages) - (output_length*(pageNum-1)), output_length)):
                currentPage = bookmarkedPages[(output_length*(pageNum-1)) + n]
                print(f"{n+1+(output_length*(pageNum-1))}. {currentPage}")
            print(f"====== {pageNum}/{maxPages} ======")\

        elif currentDisplay == "finished":
            print("Read History:")
            for n in range(min(len(readPages) - (output_length*(pageNum-1)), output_length)):
                currentPage = readPages[(output_length*(pageNum-1)) + n]
                print(f"{n+1+(output_length*(pageNum-1))}. {currentPage}")
            print(f"====== {pageNum}/{maxPages} ======")
        

        choice = input("\nChoose an option: ").strip().lower()

        if choice == "1":
            if pageNum == 1:
                print("No previous page.")
                input("Press any key to continue...")
            else:
                pageNum -= 1            
        elif choice == "2":
            if pageNum == maxPages:
                print("No next page.")
                input("Press any key to continue...")
            else:
                pageNum += 1
        elif choice == "3":
            bookmarkedPages = list(getBookmarkedPages().keys())
            if (len(bookmarkedPages)) > 0:
                pageNum = 1
                maxPages = 1 + len(bookmarkedPages)//output_length
                currentDisplay = "bookmarks"
            else:
                print("No bookmarks to display.")
                input("Press any key to continue...")
        elif choice == "4":
            readPages = list(getReadPages().keys())
            if len(readPages) > 0:
                pageNum = 1
                maxPages = 1 + len(readPages)//output_length
                currentDisplay = "finished"
            else:
                print("No pages read.")
                input("Press any key to continue...")
        elif choice == "5" and currentDisplay == "pages":
            choice2 = input("\nPlease provide page # to bookmark: ").strip()
            bookmark(orderedKeys[int(choice2)].url)
        elif choice == "6" and currentDisplay == "pages":
            choice2 = input("\nPlease provide # to mark as read: ").strip()
            finishedPage(orderedKeys[int(choice2)].url)
        
        elif choice == "b":
            if currentDisplay == "pages":
                return
            else: 
                currentDisplay = "pages"
                pageNum = 1
                maxPages = 1 + len(orderedKeys)//output_length
        else:
            print("Invalid option.")
            input("Press any key to continue...")

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
    if addRead(url) == 1:
        print("Successfully added read marker")
        return 1
    else:
        print("ERROR: addEntry detected bookmark!")
        return -1

def bookmark(url):
    bookmarks = getBookmarkedPages()
    for bookmark in bookmarks:
        if bookmark.strip("\n") is url: 
            if removeBookmark(url) == 1:
                print("Successfully removed bookmark")
                return 1
            else:
                print("ERROR: removeEntry could not find text")
                return -1
    if addBookmark(url) == 1:
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
    
    if not os.path.exists(file): return outputDict

    with open(file,"r") as targetFile:
        lines = targetFile.readlines()
    
    for i, line in enumerate(lines):
        outputDict.update({line.strip("\n"): i})

    return outputDict

def addEntry(url, file):
    if os.path.exists(file):
        with open(file, "a") as targetFile:
            lines = targetFile.readlines()

            for line in lines:
                if line.strip("\n") is url: return -1
            targetFile.write(url)
    else:
        with open(file, "w") as targetFile:
            targetFile.write(url)
    return 1

def removeEntry(url, file):
    targetExists = False

    if not os.path.exists(file): return -1

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
    tempResults = sorted(cache.keys(), key=lambda x: cache.get(x).ref_count, reverse=True)
    results = []
    for x in tempResults: results.append(cache.get(x))
    readPages = getReadPages()

    # Ranks which pages to read while ignoring already read pages
    i = 1
    for x in results:
        if readPages.get(x.url):
            results.pop(x)
        else:
            x.rank = i
            i += 1

    return results


