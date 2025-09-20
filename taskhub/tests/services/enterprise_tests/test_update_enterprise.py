import pytest
from unittest.mock import patch, MagicMock
from taskhub.core.services.enterprise_service import EnterpriseService
from taskhub.core.models import Enterprise, User
from taskhub.middlewares.exceptions import (
    InputEmptyOrNone,
    EnterprisePermissionDenied,
    EnterpriseFailUpdate,
    DomainNoChange,
    EnterpriseAlreadyExists,
    InputExceededCharacterLimit
)


class TestUpdateEnterprise:

    @pytest.mark.principal
    def test_update_enterprise_successful(self, default_enterprise, default_user):
        original_name = default_enterprise.nameEnterprise
        new_name = "Updated Enterprise Name"
        
        result = EnterpriseService.update_enterprise(
            git_owner=default_user,
            enterprise=default_enterprise,
            name_enterprise=new_name
        )
        
       
        assert result.nameEnterprise == new_name
        assert result.enterpriseId == default_enterprise.enterpriseId
        assert result.owner_Id == default_user

    @pytest.mark.principal
    def test_update_enterprise_max_length_name(self, default_enterprise, default_user):
        max_length_name = "A" * 100  
        result = EnterpriseService.update_enterprise(
            git_owner=default_user,
            enterprise=default_enterprise,
            name_enterprise=max_length_name
        )
        
        assert result.nameEnterprise == max_length_name
        assert len(result.nameEnterprise) == 100

    @pytest.mark.fails_general
    def test_update_enterprise_name_too_long(self, default_enterprise, default_user):
        too_long_name = "A" * 101  
        
        with pytest.raises(InputExceededCharacterLimit) as exc_info:
            EnterpriseService.update_enterprise(
                git_owner=default_user,
                enterprise=default_enterprise,
                name_enterprise=too_long_name
            )
        
        assert "100 characters or less" in str(exc_info.value)
        assert "101" in str(exc_info.value)

    @pytest.mark.multiple_entries_missing
    @pytest.mark.parametrize("invalid_enterprise", [
        None,
        "not_an_enterprise",
        123,
        [],
        {},
        MagicMock()
    ])
    def test_update_with_invalid_enterprise_type(self, invalid_enterprise, default_user):
        with pytest.raises(InputEmptyOrNone):
            EnterpriseService.update_enterprise(
                git_owner=default_user,
                enterprise=invalid_enterprise,
                name_enterprise="New Name"
            )

    @pytest.mark.enterprise_id
    @pytest.mark.fails_general
    @pytest.mark.parametrize("invalid_enterprise_id", [
        None,
        "",
        "   ",
        "\t\n\r"
    ])
    def test_update_with_invalid_enterprise_id(self, invalid_enterprise_id, default_user):
        enterprise = Enterprise(enterpriseId=invalid_enterprise_id, nameEnterprise="Test")
        with pytest.raises(InputEmptyOrNone):
            EnterpriseService.update_enterprise(
                git_owner=default_user,
                enterprise=enterprise,
                name_enterprise="New Name"
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
    def test_update_with_invalid_owner_type(self, default_enterprise, invalid_user_type):
        with pytest.raises(InputEmptyOrNone):
            EnterpriseService.update_enterprise(
                git_owner=invalid_user_type,
                enterprise=default_enterprise,
                name_enterprise="New Name"
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
    def test_update_with_invalid_owner_gitid(self, default_enterprise, invalid_git_id):
        invalid_user = User(gitId=invalid_git_id, userName="Invalid User")
        with pytest.raises(InputEmptyOrNone):
            EnterpriseService.update_enterprise(
                git_owner=invalid_user,
                enterprise=default_enterprise,
                name_enterprise="New Name"
            )

    @pytest.mark.fails_general
    @pytest.mark.parametrize("invalid_name", [
        None,
        "",
        "   ",
        "\t\n\r"
    ])
    def test_update_with_invalid_name(self, default_enterprise, default_user, invalid_name):
        with pytest.raises(InputEmptyOrNone):
            EnterpriseService.update_enterprise(
                git_owner=default_user,
                enterprise=default_enterprise,
                name_enterprise=invalid_name
            )

    @pytest.mark.fails_permission
    def test_update_without_permission(self, default_enterprise, default_user, another_user):
        with pytest.raises(EnterprisePermissionDenied) as exc_info:
            EnterpriseService.update_enterprise(
                git_owner=another_user,  
                enterprise=default_enterprise,
                name_enterprise="New Name"
            )
        
        assert another_user.gitId in str(exc_info.value)
        assert "does not creator" in str(exc_info.value)

    @pytest.mark.fails_general
    def test_update_same_name(self, default_enterprise, default_user):
        same_name = default_enterprise.nameEnterprise
        
        with pytest.raises(DomainNoChange) as exc_info:
            EnterpriseService.update_enterprise(
                git_owner=default_user,
                enterprise=default_enterprise,
                name_enterprise=same_name
            )
        
        assert "change is necessary" in str(exc_info.value)

    @pytest.mark.fails_general
    def test_update_name_already_exists(self, default_enterprise, default_user, user_factory):
        existing_enterprise = Enterprise(
            enterpriseId="existing_123",
            nameEnterprise="Existing Enterprise",
            owner_Id=default_user
        )
        existing_enterprise.save()
        
        try:
            with pytest.raises(EnterpriseAlreadyExists) as exc_info:
                EnterpriseService.update_enterprise(
                    git_owner=default_user,
                    enterprise=default_enterprise,
                    name_enterprise="Existing Enterprise"  
                )
            
            assert "already exists" in str(exc_info.value)
            assert "Existing Enterprise" in str(exc_info.value)
        finally:
            existing_enterprise.delete()

    @pytest.mark.handling_cases
    def test_update_enterprise_database_error(self, default_enterprise, default_user):
        with patch.object(Enterprise, "save", side_effect=Exception("Database save failed")):
            with pytest.raises(EnterpriseFailUpdate) as exc_info:
                EnterpriseService.update_enterprise(
                    git_owner=default_user,
                    enterprise=default_enterprise,
                    name_enterprise="New Name"
                )

            assert "Failed to update enterprise" in str(exc_info.value)
            assert "Database save failed" in str(exc_info.value)
            assert default_enterprise.enterpriseId in str(exc_info.value)
    
    @pytest.mark.handling_cases
    def test_update_enterprise_connection_error(self, default_enterprise, default_user):
        with patch.object(Enterprise, "save", side_effect=ConnectionError("Database connection failed")):
            with pytest.raises(EnterpriseFailUpdate) as exc_info:
                EnterpriseService.update_enterprise(
                    git_owner=default_user,
                    enterprise=default_enterprise,
                    name_enterprise="New Name"
                )
            
            assert "Database connection failed" in str(exc_info.value)

    @pytest.mark.edge_cases
    def test_update_enterprise_special_chars_name(self, default_enterprise, default_user):
        special_name = "Test Enterprise @#$%^&*()_+-=[]{}|;:,.<>?/`~"
        
        result = EnterpriseService.update_enterprise(
            git_owner=default_user,
            enterprise=default_enterprise,
            name_enterprise=special_name
        )
        
        assert result.nameEnterprise == special_name

    @pytest.mark.edge_cases
    def test_update_enterprise_unicode_name(self, default_enterprise, default_user):
        unicode_name = "Test Enterprise ñáéíóú çãõ 中文 русский"
        
        result = EnterpriseService.update_enterprise(
            git_owner=default_user,
            enterprise=default_enterprise,
            name_enterprise=unicode_name
        )
        
        assert result.nameEnterprise == unicode_name

    @pytest.mark.performance
    def test_update_enterprise_performance(self, default_enterprise, default_user):
        import time
        
        start_time = time.time()
        
        result = EnterpriseService.update_enterprise(
            git_owner=default_user,
            enterprise=default_enterprise,
            name_enterprise="Performance Test Name"
        )
        
        end_time = time.time()
        total_time = end_time - start_time

        assert result.nameEnterprise == "Performance Test Name"
        assert total_time < 1.0  

    @pytest.mark.security
    def test_update_enterprise_logging_verification(self, default_enterprise, default_user, caplog):
        enterprise_id = default_enterprise.enterpriseId
        creator_gitid = default_user.gitId
        new_name = "Logged Enterprise"
        
        with caplog.at_level('INFO'):
            result = EnterpriseService.update_enterprise(
                git_owner=default_user,
                enterprise=default_enterprise,
                name_enterprise=new_name
            )
        
        assert result.nameEnterprise == new_name
      
        log_messages = [record.message for record in caplog.records if record.levelname == 'INFO']
        assert any(f"Update enterprise: {enterprise_id} by Creator: {creator_gitid}" in msg for msg in log_messages)

    @pytest.mark.security
    def test_update_enterprise_error_logging(self, default_enterprise, default_user, caplog):
        with patch.object(Enterprise, "save", side_effect=Exception("Test error")):
            with pytest.raises(EnterpriseFailUpdate):
                with caplog.at_level('ERROR'):
                    EnterpriseService.update_enterprise(
                        git_owner=default_user,
                        enterprise=default_enterprise,
                        name_enterprise="New Name"
                    )
        
        # Verify error logging
        error_messages = [record.message for record in caplog.records if record.levelname == 'ERROR']
        assert any("Error update enterprise" in msg for msg in error_messages)
        assert any(default_enterprise.enterpriseId in msg for msg in error_messages)
        assert any(default_user.gitId in msg for msg in error_messages)

   
    def test_update_nonexistent_enterprise(self, default_user):
        from taskhub.core.models import Enterprise
        
        nonexistent_enterprise = Enterprise(
            enterpriseId="nonexistent_123",
            nameEnterprise="Nonexistent Enterprise",
            owner_Id=default_user
        )

        result = EnterpriseService.update_enterprise(
            git_owner=default_user,
            enterprise=nonexistent_enterprise,
            name_enterprise="Updated Name"
        )
        
        assert result.nameEnterprise == "Updated Name"