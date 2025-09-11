import pytest
import datetime
from unittest.mock import patch, MagicMock
from taskhub.core.services.content_repository_service import ContentRepositoryService
from taskhub.core.services.repository_service import RepositoryService
from taskhub.core.models import Repository, User, Enterprise
from taskhub.middlewares.exceptions import (
    InputEmptyOrNone,
    RepositoryAlreadyExists,
    RepositoryFailCreate,
    EnterprisePermissionDenied,
    RepositoryPermissionFailCreate,
    ContentRepositoryFailCreate,
    RepositoryPermissionFailAddedUser,
    InputExceededCharacterLimit
)

# ---------------------------
# FLUXOS FELIZES
# ---------------------------
class TestCreateRepostory:
    @pytest.mark.principal
    @pytest.mark.repository_id
    @pytest.mark.creator_id
    @pytest.mark.timestamp
    def test_create_repository_successful(self,default_user):
        repo = RepositoryService.create_repository(
            repository_id="repo001",
            git_creator=default_user
        )

        assert repo is not None
        assert repo.repository_id == "repo001"
        assert repo.creator_Id == default_user
        assert isinstance(repo.created_at, datetime.datetime)
        assert isinstance(repo.updated_at, datetime.datetime)

        saved = Repository.objects(repository_id="repo001").first()
        assert saved is not None
        assert saved.creator_Id == default_user


    @pytest.mark.integration
    @pytest.mark.principal
    def test_create_repository_with_enterprise(self,default_user):
        enterprise = Enterprise(
            owner_Id=default_user,
            enterpriseId= "enterprise_Id",
            nameEnterprise="Test Enterprise",
        )
        enterprise.save()

        repo = RepositoryService.create_repository(
            repository_id="repo002",
            git_creator=default_user,
            enterprise=enterprise
        )

        assert repo.enterpriseId == enterprise
        saved = Repository.objects(repository_id="repo002").first()
        assert saved.enterpriseId == enterprise

    @pytest.mark.integration
    @pytest.mark.principal
    def test_create_repository_with_admin_users(self,default_user):
        extra_users = []
        for i in range(2):
            user = User(gitId=f"extra{i}", email=f"extra{i}@example.com", userName=f"Extra {i}")
            user.save()
            extra_users.append(user)

        repo = RepositoryService.create_repository(
            repository_id="repo003",
            git_creator=default_user,
            admin_users=extra_users
        )
        repo.save()

        assert repo is not None
        assert len(repo.admin_repository.admin_users) == 1 + len(extra_users)
        for user in extra_users:
            assert any(a.gitId == user.gitId for a in repo.admin_repository.admin_users)


    @pytest.mark.multiple_entries_missing
    @pytest.mark.fails
    @pytest.mark.repository_id
    @pytest.mark.creator_id
    def test_create_repository_input_empty(self,default_user):

        with pytest.raises(InputEmptyOrNone):
            RepositoryService.create_repository("repo004", "")

        with pytest.raises(InputEmptyOrNone):
            RepositoryService.create_repository("repo004", " ")
        
        with pytest.raises(InputEmptyOrNone):
            RepositoryService.create_repository("repo004", "  ")
        
        with pytest.raises(InputEmptyOrNone):
            RepositoryService.create_repository("", default_user)
        
        with pytest.raises(InputEmptyOrNone):
            RepositoryService.create_repository(" ", default_user)
        
        with pytest.raises(InputEmptyOrNone):
            RepositoryService.create_repository("  ", default_user)

        with pytest.raises(InputEmptyOrNone):
            RepositoryService.create_repository("", None)
        with pytest.raises(InputEmptyOrNone):
            RepositoryService.create_repository(" ", None)
        with pytest.raises(InputEmptyOrNone):
            RepositoryService.create_repository("  ", None)

    @pytest.mark.repository_id
    @pytest.mark.fails
    def test_create_repository_already_exists(self, default_repository, default_user):
        with pytest.raises(RepositoryAlreadyExists):
            RepositoryService.create_repository(default_repository.repository_id, default_user)

    @pytest.mark.fails
    @pytest.mark.fails_general
    def test_create_repository_unexpected_error(self, default_user):
        with patch.object(ContentRepositoryService, "create_content_repository", side_effect=Exception("Unexpected")):
            with pytest.raises(RepositoryFailCreate):
                RepositoryService.create_repository("repo007",default_user)

    @pytest.mark.fails
    @pytest.mark.creator_id
    @pytest.mark.multiple_entries_missing
    def test_create_repository_with_invalid_creator(self):
        with pytest.raises(InputEmptyOrNone):
            RepositoryService.create_repository("repo008", None)

    @pytest.mark.fails
    @pytest.mark.git_id
    @pytest.mark.creator_id
    def test_create_repository_with_creator_missing_gitId(self, default_user):
        invalid_user = User(userName="Invalid User")
        
        with pytest.raises(InputEmptyOrNone):
            RepositoryService.create_repository("repo009", invalid_user)

    @pytest.mark.fails
    @pytest.mark.git_id
    @pytest.mark.whitespace
    def test_create_repository_with_creator_empty_gitId(default_user):
        invalid_user = User(gitId="", userName="Invalid User")
        
        with pytest.raises(InputEmptyOrNone):
            RepositoryService.create_repository("repo010", invalid_user)

    @pytest.mark.fails
    @pytest.mark.git_id
    @pytest.mark.whitespace
    def test_create_repository_with_creator_whitespace_gitId(default_user):
        invalid_user = User(gitId="   ", userName="Invalid User")
        
        with pytest.raises(InputEmptyOrNone):
            RepositoryService.create_repository("repo011", invalid_user)

    @pytest.mark.fails
    @pytest.mark.unauthorized
    @pytest.mark.integration
    def test_create_repository_with_enterprise_permission_denied(self, default_user):
        other_owner=User(gitId="other_owner", email="owner@example.com", userName="Owner")
        other_owner.save()
        enterprise = Enterprise(
            owner_Id=other_owner,
            enterpriseId="enterprise002",
            nameEnterprise="Test Enterprise 2"
        )
        enterprise.save()
        
        with pytest.raises(EnterprisePermissionDenied):
            RepositoryService.create_repository(
                repository_id="repo012",
                git_creator=default_user,
                enterprise=enterprise
            )

    @pytest.mark.integration
    @pytest.mark.principal
    def test_create_repository_with_enterprise_dev_user(self, default_user):
        other_owner = User(gitId="other_owner", email="owner@example.com", userName="Owner")
        other_owner.save()
        
        enterprise = Enterprise(
            owner_Id=other_owner,
            enterpriseId="enterprise003",
            nameEnterprise="Test Enterprise 3",
            devs_enterprise=[default_user]
        )
        enterprise.save()
        
        repo = RepositoryService.create_repository(
            repository_id="repo013",
            git_creator=default_user,
            enterprise=enterprise
        )
        
        assert repo.enterpriseId == enterprise
        assert repo.creator_Id == default_user

    @pytest.mark.fails
    @pytest.mark.fails_permission
    def test_create_repository_permission_service_fails(self ,default_user):
        with patch('taskhub.core.services.repository_permission_service.PermissionsService.create_repository_permission', 
                side_effect=RepositoryPermissionFailCreate("Permission failed")):
            with pytest.raises(RepositoryPermissionFailCreate):
                RepositoryService.create_repository("repo014", default_user)

    @pytest.mark.fails
    @pytest.mark.fails_content
    def test_create_repository_content_service_fails(self, default_user):
        with patch('taskhub.core.services.content_repository_service.ContentRepositoryService.create_content_repository', 
                side_effect=ContentRepositoryFailCreate("Content failed")):
            with pytest.raises(ContentRepositoryFailCreate):
                RepositoryService.create_repository("repo015", default_user)

    @pytest.mark.fails
    @pytest.mark.fails_permission
    def test_create_repository_add_admin_user_fails(self,default_user):
        admin_user = User(gitId="admin_user", email="admin@example.com", userName="Admin User")
        admin_user.save()
        
        with patch('taskhub.core.services.repository_permission_service.PermissionsService.add_dev_permission', 
                side_effect=RepositoryPermissionFailAddedUser("Add admin failed")):
            with pytest.raises(RepositoryPermissionFailAddedUser):
                RepositoryService.create_repository(
                    repository_id="repo016",
                    git_creator=default_user,
                    admin_users=[admin_user]
                )

    @pytest.mark.fails
    @pytest.mark.repository_id
    def test_create_repository_concurrent_creation(self, default_user):
        def mock_exists_first_call(*args, **kwargs):
            if not hasattr(mock_exists_first_call, 'call_count'):
                mock_exists_first_call.call_count = 0
            
            mock_exists_first_call.call_count += 1
            
            if mock_exists_first_call.call_count == 1:
                return None
            else:
                return Repository(repository_id="repo017", creator_Id=default_user)
        
        with patch.object(Repository, 'objects') as mock_objects:
            mock_objects.first = mock_exists_first_call
            
            with pytest.raises(RepositoryAlreadyExists):
                RepositoryService.create_repository("repo017", default_user)


    
    @pytest.mark.principal
    @pytest.mark.timestamp
    @pytest.mark.integration
    def test_create_repository_data_integrity(self, default_user):
        repo = RepositoryService.create_repository("repo018", default_user)
        
        assert repo.repository_id == "repo018"
        assert repo.creator_Id == default_user
        assert repo.enterpriseId is None
        assert repo.contentId is not None
        assert repo.admin_repository is not None
        assert isinstance(repo.created_at, datetime.datetime)
        assert isinstance(repo.updated_at, datetime.datetime)
        
        assert len(repo.admin_repository.admin_users) == 1
        assert repo.admin_repository.admin_users[0].gitId == default_user.gitId


    @pytest.mark.principal
    @pytest.mark.integration
    def test_create_repository_with_multiple_admin_users(self, default_user):
        admin_users = []
        for i in range(3):
            user = User(gitId=f"admin{i}", email=f"admin{i}@example.com", userName=f"Admin {i}")
            user.save()
            admin_users.append(user)
        
        repo = RepositoryService.create_repository(
            repository_id="repo019",
            git_creator=default_user,
            admin_users=admin_users
        )
        
        assert len(repo.admin_repository.admin_users) == 4  
        
        admin_git_ids = [user.gitId for user in repo.admin_repository.admin_users]
        assert default_user.gitId in admin_git_ids
        for admin_user in admin_users:
            assert admin_user.gitId in admin_git_ids

    
    @pytest.mark.repository_id
    def test_create_repository_with_large_repository_id(self, default_user):
        long_id = 'a' * 256
        with pytest.raises(InputExceededCharacterLimit):
            RepositoryService.create_repository(long_id, default_user)


    @pytest.mark.repository_id
    def test_create_repository_with_special_characters_id(self, default_user):
        special_id = "repo-test_123.456@special"
        
        repo = RepositoryService.create_repository(special_id, default_user)
        assert repo.repository_id == special_id

    @pytest.mark.fails
    @pytest.mark.fails_general
    def test_create_repository_partial_failure_rollback(self,default_user):
        admin_user = User(gitId="admin_fail", email="admin_fail@example.com", userName="Admin Fail")
        admin_user.save()

        original_save = Repository.save
        
        def failing_save(self):
            if not hasattr(failing_save, 'called'):
                failing_save.called = True
                return original_save(self)
            else:
                raise Exception("Save failed")
        
        with patch.object(Repository, 'save', side_effect=failing_save):
            with pytest.raises(RepositoryFailCreate):
                RepositoryService.create_repository(
                    repository_id="repo020",
                    git_creator=default_user,
                    admin_users=[admin_user]
                )

        assert Repository.objects(repository_id="repo020").first() is None



    @pytest.mark.timestamp
    def test_create_repository_timezone_aware(self, default_user):
        repo = RepositoryService.create_repository("repo021", default_user)
        
        assert repo.created_at.tzinfo == datetime.timezone.utc
        assert repo.updated_at.tzinfo == datetime.timezone.utc
        assert repo.updated_at >= repo.created_at
