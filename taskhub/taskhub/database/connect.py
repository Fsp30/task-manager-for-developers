
from mongoengine import connect
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
env.read_env(BASE_DIR / 'taskhub' / 'environments' / '.env')

def mongo_connect():
    connect(
        db=env('MONGO_DB_NAME'),
        host=env('MONGO_URI'),
        tls=True
    )
