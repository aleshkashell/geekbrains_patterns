import logging
import asyncio
from datetime import datetime
import motor.motor_asyncio
from interfaces import DatabaseInterface

logger = logging.getLogger('Database')


class Users(DatabaseInterface):
    def __init__(self, user=None, password=None, server="localhost", port=27017):
        if user and password:
            uri = f"mongodb://{user}:{password}@{server}:{port}/"
        else:
            uri = f"mongodb://{server}:{port}/"
        client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        db = client.users_database
        self.collection = db.users_collection

    async def create_or_update(self, user, is_active=True):
        filter_ = {
            "telegram_id": user['id']
        }
        user['is_active'] = is_active
        update_ = {
            "$set": user,
            "$currentDate": {
                "updatedAt": True  # set field updatedAt to current date automagically. Good practice ;)
            },
            "$setOnInsert": {
                "createdAt": datetime.utcnow()
                # set field createdAt to current date automagically ONLY IF it's a new record
            }

        }
        await self.collection.update_one(filter_, update_, upsert=True)

    async def remove(self, id):
        filter_ = {
            "telegram_id": id
        }
        await self.collection.delete_many(filter_)

    async def get(self, id):
        filter_ = {
            "telegram_id": id
        }
        projection_ = {
            "_id": False  # don't return the _id
        }
        document = await self.collection.find_one(filter=filter_, projection=projection_)
        logger.debug(f'Found: {document}')
        return document

    async def get_all(self, is_active=True, telegram_id=None):
        projection_ = {
            "_id": False  # don't return the _id
        }
        filter_ = {
            "is_active": is_active
        }
        if telegram_id:
            filter_['telegram_id'] = telegram_id
        cursor = self.collection.find(filter=filter_, projection=projection_)
        items = await cursor.to_list(length=None)
        return items

    async def activate(self, user):
        await self.create_or_update(user, True)

    async def deactivate(self, user):
        await self.create_or_update(user, False)
    

class Movies(DatabaseInterface):
    def __init__(self, user=None, password=None, server="localhost", port=27017):
        if user and password:
            uri = f"mongodb://{user}:{password}@{server}:{port}/"
        else:
            uri = f"mongodb://{server}:{port}/"
        client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        db = client.movies_database
        self.collection = db.movies_collection

    async def create_or_update(self, movie, watcher=None, is_active=True):
        filter_ = {
            "title": movie
        }
        record = {
            "title": movie,
            "is_active": is_active
        }
        update_ = {
            "$set": record,
            "$addToSet": {"watchers": watcher},
            "$currentDate": {
                "updatedAt": True  # set field updatedAt to current date automagically. Good practice ;)
            },
            "$setOnInsert": {
                "createdAt": datetime.utcnow()
                # set field createdAt to current date automagically ONLY IF it's a new record
            }

        }
        await self.collection.update_one(filter_, update_, upsert=True)

    # def update(self):
    #     pass

    async def remove(self):
        pass

    async def get(self):
        pass

    async def get_all(self, is_active=True, telegram_id=None):
        projection_ = {
            "_id": False  # don't return the _id
        }
        filter_ = {
            "is_active": is_active
        }
        if telegram_id:
            filter_['watchers'] = {
                "$all": [telegram_id]
            }
        cursor = self.collection.find(filter=filter_, projection=projection_)
        items = await cursor.to_list(length=None)
        return items

    async def activate(self):
        pass

    async def deactivate(self, movie, watcher):
        filter_ = {
            "title": movie
        }
        update_ = {
            "$pull": {
                "watchers": watcher
            }
        }
        await self.collection.update_one(filter_, update_)
