from pathlib import Path
from libzim.reader import Archive
import hashlib
import re

CACHE_DIR = Path("/app/cache")

class Page:
    def __init__(self, url, name, word_count, links):
        self.url: str = url
        self.name: str = name
        self.links: list = links
        self.word_count = word_count
        self.rank = -1 # lower = higher priority
        self.references = [] # IDs of pages that have this page linked
        self.ref_count = 0

        def __str__(self):
            return f"URL: {self.url}\nNAME: {self.name}\n NUMBER OF OUTBOUND LINKS: {len(self.links)}"


class Pages:
    def __init__(self):
        self.counter = 0
        self.word_counter = 0
        self.pages = dict()             # id : page
        self.hash_url = dict()          # url : page_id
        self.hash_name = dict()         # name : page_id
        self.hash_word_pages = dict()   # word_id : list of pages with that word
        self.hash_word_dict = dict()    # word : word_id


    def insert(self, url: str, name: str, word_count: dict, links: list) -> bool:
        new_word_count = dict()
        for word in word_count:

            if not self.hash_word_dict.get(word):
                self.hash_word_dict.update({word: self.word_counter})
                self.word_counter += 1

            word_id = self.hash_word_dict.get(word)

            if not self.hash_word_pages.get(word_id):
                self.hash_word_pages.update({word_id: list()})

            word_list = self.hash_word_pages.get(word_id)
            word_list.append(self.counter)
            self.hash_word_pages.update({word_id: word_list})

            new_word_count.update({word_id:word_count.get(word)})

        page = Page(url, name, new_word_count, links)
        self.pages.update({self.counter: page})
        self.hash_url.update({url: self.counter})
        self.hash_name.update({name: self.counter})
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
        word_id = self.hash_word_dict.get(word)
        return self.hash_word_pages.get(word_id)


    def getNearbyPages(self, page: Page) -> list[Page]:
        pages = list()
        for page_id in page.links:
            pages.append(self.pages.get(page_id))
        return pages


    def getDistance(self, pageOne: Page, pageTwo: Page) -> int:
        # implement bidirectional breadth-first search
        pass


def count_words(words: str) -> dict:
    word_list = words.split(" ")
    word_dict = dict()
    for word in word_list:
        count = word_dict.get(word, 0)
        word_dict.update({word:count+1})
    return word_dict


def format_links(links: list[str]) -> list[str]:
    newLinks = list()
    for link in links:
        webpage_url = link.find("://")
        if webpage_url != -1:
            third_slash = link.find("/", webpage_url+4)
            link = link[third_slash:]
        newLinks.append(link)
    return newLinks


def createCache(zim_path: Path) -> Pages:
    pages = Pages()

    # Make cache ID
    with zim_path.open("rb") as f:
        digest = hashlib.file_digest(f, "sha256")
    cache_id = digest.hexdigest()[0:20]

    if False: #Path(str(CACHE_DIR)+"/"+cache_id).is_file():
        return readCache(CACHE_DIR, cache_id)
    
    else:
        zim_file = Archive(zim_path)

        # Read every HTML page
        for page in zim_file:
            # Omit non-HTML files
            page_content = page.get_item()
            url = page_content.path
            name = page_content.title

            if page_content.mimetype not in ("text/html", "text/plain", "text/plain;charset=UTF-8"):
                continue
            else:
                page_content = bytes(page_content.content).decode("utf-8", errors="replace")

            # Variables for storing extracted data
            text: str = ""
            links: list[str] = list()
            cursor = 0

            while cursor < len(page_content):
                char = page_content[cursor]

                if char == '<':
                    cursor += 1

                    # read word until ' '
                    tag = ""
                    while (page_content[cursor] != " ") and (page_content[cursor] != ">"):
                        tag += page_content[cursor]
                        cursor += 1

                    # FILL WITH VALID HTML TAGS
                    valid_tags = ()
                    if tag in valid_tags: # SWAPTO NOT IN
                        continue

                    if page_content[cursor] == " ":
                        # continue to end of tag
                        end_tag = page_content.find('>', cursor)
                        rest_of_tag = page_content[cursor:end_tag]
                        cursor = end_tag

                        # Find link/HREF
                        href_start = rest_of_tag.find("href=\"")
                        if href_start != -1:
                            href_end = rest_of_tag.find("\"", href_start+6)
                            href_link = rest_of_tag[href_start+6:href_end]
                            links.append(href_link)
                else:
                    text += char
                cursor += 1

            # when collection is complete, format and pass data on
            text = re.sub(r'[^\w\s]', '', text)
            text = re.sub(r'\n', '', text)
            pages.insert(url, name, count_words(text), format_links(links))

        #writeCache(pages, CACHE_DIR, cache_id)
    return pages


def writeCache(pages: Pages, cache_path: Path, cache_id: str) -> bool:
    print("HI")
    with Path(str(CACHE_DIR)+"/"+cache_id).open("w", encoding="utf-8") as file:
        print("ok")
        for page in pages.pages:
            attributes = page.keys
            print(attributes)
            for a in attributes:
                value = attributes.get(a)
                file.write("Hello, world!\n")


def readCache(cache_path: Path, cache_id: str) -> Pages:
    pass


def main():
    file = "library/chessprogramming_sample_2026-11.zim"
    createCache(Path(file))
