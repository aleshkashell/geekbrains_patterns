from interfaces import StoreInterface
from database_factory import DatabaseFactory


class Store(StoreInterface):
    def __init__(self):
        users = DatabaseFactory.create_database('Users')
        movies = DatabaseFactory.create_database('Movies')

    def create_or_update_user(self):
        pass

    def get_releases_date(self):
        pass

    def get_releases_today(self):
        pass

    def create_or_update_movie(self):
        pass
