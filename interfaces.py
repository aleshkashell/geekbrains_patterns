import asyncio
from abc import ABC, abstractmethod
from aiogram import types


class RunnerInterface(ABC):
    @abstractmethod
    async def process_messages(self, *args, **kwargs):
        pass

    @abstractmethod
    def prepare(self, *args, **kwargs):
        pass

    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    @abstractmethod
    def search_digital(self, *args, **kwargs):
        pass

    @abstractmethod
    def search_bd(self, *args, **kwargs):
        pass

    @abstractmethod
    def search_torrent(self, *args, **kwargs):
        pass

    @abstractmethod
    def background_updater(self, *args, **kwargs):
        pass


class TorrentSearcherInterface(ABC):
    @abstractmethod
    def search_word(self, *args, **kwargs):
        pass

    @abstractmethod
    def search_exact(self, *args, **kwargs):
        pass


class ReleaseDateInterface(ABC):
    @abstractmethod
    def itunes(self, *args, **kwargs):
        pass

    @abstractmethod
    def imdb(self, *args, **kwargs):
        pass

    @abstractmethod
    def kinopoisk(self, *args, **kwargs):
        pass


class StoreInterface(ABC):
    @abstractmethod
    async def create_or_update_user(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get_users(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get_releases_date(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get_releases_today(self, *args, **kwargs):
        pass

    @abstractmethod
    async def create_or_update_movie(self, *args, **kwargs):
        pass


class DatabaseInterface(ABC):
    @abstractmethod
    async def create_or_update(self, *args, **kwargs):
        pass

    @abstractmethod
    async def remove(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get_all(self, *args, **kwargs):
        pass

    @abstractmethod
    async def activate(self, *args, **kwargs):
        pass

    @abstractmethod
    async def deactivate(self, *args, **kwargs):
        pass


class TgBotInterface(ABC):
    @abstractmethod
    def create_handlers(self, *args, **kwargs):
        pass

    @abstractmethod
    def run(self, *args, **kwargs):
        """Запуск получения сообщений и asyncio цикла"""
        pass

    @abstractmethod
    def handle_welcome(self, message: types.Message):
        """Обработка приветственного сообщения"""
        pass

    @abstractmethod
    async def handle_message(self, message: types.Message):
        pass

    @abstractmethod
    async def send_message(self, *args, **kwargs):
        """Отправка сообщения"""
        pass

    @abstractmethod
    def add_to_queue(self, *args, **kwargs):
        pass
