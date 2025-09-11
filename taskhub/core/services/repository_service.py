import uuid
import datetime
from datetime import timezone
from typing import Optional, List
from taskhub.core.models import (
    Repository,
    User,
    RepositoryPermission,
    Enterprise
)


from taskhub.middlewares.exceptions import (
    RepositoryNotFound, 
    RepositoryChangeDenied,
    RepositoryAlreadyExists,
    RepositoryFailDelete,
    RepositoryPermissionFailList,
    RepositoryPermissionFailDelete,
    ContentRepositoryFailDelete,
    RepositoryFailDetail,
    RepositoryPermissionFailAddedUser,
    RepositoryPermissionNotFound,
    InputEmptyOrNone,
    InputExceededCharacterLimit,
    EnterprisePermissionDenied,
    RepositoryFailCreate,
    ContentRepositoryFailCreate,
    RepositoryPermissionFailCreate
    
)

class RepositoryService:
    
    def get_repository(repository_id: str) -> Repository:
        try:
            if not repository_id or not repository_id.strip():
                raise InputEmptyOrNone(f"Value input Github ID cannot be empty or None")
            repository = Repository.objects(repository_id=repository_id).first()  
            if repository == None:
                raise RepositoryNotFound(f"Repository with ID '{repository_id}' not found")
            return repository
        except (InputEmptyOrNone, RepositoryNotFound):
            raise
        except Exception as e:
            raise RepositoryFailDetail(f"Failed detail repository ID '{repository_id}': {str(e)}") from e

    def create_repository(
        repository_id: str,
        git_creator: 'User',
        enterprise: Optional['Enterprise'] = None,
        admin_users: Optional[List['User']] = None
    ) -> Repository:

        try: 
            if not repository_id or not repository_id.strip():
                raise InputEmptyOrNone("Repository ID must be provided")

            if len(repository_id)>255:
                raise InputExceededCharacterLimit(f"Repository name/ID must be 255 characters or less. Provided: {len(repository_id)} characters" )


            if not isinstance(git_creator, User):
                raise InputEmptyOrNone("Repository creator must be a User instance")

            if not getattr(git_creator, "gitId", None) or not git_creator.gitId.strip():
                raise InputEmptyOrNone("Repository creator must have a valid gitId")
            

            
            exists_repo = Repository.objects(repository_id=repository_id).first()
            
            if exists_repo: 
                raise RepositoryAlreadyExists(f"Repository ID '{repository_id} already exists'")

            if enterprise:
                if git_creator != enterprise.owner_Id and git_creator not in enterprise.devs_enterprise:
                    raise EnterprisePermissionDenied(f"User ID: '{git_creator.gitId}' does not have permission with the enterprise ID '{enterprise.enterpriseId}'")

            datetime_now = datetime.datetime.now(tz=datetime.timezone.utc)

            repository = Repository(
                repository_id = repository_id,
                creator_Id = git_creator,
                enterpriseId = enterprise,
                created_at = datetime_now,
                updated_at = datetime_now
            )
            repository.save()

            from taskhub.core.services.repository_permission_service import PermissionsService
            permission = PermissionsService.create_repository_permission(repository, git_creator)

            repository.admin_repository = permission
            repository.save()

            from taskhub.core.services.content_repository_service import ContentRepositoryService
            content = ContentRepositoryService.create_content_repository(repository=repository, creator_repo=git_creator)

            repository.contentId = content
            repository.save()

            if admin_users:
                for admin in admin_users:
                    try:
                        PermissionsService.add_dev_permission(permission, git_creator, admin)
                    except RepositoryPermissionFailAddedUser:
                        raise RepositoryPermissionFailAddedUser(f"Failed to add user '{admin.gitId}' to repository permissions")
                
                repository.reload()    
                repository.admin_repository.reload()
            
            repository.save()
            return repository
        except (InputEmptyOrNone,InputExceededCharacterLimit,RepositoryAlreadyExists, EnterprisePermissionDenied, RepositoryPermissionFailCreate,ContentRepositoryFailCreate, RepositoryPermissionFailAddedUser):
            raise
        except Exception as e: 
            raise RepositoryFailCreate(f"Failed to create repository ID '{repository_id}': {str(e)}") from e

            

    def list_admin_users(repository_id: str) -> List[User]:
        try:
            if not repository_id or not repository_id.strip():
                raise InputEmptyOrNone(f"Value input Github ID cannot be empty or None")
            
            repository = RepositoryService.get_repository(repository_id)

            permission = RepositoryPermission.objects(admin_repository=repository).first()
            if not permission or not permission.admin_users:
                return []
                
            return list(permission.admin_users)
        except (InputEmptyOrNone,RepositoryNotFound, RepositoryPermissionNotFound):
            raise         
        except Exception as e:
            raise RepositoryPermissionFailList(
                f"Failed to list admin users for repository '{repository_id}': {str(e)}"
            ) from e
    
    def delete_repository(repository_id: str, git_creator_id: str) -> bool:
        
        try:
            if not repository_id or not repository_id.strip() or not git_creator_id or not git_creator_id.strip():
                raise InputEmptyOrNone("Both fields must be completed")
            repository = RepositoryService.get_repository(repository_id)
            
            if str(repository.creator_Id.gitId) != git_creator_id:
                raise RepositoryChangeDenied(
                    f"User '{git_creator_id}' not authorized to delete repository '{repository_id}'"
                )
            
       
            from taskhub.core.services.content_repository_service import ContentRepositoryService
            ContentRepositoryService.delete_content_repository(repository_id, git_creator_id)
            
            from taskhub.core.services.repository_permission_service import PermissionsService
            PermissionsService.delete_permission_repository(repository_id, git_creator_id)
            
            repository.delete()
            return True
      
        except (InputEmptyOrNone,RepositoryNotFound,RepositoryChangeDenied, ContentRepositoryFailDelete,RepositoryPermissionFailDelete):
            raise
        except Exception as e:
            raise RepositoryFailDelete(
                f"Failed to delete repository '{repository_id}': {str(e)}"
            ) from e