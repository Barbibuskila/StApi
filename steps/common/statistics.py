from pydantic import BaseModel


class RuntimeStats(BaseModel):
    post_posts_average_runtime: float
    get_posts_average_runtime: float

