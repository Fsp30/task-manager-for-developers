import pytest
from datetime import UTC
import datetime
from taskhub.middlewares.exceptions import (
    InputEmptyOrNone, 
    UserNotFound,
    UserFailDetail,
    RepositoryFailList,
    UserFailCreate
)
from taskhub.core.services.user_service import UserService  

from taskhub.core.models import User, Repository, RepositoryPermission


class TestQueryToUsers:

    @pytest.mark.principal
    def test_get_user_successfully(self):
            UserService.create_user("125", "get@email.com") 
            user = UserService.get_user("125")  

            assert user.gitId == "125"
            assert user.email == "get@email.com"
            assert user.userName == "125"
    
    @pytest.mark.git_id
    def test_get_user_without_gitId(self):
        with pytest.raises(InputEmptyOrNone):
            UserService.get_user("")  
        with pytest.raises(InputEmptyOrNone):
            UserService.get_user(" ") 
        with pytest.raises(InputEmptyOrNone):
            UserService.get_user(None) 
    
    @pytest.mark.not_found
    def test_get_user_not_found(self):
        with pytest.raises(UserNotFound):
            UserService.get_user("892")
    
    @pytest.mark.fails
    def test_get_user_unexpected_exception_during_query(self, mocker):
        mocker.patch('taskhub.core.services.user_service.User.objects', 
            side_effect=Exception("Query error"))

        with pytest.raises(UserFailDetail) as exc_info:
            UserService.get_user("123")
            
        assert "Failed detail user ID '123'" in str(exc_info.value)
        assert "Query error" in str(exc_info.value)

class TestToQueryUserRepository:
    
    @pytest.mark.principal
    def test_get_all_repository_of_user_successfully(self, default_repository_list):
        repository_list = UserService.list_my_repositories("123")

        repository_list = sorted(repository_list, key=lambda r: r.repository_id)
        default_repository_list = sorted(default_repository_list, key=lambda r: r.repository_id)

        assert len(repository_list) == len(default_repository_list)
        assert [repo.repository_id for repo in repository_list] == [repo.repository_id for repo in default_repository_list]
        assert all(isinstance(repo, Repository) for repo in repository_list)
        assert all(repo.creator_Id.gitId == "123" for repo in repository_list)


    @pytest.mark.git_id
    def test_get_all_repository_of_user_without_gitId(self):
        with pytest.raises(InputEmptyOrNone):
            UserService.list_my_repositories("")
        
        with pytest.raises(InputEmptyOrNone):
            UserService.list_my_repositories(" ")
        
        with pytest.raises(InputEmptyOrNone):
            UserService.list_my_repositories(None)
    
    @pytest.mark.git_id
    def test_get_all_repository_of_user_with_whitespace_in_gitId(self):
        user = UserService.create_user(" 123 ", "test@example.com")
        
        Repository.objects(creator_Id=user).delete()

        repositories = []
        for i in range(2):
            repo = Repository(
                repository_id=f"repo-{i}",
                creator_Id=user,   
            )
            repo.save()
            repositories.append(repo)

        user.repositories = repositories
        user.save()

        repos = UserService.list_my_repositories(" 123 ")

        sort = sorted(repos, key=lambda r: r.repository_id)

        assert sort[0].repository_id == "repo-0"
        assert sort[1].repository_id == "repo-1"
        assert all(repo.creator_Id == user for repo in sort)  
    
    @pytest.mark.list_none
    def test_get_repository_of_user_result_empty_list(self):
        user = UserService.create_user("123", "test@example.com")
        Repository.objects(creator_Id=user).delete()

        empty_list = UserService.list_my_repositories("123")

        assert empty_list is not None
        assert not empty_list
        assert isinstance(empty_list, list)


    @pytest.mark.not_found
    def test_get_all_repository_of_user_NotFound(self):
        with pytest.raises(UserNotFound):
            UserService.list_my_repositories("user_not_found")
    

    @pytest.mark.fails
    def test_get_all_user_unexpected_exception_during_query(self, mocker):
        mocker.patch('taskhub.core.services.user_service.User.objects', 
            side_effect=Exception("Query error"))

        with pytest.raises(RepositoryFailList) as exc_info:
            UserService.list_my_repositories("123")
            
        assert "Failed list repositories for user '123'" in str(exc_info.value)
        assert "Query error" in str(exc_info.value)

class TestToQueryUserEnterprise:
    
    @pytest.mark.principal
    def test_ge_my_permissions_user_successfully(self, default_repository_permissions):
        perms = UserService.get_my_permissions("123")

        assert len(perms) == 3

        expected_ids = [f"perm-{i}" for i in range(3)]
        actual_ids = [p.repositoryPermissionId for p in perms]
        assert actual_ids == expected_ids

        for perm in perms:
            assert any(u.gitId == "123" for u in perm.admin_users)
    
    @pytest.mark.git_id
    def test_get_my_permissions_user_wihtout_gitId(self):
        with pytest.raises(InputEmptyOrNone):
            UserService.get_my_permissions("")
        
        with pytest.raises(InputEmptyOrNone):
            UserService.get_my_permissions(" ")
        
        with pytest.raises(InputEmptyOrNone):
            UserService.get_my_permissions(None)
        
    @pytest.mark.list_none
    def test_get_permissions_of_user_result_empty_list(self):
        user = UserService.create_user("123", "test@example.com")
        RepositoryPermission.objects(admin_users=user).delete()

        empty_list = UserService.get_my_permissions("123")

        assert empty_list is not None
        assert not empty_list
        assert isinstance(empty_list, list)

    @pytest.mark.not_found
    def test_get_permissions_of_user_NotFound(self):
        with pytest.raises(UserNotFound):
            UserService.get_my_permissions("123")
    

    @pytest.mark.fails
    def test_get_all_permissions_unexpected_exception_during_query(self, mocker):
        mocker.patch('taskhub.core.services.user_service.User.objects', 
            side_effect=Exception("Query error"))
        
        with pytest.raises(UserFailCreate) as exc:

            UserService.create_user("125", "test@example.com")
        assert "Failed to create user with GitHub ID '125': Query error" in str(exc.value)

   