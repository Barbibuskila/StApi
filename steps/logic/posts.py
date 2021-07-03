from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from pymongo import DESCENDING

from steps.common.post import Post
from steps.utils.mongo_utils import convert_model_to_document, convert_document_to_model


class AsyncMongoPostsHandler:
    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str):
        """
        Mongo posts handler
        :param db: Mongo database
        :param collection_name: Database collection name
        """
        self._db: AsyncIOMotorDatabase = db
        self._collection: AsyncIOMotorCollection = db[collection_name]

    async def create_post(self, post: Post):
        """
        Insert post model to mongo as mongo document
        :param post: Post model
        :return: The new document, None if failed
        """
        document = convert_model_to_document(post)
        return await self._collection.insert_one(document)

    async def get_posts(self, skip=0, limit=0):
        """
        Get posts from database, order by creation_time
        Can take only chunk of posts by skip and limit query parameters
        :param skip: How much to skip from the start
        :param limit: How much to take
        :return: List of posts.
        """
        models = []

        if skip != 0:
            if limit != 0:
                mongo_command = lambda: self._collection.find().sort("creation_time", DESCENDING).skip(skip).limit(
                    limit)
            else:
                mongo_command = lambda: self._collection.find().sort("creation_time", DESCENDING).skip(skip)
        elif limit != 0:
            mongo_command = lambda: self._collection.find().sort("creation_time", DESCENDING).limit(limit)
        else:
            mongo_command = lambda: self._collection.find().sort("creation_time", DESCENDING)

        async for document in mongo_command():
            models.append(convert_document_to_model(document, Post))
        return models

    async def get_total_amount_of_posts(self):
        """
        Get the total amounts of posts stored in the database
        :return: amount of posts.
        """
        return await self._collection.estimated_document_count()

    async def get_top_10_creators(self):
        """
        Gets top ten posts creators
        :return: Dictionary of the top ten posts creators - User: Count
        """
        creators = {

        }
        async for document in self._collection.find():
            post = convert_document_to_model(document, Post)
            if post.user_id in creators:
                creators[post.user_id] += 1
            else:
                creators[post.user_id] = 1
        ordered_creators = dict(sorted(creators.items(), key=lambda item: item[1], reverse=True)[:11])

        return ordered_creators
