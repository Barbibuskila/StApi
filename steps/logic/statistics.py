from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

from steps.common.statistics import RuntimeStats


class AsyncMongoStatisticsHandler:
    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str):
        """
        Mongo posts handler
        :param db: Mongo database
        :param collection_name: Database collection name
        """
        self._db: AsyncIOMotorDatabase = db
        self._collection: AsyncIOMotorCollection = db[collection_name]

    async def post_requests_duration(self, request_type, duration):
        """
        Insert new request duration to the database
        :param request_type: Post or get request
        :param duration: Duration of the request
        :return: The new document, None if failed
        """
        document = {
            "type": request_type,
            "duration": duration
        }
        return await self._collection.insert_one(document)

    async def get_average_runtimes(self):
        """
        Calculate the average runtime of post and get of posts
        :return: Average runtime.
        """
        post_documents = []
        get_documents = []
        async for document in self._collection.find():
            if document["type"] == "post":
                post_documents.append(document["duration"])
            elif document["type"] == "get":
                get_documents.append(document["duration"])

        average_post = sum(post_documents) / len(post_documents)
        average_get = sum(get_documents) / len(get_documents)
        return RuntimeStats(post_posts_average_runtime=average_post, get_posts_average_runtime=average_get)
