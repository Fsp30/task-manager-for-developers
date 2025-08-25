import pytest
from unittest.mock import patch, MagicMock
from taskhub.core.services.user_service import create_user,delete_user,get_user, get_my_permissions, list_my_repositories
from taskhub.core.models import User

from taskhub.tests.mocks.user_exceptions_mock import UserAlreadyExists
from taskhub.tests.mocks.base_exception_mock import InvalidEmailFormat

class TestUserService:
    
    @patch('taskhub.core.services.user_service.User.objects')
    def test_create_user_success(self, mock_objects):
        """Test successful user creation"""
        mock_objects.return_value.first.return_value = None
        
        from taskhub.core.services.user_service import create_user
        user = create_user("test123", "test@email.com", "Test User")
        
        assert user.gitId == "test123"
        assert user.email == "test@email.com"
    