import time, logging

logger = logging.getLogger(__name__)

# time logger for logging the time taken for a function to execute
def time_logger():
    def decorator(func):
        async def wrapper(*args, **kwargs):
            start = time.time()
            result = await func(*args, **kwargs)
            end = time.time()
            logger.info(f"{func.__name__} took {end-start} seconds to execute")
            return result
        return wrapper
    return decorator