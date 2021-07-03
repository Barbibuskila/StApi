from fastapi import APIRouter, HTTPException

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
                return internal_server_error()
            return ok()
        except HTTPException as err:
            logger.error(f"Create post failed - {err}")
            return internal_server_error()
        except Exception as err:
            logger.error(f"Create post failed - {err}")
            return internal_server_error()

    @router.get("/")
    async def get_posts(skip: int = 0, limit: int = 0):
        try:
            posts = await post_handler.get_posts(skip, limit)
            return posts
        except HTTPException as err:
            logger.error(f"Retrieve posts failed - {err}")
            return internal_server_error()
        except Exception as err:
            logger.error(f"Retrieve posts failed - {err}")
            return internal_server_error()

    return router
