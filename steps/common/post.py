from datetime import datetime

from steps.common.base import MongoBaseModel


class Post(MongoBaseModel):
    """
    title: Post tile
    body: Body of the post
    user_id: user id that created the post - NOTE: there is not a users collection
    creation_time: timestamp that attached to the post when created
    """
    title: str
    body: str
    user_id: str
    creation_time: str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
