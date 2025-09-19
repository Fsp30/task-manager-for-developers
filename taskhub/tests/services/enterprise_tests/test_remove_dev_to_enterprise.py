import pytest
from unittest.mock import patch, MagicMock
from taskhub.core.services.enterprise_service import EnterpriseService
from taskhub.core.models import Enterprise, User
from taskhub.middlewares.exceptions import (
    InputEmptyOrNone,
    EnterprisePermissionDenied,
    EnterpriseFailRemoveUser
)


class TestRemoveDevToEnterprise:

    @pytest.mark.principal
    def test_remove_multiple_devs_successful(self, default_enterprise, default_user, user_factory):
        test_users = user_factory(3)
        default_enterprise.devs_enterprise.extend(test_users)
        default_enterprise.save()

        initial_dev_count = len(default_enterprise.devs_enterprise)

        devs_to_remove = test_users[:2]
        
        result = EnterpriseService.remove_dev_to_enterprise(
            enterprise=default_enterprise,
            creator_enterprise=default_user,
            devs_remove=devs_to_remove
        )

        assert len(result) == initial_dev_count - 2
        for user in devs_to_remove:
            assert user not in result
        assert default_user in result

    @pytest.mark.principal
    def test_remove_single_dev_with_list(self, default_enterprise, default_user, another_user):
        default_enterprise.devs_enterprise.append(another_user)
        default_enterprise.save()

        result = EnterpriseService.remove_dev_to_enterprise(
            enterprise=default_enterprise,
            creator_enterprise=default_user,
            devs_remove=[another_user]
        )
        
        assert another_user not in result
        assert len(result) == 1  
        assert default_user in result

    @pytest.mark.principal
    def test_remove_single_dev_directly(self, default_enterprise, default_user, another_user):

        default_enterprise.devs_enterprise.append(another_user)
        default_enterprise.save()

        result = EnterpriseService.remove_dev_to_enterprise(
            enterprise=default_enterprise,
            creator_enterprise=default_user,
            devs_remove=another_user 
        )
        
        assert another_user not in result
        assert len(result) == 1
        assert default_user in result

    @pytest.mark.list_none
    def test_remove_empty_list(self, default_enterprise, default_user):
        initial_devs = list(default_enterprise.devs_enterprise)
        
        result = EnterpriseService.remove_dev_to_enterprise(
            enterprise=default_enterprise,
            creator_enterprise=default_user,
            devs_remove=[]
        )
        
        assert result == initial_devs
        assert len(result) == 1 

    @pytest.mark.list_none
    def test_remove_none_devs(self, default_enterprise, default_user):
        initial_devs = list(default_enterprise.devs_enterprise)
        
        result = EnterpriseService.remove_dev_to_enterprise(
            enterprise=default_enterprise,
            creator_enterprise=default_user,
            devs_remove=None
        )
        
        assert result == initial_devs
        assert len(result) == 1

    @pytest.mark.edge_cases
    def test_remove_devs_not_in_enterprise(self, default_enterprise, default_user, user_factory):
        external_users = user_factory(2)
        initial_devs = list(default_enterprise.devs_enterprise)

        result = EnterpriseService.remove_dev_to_enterprise(
            enterprise=default_enterprise,
            creator_enterprise=default_user,
            devs_remove=external_users
        )

        assert result == initial_devs
        assert len(result) == 1

    @pytest.mark.fails_permission
    def test_remove_devs_without_permission(self, default_enterprise, default_user, another_user, third_user):
        default_enterprise.devs_enterprise.append(another_user)
        default_enterprise.save()

        with pytest.raises(EnterprisePermissionDenied) as exc_info:
            EnterpriseService.remove_dev_to_enterprise(
                enterprise=default_enterprise,
                creator_enterprise=another_user,  
                devs_remove=[third_user]
            )
        
        assert another_user.gitId in str(exc_info.value)

    @pytest.mark.fails_general
    def test_remove_creator_itself(self, default_enterprise, default_user):
        with pytest.raises(EnterpriseFailRemoveUser) as exc_info:
            EnterpriseService.remove_dev_to_enterprise(
                enterprise=default_enterprise,
                creator_enterprise=default_user,
                devs_remove=default_user 
            )
        
        assert "can't delete the creator" in str(exc_info.value).lower()

    @pytest.mark.multiple_entries_missing
    @pytest.mark.parametrize("invalid_enterprise", [
        None,
        "not_an_enterprise",
        123,
        [],
        {},
        MagicMock()
    ])
    def test_remove_devs_with_invalid_enterprise_type(self, invalid_enterprise, default_user, another_user):
        with pytest.raises(InputEmptyOrNone):
            EnterpriseService.remove_dev_to_enterprise(
                enterprise=invalid_enterprise,
                creator_enterprise=default_user,
                devs_remove=another_user
            )

    @pytest.mark.enterprise_id
    @pytest.mark.fails_general
    @pytest.mark.parametrize("invalid_enterprise_id", [
        None,
        "",
        "   ",
        "\t\n\r"
    ])
    def test_remove_devs_with_invalid_enterprise_id(self, invalid_enterprise_id, default_user, another_user):
        enterprise = Enterprise(enterpriseId=invalid_enterprise_id, nameEnterprise="Test")
        with pytest.raises(InputEmptyOrNone):
            EnterpriseService.remove_dev_to_enterprise(
                enterprise=enterprise,
                creator_enterprise=default_user,
                devs_remove=another_user
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
    def test_remove_devs_with_invalid_creator_type(self, default_enterprise, invalid_user_type, another_user):
        with pytest.raises(InputEmptyOrNone):
            EnterpriseService.remove_dev_to_enterprise(
                enterprise=default_enterprise,
                creator_enterprise=invalid_user_type,
                devs_remove=another_user
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
    def test_remove_devs_with_invalid_creator_gitid(self, default_enterprise, invalid_git_id, another_user):
        invalid_user = User(gitId=invalid_git_id, userName="Invalid User")
        with pytest.raises(InputEmptyOrNone):
            EnterpriseService.remove_dev_to_enterprise(
                enterprise=default_enterprise,
                creator_enterprise=invalid_user,
                devs_remove=another_user
            )

    @pytest.mark.git_id
    @pytest.mark.invalid_data
    def test_remove_devs_with_invalid_devs_list(self, default_enterprise, default_user):
        invalid_devs = [default_user, "not_a_user", 123]
        
        with pytest.raises(InputEmptyOrNone) as exc_info:
            EnterpriseService.remove_dev_to_enterprise(
                enterprise=default_enterprise,
                creator_enterprise=default_user,
                devs_remove=invalid_devs
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
    def test_remove_devs_with_invalid_dev_gitid(self, default_enterprise, default_user, invalid_git_id):
        invalid_user = User(gitId=invalid_git_id, userName="Invalid Dev User")
        
        with pytest.raises(InputEmptyOrNone) as exc_info:
            EnterpriseService.remove_dev_to_enterprise(
                enterprise=default_enterprise,
                creator_enterprise=default_user,
                devs_remove=[invalid_user]
            )
        
        assert "index 0" in str(exc_info.value)

   
    @pytest.mark.handling_cases
    def test_remove_devs_database_save_error(self, default_enterprise, default_user, user_factory):
        test_users = user_factory(2)
        default_enterprise.devs_enterprise.extend(test_users)
        default_enterprise.save()

        with patch.object(Enterprise, "save", side_effect=Exception("Database save failed")):
            with pytest.raises(EnterpriseFailRemoveUser) as exc_info:
                EnterpriseService.remove_dev_to_enterprise(
                    enterprise=default_enterprise,
                    creator_enterprise=default_user,
                    devs_remove=test_users
                )

            assert "Failed remove dev(s)" in str(exc_info.value)
            assert "Database save failed" in str(exc_info.value)
            assert default_enterprise.enterpriseId in str(exc_info.value)

   
    @pytest.mark.handling_cases
    def test_remove_devs_database_connection_error(self, default_enterprise, default_user, another_user):
        default_enterprise.devs_enterprise.append(another_user)
        default_enterprise.save()

        with patch.object(Enterprise, "save", side_effect=ConnectionError("Database connection failed")):
            with pytest.raises(EnterpriseFailRemoveUser) as exc_info:
                EnterpriseService.remove_dev_to_enterprise(
                    enterprise=default_enterprise,
                    creator_enterprise=default_user,
                    devs_remove=[another_user]
                )
            
            assert "Database connection failed" in str(exc_info.value)

   
    @pytest.mark.edge_cases
    def test_remove_all_devs_except_owner(self, default_enterprise, default_user, user_factory):
        test_users = user_factory(5)
        default_enterprise.devs_enterprise.extend(test_users)
        default_enterprise.save()

        result = EnterpriseService.remove_dev_to_enterprise(
            enterprise=default_enterprise,
            creator_enterprise=default_user,
            devs_remove=test_users
        )

        assert len(result) == 1  
        assert default_user in result
        for user in test_users:
            assert user not in result

    @pytest.mark.performance
    def test_remove_many_devs_performance(self, default_enterprise, default_user, user_factory):
        import time
        test_users = user_factory(50)
        default_enterprise.devs_enterprise.extend(test_users)
        default_enterprise.save()

        start_time = time.time()
        
        result = EnterpriseService.remove_dev_to_enterprise(
            enterprise=default_enterprise,
            creator_enterprise=default_user,
            devs_remove=test_users
        )
        
        end_time = time.time()
        total_time = end_time - start_time

        assert total_time < 2.0
        assert len(result) == 1  

    @pytest.mark.security
    def test_remove_devs_with_malicious_input(self, default_enterprise, default_user):
        malicious_user = User(
            gitId="'; DROP TABLE users; --", 
            email="malicious@test.com", 
            userName="SQL Injection"
        )
        malicious_user.save()

        default_enterprise.devs_enterprise.append(malicious_user)
        default_enterprise.save()

        result = EnterpriseService.remove_dev_to_enterprise(
            enterprise=default_enterprise,
            creator_enterprise=default_user,
            devs_remove=[malicious_user]
        )
        
        assert malicious_user not in result
        assert len(result) == 1
        malicious_user.delete()

    @pytest.mark.integration
    def test_remove_devs_preserves_remaining_members(self, default_enterprise, default_user, user_factory):
        all_users = user_factory(5)
        default_enterprise.devs_enterprise.extend(all_users)
        default_enterprise.save()

        users_to_remove = all_users[:2]
        users_to_keep = all_users[2:] + [default_user]

        result = EnterpriseService.remove_dev_to_enterprise(
            enterprise=default_enterprise,
            creator_enterprise=default_user,
            devs_remove=users_to_remove
        )

        assert len(result) == len(users_to_keep)
        for user in users_to_remove:
            assert user not in result
        for user in users_to_keep:
            assert user in result