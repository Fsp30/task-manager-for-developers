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

class TestListDevsEnterprise:
        @pytest.mark.principal
        @pytest.mark.integration
        def test_list_devs_enterprise_successful(self, default_enterprise_with_devs):
            devs = EnterpriseService.list_devs_enterprise(default_enterprise_with_devs.enterpriseId)
        
            assert devs is not None
            assert len(devs) == 3  
            dev_ids = [dev.gitId for dev in devs]
            assert default_enterprise_with_devs.owner_Id.gitId in dev_ids


        @pytest.mark.principal
        @pytest.mark.list_none
        def test_list_devs_enterprise_empty_with_only_the_owner(self, default_enterprise):
            devs = EnterpriseService.list_devs_enterprise(default_enterprise.enterpriseId)
        
            assert len(devs) == 1  


        @pytest.mark.fails
        @pytest.mark.not_found
        def test_list_devs_enterprise_not_found(self):
            with pytest.raises(EnterpriseNotFound):
                EnterpriseService.list_devs_enterprise("non_existent_enterprise")

        
        @pytest.mark.enterprise_id
        @pytest.mark.whitespace
        def test_list_devs_enterprise_with_whitespace_id(self):
            with pytest.raises(InputEmptyOrNone):
                    EnterpriseService.list_devs_enterprise("   ")
            
            with pytest.raises(InputEmptyOrNone):
                    EnterpriseService.list_devs_enterprise("")

        @pytest.mark.enterprise_id
        @pytest.mark.multiple_entries_missing
        def test_list_devs_enterprise_none_empty_id(self):
            with pytest.raises(InputEmptyOrNone):
                    EnterpriseService.list_devs_enterprise(None)



        @pytest.mark.enterprise_id
        def test_list_devs_enterprise_with_special_characters_id(self, enterprise_special_chars):
            devs = EnterpriseService.list_devs_enterprise(enterprise_special_chars.enterpriseId)

            assert len(devs) == 1
            
        @pytest.mark.enterprise_id
        def test_get_enterprise_with_long_id(self, enterprise_long_id):
            devs = EnterpriseService.list_devs_enterprise(enterprise_long_id.enterpriseId)
            
            assert len(devs) == 1
            

        @pytest.mark.fails
        @pytest.mark.fails_general
        def test_list_devs_enterprise_database_error(self,mocker , default_enterprise):
              
                mocker.patch("taskhub.core.models.enterprise.Enterprise.objects", side_effect=Exception("Database error"))
                with pytest.raises(UserFailList):
                        EnterpriseService.list_devs_enterprise(default_enterprise.enterpriseId)
        
                
        @pytest.mark.fails
        @pytest.mark.fails_general
        def test_list_devs_enterprise_get_enterprise_fails(self):
            
            with patch('taskhub.core.services.enterprise_service.EnterpriseService.get_enterprise', 
                       side_effect=Exception("Get enterprise failed")):
                with pytest.raises(UserFailList):
                    EnterpriseService.list_devs_enterprise("test_enterprise")

        @pytest.mark.integration
        def test_list_devs_enterprise_large_number_of_devs(self, enterprise_many_devs):
            devs = EnterpriseService.list_devs_enterprise(enterprise_many_devs.enterpriseId)
        
            assert len(devs) == 51 
