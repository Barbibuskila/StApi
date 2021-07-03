from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

from steps.common.post import Post
from steps.utils.mongo_utils import convert_model_to_document


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
