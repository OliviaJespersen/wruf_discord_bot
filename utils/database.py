import redis.asyncio as redis


# Setup

r = redis.Redis(host='redis-database', port=6379, decode_responses=True)


# Score Management

async def _get_score_sum(user_id: str) -> int:
    """
    Retrieve the score sum for a specific user.

    Args:
        user_id (str): The ID of the user whose score is to be retrieved.

    Returns:
        int: The score sum of the user. Returns 0 if the user has no score.
    """    
    score = await r.hget("score_sums", user_id)

    return int(score) if score is not None else 0

async def _set_score_sum(user_id: str, score: int) -> None:
    """
    Set the score sum for a specific user.

    Args:
        user_id (str): The ID of the user whose score is to be set.
        score (int): The score sum to set for the user.
    """
    await r.hset("score_sums", user_id, score)

async def _get_analysis_count(user_id: str) -> int:
    """
    Retrieve the analysis count for a specific user.

    Args:
        user_id (str): The ID of the user whose count is to be retrieved.

    Returns:
        int: The analysis count of the user. Returns 0 if the user has no count.
    """
    count = await r.hget("analysis_counts", user_id)
    
    return int(count) if count is not None else 0

async def _set_analysis_count(user_id: str, count: int) -> None:
    """
    Set the analysis count for a specific user.

    Args:
        user_id (str): The ID of the user whose analysis count is to be set.
        count (int): The analysis count to set for the user.
    """
    await r.hset("analysis_counts", user_id, count)

async def get_average_score(user_id: str) -> float:
    """
    Retrieve the average score for a specific user from a sorted set.

    Args:
        user_id (str): The ID of the user whose average score is to be retrieved.

    Returns:
        float: The average score of the user. Returns 0.0 if the user has no scores.
    """
    average = await r.zscore("average_scores" , user_id)
    
    return average if average is not None else 0.0

async def _set_average_score(user_id: str) -> None:
    """
    Set the average score for a specific user.

    Args:
        user_id (str): The ID of the user whose average score is to be set.
        average (float): The average score to set for the user.
    """
    score = await _get_score_sum(user_id)
    count = await _get_analysis_count(user_id)
    scaled_average = (score / count) * (1 + (count / 100))

    await r.zadd("average_scores", {user_id: scaled_average})

async def get_all_average_scores() -> list[tuple[str, float]]:
    """
    Retrieve all average scores from the database.

    Returns:
        list[tuple[str, float]]: A list of tuples containing user IDs and their average scores.
    """
    scores = await r.zrevrange("average_scores", 0, -1, withscores=True)

    return [(user_id, score) for user_id, score in scores]

async def update_score(user_id: str, earned: int) -> None:
    """
    Update the score for a specific user by adding the earned points.

    Args:
        user_id (str): The ID of the user whose score is to be updated.
        earned (int): The points to add to the user's score.
    """
    old_score = await _get_score_sum(user_id)
    new_score = old_score + earned
    await _set_score_sum(user_id, new_score)

    old_count = await _get_analysis_count(user_id)
    new_count = old_count + 1
    await _set_analysis_count(user_id, new_count)

    await _set_average_score(user_id)


# Resource Management

async def add_resource(resource_hash: str) -> None:
    """
    Add a resource hash to the database.

    Args:
        resource_hash (str): The hash of the resource to add.
    """
    await r.sadd("analyzed_images", resource_hash)
    
async def check_resource(resource_hash: str) -> bool:
    """
    Check if a resource hash is already stored in the database.

    Args:
        resource_hash (str): The hash of the resource to check.

    Returns:
        bool: True if the resource hash exists, False otherwise.
    """
    exists = await r.sismember("analyzed_images", resource_hash)
    
    return bool(exists)


# Maintenance functions

async def clear_scores() -> None:
    """
    Clear all user scores from the database.
    """
    await r.delete("score_sums", "analysis_counts", "average_scores")

async def clear_resources() -> None:
    """
    Clear all stored resource hashes from the database.
    """
    await r.delete("analyzed_images")

async def clear_database() -> None:
    """
    Flush all data from the Redis database.
    """
    await r.flushdb()
