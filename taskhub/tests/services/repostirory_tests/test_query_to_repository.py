import pytest
from datetime import UTC
from taskhub.middlewares.exceptions import(
    RepositoryNotFound,
    RepositoryFailDetail, 
    RepositoryPermissionFailList,

    
    InputEmptyOrNone
)
from taskhub.core.services.repository_service import RepositoryService
from taskhub.core.models import User, Repository, RepositoryPermission

class TestQueryToRepository:
    @pytest.mark.principal
    def test_get_repository_successfully(self,default_repository):
        repo = RepositoryService.get_repository("test_repo_id")

        assert repo.creator_Id.gitId == "creator123"
        assert repo.enterpriseId.enterpriseId == "enterprise123"
        assert len(repo.admin_repository.admin_users) == 4
    
    @pytest.mark.repository_id
    def test_get_repository_without_gitId(self):
        with pytest.raises(InputEmptyOrNone):
            RepositoryService.get_repository("")
        with pytest.raises(InputEmptyOrNone):
            RepositoryService.get_repository(" ")
        with pytest.raises(InputEmptyOrNone):
            RepositoryService.get_repository(None)
    
    @pytest.mark.not_found
    def test_get_repository_not_found(self):
        with pytest.raises(RepositoryNotFound):
            RepositoryService.get_repository("repo_not_found")
    
    @pytest.mark.fails
    def test_get_repository_unexpected_exception_during_query(self, mocker):
        mocker.patch('taskhub.core.services.repository_service.Repository.objects', 
            side_effect=Exception("Query error"))

        with pytest.raises(RepositoryFailDetail) as exc_info:
            RepositoryService.get_repository("4654")
        
        assert "Failed detail repository ID '4654'" in str(exc_info.value)
        assert "Query error" in str(exc_info.value)



class TestListAdminUsers:

    @pytest.mark.principal
    def test_list_admin_users_successfully(self, default_repository):
        admin_users = RepositoryService.list_admin_users("test_repo_id")
        
        assert len(admin_users) == 4 
        assert all(isinstance(user, User) for user in admin_users)
        
        expected_git_ids = {"creator123", "admin0", "admin1", "admin2"}
        actual_git_ids = {user.gitId for user in admin_users}
        assert expected_git_ids == actual_git_ids

    @pytest.mark.repository_id
    def test_list_admin_users_without_repository_id(self):
        with pytest.raises(InputEmptyOrNone):
            RepositoryService.list_admin_users("")
        
        with pytest.raises(InputEmptyOrNone):
            RepositoryService.list_admin_users(" ")
        
        with pytest.raises(InputEmptyOrNone):
            RepositoryService.list_admin_users(None)

    @pytest.mark.repository_id
    def test_list_admin_users_with_whitespace_in_repository_id(self):
        creator = User(
            gitId="test_creator", 
            email="test@example.com",
            userName="Test Creator"
        )
        creator.save()
        
        repository = Repository(
            repository_id=" repo_with_spaces ",
            creator_Id=creator
        )
        repository.save()
        
        permissions = RepositoryPermission(
            repositoryPermissionId="space_perm",
            admin_repository=repository,
            admin_users=[creator]
        )
        permissions.save()
        
        repository.admin_repository = permissions
        repository.save()
        
        admin_users = RepositoryService.list_admin_users(" repo_with_spaces ")
        assert len(admin_users) == 1
        assert admin_users[0].gitId == "test_creator"

    @pytest.mark.list_none
    def test_list_admin_users_result_empty_list(self):
        creator = User(
            gitId="test_creator", 
            email="test@example.com",
            userName="Test Creator"
        )
        creator.save()
        
        repository = Repository(
            repository_id="repo_no_admins",
            creator_Id=creator
        )
        repository.save()
        
        permissions = RepositoryPermission(
            repositoryPermissionId="no_admins_perm",
            admin_repository=repository,
            admin_users=[]  # Lista vazia
        )
        permissions.save()
        
        repository.admin_repository = permissions
        repository.save()
        
        empty_list = RepositoryService.list_admin_users("repo_no_admins")
        
        assert empty_list is not None
        assert not empty_list
        assert isinstance(empty_list, list)

    @pytest.mark.not_found
    def test_list_admin_users_repository_not_found(self):
        with pytest.raises(RepositoryNotFound):
            RepositoryService.list_admin_users("non_existent_repo")

    @pytest.mark.not_found
    def test_list_admin_users_permission_not_found(self):
        creator = User(
            gitId="test_creator", 
            email="test@example.com",
            userName="Test Creator"
        )
        creator.save()
        
        repository = Repository(
            repository_id="repo_no_perms",
            creator_Id=creator
        )
        repository.save()
        
        empty_list = RepositoryService.list_admin_users("repo_no_perms")
        assert empty_list == []
        assert len(empty_list) == 0

    @pytest.mark.fails
    def test_list_admin_users_unexpected_exception_during_query(self, mocker):
        mocker.patch('taskhub.core.services.repository_service.RepositoryService.get_repository', 
            side_effect=Exception("Database error"))

        with pytest.raises(RepositoryPermissionFailList) as exc_info:
            RepositoryService.list_admin_users("test_repo_id")
            
        assert "Failed to list admin users for repository 'test_repo_id'" in str(exc_info.value)
        assert "Database error" in str(exc_info.value)

    @pytest.mark.fails
    def test_list_admin_users_unexpected_exception_during_permission_query(self, mocker):
        creator = User(
            gitId="test_creator", 
            email="test@example.com",
            userName="Test Creator"
        )
        repository = Repository(repository_id="test_repo_id", creator_Id=creator)
        
        mocker.patch('taskhub.core.services.repository_service.RepositoryService.get_repository', 
            return_value=repository)
        mocker.patch('taskhub.core.models.RepositoryPermission.objects', 
            side_effect=Exception("Permission query error"))

        with pytest.raises(RepositoryPermissionFailList) as exc_info:
            RepositoryService.list_admin_users("test_repo_id")
            
        assert "Failed to list admin users for repository 'test_repo_id'" in str(exc_info.value)
        assert "Permission query error" in str(exc_info.value)
