import os
from aiogram import Bot, Dispatcher, executor, types
from interfaces import TgBotInterface


class TgBot(TgBotInterface):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
        if not self.API_TOKEN:
            print("Error read token")
            exit(1)
        bot = Bot(token=self.API_TOKEN)
        self.dp = Dispatcher(bot)
        self.create_handlers()
        self.welcome_message = f'Hi! This is a bot for lookup movie release.\n' \
                               f'You can use command /help for additional information.'
        self.help_message = f''

    async def add_to_queue(self):
        pass

    def create_handlers(self):
        self.dp.register_message_handler(callback=self.handle_welcome, commands=['start', 'help'])
        self.dp.register_message_handler(callback=self.cats, regexp='(^cat[s]?$|puss)')
        self.dp.register_message_handler(callback=self.handle_message)

    def run(self):
        executor.start_polling(self.dp, skip_updates=True)

    async def handle_message(self, message: types.Message):
        await self.queue.put(message)
        await message.answer(message.text)

    async def handle_welcome(self, message: types.Message):
        qmessage = {
            'type': 'start',
            'content': message.to_python()
        }
        await self.queue.put(qmessage)
        await message.reply(self.welcome_message)

    async def send_message(self):
        pass

    async def send_welcome(self, message: types.Message):
        await self.queue.put(message)
        print(dir(message))
        await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")

    async def cats(self, message: types.Message):
        with open('data/cats.jpg', 'rb') as photo:
            await message.reply_photo(photo, caption='Cats are here 😺')
