import os
from enum import Enum


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)


class RedisKeys(Enum):
    ORDER_ALLOCATED = "order.allocated"
