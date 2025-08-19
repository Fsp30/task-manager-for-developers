import uuid, datetime
from typing import List, Optional
from taskhub.core.models import Task, ContentRepository,Repository,RepositoryPermission
from taskhub.core.services.user_service import get_user
from taskhub.middlewares.exceptions import (
        TaskAlreadyExists,
        TaskFailCreate,
        TaskFailDelete,
        TaskFailList,
        TaskFailDetail,
        TaskFailUpdate,
        TaskNotFound,
        TaskPermissionDenied,
        UserNotFound,
        RepositoryNotFound,
        ContentRepositoryNotFound,
        InvalidRepositoryAccess,
        InputExceededCharacterLimit
)

def get_task(task_id: str) -> Task:
        try:
                task = Task.objects(taskId=task_id).first()
                if not task:
                        raise TaskNotFound(f"Task with ID: '{task_id}' not found")
                return task
        except Exception as e:
                raise TaskFailDetail(f"Failed to get task ID '{task_id}'; {str(e)}") from e

def get_all_task_in_repository(git_user_id: str, content_repository_id: str) -> List[Task]:
    try:
        content_repo = ContentRepository.objects(contentId=content_repository_id).first()
        if not content_repo:
            raise ContentRepositoryNotFound(f"Content repository {content_repository_id} not found")

        has_permission = RepositoryPermission.objects(
            admin_repository=content_repo.repositoryId,
            admin_users=git_user_id
        ).count() > 0

        if not has_permission:
            raise InvalidRepositoryAccess(f"User {git_user_id} has no admin rights for repository {content_repository_id}")

        tasks = Task.objects(
            repositoryId=content_repo.repositoryId,
            content_type='task'  
        ).order_by('-created_task_at')

        return list(tasks)

    except ContentRepositoryNotFound:
        raise 
    except Exception as e:
        raise TaskFailList( f"Failed to retrieve tasks for repository {content_repository_id}: {str(e)}") from e
        
        
def create_task(
    git_user_id: str,
    content_repository_id: str,
    title: str,
    resolvers: Optional[List[str]] = None,
    description: str = "",
    status: str = "pending",
    priority: str = "medium",
    deadline: Optional[datetime.datetime] = None,
    tags: Optional[List[str]] = None
) -> Task:
    
    try:
        if len(title)>120 or len(description)>5000:
             raise InputExceededCharacterLimit(f"Title must be between 1 and 120 characters; title:{len(title)}, description:{len(description)}")
        content_repo = ContentRepository.objects(contentId=content_repository_id).first()
        if not content_repo:
            raise ContentRepositoryNotFound(f"Content repository {content_repository_id} not found")

        has_permission = RepositoryPermission.objects(
            admin_repository=content_repo.repositoryId,
            admin_users=git_user_id
        ).count() > 0

        if not has_permission:
            raise InvalidRepositoryAccess(f"User {git_user_id} has no admin rights for repository {content_repository_id}")

        author_user = get_user(git_user_id)
        resolver_users = [get_user(resolver_id) for resolver_id in resolvers] if resolvers else []

        task_id = str(uuid.uuid4())
        task = Task(
            taskId=task_id,
            link_content_id=content_repo,  
            repositoryId=content_repo.repositoryId,
            title=title,
            author=author_user,
            resolvers=resolver_users,
            description=description,
            status=status,
            priority=priority,
            deadline=deadline,
            tags=tags if tags else [],
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
            content_type='task'
        )
        task.save()

        ContentRepository.objects(contentId=content_repository_id).update_one(push__tasks=task)

        return task


    except InputExceededCharacterLimit as e:
        if 'task' in locals():
             task.delete()
    except UserNotFound as e:
        if 'task' in locals():
            task.delete()
        raise
    except Exception as e:
        if 'task' in locals():
            task.delete()
        raise TaskFailCreate(f"Failed to create task: {str(e)}") from e