import asyncio
import aiohttp
from aiohttp import client_exceptions
from lxml import html
from interfaces import TorrentInterface
from logger import Log


class Rutor(TorrentInterface):
    def __init__(self):
        self.log = Log(__name__)
        self.session = aiohttp.ClientSession()
        self._init_variables()

    def _init_logging(self):
        pass

    def _init_variables(self):
        self._rutor = dict()
        self._rutor['protocols'] = ['http', 'https']
        self._rutor['host'] = ['rutor.is', 'rutor.info', '6tor.net']
        self._rutor['search_string'] = '/search/'
        self._rutor['search_keyword'] = '/search/0/0/100/0/'
        self._rutor['search_words'] = ''

    async def fetch_url(self, url):
        try:
            async with self.session.get(url, allow_redirects=False) as resp:
                if resp.status != 200:
                    self.log.info(f"Got code {resp.status} from {url}")
                    await asyncio.sleep(2.0)
                    return None
                return await resp.text()
        except client_exceptions.ClientConnectionError as e:
            self.log.info(e)
            await asyncio.sleep(2.0)
            return None

    def _generate_links(self, search_str, method='search_string'):
        links = list()
        for host in self._rutor['host']:
            for proto in self._rutor['protocols']:
                links.append(f"{proto}://{host}{self._rutor[method]}{search_str}")
        return links

    @staticmethod
    def parse(html_text):
        tree = html.fromstring(html_text)
        elements = tree.xpath('//table[@width]//tr')
        results = list()
        for e in elements:
            data = e.xpath('./td//text()')
            link = e.xpath('.//a/@href')
            if len(data) == 7:
                element = {
                    "date": data[0],
                    "name": data[2],
                    "size": data[3],
                    "link": link[2]
                }
            elif len(data) == 8:
                element = {
                    "date": data[0],
                    "name": data[2],
                    "size": data[4],
                    "link": link[2]
                }
            else:
                continue
            results.append(element)
        return results

    async def search(self, search_str):
        futures = [self.fetch_url(link) for link in self._generate_links(search_str)]
        self.log.debug(f"Generated links: {'  '.join(self._generate_links(search_str))}")
        return await self.run_search(futures)

    async def run_search(self, futures):
        done, pending = await asyncio.wait(futures, return_when=asyncio.FIRST_COMPLETED)
        for future in pending:
            future.cancel()
        try:
            html_page = done.pop().result()
        except:
            return None
        # !!! Make run in executor
        return self.parse(html_page)

    async def search_keywords(self, keywords):
        if type(keywords) is list:
            keywords = ' '.join(keywords)
        futures = [self.fetch_url(link) for link in self._generate_links(search_str=keywords, method='search_keyword')]
        self.log.debug(f"Generated links: "
                       f"{'  '.join(self._generate_links(search_str=keywords, method='search_keyword'))}")
        return await self.run_search(futures)
