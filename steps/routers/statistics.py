from fastapi import APIRouter


def create_statistics_router():
    router = APIRouter()

    @router.get("/topcreators")
    def get_top_creators():
        pass

    @router.get("/runtimes")
    def get_average_runtime_of_posts_functions():
        pass

    return router
