import asyncio
from test import TgBot


class Runner:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.message = 'hello'
        self.queue = asyncio.Queue()
        self.bot = TgBot(self.queue)

    async def logic(self):
        while True:
            print(self.message)
            await asyncio.sleep(5)

    def prepare(self):
        self.loop.create_task(self.process_messages())
        self.loop.create_task(self.logic())

    async def process_messages(self):
        while True:
            item = await self.queue.get()
            if item is None:
                break
            print(f'Item from queue: {item}')
            print(f'Item text: {item.text}')

    def run(self):
        self.prepare()
        # Bot exec run loop forever
        self.bot.run()


async def main():
    while True:
        print('hello')
        await asyncio.sleep(5)


if __name__ == '__main__':
    runner = Runner()
    runner.run()
