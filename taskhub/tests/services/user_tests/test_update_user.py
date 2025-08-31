import pytest
from datetime import UTC
import datetime
from taskhub.middlewares.exceptions import (
    UserNotFound, 
    InputEmptyOrNone, 
    InputExceededCharacterLimit,
    UserFailUpdate
)
from taskhub.core.services import UserService
from taskhub.core.models import User



class TestUpdateUserService:

        @pytest.mark.principal
        def test_update_user_successfully(self, default_user):
                updated_user = UserService.update_user("123", "test2@example.com", "updateName")
                assert updated_user.gitId == "123"
                assert updated_user.email == "test2@example.com"
                assert updated_user.userName == "updateName"
                assert updated_user.updated_at.tzinfo == UTC
        
        @pytest.mark.userName
        def test_update_user_without_userName(self, default_user):
                updated_user = UserService.update_user("123", "test2@example.com")
                assert updated_user.gitId == "123"
                assert updated_user.email == "test2@example.com"
                assert updated_user.userName == "Filipe"
                assert updated_user.updated_at.tzinfo == UTC
        
        @pytest.mark.email
        def test_update_user_without_email_forced_params(self, default_user):
                updated_user = UserService.update_user(git_id="123",user_name = "updateName")
                assert updated_user.gitId == "123"
                assert updated_user.email == "filipe@example.com"
                assert updated_user.userName == "updateName"
                assert updated_user.updated_at.tzinfo == UTC
        
        @pytest.mark.email
        def test_update_user_with_is_None(self, default_user):
                updated_user = UserService.update_user("123",None, "updateName")
                assert updated_user.gitId == "123"
                assert updated_user.email == "filipe@example.com"
                assert updated_user.userName == "updateName"
                assert updated_user.updated_at.tzinfo == UTC

        @pytest.mark.multiple_entries_missing
        def test_update_user_without_userName_and_email(self,default_user):
                with pytest.raises(InputEmptyOrNone):
                        UserService.update_user("123")


        @pytest.mark.userName
        def test_update_user_with_userName_exceeds_100_characters(self, default_user):
                long_name = "A" * 101
                with pytest.raises(InputExceededCharacterLimit):
                        UserService.update_user("123", None, long_name)

        @pytest.mark.git_id
        def test_update_user_of_notFound(self):
                with pytest.raises(UserNotFound):
                        UserService.update_user("456", "test@example.com")
        

        @pytest.mark.fails
        def test_update_user_unexpected_exception_during_query(self, mocker):
                mocker.patch('taskhub.core.services.user_service.User.objects', 
                side_effect=Exception("Query error"))
                
                with pytest.raises(UserFailUpdate) as exc:
                        UserService.update_user("125", "test@example.com")
                msg = str(exc.value)
                assert "Failed update user with ID '125'" in msg
                assert "Query error" in msg