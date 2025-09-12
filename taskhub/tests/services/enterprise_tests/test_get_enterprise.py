import pytest
from unittest.mock import patch, MagicMock
from taskhub.core.services.enterprise_service import EnterpriseService
from taskhub.core.models import Enterprise, User, Repository
from taskhub.middlewares.exceptions import (
    EnterpriseNotFound,
    EnterpriseFailDetail,
    UserFailList,
    RepositoryFailList,
    InputEmptyOrNone
)

# ---------------------------
# TESTES PARA get_enterprise
# ---------------------------
class TestToGetEnterprise:
        @pytest.mark.principal
        @pytest.mark.enterprise_id
        def test_get_enterprise_successful(self, default_enterprise):
            enterprise = EnterpriseService.get_enterprise(default_enterprise.enterpriseId)
            
            assert enterprise is not None
            assert enterprise.enterpriseId == default_enterprise.enterpriseId
            assert enterprise.nameEnterprise == default_enterprise.nameEnterprise
            assert enterprise.owner_Id == default_enterprise.owner_Id


        @pytest.mark.fails
        @pytest.mark.not_found
        @pytest.mark.enterprise_id
        def test_get_enterprise_not_found(self):
            with pytest.raises(EnterpriseNotFound):
                    EnterpriseService.get_enterprise("non_existent_enterprise")


        @pytest.mark.fails
        @pytest.mark.fails_general
        def test_get_enterprise_database_error(self, mocker):
            mocker.patch("taskhub.core.models.enterprise.Enterprise.objects", side_effect=Exception("DB error"))
            
            with pytest.raises(EnterpriseFailDetail):
                EnterpriseService.get_enterprise("test_enterprise")


        @pytest.mark.enterprise_id
        @pytest.mark.whitespace
        def test_get_enterprise_with_whitespace_id(self):
            with pytest.raises(InputEmptyOrNone):
                    EnterpriseService.get_enterprise("   ")
            
            with pytest.raises(InputEmptyOrNone):
                    EnterpriseService.get_enterprise("")


        @pytest.mark.enterprise_id
        @pytest.mark.multiple_entries_missing
        def test_get_enterprise_none_empty_id(self):
            with pytest.raises(InputEmptyOrNone):
                    EnterpriseService.get_enterprise(None)



        @pytest.mark.enterprise_id
        def test_get_enterprise_with_special_characters_id(self, enterprise_special_chars):
            enterprise = EnterpriseService.get_enterprise(enterprise_special_chars.enterpriseId)
            
            assert enterprise is not None
            assert enterprise.enterpriseId == enterprise_special_chars.enterpriseId


        @pytest.mark.now
        @pytest.mark.enterprise_id
        def test_get_enterprise_with_long_id(self, enterprise_long_id):
            enterprise = EnterpriseService.get_enterprise(enterprise_long_id.enterpriseId)
            
            assert enterprise is not None
            assert enterprise.enterpriseId == enterprise_long_id.enterpriseId



