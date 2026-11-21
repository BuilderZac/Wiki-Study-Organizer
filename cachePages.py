#from libzim import reader

class Page:
    def __init__(self, url, name):
        self.url: str = url
        self.name: str = name
        self.links: list = [] # IDs of other pages
        self.word_count = dict()

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
        pass

def createCache() -> Pages:
    pages = Pages()
    pass


def readCache() -> Pages:
    pass

