import pytest
from unittest.mock import patch, MagicMock
from taskhub.core.services.enterprise_service import EnterpriseService
from taskhub.core.models import Enterprise, User
from taskhub.middlewares.exceptions import (
    InputEmptyOrNone,
    EnterprisePermissionDenied,
    EnterpriseFailAddedUser
)


class TestAddDevsInEnterprise:

    @pytest.mark.principal
    def test_add_multiple_devs_successful(self, default_enterprise, default_user, user_factory):
        test_users = user_factory(3)

        result = EnterpriseService.add_devs_in_enterprise(
            enterprise=default_enterprise,
            git_dev_enterprise=default_user,
            new_devs=test_users
        )

        assert len(result) == 1 + 3  
        for user in test_users:
            assert user in result
        assert default_user in result


    @pytest.mark.principal
    def test_add_single_dev_with_list(self, default_enterprise, default_user, another_user):
        result = EnterpriseService.add_devs_in_enterprise(
            enterprise=default_enterprise,
            git_dev_enterprise=default_user,
            new_devs=[another_user]
        )
        
        assert another_user in result
        assert len(result) == 2

    @pytest.mark.principal
    def test_add_single_dev_directly(self, default_enterprise, default_user, another_user):
        result = EnterpriseService.add_devs_in_enterprise(
            enterprise=default_enterprise,
            git_dev_enterprise=default_user,
            new_devs=another_user  
        )
        
        assert another_user in result
        assert len(result) == 2

    @pytest.mark.list_none
    def test_add_empty_list(self, default_enterprise, default_user):
        initial_devs = list(default_enterprise.devs_enterprise)
        
        result = EnterpriseService.add_devs_in_enterprise(
            enterprise=default_enterprise,
            git_dev_enterprise=default_user,
            new_devs=[]
        )
        
        assert result == initial_devs
        assert len(result) == 1

    def test_add_devs_already_in_enterprise(self, default_enterprise, default_user, user_factory, another_user):
        test_users = user_factory(2)
        default_enterprise.devs_enterprise.extend(test_users)
        default_enterprise.save()

        initial_devs = list(default_enterprise.devs_enterprise)

        new_user = another_user  
        result = EnterpriseService.add_devs_in_enterprise(
            enterprise=default_enterprise,
            git_dev_enterprise=default_user,
            new_devs=test_users + [new_user]
        )

        assert len(result) == len(initial_devs) + 1
        assert new_user in result
        for user in test_users:
            assert user in result


    @pytest.mark.multiple_entries_missing
    @pytest.mark.parametrize("invalid_enterprise", [
        None,
        "not_an_enterprise",
        123,
        [],
        {},
        MagicMock()
    ])
    def test_add_devs_with_invalid_enterprise_type(self, invalid_enterprise, default_user, another_user):
        with pytest.raises(InputEmptyOrNone):
            EnterpriseService.add_devs_in_enterprise(
                enterprise=invalid_enterprise,
                git_dev_enterprise=default_user,
                new_devs=another_user
            )

    @pytest.mark.enterprise_id
    @pytest.mark.fails_general
    @pytest.mark.parametrize("invalid_enterprise_id", [
        None,
        "",
        "   ",
        "\t\n\r"
    ])
    def test_add_devs_with_invalid_enterprise_id(self, invalid_enterprise_id, default_user, another_user):
        enterprise = Enterprise(enterpriseId=invalid_enterprise_id, nameEnterprise="Test")
        with pytest.raises(InputEmptyOrNone):
            EnterpriseService.add_devs_in_enterprise(
                enterprise=enterprise,
                git_dev_enterprise=default_user,
                new_devs=another_user
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
    def test_add_devs_with_invalid_performing_user_type(self, default_enterprise, invalid_user_type, another_user):
        with pytest.raises(InputEmptyOrNone):
            EnterpriseService.add_devs_in_enterprise(
                enterprise=default_enterprise,
                git_dev_enterprise=invalid_user_type,
                new_devs=another_user
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
    def test_add_devs_with_invalid_performing_user_gitid(self, default_enterprise, invalid_git_id, another_user):
        invalid_user = User(gitId=invalid_git_id, userName="Invalid User")
        with pytest.raises(InputEmptyOrNone):
            EnterpriseService.add_devs_in_enterprise(
                enterprise=default_enterprise,
                git_dev_enterprise=invalid_user,
                new_devs=another_user
            )

    @pytest.mark.git_id
    @pytest.mark.invalid_data
    def test_add_devs_with_invalid_new_users_list(self, default_enterprise, default_user):
        invalid_devs = [default_user, "not_a_user", 123]
        
        with pytest.raises(InputEmptyOrNone) as exc_info:
            EnterpriseService.add_devs_in_enterprise(
                enterprise=default_enterprise,
                git_dev_enterprise=default_user,
                new_devs=invalid_devs
            )
        
        assert "index 1" in str(exc_info.value)

    @pytest.mark.parametrize("invalid_git_id", [
        None,
        "",
        "   ",
        "\t\n\r"
    ])
    @pytest.mark.git_id
    @pytest.mark.invalid_data
    def test_add_devs_with_invalid_new_user_gitid(self, default_enterprise, default_user, invalid_git_id):
        invalid_user = User(gitId=invalid_git_id, userName="Invalid New User")
        
        with pytest.raises(InputEmptyOrNone) as exc_info:
            EnterpriseService.add_devs_in_enterprise(
                enterprise=default_enterprise,
                git_dev_enterprise=default_user,
                new_devs=[invalid_user]
            )
        
        assert "index 0" in str(exc_info.value)

    @pytest.mark.fails_permission
    def test_add_devs_without_permission(self, default_enterprise, default_user, another_user, third_user):

        with pytest.raises(EnterprisePermissionDenied) as exc_info:
            EnterpriseService.add_devs_in_enterprise(
                enterprise=default_enterprise,
                git_dev_enterprise=another_user,  
                new_devs=[third_user]
            )
        
        assert another_user.gitId in str(exc_info.value)

    @pytest.mark.handling_cases
    def test_add_devs_database_save_error(self, default_enterprise, default_user, user_factory):
        test_users = user_factory(3) 

        with patch.object(Enterprise, "save", side_effect=Exception("Database save failed")):
            with pytest.raises(EnterpriseFailAddedUser) as exc_info:
                EnterpriseService.add_devs_in_enterprise(
                    enterprise=default_enterprise,
                    git_dev_enterprise=default_user,
                    new_devs=test_users
                )

            assert "Failed to add users" in str(exc_info.value)
            assert "Database save failed" in str(exc_info.value)
            assert default_enterprise.enterpriseId in str(exc_info.value)

    @pytest.mark.handling_cases
    def test_add_devs_database_connection_error(self, default_enterprise, default_user, another_user):
        with patch.object(Enterprise, "save", side_effect=ConnectionError("Database connection failed")):
            with pytest.raises(EnterpriseFailAddedUser) as exc_info:
                EnterpriseService.add_devs_in_enterprise(
                    enterprise=default_enterprise,
                    git_dev_enterprise=default_user,
                    new_devs=[another_user]
                )
            
            assert "Database connection failed" in str(exc_info.value)

    @pytest.mark.list_none
    @pytest.mark.edge_cases
    def test_add_devs_to_enterprise_empty_dev_list(self, default_user, another_user):
        enterprise = Enterprise(
            enterpriseId="test-empty",
            nameEnterprise="Test Empty",
            owner_Id=default_user,
            devs_enterprise=[]  
        )
        
        with pytest.raises(EnterprisePermissionDenied):
            EnterpriseService.add_devs_in_enterprise(
                enterprise=enterprise,
                git_dev_enterprise=default_user,
                new_devs=[another_user]
            )

    @pytest.mark.edge_cases
    def test_add_large_number_of_devs(self, default_enterprise, default_user, user_factory):
        large_user_list = user_factory(50)
        
        result = EnterpriseService.add_devs_in_enterprise(
            enterprise=default_enterprise,
            git_dev_enterprise=default_user,
            new_devs=large_user_list
        )
        
        assert len(result) == 51  
        for user in large_user_list:
            assert user in result

    @pytest.mark.edge_cases
    def test_add_mixed_duplicate_and_new_devs(self, default_enterprise, default_user, user_factory):
        existing_users = user_factory(3)
        for user in existing_users:
            default_enterprise.devs_enterprise.append(user)
        default_enterprise.save()
        
        new_users = user_factory(2)
        result = EnterpriseService.add_devs_in_enterprise(
            enterprise=default_enterprise,
            git_dev_enterprise=default_user,
            new_devs=existing_users + new_users  
        )
        
        assert len(result) == 6  
        for user in new_users:
            assert user in result


    @pytest.mark.integration
    def test_add_devs_preserves_existing_members(self, default_enterprise, default_user, user_factory):
        initial_users = user_factory(3)
        for user in initial_users:
            default_enterprise.devs_enterprise.append(user)
        default_enterprise.save()
        
        initial_dev_count = len(default_enterprise.devs_enterprise)
        
        new_users = user_factory(2)
        result = EnterpriseService.add_devs_in_enterprise(
            enterprise=default_enterprise,
            git_dev_enterprise=default_user,
            new_devs=new_users
        )
        
        assert len(result) == initial_dev_count + 2
        for user in new_users:
            assert user in result
        for user in initial_users:
            assert user in result
        assert default_user in result

    # # ---------------------------
    # # PERFORMANCE TESTS
    # # ---------------------------

    @pytest.mark.performance
    def test_add_many_devs_performance(self, default_enterprise, default_user, user_factory):
        import time
        test_users = user_factory(100)
        start_time = time.time()
        
        result = EnterpriseService.add_devs_in_enterprise(
            enterprise=default_enterprise,
            git_dev_enterprise=default_user,
            new_devs=test_users
        )
        
        end_time = time.time()
        total_time = end_time - start_time

        assert total_time < 2.0  
        assert len(result) == 101  
    

    @pytest.mark.security
    def test_add_devs_with_malicious_input(self, default_enterprise, default_user, user_factory):
        
        malicious_users = [
            User(gitId="'; DROP TABLE users; --", email="test@email1.com", userName="SQL Injection"),
            User(gitId="<script>alert('xss')</script>", email="test@email2.com", userName="XSS Attempt"),
            User(gitId="../etc/passwd", email="test@email3.com", userName="Path Traversal")
        ]
        for user in malicious_users:
            user.save()
 
        result = EnterpriseService.add_devs_in_enterprise(
            enterprise=default_enterprise,
            git_dev_enterprise=default_user,
            new_devs=malicious_users
        )
        
        for user in malicious_users:
            assert user in result
        assert len(default_enterprise.devs_enterprise) == 1 + len(malicious_users)