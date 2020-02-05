import asyncio
# import logging
from interfaces import RunnerInterface
from store import Store
from tgbot import TgBot
from torrsearch import TorrSearch
from logger import Log


class Runner(RunnerInterface):
    def __init__(self):
        super().__init__()
        self.store = Store()
        self.torr_searcher = TorrSearch()
        self.loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue()
        self.bot = TgBot(self.queue)
        self.log = Log(__name__)

    async def background_updater(self):
        await asyncio.sleep(5.0)
        self.log.debug(f"Start update after 5 seconds")
        while True:
            await asyncio.sleep(10)
            movies = await self.store.get_movies()
            self.log.debug(f"Search for {movies}")
            for movie in movies:
                self.log.debug(f"Find '{movie['title']}' for users: {movie['watchers']}")
                result = await self.torr_searcher.search_word(movie['title'])
                self.log.debug(f"Result: {result}")
                if result:
                    message = self.format_films(movie['title'], result)
                    for watcher in movie['watchers']:
                        await self.bot.send_message(watcher, message)
                    await self.store.create_or_update_movie(movie=movie['title'], is_active=False)

    @staticmethod
    def format_films(search_str, films):
        msg = f'По запросу: "{search_str}" найдены следущие раздачи:\n'
        for i in films[:6]:
            msg += f"---\n{i['date']}  |  {i['size']}  |  {i['name']}\n"
        return msg

    async def process_messages(self):
        while True:
            item = await self.queue.get()
            if item is not None:
                self.log.info(item)
                if not isinstance(item, dict) or 'type' not in item.keys():
                    self.log.error(f"Get incorrect object from tgbot: {item}")
                if item['type'] == 'start':
                    await self.store.create_or_update_user(item['content']['from'])
                elif item['type'] == 'deactivate':
                    await self.store.create_or_update_user(item['content']['from'], is_active=False)
                elif item['type'] == 'ignore':
                    watcher = item['content']['from']['id']
                    movie = item['content']['text'][8:].strip()
                    self.log.debug(f"User {watcher} trying ignore: {movie}")
                    await self.store.ignore_movie(movie=movie, watcher=watcher)
                    answer = f"You are unsubscribed from '{movie}' search."
                    await self.bot.send_message(watcher, answer)
                elif item['type'] == 'list':
                    watcher = item['content']['from']['id']
                    movies = await self.store.get_movies(telegram_id=watcher)
                    results = '\n'.join([i['title'] for i in movies])
                    answer = f"You are waiting for:\n" \
                             f"{results}"
                    await self.bot.send_message(watcher, answer)
                elif item['type'] == 'message':
                    movie = item['content']['text'].strip()
                    watcher = item['content']['from']['id']
                    if movie.startswith('/'):
                        answer = f"Incorrect command. Use /help for additional information."
                    else:
                        if await self.store.get_users(telegram_id=watcher):
                            await self.store.create_or_update_movie(movie=movie, watcher=watcher)
                            answer = f"Title '{movie}' was added"
                        else:
                            answer = f'You need /start chatting with bot before make requests.'
                    await self.bot.send_message(watcher, answer)
                else:
                    self.log.error(f"Unknown type from item: {item}")

    def prepare(self):
        self.loop.create_task(self.process_messages())
        self.loop.create_task(self.background_updater())

    def run(self):
        self.prepare()
        # Bot exec run loop forever
        self.bot.run()

    async def search_digital(self, keywords):
        pass

    async def search_bd(self):
        pass

    async def search_torrent(self, keywords):
        return await self.torr_searcher.search_word(keywords)


if __name__ == '__main__':
    runner = Runner()
    runner.run()
