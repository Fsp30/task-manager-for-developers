# taskhub/tests/conftest.py
import pytest
from unittest.mock import patch, MagicMock
import sys

@pytest.fixture(autouse=True)
def mock_mongodb_connection():
    with patch('mongoengine.connect') as mock_connect:
        with patch('mongoengine.connection.get_connection') as mock_get_conn:
            mock_conn = MagicMock()
            mock_get_conn.return_value = mock_conn
            yield

@pytest.fixture(autouse=True)
def mock_all_exceptions():
    from .mocks.user_exceptions_mock import UserAlreadyExists, UserNotFound
    from .mocks.base_exception_mock import InvalidEmailFormat, InputExceededCharacterLimit
    
    exceptions_to_mock = {
        'taskhub.middlewares.exceptions.user.user_exception_handler.UserAlreadyExists': UserAlreadyExists,
        'taskhub.middlewares.exceptions.user.user_exception_handler.UserNotFound': UserNotFound,
        'taskhub.middlewares.exceptions.base_exception_handler.InvalidEmailFormat': InvalidEmailFormat,
        'taskhub.middlewares.exceptions.base_exception_handler.InputExceededCharacterLimit': InputExceededCharacterLimit,
    }
    
    patches = []
    for target, mock_class in exceptions_to_mock.items():
        patches.append(patch(target, mock_class))
    
  
    for p in patches:
        p.start()
    
    yield
  
    for p in patches:
        p.stop()