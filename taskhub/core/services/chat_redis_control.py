from taskhub.infra.database.redis.connect_redis import redis_client
from datetime import datetime 
import json

r = redis_client

def save_message(chat_id:str, userId:str, message:str):
        key = f"chat:{chat_id}"
        data = {
                "userId": userId,
                "timestamp": datetime.utcnow().isoformat(), 
                "message": message
        }
        r.rpush(key, json.dumps(data))
        r.expire(key, 60 * 60 * 48)


