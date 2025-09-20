import pytest
from unittest.mock import patch, MagicMock
from taskhub.core.services.enterprise_service import EnterpriseService
from taskhub.core.models import Enterprise, User, Repository
from taskhub.middlewares.exceptions import (
    InputEmptyOrNone,
    EnterprisePermissionDenied,
    EnterpriseFailDelete,
    EnterpriseNotFound
)


class TestDeleteEnterprise:

    @pytest.mark.principal
    def test_delete_enterprise_successful(self, default_enterprise, default_user):
        enterprise_id = default_enterprise.enterpriseId
        
        result = EnterpriseService.delete_enterprise(
            enterprise=default_enterprise,
            creator_enterprise=default_user
        )
        
        assert result is True
        
        with pytest.raises(Enterprise.DoesNotExist):
            Enterprise.objects.get(enterpriseId=enterprise_id)

    @pytest.mark.multiple_entries_missing
    @pytest.mark.parametrize("invalid_enterprise", [
        None,
        "not_an_enterprise",
        123,
        [],
        {},
        MagicMock()
    ])
    def test_delete_with_invalid_enterprise_type(self, invalid_enterprise, default_user):
        with pytest.raises(InputEmptyOrNone):
            EnterpriseService.delete_enterprise(
                enterprise=invalid_enterprise,
                creator_enterprise=default_user
            )

    @pytest.mark.enterprise_id
    @pytest.mark.fails_general
    @pytest.mark.parametrize("invalid_enterprise_id", [
        None,
        "",
        "   ",
        "\t\n\r"
    ])
    def test_delete_with_invalid_enterprise_id(self, invalid_enterprise_id, default_user):
        enterprise = Enterprise(enterpriseId=invalid_enterprise_id, nameEnterprise="Test")
        with pytest.raises(InputEmptyOrNone):
            EnterpriseService.delete_enterprise(
                enterprise=enterprise,
                creator_enterprise=default_user
            )

    @pytest.mark.git_id
    @pytest.mark.fails_general
    @pytest.mark.parametrize("invalid_user_type", [
        None,
        "not_a_user",
        123,
        [],
        {},
        MagicMock()
    ])
    def test_delete_with_invalid_creator_type(self, default_enterprise, invalid_user_type):
        with pytest.raises(InputEmptyOrNone):
            EnterpriseService.delete_enterprise(
                enterprise=default_enterprise,
                creator_enterprise=invalid_user_type
            )

    @pytest.mark.git_id
    @pytest.mark.invalid_data
    @pytest.mark.fails_general
    @pytest.mark.parametrize("invalid_git_id", [
        None,
        "",
        "   ",
        "\t\n\r"
    ])
    def test_delete_with_invalid_creator_gitid(self, default_enterprise, invalid_git_id):
        invalid_user = User(gitId=invalid_git_id, userName="Invalid User")
        with pytest.raises(InputEmptyOrNone):
            EnterpriseService.delete_enterprise(
                enterprise=default_enterprise,
                creator_enterprise=invalid_user
            )

    @pytest.mark.fails_permission
    def test_delete_without_permission(self, default_enterprise, default_user, another_user):

        default_enterprise.devs_enterprise.append(another_user)
        default_enterprise.save()

        with pytest.raises(EnterprisePermissionDenied) as exc_info:
            EnterpriseService.delete_enterprise(
                enterprise=default_enterprise,
                creator_enterprise=another_user  
            )
        
        assert another_user.gitId in str(exc_info.value)
        assert "does not creator" in str(exc_info.value)

    @pytest.mark.handling_cases
    def test_delete_enterprise_database_error(self, default_enterprise, default_user):
        with patch.object(Enterprise, "delete", side_effect=Exception("Database delete failed")):
            with pytest.raises(EnterpriseFailDelete) as exc_info:
                EnterpriseService.delete_enterprise(
                    enterprise=default_enterprise,
                    creator_enterprise=default_user
                )

            assert "Failed to delete enterprise" in str(exc_info.value)
            assert "Database delete failed" in str(exc_info.value)
            assert default_enterprise.enterpriseId in str(exc_info.value)

    @pytest.mark.handling_cases
    def test_delete_enterprise_connection_error(self, default_enterprise, default_user):
        with patch.object(Enterprise, "delete", side_effect=ConnectionError("Database connection failed")):
            with pytest.raises(EnterpriseFailDelete) as exc_info:
                EnterpriseService.delete_enterprise(
                    enterprise=default_enterprise,
                    creator_enterprise=default_user
                )
            
            assert "Database connection failed" in str(exc_info.value)


    @pytest.mark.edge_cases
    def test_delete_enterprise_with_repositories(self, enterprise_with_repositories, default_user):
        repository_count = len(enterprise_with_repositories.repositorys_Id)
        
        result = EnterpriseService.delete_enterprise(
            enterprise=enterprise_with_repositories,
            creator_enterprise=default_user
        )
        
        assert result is True
        
        with pytest.raises(Enterprise.DoesNotExist):
            Enterprise.objects.get(enterpriseId=enterprise_with_repositories)
      
        remaining_repos = Repository.objects(enterpriseId=enterprise_with_repositories)
        assert len(remaining_repos) == repository_count


    @pytest.mark.edge_cases
    def test_delete_enterprise_with_many_devs(self, enterprise_many_devs, default_user):
        enterprise_id = enterprise_many_devs.enterpriseId
        dev_count = len(enterprise_many_devs.devs_enterprise)
        
        result = EnterpriseService.delete_enterprise(
            enterprise=enterprise_many_devs,
            creator_enterprise=default_user
        )
        
        assert result is True

        with pytest.raises(Enterprise.DoesNotExist):
            Enterprise.objects.get(enterpriseId=enterprise_id)
 
        for dev in enterprise_many_devs.devs_enterprise:
            assert User.objects.get(gitId=dev.gitId) is not None


    @pytest.mark.edge_cases
    def test_delete_enterprise_special_chars_id(self, enterprise_special_chars, default_user):
        enterprise_id = enterprise_special_chars.enterpriseId
        
        result = EnterpriseService.delete_enterprise(
            enterprise=enterprise_special_chars,
            creator_enterprise=default_user
        )
        
        assert result is True
        
        with pytest.raises(Enterprise.DoesNotExist):
            Enterprise.objects.get(enterpriseId=enterprise_id)


    @pytest.mark.edge_cases
    def test_delete_enterprise_long_id(self, enterprise_long_id, default_user):

        enterprise_id = enterprise_long_id.enterpriseId
        
        result = EnterpriseService.delete_enterprise(
            enterprise=enterprise_long_id,
            creator_enterprise=default_user
        )
        
        assert result is True
        
        with pytest.raises(Enterprise.DoesNotExist):
            Enterprise.objects.get(enterpriseId=enterprise_id)

    @pytest.mark.performance
    def test_delete_enterprise_performance(self, default_enterprise, default_user):

        import time
        
        start_time = time.time()
        
        result = EnterpriseService.delete_enterprise(
            enterprise=default_enterprise,
            creator_enterprise=default_user
        )
        
        end_time = time.time()
        total_time = end_time - start_time

        assert result is True
        assert total_time < 1.0  


    @pytest.mark.security
    def test_delete_enterprise_error_logging(self, default_enterprise, default_user, caplog):
        with patch.object(Enterprise, "delete", side_effect=Exception("Test error")):
            with pytest.raises(EnterpriseFailDelete):
                with caplog.at_level('ERROR'):
                    EnterpriseService.delete_enterprise(
                        enterprise=default_enterprise,
                        creator_enterprise=default_user
                    )
        
  
        error_messages = [record.message for record in caplog.records if record.levelname == 'ERROR']
        assert any("Failed delete enterprise" in msg for msg in error_messages)
        assert any(default_enterprise.enterpriseId in msg for msg in error_messages)
        assert any(default_user.gitId in msg for msg in error_messages)

    def test_delete_already_deleted_enterprise(self, default_enterprise, default_user):
      
        enterprise_id = default_enterprise.enterpriseId
    
        
        result1 = EnterpriseService.delete_enterprise(
                enterprise=default_enterprise,
                creator_enterprise=default_user
        )
        assert result1 is True
        
        already_deleted_enterprise = Enterprise(
                enterpriseId=enterprise_id,
                nameEnterprise="Test Enterprise",
                owner_Id=default_user
        )
        
        with pytest.raises(EnterpriseNotFound) as exc_info:
                EnterpriseService.delete_enterprise(
                enterprise=already_deleted_enterprise,
                creator_enterprise=default_user
                )
        
        assert f"Enterprise with ID '{enterprise_id}' does not exist" in str(exc_info.value)