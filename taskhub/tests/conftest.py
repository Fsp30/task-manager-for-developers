import pytest
import mongomock
import fakeredis
from mongoengine import connect, disconnect
from django.conf import settings


@pytest.fixture(scope="session", autouse=True)
def mongo_test_connection():
    """Conexão Mongo mockada para rodar os testes."""
    disconnect()  # garante que não vai pegar a conexão real
    connect(
        db="test_db",
        host="mongodb://localhost",  # não conecta de fato
        alias="default",
        uuidRepresentation="standard",
        mongo_client_class=mongomock.MongoClient,
    )
    yield
    disconnect()


@pytest.fixture(scope="session")
def fake_redis():
    """Redis fake para testes."""
    return fakeredis.FakeRedis(decode_responses=True)


@pytest.fixture
def redis_client(monkeypatch, fake_redis):
    """Substitui redis real pelo fake no código."""
    # se no seu código vc importa Redis assim:
    # from redis import Redis
    # então aqui fazemos o patch
    import redis

    monkeypatch.setattr(redis, "Redis", lambda *a, **kw: fake_redis)
    return fake_redis
