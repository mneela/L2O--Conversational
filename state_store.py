import os
from dotenv import load_dotenv
from upstash_redis import Redis
from models import ConversationState

# Load environment variables from .env file
load_dotenv()

# Load Redis credentials from environment
redis_url = os.getenv("UPSTASH_REDIS_REST_URL")
redis_token = os.getenv("UPSTASH_REDIS_REST_TOKEN")

if not redis_url or not redis_token:
    raise ValueError("Missing UPSTASH_REDIS_REST_URL or UPSTASH_REDIS_REST_TOKEN environment variables")

redis = Redis(url=redis_url, token=redis_token)

TTL_SECONDS = 60 * 60 * 24  # 24 hours

def _key(user_id: str) -> str:
    return f"convo:{user_id}"

def get_state(user_id: str):
    data = redis.get(_key(user_id))
    if not data:
        return None
    return ConversationState.model_validate_json(data)

def save_state(state: ConversationState):
    redis.set(_key(state.user_id), state.model_dump_json(), ex=TTL_SECONDS)

def delete_state(user_id: str):
    redis.delete(_key(user_id))
