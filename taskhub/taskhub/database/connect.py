from mongoengine import connect
import environ
from pathlib import Path

env = environ.Env(DEBUG=(bool, True))
BASE_DIR = Path(__file__).resolve().parent.parent
env.read_env(BASE_DIR / 'environments' / '.env')

MONGO_DB_NAME = env('MONGO_DB_NAME')
MONGO_URI = env('MONGO_URI')

connect(db=MONGO_DB_NAME, host=MONGO_URI)

print(f"✅ Conectado ao MongoDB: {MONGO_DB_NAME}")
