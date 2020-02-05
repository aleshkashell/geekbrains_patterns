from interfaces import TorrentSearcherInterface
from rutor import Rutor


class TorrSearch(TorrentSearcherInterface):
    rutor = Rutor()

    def __init__(self):
        pass

    async def search_exact(self, search_str):
        return await self.rutor.search(search_str)

    async def search_word(self, keywords):
        return await self.rutor.search_keywords(keywords)
