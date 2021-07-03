from fastapi import APIRouter


def create_basic_router():
    router = APIRouter()

    @router.get("/")
    def health_check():
        return "Welcome To Steps Api"

    return router
