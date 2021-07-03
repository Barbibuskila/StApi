from fastapi import APIRouter
from steps.logic.posts import AsyncMongoPostsHandler
from steps.responses import ok, internal_server_error
from loguru import logger


def create_statistics_router(post_handler: AsyncMongoPostsHandler):
    """
    Create statistics router contain all stats logic
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
            logger.error(err)

    @router.get("/runtimes")
    def get_average_runtime_of_posts_functions():
        pass

    return router
