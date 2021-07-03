from fastapi import APIRouter

from steps.common.post import Post


def create_posts_router():
    router = APIRouter()

    @router.post("/")
    def post(post_data: Post):
        pass

    @router.get("/")
    def get_posts(skip: 0, limit: 0):
        pass
