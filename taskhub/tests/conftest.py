import pytest
import mongomock
import fakeredis
from mongoengine import connect, disconnect, get_db
from taskhub.core.services.user_service import UserService
from taskhub.core.services.repository_service import RepositoryService
from taskhub.core.services.enterprise_service import EnterpriseService
from taskhub.core.services.repository_permission_service import PermissionsService
from taskhub.core.models import User, Repository, RepositoryPermission, Enterprise


# ============================================================
# Infra
# ============================================================

@pytest.fixture(scope="session", autouse=True)
def mongo_test_connection():
    disconnect()  
    connect(
        db="test_db",
        host="mongodb://localhost",  
        alias="default",
        uuidRepresentation="standard",
        mongo_client_class=mongomock.MongoClient,
    )
    yield
    disconnect()


@pytest.fixture(autouse=True)
def clear_mongo_collections():
    db = get_db()
    for collection in db.list_collection_names():
        db[collection].delete_many({})


@pytest.fixture(scope="session")
def fake_redis():
    return fakeredis.FakeRedis(decode_responses=True)


@pytest.fixture
def redis_client(monkeypatch, fake_redis):
    import redis
    monkeypatch.setattr(redis, "Redis", lambda *a, **kw: fake_redis)
    return fake_redis


# ============================================================
# Usuários básicos
# ============================================================

@pytest.fixture
def default_user():
    user = UserService.create_user("123", "filipe@example.com", "Filipe")
    yield user
    user.delete()


@pytest.fixture
def another_user(): 
    another_user = UserService.create_user("456", "another@user.gmail.com")
    yield another_user
    another_user.delete()


@pytest.fixture
def third_user():
    third_user = UserService.create_user("789", "Third@user.com")
    return third_user


# ============================================================
# Empresas
# ============================================================

@pytest.fixture
def default_enterprise(default_user):
    enterprise = Enterprise(
        owner_Id=default_user,
        enterpriseId="enterprise123",
        nameEnterprise="Test Enterprise",
        devs_enterprise=[default_user]
    )
    enterprise.save()
    yield enterprise
    enterprise.delete()


@pytest.fixture
def default_enterprise_with_devs(default_user):
    """Cria uma empresa com desenvolvedores"""
    devs = []
    for i in range(2):
        user = User(gitId=f"dev{i}", email=f"dev{i}@example.com", userName=f"Developer {i}")
        user.save()
        devs.append(user)
    devs.append(default_user)

    enterprise = Enterprise(
        owner_Id=default_user,
        enterpriseId="enterprise_with_devs",
        nameEnterprise="Enterprise with Devs",
        devs_enterprise=devs 
    )
    enterprise.save()
    yield enterprise
    
    for user in devs:
        user.delete()
    enterprise.delete()


@pytest.fixture
def enterprise_with_repositories(default_user):
    enterprise = Enterprise(
        owner_Id=default_user,
        enterpriseId="enterprise_with_repos",
        nameEnterprise="Enterprise with Repos",
        devs_enterprise=[default_user]
    )
    enterprise.save()
    
    repos = []
    for i in range(1, 3):
        repo = Repository(
            repository_id=f"repo_enterprise_{i}",
            creator_Id=default_user,
            enterpriseId=enterprise
        )
        repo.save()
        enterprise.repositorys_Id.append(repo)
        enterprise.save()   
    
    yield enterprise
    enterprise.delete()


@pytest.fixture
def enterprise_special_chars(default_user):
    enterprise = Enterprise(
        owner_Id=default_user,
        enterpriseId="test@enterprise_123!-special",
        nameEnterprise="Special Chars Enterprise",
        devs_enterprise=[default_user]
    )
    enterprise.save()
    yield enterprise
    enterprise.delete()


@pytest.fixture
def enterprise_long_id(default_user):
    long_id = "a" * 100
    enterprise = Enterprise(
        owner_Id=default_user,
        enterpriseId=long_id,
        nameEnterprise="Long ID Enterprise",
        devs_enterprise=[default_user]
    )
    enterprise.save()
    yield enterprise
    enterprise.delete()


