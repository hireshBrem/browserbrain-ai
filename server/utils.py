import os
import json
import redis
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv
from langcache import LangCache

load_dotenv()

# Initialize LangCache for semantic caching
langcache_client = LangCache(
    server_url=os.getenv("LANGCACHE_SERVER_URL", "https://aws-us-east-1.langcache.redis.io"),
    cache_id=os.getenv("LANGCACHE_CACHE_ID", ""),
    api_key=os.getenv("LANGCACHE_API_KEY", "")
)

# ===== Long-Term Memory Functions =====

def store_long_term_memory(user_id: str, key: str, value: str) -> bool:
    """Store a long-term memory item for a user"""
    try:
        redis_key = f"longterm_memory:{user_id}"
        redis_client.hset(redis_key, key, value)
        print(f"Stored memory: {key} = {value} for user {user_id}")
        return True
    except Exception as e:
        print(f"Error storing long-term memory: {e}")
        return False

def get_long_term_memory(user_id: str, key: str) -> Optional[str]:
    """Retrieve a specific long-term memory item for a user"""
    try:
        redis_key = f"longterm_memory:{user_id}"
        value = redis_client.hget(redis_key, key)
        print(f"Retrieved memory: {key} = {value} for user {user_id}")
        return value
    except Exception as e:
        print(f"Error retrieving long-term memory: {e}")
        return None

def get_all_long_term_memories(user_id: str) -> Dict[str, str]:
    """Retrieve all long-term memories for a user"""
    try:
        redis_key = f"longterm_memory:{user_id}"
        memories = redis_client.hgetall(redis_key)
        print(f"Retrieved all memories for user {user_id}: {memories}")
        return memories
    except Exception as e:
        print(f"Error retrieving all long-term memories: {e}")
        return {}

def store_conversation_history(user_id: str, task: str, result: str) -> bool:
    """Store conversation/task history in Redis"""
    try:
        redis_key = f"conversation_history:{user_id}"
        timestamp = datetime.now().isoformat()
        history_entry = json.dumps({
            "timestamp": timestamp,
            "task": task,
            "result": result
        })
        # Use a list to store conversation history
        redis_client.rpush(redis_key, history_entry)
        # Keep only last 100 conversations to avoid unbounded growth
        redis_client.ltrim(redis_key, -100, -1)
        print(f"Stored conversation history for user {user_id}")
        return True
    except Exception as e:
        print(f"Error storing conversation history: {e}")
        return False

def get_conversation_history(user_id: str, limit: int = 10) -> List[Dict]:
    """Retrieve recent conversation history for a user"""
    try:
        redis_key = f"conversation_history:{user_id}"
        # Get last N conversations
        history = redis_client.lrange(redis_key, -limit, -1)
        return [json.loads(entry) for entry in history]
    except Exception as e:
        print(f"Error retrieving conversation history: {e}")
        return []

# ===== LangCache Semantic Caching Functions =====

def get_cached_response(query: str) -> Optional[str]:
    """Check if a similar query has been cached"""
    try:
        res = langcache_client.search(
            prompt=query,
            similarity_threshold=1
        )

        print(f"Cached response: {res}")
        
        # Check if res has a data attribute and if it's empty
        if hasattr(res, 'data') and isinstance(res.data, list):
            if len(res.data) == 0:
                print(f"No cached response found for query: {query[:50]}...")
                print(f"✗ Cache MISS for query: {query[:50]}...")
                return None
            # If data array has items, get the first one
            res = res.data[0]
        
        # Handle case where res might be a list directly
        if isinstance(res, list):
            if len(res) == 0:
                print(f"No cached response found for query: {query[:50]}...")
                print(f"✗ Cache MISS for query: {query[:50]}...")
                return None
            res = res[0]
        
        if res:
            print(f"✓ Cache HIT for query: {query[:50]}...")
            # Return only the response field from the cache entry
            return res.response if hasattr(res, 'response') else str(res)
        else:
            print(f"No cached response found for query: {query[:50]}...")
            print(f"✗ Cache MISS for query: {query[:50]}...")
        return None
    except Exception as e:
        print(f"Error checking cache: {e}")
        return None

def cache_response(query: str, response: str) -> bool:
    """Cache a query-response pair for future semantic matching"""
    try:
        res = langcache_client.set(
            prompt=query,
            response=response,
        )

        print(f"Cached set for query: {query}")
        return res
    except Exception as e:
        print(f"Error caching response: {e}")
        return False

