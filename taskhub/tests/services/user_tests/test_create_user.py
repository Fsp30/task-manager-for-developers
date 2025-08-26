import pytest
from datetime import UTC
import datetime
from taskhub.middlewares.exceptions import (
    UserAlreadyExists, 
    InputEmptyOrNone, 
    InvalidEmailFormat, 
    InputExceededCharacterLimit,
    UserFailCreate
)
from taskhub.core.services.user_service import create_user
from taskhub.core.models import User



class TestCreateUserService:

        def test_create_user_successfully(self):
                user = create_user("124", "test@example.com", "test_example")  

                assert user is not None
                assert user.gitId == "124"
                assert user.email == "test@example.com"
                assert user.userName == "test_example"
                assert isinstance(user.created_at, datetime.datetime)
                assert isinstance(user.updated_at, datetime.datetime)

                saved_user = User.objects(gitId="124").first()
                assert saved_user is not None
                assert saved_user.email == "test@example.com"

        def test_create_user_duplicate(self, default_user):
                with pytest.raises(UserAlreadyExists):
                        create_user("123", "filipe@example.com", "Filipe")
        
        def test_create_user_without_name_uses_git_id(self):

                user = create_user("789", "withoutName@example.com")

                assert user.userName == "789"
                assert user.email == "withoutName@example.com"

                


    


