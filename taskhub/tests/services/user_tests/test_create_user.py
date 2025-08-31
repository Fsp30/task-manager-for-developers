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
from taskhub.core.services import UserService
from taskhub.core.models import User



class TestCreateUserService:

        @pytest.mark.principal
        def test_create_user_successfully(self):
                user = UserService.create_user("124", "test@example.com", "test_example")  

                assert user is not None
                assert user.gitId == "124"
                assert user.email == "test@example.com"
                assert user.userName == "test_example"
                assert isinstance(user.created_at, datetime.datetime)
                assert isinstance(user.updated_at, datetime.datetime)

                saved_user = User.objects(gitId="124").first()
                assert saved_user is not None
                assert saved_user.email == "test@example.com"

        @pytest.mark.principal
        def test_create_user_duplicate(self, default_user):
                with pytest.raises(UserAlreadyExists):
                        UserService.create_user("123", "filipe@example.com", "Filipe")

        @pytest.mark.userName
        def test_create_user_without_name_uses_git_id(self):

                user = UserService.create_user("789", "withoutName@example.com")

                assert user.userName == "789"
                assert user.email == "withoutName@example.com"
        
        @pytest.mark.email
        def test_create_user_without_email(self):
                with pytest.raises(InputEmptyOrNone):
                        UserService.create_user("123", "")
                with pytest.raises(InputEmptyOrNone):
                        UserService.create_user("123", " ")
                with pytest.raises(InputEmptyOrNone):
                        UserService.create_user("123", None)
        
        @pytest.mark.git_id
        def test_create_user_empty_git_id(self):
                with pytest.raises(InputEmptyOrNone):
                        UserService.create_user("", "test@example.com")
                with pytest.raises(InputEmptyOrNone):
                        UserService.create_user(" ", "test@example.com")
                with pytest.raises(InputEmptyOrNone):
                        UserService.create_user(None,  "test@example.com")

        @pytest.mark.userName
        def test_create_user_with_userName_exceeds_100_characters(self):
                long_name = "A" * 101
                with pytest.raises(InputExceededCharacterLimit):
                        UserService.create_user("userTest", "test@example.com", long_name)
        
        @pytest.mark.userName
        def test_create_user_with_userName_exactly_100_characters(self):
                username_test = "A" * 100
                user = UserService.create_user("userTest", "test@example.com", username_test)

                assert user.userName == username_test


        @pytest.mark.git_id
        def test_create_user_with_whitespace_in_gitId(self):
                with pytest.raises(InputEmptyOrNone):
                        UserService.create_user(" ", "test@example.com")
                
                user = UserService.create_user(" test ", "test@example.com")
                assert user.gitId == " test "
                assert user.userName == " test "
                
        @pytest.mark.timestamp
        def test_create_user_timestame_is_UTC(self):
                user = UserService.create_user("test", "test@example.com")

                assert user.created_at.tzinfo == UTC
                assert user.updated_at.tzinfo == UTC

                assert abs((user.created_at - user.updated_at).total_seconds()) < 1

        @pytest.mark.fails
        def test_create_user_unexpected_exception_during_query(self, mocker):
                mocker.patch('taskhub.core.services.user_service.User.objects', 
                        side_effect=Exception("Query error"))
                
                with pytest.raises(UserFailCreate) as exc_info:
                        UserService.create_user("123", "test@example.com")
                
                assert "Failed to create user with GitHub ID '123'" in str(exc_info.value)
                assert "Query error" in str(exc_info.value)
                        







    


