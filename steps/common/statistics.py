from pydantic import BaseModel


class RuntimeStats(BaseModel):
    """
    post_posts_average_runtime: average runtime of the post posts http request
    get_posts_average_runtime: average runtime of the get posts http request
    """
    post_posts_average_runtime: float
    get_posts_average_runtime: float
