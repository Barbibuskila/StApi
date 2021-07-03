from datetime import datetime

from steps.common.base import MongoBaseModel


class Post(MongoBaseModel):
    title: str
    body: str
    user_id: str
    creation_time: str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
