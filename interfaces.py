import asyncio
from abc import ABC, abstractmethod
from aiogram import types


class RunnerInterface(ABC):
    @abstractmethod
    async def process_messages(self):
        pass

    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def search_digital(self):
        pass

    @abstractmethod
    def search_bd(self):
        pass

    @abstractmethod
    def search_torrent(self):
        pass

    @abstractmethod
    def background_updater(self):
        pass


class TorrentSearcherInterface(ABC):
    @abstractmethod
    def search_word(self):
        pass

    @abstractmethod
    def search_exact(self):
        pass


class ReleaseDateInterface(ABC):
    @abstractmethod
    def itunes(self):
        pass

    @abstractmethod
    def imdb(self):
        pass

    @abstractmethod
    def kinopoisk(self):
        pass


class StoreInterface(ABC):
    @abstractmethod
    def create_or_update_user(self):
        pass

    @abstractmethod
    def get_releases_date(self):
        pass

    @abstractmethod
    def get_releases_today(self):
        pass

    @abstractmethod
    def create_or_update_movie(self):
        pass


class DatabaseInterface(ABC):
    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def remove(self):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def activate(self):
        pass

    @abstractmethod
    def deactivate(self):
        pass


class TgBotInterface(ABC):
    @abstractmethod
    def create_handlers(self):
        pass

    @abstractmethod
    def run(self):
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
    async def send_message(self):
        """Отправка сообщения"""
        pass

    @abstractmethod
    def add_to_queue(self):
        pass
