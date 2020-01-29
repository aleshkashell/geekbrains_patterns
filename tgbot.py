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
        self.bot = Bot(token=self.API_TOKEN)
        self.dp = Dispatcher(self.bot)
        self.create_handlers()
        self.welcome_message = f'Hi! This is a bot for lookup movie release.\n' \
                               f'You can use command /help for additional information.'
        self.help_message = f"Just text some film title and when it will be released I'll notify you in telegram.\n" \
                            f"For view your active searches use /list\n" \
                            f"If you don't want check any title text me /ignore title_name\n" \
                            f"If you want unsubscribe yourself from bot use command /deactivate"

    async def add_to_queue(self, type, message):
        request = {
            'type': type,
            'content': message.to_python()
        }
        await self.queue.put(request)

    def create_handlers(self):
        self.dp.register_message_handler(callback=self.handle_welcome, commands=['start'])
        self.dp.register_message_handler(callback=self.handle_deactivate, commands=['deactivate'])
        self.dp.register_message_handler(callback=self.handle_help, commands=['help'])
        self.dp.register_message_handler(callback=self.handle_ignore, commands=['ignore'])
        self.dp.register_message_handler(callback=self.handle_list, commands=['list'])
        self.dp.register_message_handler(callback=self.cats, regexp='(^cat[s]?$|puss)')
        self.dp.register_message_handler(callback=self.handle_message)

    def run(self):
        executor.start_polling(self.dp, skip_updates=True)

    async def handle_deactivate(self, message: types.Message):
        await self.add_to_queue('deactivate', message)

    async def handle_help(self, message: types.Message):
        await message.answer(self.help_message)

    async def handle_ignore(self, message: types.Message):
        await self.add_to_queue('ignore', message)

    async def handle_list(self, message: types.Message):
        await self.add_to_queue('list', message)

    async def handle_message(self, message: types.Message):
        await self.add_to_queue('message', message)

    async def handle_welcome(self, message: types.Message):
        await self.add_to_queue('start', message)
        await message.reply(self.welcome_message)

    async def send_message(self, user_id, message):
        await self.bot.send_message(user_id, message)

    async def cats(self, message: types.Message):
        with open('data/cats.jpg', 'rb') as photo:
            await message.reply_photo(photo, caption='Cats are here 😺')
