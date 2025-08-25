import os
import django
import pytest
from unittest.mock import patch


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskhub.config.settings')

django.setup()

@pytest.fixture(autouse=True)
def mock_mongo_connection():
    with patch('mongoengine.connect') as mock_connect:
        yield mock_connect

@pytest.fixture(autouse=True)
def mock_redis_connection():
    with patch('taskhub.infra.database.redis.connect_redis.redis_client') as mock_redis:
        mock_redis.return_value = None
        yield mock_redis

@pytest.fixture
def django_settings():
    from django.conf import settings
    return settings