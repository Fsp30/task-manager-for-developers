import pytest
from unittest.mock import patch, MagicMock
from taskhub.middlewares.exceptions import (
    InputEmptyOrNone, 
    RepositoryNotFound,
    RepositoryChangeDenied,
    ContentRepositoryFailDelete,
    RepositoryPermissionFailDelete,
    RepositoryFailDelete
)
from taskhub.core.services.repository_service import RepositoryService
from taskhub.core.models import User, Repository


class TestDeleteRepository:

    @pytest.mark.principal
    def test_delete_repository_successfully(self, default_repository):
        with patch('taskhub.core.services.content_repository_service.ContentRepositoryService.delete_content_repository') as mock_content_delete, \
             patch('taskhub.core.services.repository_permission_service.PermissionsService.delete_permission_repository') as mock_perm_delete:
            
            result = RepositoryService.delete_repository("test_repo_id", "creator123")

            assert result is True
            mock_content_delete.assert_called_once_with("test_repo_id", "creator123")
            mock_perm_delete.assert_called_once_with("test_repo_id", "creator123")
 
            with pytest.raises(Repository.DoesNotExist):
                Repository.objects.get(repository_id="test_repo_id")

    @pytest.mark.repository_id
    def test_delete_repository_empty_repository_id(self):
        with pytest.raises(InputEmptyOrNone):
            RepositoryService.delete_repository("", "creator123")
        
        with pytest.raises(InputEmptyOrNone):
            RepositoryService.delete_repository(" ", "creator123")
        
        with pytest.raises(InputEmptyOrNone):
            RepositoryService.delete_repository(None, "creator123")

    @pytest.mark.creator_id
    def test_delete_repository_empty_creator_id(self):
        with pytest.raises(InputEmptyOrNone):
            RepositoryService.delete_repository("test_repo_id", "")
        
        with pytest.raises(InputEmptyOrNone):
            RepositoryService.delete_repository("test_repo_id", " ")
        
        with pytest.raises(InputEmptyOrNone):
            RepositoryService.delete_repository("test_repo_id", None)

    @pytest.mark.multiple_entries_missing
    def test_delete_repository_both_fields_empty(self):
        with pytest.raises(InputEmptyOrNone):
            RepositoryService.delete_repository("", "")
        
        with pytest.raises(InputEmptyOrNone):
            RepositoryService.delete_repository(" ", " ")
        
        with pytest.raises(InputEmptyOrNone):
            RepositoryService.delete_repository(None, None)

    @pytest.mark.not_found
    def test_delete_repository_not_found(self):
        with patch('taskhub.core.services.repository_service.RepositoryService.get_repository', 
                  side_effect=RepositoryNotFound()):
            with pytest.raises(RepositoryNotFound):
                RepositoryService.delete_repository("non_existent_repo", "creator123")

    @pytest.mark.unauthorized
    def test_delete_repository_unauthorized_user(self, default_repository):
        with pytest.raises(RepositoryChangeDenied) as exc_info:
            RepositoryService.delete_repository("test_repo_id", "unauthorized_user")
        
        assert "User 'unauthorized_user' not authorized to delete repository 'test_repo_id'" in str(exc_info.value)

    @pytest.mark.fails_content
    def test_delete_repository_content_delete_fails(self, default_repository):
        with patch('taskhub.core.services.content_repository_service.ContentRepositoryService.delete_content_repository', 
                  side_effect=ContentRepositoryFailDelete("Content delete failed")), \
             pytest.raises(ContentRepositoryFailDelete):
            RepositoryService.delete_repository("test_repo_id", "creator123")

    @pytest.mark.fails_permission
    def test_delete_repository_permission_delete_fails(self, default_repository):
        with patch('taskhub.core.services.content_repository_service.ContentRepositoryService.delete_content_repository'), \
             patch('taskhub.core.services.repository_permission_service.PermissionsService.delete_permission_repository', 
                  side_effect=RepositoryPermissionFailDelete("Permission delete failed")), \
             pytest.raises(RepositoryPermissionFailDelete):
            RepositoryService.delete_repository("test_repo_id", "creator123")

    @pytest.mark.fails_general
    def test_delete_repository_general_exception(self, default_repository):
        with patch('taskhub.core.services.repository_service.RepositoryService.get_repository', 
                  side_effect=Exception("Database connection error")), \
             pytest.raises(RepositoryFailDelete) as exc_info:
            RepositoryService.delete_repository("test_repo_id", "creator123")
        
        assert "Failed to delete repository 'test_repo_id'" in str(exc_info.value)
        assert "Database connection error" in str(exc_info.value)

    @pytest.mark.fails_general
    def test_delete_repository_delete_operation_fails(self, default_repository):
        with patch('taskhub.core.services.content_repository_service.ContentRepositoryService.delete_content_repository'), \
             patch('taskhub.core.services.repository_permission_service.PermissionsService.delete_permission_repository'), \
             patch.object(Repository, 'delete', side_effect=Exception("Delete operation failed")), \
             pytest.raises(RepositoryFailDelete) as exc_info:
            RepositoryService.delete_repository("test_repo_id", "creator123")
        
        assert "Failed to delete repository 'test_repo_id'" in str(exc_info.value)
        assert "Delete operation failed" in str(exc_info.value)

    @pytest.mark.whitespace
    def test_delete_repository_with_whitespace_in_ids(self):
        creator_with_spaces = User(
            gitId=" creator123 ",
            email="creator@example.com",
            userName="Creator User"
        )
        creator_with_spaces.save()
        
        repository_with_spaces = Repository(
            repository_id=" test_repo_id ",
            creator_Id=creator_with_spaces
        )
        repository_with_spaces.save()
        
        with patch('taskhub.core.services.content_repository_service.ContentRepositoryService.delete_content_repository'), \
             patch('taskhub.core.services.repository_permission_service.PermissionsService.delete_permission_repository'):
            
            result = RepositoryService.delete_repository(" test_repo_id ", " creator123 ")
            assert result is True

    @pytest.mark.integration
    def test_delete_repository_verifies_creator_id_correctly(self, default_repository):
        with pytest.raises(RepositoryChangeDenied):
            RepositoryService.delete_repository("test_repo_id", "123") 
        
 
        with patch('taskhub.core.services.content_repository_service.ContentRepositoryService.delete_content_repository'), \
             patch('taskhub.core.services.repository_permission_service.PermissionsService.delete_permission_repository'):
            result = RepositoryService.delete_repository("test_repo_id", "creator123")
            assert result is True

    @pytest.mark.fails_general
    def test_delete_repository_unexpected_exception_during_imports(self, default_repository):
        with patch('taskhub.core.services.repository_service.RepositoryService.get_repository', 
                  return_value=default_repository), \
             patch('taskhub.core.services.content_repository_service.ContentRepositoryService.delete_content_repository', 
                  side_effect=Exception("Unexpected error during content deletion")), \
             pytest.raises(RepositoryFailDelete) as exc_info:
            RepositoryService.delete_repository("test_repo_id", "creator123")
        
        assert "Failed to delete repository 'test_repo_id'" in str(exc_info.value)
        assert "Unexpected error during content deletion" in str(exc_info.value)