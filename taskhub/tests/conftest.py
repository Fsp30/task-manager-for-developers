import pytest
import mongomock
import fakeredis
from taskhub.core.services.user_service import create_user
from mongoengine import connect, disconnect, get_db

@pytest.fixture(scope="session", autouse=True)
def mongo_test_connection():
    disconnect()  
    connect(
        db="test_db",
        host="mongodb://localhost",  
        alias="default",
        uuidRepresentation="standard",
        mongo_client_class=mongomock.MongoClient,
    )
    yield
    disconnect()

@pytest.fixture(autouse=True)
def clear_mongo_collections():
    db = get_db()
    for collection in db.list_collection_names():
        db[collection].delete_many({})

@pytest.fixture(scope="session")
def fake_redis():
    return fakeredis.FakeRedis(decode_responses=True)

@pytest.fixture
def redis_client(monkeypatch, fake_redis):
    import redis
    monkeypatch.setattr(redis, "Redis", lambda *a, **kw: fake_redis)
    return fake_redis



@pytest.fixture
def default_user():
    user = create_user("123", "filipe@example.com", "Filipe")
    return user
