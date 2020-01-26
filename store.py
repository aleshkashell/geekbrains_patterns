from interfaces import StoreInterface
from database_factory import DatabaseFactory


class Store(StoreInterface):
    def __init__(self):
        self.users = DatabaseFactory.create_database('Users')
        self.movies = DatabaseFactory.create_database('Movies')

    async def create_or_update_user(self, user):
        await self.users.create_or_update(user)

    async def get_users(self, is_active=True, telegram_id=None):
        return await self.users.get_all(is_active=is_active, telegram_id=telegram_id)

    async def get_movies(self, is_active=True, telegram_id=None):
        return await self.movies.get_all(is_active=is_active, telegram_id=telegram_id)

    async def get_releases_date(self):
        pass

    async def get_releases_today(self):
        pass

    async def create_or_update_movie(self, movie, watcher):
        await self.movies.create_or_update(movie, watcher)
