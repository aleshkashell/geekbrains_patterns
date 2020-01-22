import logging
from interfaces import DatabaseInterface

logger = logging.getLogger('Database')


class Users(DatabaseInterface):
    def __init__(self):
        logger.debug('Users db was created')

    def create(self):
        pass

    def update(self):
        pass

    def remove(self):
        pass

    def get(self):
        pass

    def activate(self):
        pass

    def deactivate(self):
        pass
    

class Movies(DatabaseInterface):
    def __init__(self):
        super().__init__()
        logger.debug('Users db was created')

    def create(self):
        pass

    def update(self):
        pass

    def remove(self):
        pass

    def get(self):
        pass

    def activate(self):
        pass

    def deactivate(self):
        pass