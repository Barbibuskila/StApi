from fastapi import APIRouter
from loguru import logger

from steps.logic.posts import AsyncMongoPostsHandler
from steps.logic.statistics import AsyncMongoStatisticsHandler
from steps.responses import internal_server_error


def create_statistics_router(post_handler: AsyncMongoPostsHandler, stats_handler: AsyncMongoStatisticsHandler):
    """
    Create statistics router contain all stats logic
    :param stats_handler: statistics database handler
    :param post_handler: posts database handler
    :return: Fastapi router
    """
    router = APIRouter()

    @router.get("/topcreators")
    async def get_top_creators():
        try:
            creators = await post_handler.get_top_10_creators()
            return creators
        except Exception as err:
            logger.error(f"Cannot get top creators - {err}")
            return internal_server_error()

    @router.get("/runtimes")
    async def get_average_runtime_of_posts_functions():
        try:
            average_runtime = await stats_handler.get_average_runtimes()
            return average_runtime
        except Exception as err:
            logger.error(f"Cannot get average runtime - {err}")
            return internal_server_error()

    return router
