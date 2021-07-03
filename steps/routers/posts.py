from fastapi import APIRouter

from steps.common.post import Post
from steps.logic.posts import AsyncMongoPostsHandler
from loguru import logger
from steps.responses import ok, internal_server_error


def create_posts_router(post_handler: AsyncMongoPostsHandler):
    """
    Create posts router that contain all posts logics.
    :param post_handler: posts database handler
    :return: Fastapi router.
    """
    router = APIRouter()

    @router.post("/")
    async def post(post_data: Post):
        """
        Create post and insert it to database
        :param post_data: post data from the http request body
        :return: Http response according to the result of the post creation.
        """
        try:
            new_post = await post_handler.create_post(post=post_data)
            if new_post is None:
                logger.error("Create post failed - unknown reason")
                return ok()
        except Exception as err:
            logger.error(f"Create post failed - {err}")
            return internal_server_error()

    @router.get("/")
    def get_posts(skip: 0, limit: 0):
        return []

    return router
