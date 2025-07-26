import environ
import redis
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env.read_env(BASE_DIR / 'taskhub' / 'config' / 'environments' / '.env')  

def redis_connect():
    host=env('HOST_REDIS')
    port=env.int('PORT_REDIS')
    decode=env.bool('DECODE_RESPONSES')

    return redis.Redis(
        host=host,
        port=port,
        decode_responses=decode
    )

redis_client = redis_connect()
