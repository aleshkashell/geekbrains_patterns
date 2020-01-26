import asyncio
import logging
from interfaces import RunnerInterface
from store import Store
from tgbot import TgBot


logging.basicConfig(level=logging.INFO)


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
                elif item['type'] == 'message':
                    movie = item['content']['text']
                    watcher = item['content']['from']['id']
                    if await self.store.get_users(telegram_id=watcher):
                        await self.store.create_or_update_movie(movie, watcher)
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
