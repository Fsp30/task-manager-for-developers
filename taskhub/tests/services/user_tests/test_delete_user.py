import pytest
from datetime import UTC
import datetime
from taskhub.middlewares.exceptions import (
    InputEmptyOrNone, 
    UserNotFound,
    UserFailDelete
)
from taskhub.core.services.user_service import UserService  

from taskhub.core.models import User, Repository, RepositoryPermission


class TestDeleteUsers:

        @pytest.mark.principal
        def test_delete_user_successfully(self, default_user):
                deleted_user = UserService.delete_user("123")
                assert deleted_user == True
        
        @pytest.mark.git_id
        def test_delete_without_gitId(self):
                with pytest.raises(InputEmptyOrNone):
                        UserService.delete_user("")
                with pytest.raises(InputEmptyOrNone):
                        UserService.delete_user(" ")
                with pytest.raises(InputEmptyOrNone):
                        UserService.delete_user(None)

        @pytest.mark.not_found
        def test_delete_user_notFound(self):
                with pytest.raises(UserNotFound):
                        UserService.delete_user("test_delete_not_found")

        @pytest.mark.fails
        def test_delete_user_unexpected_exception_during_query(self, mocker):
                mocker.patch('taskhub.core.services.user_service.User.objects', 
                side_effect=Exception("Query error"))
                
                with pytest.raises(UserFailDelete) as exc:
                        UserService.delete_user("125")
                msg = str(exc.value)
                assert "Failed delete user with ID '125'" in msg
                assert "Query error" in msg
