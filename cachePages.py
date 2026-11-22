from pathlib import Path
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


def count_words(words: str) -> dict:
    word_list = words.split(" ")
    word_dict = dict()
    for word in word_list:
        count = word_dict.get(word, 0)
        word_dict.update({word:count+1})
    return word_dict


def format_links(links: list[str]) -> list[str]:
    for link in links:
        webpage_url = link.find("://")
        if webpage_url != -1:
            third_slash = link.find("/", webpage_url+3)
            link = link[third_slash:]
    return links


def createCache(zim_path: Path) -> Pages:
    pass
    pages = Pages()

    # Make cache ID
    with zim_path.open("rb") as f:
        digest = hashlib.file_digest(f, "sha256")
    cache_id = digest.hexdigest()[0:20]

    cache_dir = Path(""+cache_id)

    if cache_dir.is_file():
        return readCache(cache_dir)
    
    else:
        zim_file = Archive(zim_path)

        # for debugging
        print(f"{zim_file.entry_count} entries found")

        # Read every HTML page
        for page in zim_file:
            # Omit non-HTML files
            page_content = page.get_item()
            if page_content.mimetype != "text/html":
                continue
            else:
                page_content = bytes(page_content.content).decode("utf-8")

            # Initialize stacks for tags, content, links
            #tags: list[str] = list()
            text: str = ""
            links: list[str] = list()
            cursor = 0

            while cursor < len(page_content):
                char = page_content[cursor]

                # anything between end of open_tag and beginning of close_tag are saved in words

                if char == '<':
                    cursor += 1

                    # read word until ' '
                    tag = ""
                    while (page_content[cursor] != " ") and (page_content[cursor] != ">"):
                        tag += page_content[cursor]
                        cursor += 1

                    valid_tags = ()
                    if tag in valid_tags:
                        continue

                    if page_content[cursor] == " ":
                        # continue to end of tag
                        end_tag = page_content.find('>', cursor)
                        rest_of_tag = page_content[cursor:end_tag]
                        cursor = end_tag

                        # find href
                        href_start = rest_of_tag.find("href=\"")
                        href_end = rest_of_tag.find("\"")
                        if href_start != -1:
                            href_link = rest_of_tag[href_start+5:href_end]
                            links.append(href_link)

                    # is open tag
                    else:
                        # add to tag stack
                        #tags.append(tag)
                        cursor += 1 # skip " "

                        pass
                cursor += 1

            # when collection is complete, format and pass data on
            count_words(text)
            newLinks = format_links(links)


def writeCache():
    pass


def readCache(cache_path: Path) -> Pages:
    pass


def main():
    file = "library/finiki_en_all_maxi_2024-06.zim"
    createCache(Path(file))

main()