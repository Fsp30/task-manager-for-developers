import pytest
import mongomock
import fakeredis
from taskhub.core.services.user_service import UserService
from taskhub.core.services.repository_service import RepositoryService
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
def default_repository_list():
    from taskhub.core.models import Repository, User
    from datetime import datetime, UTC
    
    user = UserService.create_user("123", "test@example.com")
    
    Repository.objects(creator_Id=user).delete()

    
    repositories = []
    for i in range(5):
        repo = Repository(
            repository_id=f"repo-{i}",
            creator_Id=user,
        )
        repo.save()
        repositories.append(repo)

    user.repositories = repositories
    user.save()
    
    return repositories