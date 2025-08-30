from typing import Optional, List
import uuid, datetime
from datetime import UTC
from taskhub.core.models import( 
    RepositoryPermission,
    Repository,
    User
)
from taskhub.core.services.user_service import UserService
from taskhub.core.services.repository_service import RepositoryService

from taskhub.middlewares.exceptions import (
        UserPermissionDenied,
        UserNotFound,
        UserFailList,
        RepositoryPermissionNotFound,
        RepositoryPermissionFailDetail,
        RepositoryPermissionFailAddedUser,
        RepositoryPermissionFailRemoveUser,
        RepositoryPermissionFailCreate,
        InvalidRepositoryAccess,
        RepositoryNotFound,
        RepositoryPermissionFailDelete


)
class PermissionsService:
    def get_permission_repository(repository_id: str, git_user_id:str) -> RepositoryPermission:
        try:
            user = UserService.get_user(git_user_id)
            repository = Repository.objects(repository_id=repository_id).first()
            
            if not repository:
                raise RepositoryNotFound(f"Repository with ID {repository_id} not found")
    
            if not repository.admin_repository:
                raise RepositoryPermissionNotFound(f"No permission found for repository {repository_id}")
                
            permission = repository.admin_repository

            if user not in permission.admin_users:
                raise UserPermissionDenied(
                    f"User {git_user_id} has no permission to access repository {repository_id}"
                )
            
            return permission
            
        except UserNotFound:
            raise
        except RepositoryNotFound:
            raise RepositoryPermissionNotFound(f"Repository {repository_id} not found")
        except Exception as e:
            raise RepositoryPermissionFailDetail(f"Failed to get repository permission: {str(e)}") from e

    def get_all_devs(repository_permission_id:str, git_user_id:str) -> List[User]:
        try:
            permission = PermissionsService.get_permission_repository(git_user_id,repository_permission_id)
            return list(permission.admin_users) if permission.admin_users else []
        
        except RepositoryPermissionNotFound:
            raise
        except Exception as e:
            raise UserFailList(f"Failed to list developers for permission {repository_permission_id}: {str(e)}") from e


    def create_repository_permission(repository_id: str,  git_creator_id: str) -> RepositoryPermission:

        try:
            user = UserService.get_user(git_creator_id)
            repository = RepositoryService.get_repository(repository_id)  

            if str(repository.creator_Id) != git_creator_id:
                raise InvalidRepositoryAccess(f"User {git_creator_id} is not the repository creator")
    
            permission = RepositoryPermission(
                repositoryPermissionId=str(uuid.uuid4()),
                admin_users=[user], 
                admin_repository=repository,
                created_at=datetime.datetime.now(UTC),
                updated_at=datetime.datetime.now(UTC)  
            )
            permission.save()
            
            return permission
            
        except UserNotFound:
            raise
        except RepositoryNotFound:
            raise
        except InvalidRepositoryAccess:
            raise
        except Exception as e:
            raise RepositoryPermissionFailCreate(f"Failed to create repository permission: {str(e)}") from e

    def add_dev_permission(repository_permission_id: str, git_admin_id: str, git_new_user_id: str) -> List[User]:
        try:
            permission = PermissionsService.get_permission_repository(repository_permission_id, git_admin_id)
            admin_user = UserService.get_user(git_admin_id)
            new_user = UserService.get_user(git_new_user_id)
            
            if admin_user not in permission.admin_users:
                raise InvalidRepositoryAccess(f"User {git_admin_id} is not authorized to add permissions" )
            
            if new_user not in permission.admin_users:
                permission.admin_users.append(new_user)
                permission.save()
            
            return list(permission.admin_users)
            
        except RepositoryPermissionNotFound:
            raise
        except UserNotFound:
            raise
        except InvalidRepositoryAccess:
            raise
        except Exception as e:
            raise RepositoryPermissionFailAddedUser(f"Failed to add user '{git_new_user_id}' to repository permissions: {str(e)}") from e
        
    def remove_dev_permission(repository_permission_id: str, git_admin_id: str, git_remove_user_id: str) -> List[User]:
            try:
                permission = PermissionsService.get_permission_repository(repository_permission_id)
                admin_user = UserService.get_user(git_admin_id)
                user_to_remove = UserService.get_user(git_remove_user_id)

                if admin_user not in permission.admin_users:
                    raise InvalidRepositoryAccess(f"User {git_admin_id} is not authorized to add permissions" )
                
                if user_to_remove not in permission.admin_users:
                    raise UserNotFound(f"User '{git_remove_user_id}' not found in permission list with ID '{repository_permission_id}'")
                
                permission.admin_users.remove(user_to_remove)
                permission.save()

                return list(permission.admin_users)
            
            except RepositoryPermissionNotFound:
                    raise
            except UserNotFound:
                    raise
            except InvalidRepositoryAccess:
                    raise
            except Exception as e:
                    raise RepositoryPermissionFailRemoveUser(f"Failed to remove user '{git_remove_user_id}' to repository permissions: {str(e)}") from e

    def delete_permission_repository(repository_id: str, git_creator_id: str) -> bool:
        try:
            repository = RepositoryService.get_repository(repository_id)
            if str(repository.creator_Id.id) != git_creator_id:
                raise InvalidRepositoryAccess(
                    f"Exclusive permission: Only the creator can delete permissions for repository '{repository_id}'"
                )

            permission = RepositoryPermission.objects(admin_repository=repository).first()
            if not permission:
                raise RepositoryPermissionNotFound(f"No permissions found for repository '{repository_id}'")

            permission.delete()
            return True

        except RepositoryNotFound:
            raise
        except InvalidRepositoryAccess:
            raise
        except RepositoryPermissionNotFound:
            raise
        except Exception as e:
            raise RepositoryPermissionFailDelete(f"Failed to delete permissions for repository '{repository_id}': {str(e)}") from e


            
                
                    
            

   
        