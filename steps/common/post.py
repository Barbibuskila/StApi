from datetime import datetime

from steps.common.base import MongoBaseModel


class Post(MongoBaseModel):
    title: str
    body: str
    user_id: str
    creation_time: datetime = datetime.now()
