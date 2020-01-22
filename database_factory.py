from database import Users, Movies


class DatabaseFactory:

    @staticmethod
    def create_database(database_type):
        databases = {
            'Users': Users,
            'Movies': Movies
        }
        cls = databases.get(database_type)
        if cls:
            return cls()
        return None
