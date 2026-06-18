import os
import json
import redis.asyncio as redis
from functools import wraps
from fastapi import Request, Response
from typing import Callable, Any

# Get Redis URL from environment or default to local
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Initialize Redis client pool
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

def cache_response(expire_seconds: int = 300):
    """
    Decorator to cache FastAPI endpoint responses using Redis.
    Uses the request URL and query params as the cache key.
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Check if cache is globally disabled for dev
            if os.getenv("USE_CACHE", "True").lower() in ["false", "0", "no"]:
                return await func(*args, **kwargs)
                
            request: Request = kwargs.get("request")
            if not request:
                # If no request object in kwargs, skip caching
                return await func(*args, **kwargs)
                
            # Generate cache key based on URL and query params
            cache_key = f"cache:{request.url.path}?{request.url.query}"
            
            # Try to fetch from cache
            cached_data = await redis_client.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
                
            # Execute original function
            response_data = await func(*args, **kwargs)
            
            # If response is a Pydantic model or list of models, convert to dict
            try:
                # Try standard Pydantic serialization
                if hasattr(response_data, "model_dump"):
                    serializable = response_data.model_dump()
                elif isinstance(response_data, list) and len(response_data) > 0 and hasattr(response_data[0], "model_dump"):
                    serializable = [item.model_dump() for item in response_data]
                else:
                    serializable = response_data
                    
                # Store in Redis
                await redis_client.set(
                    cache_key,
                    json.dumps(serializable, default=str), # default=str handles datetimes/UUIDs
                    ex=expire_seconds
                )
            except Exception as e:
                print(f"Failed to cache response: {e}")
                
            return response_data
            
        return wrapper
    return decorator
