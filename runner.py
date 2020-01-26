import asyncio
import logging
from interfaces import RunnerInterface
from store import Store
from tgbot import TgBot


logging.basicConfig(level=logging.DEBUG)


class Runner(RunnerInterface):
    def __init__(self):
        super().__init__()
        self.store = Store()
        self.loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue()
        self.bot = TgBot(self.queue)
        self.log = logging.getLogger()

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
                    await self.store.create_or_update_movie(movie=movie, watcher=watcher, deactivate=True)
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

    def run(self):
        self.prepare()
        # Bot exec run loop forever
        self.bot.run()

    def search_digital(self):
        pass

    def search_bd(self):
        pass

    def search_torrent(self):
        pass

    def background_updater(self):
        pass


if __name__ == '__main__':
    runner = Runner()
    runner.run()
