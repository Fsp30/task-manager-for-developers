import uuid
import datetime
from typing import Optional, List
from taskhub.core.models import (
    Repository,
    User,
    RepositoryPermission
)
from taskhub.core.services.user_service import UserService

from taskhub.middlewares.exceptions import (
    RepositoryNotFound, 
    RepositoryFailList, 
    RepositoryAlreadyExists,
    RepositoryFailCreate,
    RepositoryFailDelete,
    RepositoryPermissionFailList,
    RepositoryPermissionFailDelete,
    UserNotFound,
    ContentRepositoryFailDelete
)

class RepositoryService:
    
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
            RepositoryService.get_repository(repository_id)
            raise RepositoryAlreadyExists(f"Repository with ID '{repository_id}' already exists")
        except RepositoryNotFound:
            pass  
        
        try:
            creator_user = UserService.get_user(git_creator_id)
            
            from taskhub.core.services.enterprise_service import EnterpriseService
            enterprise_ref = EnterpriseService.get_enterprise(enterprise_id) if enterprise_id else None
            
            repository = Repository(
                repository_id=repository_id,
                creator_Id=creator_user,
                enterpriseId=enterprise_ref,
                created_at=datetime.datetime.utcnow()
            )
            repository.save()
            
            from taskhub.core.services.repository_permission_service import PermissionsService
            permission = PermissionsService.create_repository_permission(repository_id, git_creator_id)

            from taskhub.core.services.content_repository_service import ContentRepositoryService
            content = ContentRepositoryService.create_content_repository(
                repository=repository,  
                git_creator_id=git_creator_id
            )
            
            repository.admin_repository = permission
            repository.content_Id = content
            repository.save()
            
            if admin_users:
                for user_id in admin_users:
                    try:
                        PermissionsService.add_dev_permission(permission.repositoryPermissionId, git_creator_id, user_id)
                    except Exception as e:
                        print(f"Warning: Failed to add admin user {user_id}: {str(e)}")
            
            return repository
            
        except UserNotFound:
            if 'repository' in locals():
                repository.delete()
            raise
        except Exception as e:
            if 'repository' in locals():
                repository.delete()
            if 'content' in locals() and content:
                content.delete()
            if 'permission' in locals() and permission:
                permission.delete()
                
            raise RepositoryFailCreate(f"Failed to create repository: {str(e)}") from e

    def list_admin_users(repository_id: str) -> List[User]:
        try:
            repository = RepositoryService.get_repository(repository_id)
        except RepositoryNotFound:
            raise
        
        try:
            permission = RepositoryPermission.objects(admin_repository=repository).first()
            if not permission or not permission.admin_users:
                return []
                
            return list(permission.admin_users)          
        except Exception as e:
            raise RepositoryPermissionFailList(
                f"Failed to list admin users for repository {repository_id}: {str(e)}"
            ) from e
    
    def delete_repository(repository_id: str, git_creator_id: str) -> bool:
        
        try:
            repository = RepositoryService.get_repository(repository_id)
            
            if str(repository.creator_Id.gitId) != git_creator_id:
                raise RepositoryPermissionFailDelete(
                    f"User '{git_creator_id}' not authorized to delete repository '{repository_id}'"
                )
            
       
            from taskhub.core.services.content_repository_service import ContentRepositoryService
            ContentRepositoryService.delete_content_repository(repository_id, git_creator_id)
            
            from taskhub.core.services.repository_permission_service import PermissionsService
            PermissionsService.delete_permission_repository(repository_id, git_creator_id)
            
            repository.delete()
            return True
            
        except RepositoryNotFound:
            raise
        except ContentRepositoryFailDelete:
            raise
        except RepositoryPermissionFailDelete:
            raise
        except Exception as e:
            raise RepositoryFailDelete(
                f"Failed to delete repository '{repository_id}': {str(e)}"
            ) from e