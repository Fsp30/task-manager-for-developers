import uuid, datetime
from typing import List, Optional
from taskhub.core.models import Task, ContentRepository,Repository,RepositoryPermission
from taskhub.core.services.user_service import UserService
from taskhub.middlewares.exceptions import (
        TaskFailCreate,
        TaskFailDelete,
        TaskFailList,
        TaskFailDetail,
        TaskFailUpdate,
        TaskNotFound,
        TaskPermissionDenied,
        UserNotFound,
        ContentRepositoryNotFound,
        InvalidRepositoryAccess,
        InputExceededCharacterLimit,
        TaskInvalidStatus,
        TaskInvalidPriority,
        TaskFailAddedUser,
        TaskFailRemoveUser
)

class TaskService:
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
            if len(title)>120:
                raise InputExceededCharacterLimit(f"Title must be between 1 and 120 characters; title:{len(title)}")
        
            if  len(description)>5000:
                raise InputExceededCharacterLimit(f"Description must be between 1 and 5000 characters; description:{len(description)}")
            
            content_repo = ContentRepository.objects(contentId=content_repository_id).first()
            
            if not content_repo:
                raise ContentRepositoryNotFound(f"Content repository {content_repository_id} not found")

            has_permission = RepositoryPermission.objects(
                admin_repository=content_repo.repositoryId,
                admin_users=git_user_id
            ).count() > 0

            if not has_permission:
                raise InvalidRepositoryAccess(f"User {git_user_id} has no admin rights for repository {content_repository_id}")

            author_user = UserService.get_user(git_user_id)
            resolver_users = [UserService.get_user(resolver_id) for resolver_id in resolvers] if resolvers else []

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


    def _can_edit_task(task:Task, user_id) -> bool:
        if str(task.author.id) == user_id:
            return True

        resolvers_ids = [str(resolver.id) for resolver in task.resolvers]
        if user_id in resolvers_ids:
            return True

        return False

    def update_task(
        task_id: str,
        author_id: Optional[str] = None,
        title: Optional[str] = None,
        resolver_id: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        deadline: Optional[datetime.datetime] = None,
        tags: Optional[List[str]] = None
        ) -> Task:
        try:
            task = TaskService.get_task(task_id)
            
            if author_id and not TaskService._can_edit_task(task, author_id):
                raise TaskPermissionDenied(f"User {author_id} cannot edit task {task_id}")
            
            if resolver_id and not TaskService._can_edit_task(task, resolver_id):
                raise TaskPermissionDenied(f"User {resolver_id} cannot edit task {task_id}")
            
            if title and len(title)>120:
                raise InputExceededCharacterLimit(f"Title must be between 1 and 120 characters; title:{len(title)}")
                
            if description and len(description)>5000:
                raise InputExceededCharacterLimit(f"Description must be between 1 and 5000 characters; description:{len(description)}")

            if status and status not in ['pending', 'in_progress', 'completed', 'cancelled']:
                raise TaskInvalidStatus(f"Invalid status: {status}")             
        
            if priority and priority not in ['low', 'medium', 'high']:
                raise TaskInvalidPriority(f"Invalid priority: {priority}")
            
            if title: task.title = title
            if description: task.description = description
            if status: task.status = status
            if priority: task.priority = priority
            if deadline is not None: task.deadline = deadline
            if tags is not None: task.tags = tags    

            task.save()
            return task
        except(TaskNotFound, TaskPermissionDenied, InputExceededCharacterLimit, TaskInvalidStatus, TaskInvalidPriority):
            raise
        except Exception as e:
            raise TaskFailUpdate(f"Failed to update task: {task_id}; {str(e)}") from e   


    def add_resolvers_to_task(task_id: str, author_id: str, _resolvers_ids: List[str]) -> Task:
        try:
            task = TaskService.get_task(task_id)
            if str(task.author.id) != author_id:
                raise TaskPermissionDenied(f"User {author_id} is not the author of task {task_id}")
            
            new_resolvers = [UserService.get_user(resolver_id) for resolver_id in _resolvers_ids]
            
            current_resolver_ids = [str(resolver.id) for resolver in task.resolvers]
            
            for new_resolver in new_resolvers:
                if str(new_resolver.id) not in current_resolver_ids:
                    task.resolvers.append(new_resolver)
            
            task.save()
            return task
            
        except (TaskNotFound, UserNotFound, TaskPermissionDenied):
            raise
        except Exception as e:
            raise TaskFailAddedUser(f"Failed to add resolvers {_resolvers_ids} to task {task_id}; {str(e)}") from e

    def remove_resolver_from_task(task_id: str, author_id: str, resolver_id_to_remove: str) -> bool:
        try:
            task = TaskService.get_task(task_id)
            
            if str(task.author.id) != author_id:
                raise TaskPermissionDenied(f"User {author_id} is not the author of task {task_id}")
            
            resolver_to_remove = UserService.get_user(resolver_id_to_remove)

            current_resolver_ids = [str(resolver.id) for resolver in task.resolvers]
    
            if str(resolver_to_remove.id) in current_resolver_ids:
                for resolver in task.resolvers:
                    if str(resolver.id) == resolver_id_to_remove:
                        task.resolvers.remove(resolver)
                        task.save()
                        return True
                
        except (TaskNotFound, UserNotFound, TaskPermissionDenied):
            raise
        except Exception as e:
            raise TaskFailRemoveUser(f"Failed to remove resolver {resolver_id_to_remove} from task {task_id}: {str(e)}") from e


    def delete_task(task_id:str, author_id:str) -> bool:
        try:
            task = TaskService.get_task(task_id)
            UserService.get_user(author_id)
            if str(task.author.id) != author_id:
                raise TaskPermissionDenied(f"User {author_id} is not the author of task {task_id}. Only the author can delete tasks.")
            
            task.delete()
            return True
        
        except (TaskNotFound, UserNotFound, TaskPermissionDenied):
            raise
        except Exception as e:
            raise TaskFailDelete(f"Failed delete task with ID: {task_id}; {str(e)}") from e 