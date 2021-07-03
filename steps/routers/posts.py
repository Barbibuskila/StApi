from time import time

from fastapi import APIRouter, HTTPException
from loguru import logger

from steps.common.post import Post
from steps.logic.posts import AsyncMongoPostsHandler
from steps.logic.statistics import AsyncMongoStatisticsHandler
from steps.responses import ok, internal_server_error


def create_posts_router(post_handler: AsyncMongoPostsHandler, stats_handler: AsyncMongoStatisticsHandler):
    """
    Create posts router that contain all posts logics.
    :param stats_handler: statistics database handler
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
            start = time()
            new_post = await post_handler.create_post(post=post_data)
            if new_post is None:
                logger.error("Create post failed - unknown reason")
                return internal_server_error()
            total = time() - start
            await insert_to_statistics("post", total)
            return ok()
        except HTTPException as err:
            logger.error(f"Create post failed - {err}")
            return internal_server_error()
        except Exception as err:
            logger.error(f"Create post failed - {err}")
            return internal_server_error()

    @router.get("/")
    async def get_posts(skip: int = 0, limit: int = 0):
        """
        Get posts from database, order by creation_time
        Can take only chunk of posts by skip and limit query parameters
        :param skip: How much to skip from the start
        :param limit: How much to take
        :return: List of posts.
        """
        try:
            start = time()
            posts = await post_handler.get_posts(skip, limit)
            total = time() - start
            await insert_to_statistics("get", total)
            return posts
        except HTTPException as err:
            logger.error(f"Retrieve posts failed - {err}")
            return internal_server_error()
        except Exception as err:
            logger.error(f"Retrieve posts failed - {err}")
            return internal_server_error()

    @router.get("/postsnumber")
    async def get_total_posts():
        """
        Get the total amounts of posts stored in the database
        :return: amount of posts.
        """
        try:
            posts = await post_handler.get_total_amount_of_posts()
            return posts
        except HTTPException as err:
            logger.error(f"Retrieve amount of posts failed - {err}")
            return internal_server_error()
        except Exception as err:
            logger.error(f"Retrieve amount of posts failed - {err}")
            return internal_server_error()

    async def insert_to_statistics(request_type, duration):
        try:
            result = await stats_handler.post_requests_duration(request_type, duration)
            if result is None:
                logger.error("Cannot insert request stats to database")
        except HTTPException as err:
            logger.error("Cannot insert request stats to database")
        except Exception as err:
            logger.error("Cannot insert request stats to database")

    return router
