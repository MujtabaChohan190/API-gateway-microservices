#fixed window - 100 requests , 60 seconds
from redis_client import redis_client

RATE_LIMIT = 5
WINDOW = 60

async def check_rate_limit(client_id : str):

    key = f"rate_limit:{client_id}"
    request_count = await redis_client.incr(key)

    if request_count == 1:
        await redis_client.expire(key,WINDOW)

    if request_count > RATE_LIMIT:
        return False

    return True