import pytest
import uuid
from unittest.mock import patch, MagicMock
from taskhub.core.services.enterprise_service import EnterpriseService
from taskhub.core.models import Enterprise, User
from taskhub.middlewares.exceptions import (
    InputEmptyOrNone,
    InputExceededCharacterLimit,
    EnterpriseAlreadyExists,
    EnterpriseFailCreate
)


class TestCreateEnterprise:
    @pytest.mark.principal
    def test_create_enterprise_successful(self, default_user):
        enterprise = EnterpriseService.create_enterprise(
            git_owner=default_user,
            name_enterprise="My Enterprise"
        )

        assert enterprise is not None
        assert enterprise.owner_Id == default_user
        assert enterprise.nameEnterprise == "My Enterprise"
        assert enterprise.enterpriseId is not None
        assert len(enterprise.enterpriseId) == 36  
        assert default_user in enterprise.devs_enterprise
        assert enterprise.gitId_enterprise is None  

        saved = Enterprise.objects(nameEnterprise="My Enterprise").first()
        assert saved is not None
        assert saved.enterpriseId == enterprise.enterpriseId

    @pytest.mark.integration
    def test_create_enterprise_with_custom_id(self, default_user):
        custom_id = "custom_enterprise_id_123"
        enterprise = EnterpriseService.create_enterprise(
            git_owner=default_user,
            name_enterprise="Enterprise Custom",
            git_enterprise_id=custom_id
        )

        assert enterprise.enterpriseId == custom_id
        assert enterprise.gitId_enterprise == custom_id
        assert enterprise.nameEnterprise == "Enterprise Custom"

    @pytest.mark.edge_cases
    def test_create_enterprise_with_minimal_name_length(self, default_user):
        minimal_name = "A"  
        enterprise = EnterpriseService.create_enterprise(
            git_owner=default_user,
            name_enterprise=minimal_name
        )
        assert enterprise.nameEnterprise == minimal_name

    @pytest.mark.edge_cases
    def test_create_enterprise_with_maximum_name_length(self, default_user):
        max_name = "A" * 100  
        enterprise = EnterpriseService.create_enterprise(
            git_owner=default_user,
            name_enterprise=max_name
        )
        assert enterprise.nameEnterprise == max_name
        assert len(enterprise.nameEnterprise) == 100

    @pytest.mark.integration
    def test_create_enterprise_with_special_characters_name(self, default_user):
        enterprise = EnterpriseService.create_enterprise(
            git_owner=default_user,
            name_enterprise="Enterprise @#$%&*() 123"
        )
        assert enterprise.nameEnterprise == "Enterprise @#$%&*() 123"

    @pytest.mark.integration
    def test_create_enterprise_with_unicode_characters(self, default_user):
        enterprise = EnterpriseService.create_enterprise(
            git_owner=default_user,
            name_enterprise="Empresa Español ñáéíóú 中文"
        )
        assert enterprise.nameEnterprise == "Empresa Español ñáéíóú 中文"

    @pytest.mark.parametrize("invalid_owner", [
        None,
        "not_a_user",
        123,
        [],
        {},
        MagicMock()  
    ])
    def test_create_enterprise_with_invalid_owner_type(self, invalid_owner):
        with pytest.raises(InputEmptyOrNone):
            EnterpriseService.create_enterprise(
                git_owner=invalid_owner,
                name_enterprise="Test Enterprise"
            )

    @pytest.mark.parametrize("invalid_git_id", [
        None,
        "",
        "   ",
        "\t\n\r"
    ])
    def test_create_enterprise_with_invalid_git_id(self, invalid_git_id):
        user = User(gitId=invalid_git_id, userName="Test User")
        with pytest.raises(InputEmptyOrNone):
            EnterpriseService.create_enterprise(user, "Test Enterprise")

    def test_create_enterprise_with_none_git_id_attribute(self):

        user = User(userName="Test User")

        if hasattr(user, 'gitId'):
            delattr(user, 'gitId')
        with pytest.raises(InputEmptyOrNone):
            EnterpriseService.create_enterprise(user, "Test Enterprise")

    @pytest.mark.parametrize("invalid_name", [
        None,
        "",
        "   ",
        "\t\n\r"
    ])
    def test_create_enterprise_with_empty_name(self, default_user, invalid_name):
        with pytest.raises(InputEmptyOrNone):
            EnterpriseService.create_enterprise(default_user, invalid_name)

    def test_create_enterprise_with_name_too_long(self, default_user):
        long_name = "A" * 101  
        with pytest.raises(InputExceededCharacterLimit) as exc_info:
            EnterpriseService.create_enterprise(default_user, long_name)
        
        assert "101" in str(exc_info.value)

    @pytest.mark.fails_general
    def test_create_enterprise_already_exists(self, default_user):
     
        EnterpriseService.create_enterprise(default_user, "Duplicate Enterprise")
        
        with pytest.raises(EnterpriseAlreadyExists) as exc_info:
            EnterpriseService.create_enterprise(default_user, "Duplicate Enterprise")
        
        assert "Duplicate Enterprise" in str(exc_info.value)

    @pytest.mark.fails
    @pytest.mark.parametrize("mock_target,side_effect,expected_error", [
        ("uuid.uuid4", Exception("UUID generation failed"), "UUID generation failed"),
        ("taskhub.core.services.enterprise_service.Enterprise.save", 
         Exception("DB error"), "DB error")
    ])
    def test_create_enterprise_unexpected_errors(self, default_user, mock_target, side_effect, expected_error):
        with patch(mock_target, side_effect=side_effect):
            with pytest.raises(EnterpriseFailCreate) as exc_info:
                EnterpriseService.create_enterprise(default_user, "Test Enterprise")
            
            assert expected_error in str(exc_info.value)


    @pytest.mark.fails_general
    def test_create_enterprise_database_connection_error(self, default_user):
        with patch.object(Enterprise, "save", side_effect=ConnectionError("Database connection failed")):
            with pytest.raises(EnterpriseFailCreate) as exc_info:
                EnterpriseService.create_enterprise(default_user, "Test Enterprise")
            
            assert "Database connection failed" in str(exc_info.value)


    @pytest.mark.integration 
    def test_create_enterprise_data_integrity(self, default_user):
        enterprise_name = "Integrity Test Enterprise"
        enterprise = EnterpriseService.create_enterprise(
            git_owner=default_user,
            name_enterprise=enterprise_name
        )

        assert enterprise.nameEnterprise == enterprise_name
        assert enterprise.owner_Id == default_user
        assert default_user in enterprise.devs_enterprise
        assert len(enterprise.devs_enterprise) == 1
        assert isinstance(enterprise.enterpriseId, str)
        assert len(enterprise.enterpriseId) == 36  
        assert enterprise.gitId_enterprise is None
        assert enterprise.created_at is not None
        assert enterprise.updated_at is not None

    @pytest.mark.integration
    def test_create_multiple_enterprises_same_owner(self, default_user):
        enterprise1 = EnterpriseService.create_enterprise(
            git_owner=default_user,
            name_enterprise="Enterprise 1"
        )
        
        enterprise2 = EnterpriseService.create_enterprise(
            git_owner=default_user,
            name_enterprise="Enterprise 2"
        )
        
        assert enterprise1.owner_Id == default_user
        assert enterprise2.owner_Id == default_user
        assert enterprise1.nameEnterprise != enterprise2.nameEnterprise
        assert enterprise1.enterpriseId != enterprise2.enterpriseId

    @pytest.mark.enterprise_id
    def test_create_enterprise_with_very_long_custom_id(self, default_user):
        long_custom_id = "x" * 100  
        enterprise = EnterpriseService.create_enterprise(
            git_owner=default_user,
            name_enterprise="Long ID Enterprise",
            git_enterprise_id=long_custom_id
        )
        
        assert enterprise.enterpriseId == long_custom_id
        assert enterprise.gitId_enterprise == long_custom_id

    @pytest.mark.enterprise_id
    def test_create_enterprise_with_numeric_custom_id(self, default_user):
        numeric_id = "1234567890"
        enterprise = EnterpriseService.create_enterprise(
            git_owner=default_user,
            name_enterprise="Numeric ID Enterprise",
            git_enterprise_id=numeric_id
        )
        
        assert enterprise.enterpriseId == numeric_id
        assert enterprise.gitId_enterprise == numeric_id

    @pytest.mark.enterprise_id
    def test_create_enterprise_with_special_characters_custom_id(self, default_user):
        special_id = "custom-id_123@test.com"
        enterprise = EnterpriseService.create_enterprise(
            git_owner=default_user,
            name_enterprise="Special ID Enterprise",
            git_enterprise_id=special_id
        )
        
        assert enterprise.enterpriseId == special_id
        assert enterprise.gitId_enterprise == special_id

    @pytest.mark.performance
    def test_create_multiple_enterprises_performance(self, default_user):
        import time
        
        start_time = time.time()
        
        for i in range(10):  
            EnterpriseService.create_enterprise(
                git_owner=default_user,
                name_enterprise=f"Performance Test {i}"
            )
        
        end_time = time.time()
        total_time = end_time - start_time
        
        assert total_time < 5.0  

    @pytest.mark.security
    def test_create_enterprise_with_sql_injection_attempt(self, default_user):
        malicious_name = "Test'; DROP TABLE enterprises; --"
        
        enterprise = EnterpriseService.create_enterprise(
            git_owner=default_user,
            name_enterprise=malicious_name
        )
        
        assert enterprise.nameEnterprise == malicious_name
        saved = Enterprise.objects(nameEnterprise=malicious_name).first()
        assert saved is not None

    @pytest.mark.security
    def test_create_enterprise_with_xss_attempt(self, default_user):
        xss_name = "<script>alert('xss')</script>"
        
        enterprise = EnterpriseService.create_enterprise(
            git_owner=default_user,
            name_enterprise=xss_name
        )
        
        assert enterprise.nameEnterprise == xss_name
