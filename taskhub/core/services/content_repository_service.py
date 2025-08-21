import uuid, datetime
from enum import Enum
from typing import Optional,List
from taskhub.core.models import ContentRepository
from taskhub.core.models import Repository
from taskhub.core.services.repository_service import get_repository
from taskhub.core.services.user_service import get_user
from taskhub.core.services.repository_permission_service import get_permission_repository
from taskhub.middlewares.exceptions import (
        ContentRepositoryNotFound,
        ContentRepositoryPermissionDenied,
        InvalidRepositoryAccess,
        UserNotFound,
        ContentRepositoryFailDetail,
        RepositoryPermissionNotFound, 
        ContentRepositoryAlreadyExists,
        RepositoryNotFound,
        ContentRepositoryFailCreate,
        RepositoryPermissionFailDelete,
        ContentRepositoryFailDelete


)

def get_content_repository(git_user_id: str, content_repository_id: str) -> ContentRepository:
    try:
        user = get_user(git_user_id)
        content = ContentRepository.objects(contentId=content_repository_id).first()
        
        if not content:
            raise ContentRepositoryNotFound(f"Content Repository with ID '{content_repository_id}' not found")
        
        permission = get_permission_repository(str(content.repositoryId.id), git_user_id)

        if user not in permission.admin_users:
            raise ContentRepositoryPermissionDenied(
                f"User {git_user_id} not permission to access content repository"
            )
        
        return content
        
    except UserNotFound:
        raise
    except RepositoryPermissionNotFound:
        raise ContentRepositoryPermissionDenied(
            f"User {git_user_id} has no permissions for this content"
        )
    except Exception as e:
        raise ContentRepositoryFailDetail(
            f"Failed to get content repository with ID '{content_repository_id}': {str(e)}"
        ) from e

def create_content_repository(
    repository: 'Repository', 
    git_creator_id: str,
    content_type: str = 'content_repository',
    working_tag: Optional[str] = None,
    chat_id: Optional[str] = None
) -> ContentRepository:

    try:
        creator_user = get_user(git_creator_id)
        permission = get_permission_repository( git_creator_id, str(repository.repository_id))
        
        content_id = str(uuid.uuid4())
        chat_id = chat_id or str(uuid.uuid4())
        
        content = ContentRepository(
            repositoryId=repository,
            contentId=content_id,
            admin_users=permission,  
            working_tag=working_tag,
            chat_id=chat_id,
            content_type=content_type,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        
        content.save()
        return content
        
    except UserNotFound:
        raise
    except Exception as e:
        raise ContentRepositoryFailCreate(f"Failed to create content repository: {str(e)}") from e


def delete_content_repository(repository_id: str, git_creator_id: str) -> bool:
    try:
        repository = get_repository(repository_id)
        content_repository = ContentRepository.objects(content_Id=str(repository.content_Id)).first()
        
        if not content_repository:
            raise ContentRepositoryNotFound(f"Content Repository with ID {repository.content_Id} not found")
        
        if str(repository.creator_Id.id) != git_creator_id:
            raise RepositoryPermissionFailDelete(
                f"User '{git_creator_id}' not authorized to delete repository '{repository_id}'"
            )

        content_repository.delete()
        return True
        
    except RepositoryNotFound:
        raise
    except ContentRepositoryNotFound:
        raise
    except RepositoryPermissionFailDelete:
        raise
    except Exception as e:
        raise ContentRepositoryFailDelete(
            f"Failed to delete content Repository with ID '{content_repository.content_Id}': {str(e)}"
        ) from e