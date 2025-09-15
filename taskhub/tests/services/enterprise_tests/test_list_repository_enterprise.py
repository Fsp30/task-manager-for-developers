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
class TestListRepostoryEnterprise:
        @pytest.mark.principal
        @pytest.mark.integration
        def test_list_repositories_enterprise_successful(self, enterprise_with_repositories):
            repos = EnterpriseService.list_repositories_enterprise(enterprise_with_repositories.enterpriseId)
        
            assert repos is not None
            assert len(repos) == 2

            repo_ids = [repo.repository_id for repo in repos]
            assert "repo_enterprise_1" in repo_ids
            assert "repo_enterprise_2" in repo_ids


        @pytest.mark.principal
        @pytest.mark.list_none
        def test_list_repositories_enterprise_empty_list(self, default_enterprise):

            repos = EnterpriseService.list_repositories_enterprise(default_enterprise.enterpriseId)
        
            assert repos == []


        @pytest.mark.fails
        @pytest.mark.not_found
        def test_list_repositories_enterprise_not_found(self):
            with pytest.raises(EnterpriseNotFound):
                EnterpriseService.list_repositories_enterprise("non_existent_enterprise")


        @pytest.mark.fails
        @pytest.mark.fails_general
        def test_list_repositories_enterprise_database_error(self, mocker , default_enterprise):
            mocker.patch('taskhub.core.services.enterprise_service.EnterpriseService.get_enterprise', side_effect=Exception("Database error"))
        
            with pytest.raises(RepositoryFailList):
                EnterpriseService.list_repositories_enterprise(default_enterprise.enterpriseId)


        @pytest.mark.fails
        @pytest.mark.fails_general
        def test_list_repositories_enterprise_get_enterprise_fails(self, mocker):

            with mocker.patch('taskhub.core.services.enterprise_service.EnterpriseService.get_enterprise',side_effect=Exception("Get enterprise failed")): 
                with pytest.raises(RepositoryFailList):       
                    EnterpriseService.list_repositories_enterprise("test_enterprise")
                    

        @pytest.mark.integration
        def test_list_repositories_enterprise_large_number_of_repos(self ,enterprise_many_repos):
            repos = EnterpriseService.list_repositories_enterprise(enterprise_many_repos.enterpriseId)
        
            assert len(repos) == 100  
