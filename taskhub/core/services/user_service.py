from datetime import UTC
import datetime
from typing import List, Optional
from taskhub.core.models import User
from taskhub.core.models import Repository
from taskhub.core.models import RepositoryPermission
from taskhub.utils import Validations
from taskhub.middlewares.exceptions import (
        UserAlreadyExists,
        UserFailDetail,
        UserFailCreate,
        UserFailDelete,
        UserFailUpdate,
        UserNotFound,
        RepositoryFailList, 
        InputExceededCharacterLimit,
        InvalidEmailFormat,
        RepositoryPermissionFailList,
        InputEmptyOrNone
)

class UserService:
        def get_user(git_id:str) -> User:
                try:
                        if not git_id or not git_id.strip():
                               raise InputEmptyOrNone(f"Value input Github ID cannot be empty or None")
                        user = User.objects(gitId=git_id).first()
                        if not user:
                                raise UserNotFound(f"User with ID: {git_id} not found")        
                        return user
                except (InputEmptyOrNone ,UserNotFound):
                        raise
                except Exception as e:
                        raise UserFailDetail(f"Failed detail user ID '{git_id}': {str(e)}") from e

        def create_user(git_id: str, user_email: str, user_name: Optional[str] = None) -> User:
                try:
                        if not git_id or not git_id.strip():
                                raise InputEmptyOrNone(f"Value input Github ID cannot be empty or None")
                        
                        if not user_email or not user_email.strip():
                                raise InputEmptyOrNone(f"Value input email cannot be empty or None")

                        existing_user = User.objects(gitId=git_id).first()
                        if existing_user:
                                raise UserAlreadyExists(f"User with GitHub ID '{git_id}' already exists")

                        existing_email = User.objects(email=user_email).first()
                        if existing_email:
                                raise UserAlreadyExists(f"User with email '{user_email}' already exists")

                        Validations.validate_email(user_email)  

                        _user_name = user_name or git_id

                        if len(_user_name) > 100:
                                raise InputExceededCharacterLimit(f"User name must be 100 characters or less. Provided: {len(_user_name)} characters" )

                        new_user = User(
                                gitId=git_id,
                                email=user_email,
                                userName=_user_name,
                                created_at=datetime.datetime.now(UTC),
                                updated_at=datetime.datetime.now(UTC)  
                        )

                        new_user.save()
                        return new_user

                except (InputEmptyOrNone,UserAlreadyExists, InvalidEmailFormat, InputExceededCharacterLimit):
                        raise
                except Exception as e:
                        raise UserFailCreate( f"Failed to create user with GitHub ID '{git_id}': {str(e)}") from e

        def list_my_repositories(git_id:str) -> List[Repository]:
                try:
                        if not git_id or not git_id.strip():
                                raise InputEmptyOrNone(f"Value input Github ID cannot be empty or None")
                        user = UserService.get_user(git_id)  
                        return list(user.repositories) if user.repositories else []
                except (InputEmptyOrNone,UserNotFound):
                        raise
                except Exception as e:
                        raise RepositoryFailList(f"Failed list repositories for user '{git_id}'; {str(e)}") from e
                

        def get_my_permissions(git_id: str) -> List[RepositoryPermission]:
                try: 
                        if not git_id or not git_id.strip():
                                raise InputEmptyOrNone(f"Value input Github ID cannot be empty or None")
                        user = UserService.get_user(git_id)
                        return list(user.repository_permissions) if user.repository_permissions else []
                except (InputEmptyOrNone,UserNotFound): 
                        raise
                except Exception as e:  
                        raise RepositoryPermissionFailList(f"Failed list permissions for user '{git_id}': {str(e)}") from e
                

        def update_user(git_id: str, user_email:Optional[str] = None, user_name:Optional[str] = None):
                try:
                        if not user_email and not user_name:
                                raise InputEmptyOrNone("At least one of user_email or user_name must be provided")
                        
                        user = UserService.get_user(git_id)

                        if user_name and len(user_name) > 100:
                                raise InputExceededCharacterLimit(f"User name must be 100 characters or less (got {len(user_name)})")

                        update_fields = {}
                
                        if user_email and user_email != str(user.email):
                                Validations.validate_email(user_email)
                                user.email = user_email
                                update_fields["email"] = user_email

                        
                        if user_name and user_name != str(user.userName):
                                user.userName = user_name
                                update_fields["user_name"] = user_name

                        if update_fields:
                                user.save()

                        return user

                except (InputEmptyOrNone,UserNotFound, InvalidEmailFormat, InputExceededCharacterLimit):
                        raise
                except Exception as e:
                        raise UserFailUpdate(f"Failed update user with ID '{git_id}': {str(e)}") from e
                

        def delete_user(git_id: str) -> bool:
                try:
                        if not git_id or not git_id.strip():
                                raise InputEmptyOrNone(f"Value input Github ID cannot be empty or None")
                        user = UserService.get_user(git_id)  
                        user.delete()
                        return True
                except (InputEmptyOrNone,UserNotFound):  
                        raise
                except Exception as e: 
                        raise UserFailDelete(f"Failed delete user with ID '{git_id}': {str(e)}") from e