@pytest.fixture
def enterprise_many_devs(default_user):
    devs = []
    for i in range(50):
        user = User(gitId=f"many_devs_{i}", email=f"dev{i}@example.com", userName=f"Dev {i}")
        user.save()
        devs.append(user)
    
    devs.append(default_user)
    enterprise = Enterprise(
        owner_Id=default_user,
        enterpriseId="enterprise_many_devs",
        nameEnterprise="Enterprise with Many Devs",
        devs_enterprise=devs
    )
    enterprise.save()
    yield enterprise
    
    for user in devs:
        user.delete()
    enterprise.delete()


@pytest.fixture
def enterprise_many_repos(default_user):
    enterprise = Enterprise(
        owner_Id=default_user,
        enterpriseId="enterprise_many_repos",
        nameEnterprise="Enterprise with Many Repos"
    )
    enterprise.save()
    
    repos = []
    for i in range(100):
        repo = Repository(
            repository_id=f"repo_many_{i}",
            creator_Id=default_user,
            enterpriseId=enterprise
        )
        repo.save()
        repos.append(repo)
        enterprise.repositorys_Id.append(repo)
        enterprise.save()
    
    yield enterprise
    
    for repo in repos:
        repo.delete()
    enterprise.delete()


# ============================================================
# Repositórios
# ============================================================

@pytest.fixture
def default_repository_list():
    user = UserService.create_user("123", "test@example.com")
    Repository.objects(creator_Id=user).delete()
    
    repositories = []
    for i in range(5):
        repo = Repository(
            repository_id=f"repo-{i}",
            creator_Id=user,
        )
        repo.save()
        repositories.append(repo)

    user.repositories = repositories
    user.save()
    
    return repositories


@pytest.fixture
def default_repository_permissions():
    user = UserService.create_user("123", "test@example.com")
    RepositoryPermission.objects(admin_users=user).delete()

    repositories = []
    for i in range(3):
        repo = Repository(
            repository_id=f"repo-{i}",
            creator_Id=user,
        )
        repo.save()
        repositories.append(repo)

    permissions = []
    for i, repo in enumerate(repositories):
        perm = RepositoryPermission(
            repositoryPermissionId=f"perm-{i}",
            repository=repo,
            admin_users=[user],
        )
        perm.save()
        permissions.append(perm)

    user.repository_permissions = permissions
    user.save()

    return permissions


@pytest.fixture
def default_repository():
    creator = User(
        gitId="creator123",
        email="creator@example.com",
        userName="Creator User"
    )
    creator.save()

    admins = []
    for i in range(3):
        admin = User(
            gitId=f"admin{i}",
            email=f"admin{i}@example.com",
            userName=f"Admin {i}"
        )
        admin.save()
        admins.append(admin)

    enterprise = Enterprise(
        owner_Id=creator,
        enterpriseId="enterprise123",
        nameEnterprise="Test Enterprise"
    )
    enterprise.save()

    repository = Repository(
        repository_id="test_repo_id",
        creator_Id=creator,
        enterpriseId=enterprise
    )
    repository.save()

    permissions = RepositoryPermission(
        repositoryPermissionId="perm_repo_id",
        repository=repository, 
        admin_users=[creator] + admins
    )
    permissions.save()
    repository.save()

    return repository


# ============================================================
# Factories / Helpers
# ============================================================

import uuid
import pytest
from taskhub.core.models import User
from taskhub.core.services.enterprise_service import EnterpriseService

@pytest.fixture
def user_factory():
    created_users = []

    def _factory(count: int = 1):
        users = []
        for _ in range(count):
            suffix = str(uuid.uuid4())[:8]
            user = User(
                gitId=f"test_user_{suffix}",
                email=f"user_{suffix}@test.com",
                userName=f"user_{suffix}"
            )
            user.save()
            users.append(user)

        created_users.extend(users)
        return users[0] if count == 1 else users

    yield _factory

    for user in created_users:
        user.delete()

