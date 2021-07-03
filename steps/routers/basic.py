from fastapi import APIRouter


def create_basic_router():
    """
    Creates basic router, health check and other routes.
    :return: Basic Fastapi router
    """
    router = APIRouter()

    @router.get("/")
    def health_check():
        """
        Basic route for checking if the api is alive.
        """
        return "Welcome To Steps Api"

    return router
