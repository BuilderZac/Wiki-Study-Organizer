from pathlib import Path
import re
from libzim.reader import Archive
import hashlib

class Page:
    def __init__(self, url, name):
        self.url: str = url
        self.name: str = name
        self.links: list = [] # IDs of other pages
        self.word_count = dict()
        self.rank = -1 # lower = higher priority
        self.references = [] # IDs of pages that have this page linked
        self.ref_count = 0

class Pages:
    def __init__(self):
        self.pages = dict()
        self.counter = 0
        self.hash_url = dict()
        self.hash_name = dict()
        self.hash_word = dict()

    def insert(self, page: Page):
        self.pages.update({self.counter: page})
        self.hash_url.update({page.url: self.counter})
        self.hash_name.update({page.name: self.counter})

        # To-do: Update word hash map to include page IDs that contain a given word.
        for word in page.word_count:
            pass
        
        self.counter += 1

    def getPageByName(self, name: str) -> Page:
        id = self.hash_name.get(name)
        return self.pages.get(id)


    def getPageByURL(self, url: str) -> Page:
        id = self.hash_url.get(url)
        return self.pages.get(id)


    def getPageByID(self, id: int) -> Page:
        return self.pages.get(id)


    def getPagesByWord(self, word: str) -> list[Page]:
        return self.hash_word.get(word)


    def getNearbyPages(self, page: Page) -> list[Page]:
        pages = list()
        for page_id in page.links:
            pages.append(self.pages.get(page_id))
        return pages


    def getDistance(self, pageOne: Page, pageTwo: Page) -> int:
        # implement bidirectional breadth-first search
        pass

def createCache(zim_path: Path) -> Pages:
    pages = Pages()

    # Make cache ID
    with zim_path.open("rb") as f:
        digest = hashlib.file_digest(f, "sha256")
    cache_id = digest.hexdigest()[0:20]

    # To-do: find cache directory
    cache_dir = Path(""+cache_id)

    if cache_dir.is_file():
        return readCache(cache_dir)
    
    else:
        # To-do: read ZIM file
        # create cache file
        pages = Pages()
        print(cache_id)

        zim = Archive(zim_path)
        print(f"Total entries: {zim.entry_count}")
        for page in zim:
            if page.is_redirect:
                page = page.get_redirect_entry()

            page_content = page.get_item()
            if page_content.mimetype == ("text/html"):
                text = bytes(page_content.content).decode("utf-8", errors="replace")
                print(text)

                words = ""
                while "</" in text:
                    tag_index = text.find("<")
                    if tag_index == -1:
                        break

                    tag_end_index = text.find(">", tag_index+1)
                    if tag_end_index == -1:
                        break

                    tag = text[tag_index+1:tag_end_index].strip()
                    print(tag)

                    if (not tag) or (tag.startswith("/")):
                        text = text[tag_end_index+1:]
                        continue

                    tag_name = tag.split(None, 1)[0].lower().rstrip("/")
                    end_tag = f"</{tag_name}>"

                    end_index = text.find(end_tag, tag_end_index + 1)
                    if end_index == -1:
                        text = text[tag_end_index + 1:]
                        continue

                    words = text[tag_end_index + 1:end_index]
                    text = text[end_index + len(end_tag):]
                print(words)

                # Parse links out of plaintext

                #pattern = "|".join(map(re.escape, tags))
                #result = re.sub(pattern, " ", text)
                #print(result)

def readCache(cache_path: Path) -> Pages:
    pass

def main():
    file = "library/finiki_en_all_maxi_2024-06.zim"
    createCache(Path(file))

main()