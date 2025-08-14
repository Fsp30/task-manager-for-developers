import uuid, datetime
from typing import Optional, List
from taskhub.core.models import Repository
from taskhub.core.models import ContentRepository
from taskhub.core.models import RepositoryPermission
from taskhub.core.models import User
from taskhub.core.services.user_service import get_user
from taskhub.core.services.enterprise_service import get_enterprise
from taskhub.core.services.repository_permission_service import create_repository_permission
from taskhub.core.services.repository_permission_service import add_dev_permission
from taskhub.middlewares.exceptions import (
    RepositoryNotFound, 
    RepositoryFailList, 
    RepositoryAlreadyExists,
    RepositoryFailCreate,
    RepositoryFailDelete,
    RepositoryPermissionFailList,
    RepositoryPermissionFailDelete,
    UserNotFound,
        
)


def get_repository(repository_id: str) -> Repository:
    try:
        repository = Repository.objects(repository_id=repository_id).first()  
        if not repository:
            raise RepositoryNotFound(f"Repository with ID '{repository_id}' not found")
        return repository
    except Exception as e:
        raise RepositoryFailList(f"Failed to get repository: {str(e)}") from e

def create_repository(
    repository_id: str,
    git_creator_id: str,
    enterprise_id: Optional[str] = None,
    admin_users: Optional[List[str]] = None
) -> Repository:
    
    try:
        get_repository(repository_id)
        raise RepositoryAlreadyExists(f"Repository with ID '{repository_id}' already exists")
    except RepositoryNotFound:
        pass
    
    try:
        creator_user = get_user(git_creator_id)  
        enterprise_ref = get_enterprise(enterprise_id) if enterprise_id else None
        

        content = ContentRepository(content_Id=str(uuid.uuid4()))
        content.save()
        
        permission = create_repository_permission(repository_id, git_creator_id)
        
        repository = Repository(
            repository_id=repository_id,
            creator_Id=creator_user,
            content_Id=content,
            admin_repository=permission,
            enterpriseId=enterprise_ref,
            created_at=datetime.datetime.utcnow()
        )
        
        repository.save()
        if admin_users:
            for user_id in admin_users:
                add_dev_permission(permission.repositoryPermissionId, git_creator_id, user_id)
        
        return repository
    except UserNotFound:
        raise
    except RepositoryNotFound:
        raise

    except Exception as e:
        raise RepositoryFailCreate(f"Failed to create repository: {str(e)}") from e

def list_admin_users(repository_id: str) -> List[User]:
    try: 
        repository = get_repository(repository_id)
        raise RepositoryNotFound(f"Repository with ID '{repository_id}' not exists")
    except RepositoryAlreadyExists:
        pass 
    
    try:
            
        permission = RepositoryPermission.objects(admin_repository=repository).first()
        if not permission or not permission.admin_users:
            return []
            
        return list(permission.admin_users)          
    except RepositoryNotFound:
        raise
    except Exception as e:
        raise RepositoryPermissionFailList(
            f"Failed to list admin users for repository {repository_id}: {str(e)}"
        ) from e
    
def delete_repository(repository_id: str, git_creator_id: str) -> bool:
    
    try:
        repository = get_repository(repository_id)
        
        if str(repository.creator_Id.id) != git_creator_id:
            raise RepositoryPermissionFailDelete(
                f"User '{git_creator_id}' not authorized to delete repository '{repository_id}'"
            )
        repository.delete()
        return True
        
    except RepositoryNotFound:
        raise
    except RepositoryPermissionFailDelete:
        raise
    except Exception as e:
        raise RepositoryFailDelete(
            f"Failed to delete repository '{repository_id}': {str(e)}"
        ) from e
