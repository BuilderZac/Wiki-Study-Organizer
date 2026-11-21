#from libzim import reader

class Page:
    def __init__(self, url, name):
        self.url: str = url
        self.name: str = name
        self.links: list = [] # IDs of other pages
        self.word_count = dict()

def getPageByName(name: str) -> Page:
    pass


def getPageByURL(url: str) -> Page:
    pass


def getPageByID(id: int) -> Page:
    pass


def getPagesByWord(word: str) -> list[Page]:
    pass


def getNearbyPages(page: Page) -> list[Page]:
    pass


def pageDistance() -> int:
    pass

def createCache() -> dict:
    pages = dict() # { id: Page }
    counter: int = 0
    pass


def readCache():
    pass

