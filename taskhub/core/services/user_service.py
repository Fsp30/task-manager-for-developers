import datetime
from typing import List, Optional
from taskhub.core.models import User
from taskhub.core.models import Repository
from taskhub.core.models import RepositoryPermission
from taskhub.utils.validation_email import validate_email
from taskhub.middlewares.exceptions import (
        UserAlreadyExists,
        UserFailDetail,
        UserFailCreate,
        UserFailDelete,
        UserFailUpdate,
        UserNotFound,
        UserPermissionDenied, 
        RepositoryFailList, 
        InputExceededCharacterLimit,
        InvalidEmailFormat
)


def get_user(git_id:str) -> User:
        try:
                user = User.objects(gitId=git_id).first()
                if not user:
                        raise UserNotFound(f"User with ID: {git_id} not found")        
                return user
        except UserNotFound:
               raise
        except Exception as e:
                raise UserFailDetail(f"Failed detail user ID {git_id}: {str(e)}") from e

def create_user(git_id: str, user_email: str, user_name: Optional[str] = None) -> User:
    try:
        existing_user = User.objects(gitId=git_id).first()
        if existing_user:
            raise UserAlreadyExists(f"User with GitHub ID '{git_id}' already exists")
        
        existing_email = User.objects(email=user_email).first()
        if existing_email:
              raise UserAlreadyExists(f"User with email '{user_email}' already exists")

        validate_email(user_email)  

        _user_name = user_name or git_id
        
        if len(_user_name) > 100:
            raise InputExceededCharacterLimit(f"User name must be 100 characters or less. Provided: {len(_user_name)} characters" )
        
        new_user = User(
            gitId=git_id,
            email=user_email,
            userName=_user_name,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()  
        )
        
        new_user.save()
        return new_user
        
    except (UserAlreadyExists, InvalidEmailFormat, InputExceededCharacterLimit):
        # Re-raise expected exceptions
        raise
    except Exception as e:
        raise UserFailCreate(
            f"Failed to create user with GitHub ID '{git_id}': {str(e)}"
        ) from e

                

def list_my_repository(gitId:str) -> List[Repository]:
        if not User.objects(gitId=gitId).first():
                raise UserNotFound(f"failed search repository's: {str(gitId)}") 
        
        try:                
                repository = Repository.objects(creator_Id=gitId).all()
                return List(repository)

        except Exception as e:
                raise RepositoryFailList() from e
        

def update_user(gitId:str,email:str = None ,userName:str = None):
        try:
                user = get_user(gitId)
                if email:
                        user.email = email
                if userName:
                        user.userName = userName
                

                user.save()
                return user
        except UserNotFound:
                raise
        except Exception as e:
                raise UserFailUpdate(f"failed update: {str(e)}") from e
        

def delete_user(gitId: str) -> bool:
    try:
        user = get_user(gitId)
        user.delete()
        return True
    except UserNotFound:
        raise
    except Exception as e:
        raise UserFailDelete(f"failed delete: {str(e)}") from e
        

def get_my_permissions(gitId: str) -> List[RepositoryPermission]:
    if not User.objects(gitId=gitId).first(): 
        raise UserNotFound(f"User {gitId} not found")
    
    try:
        permissions = RepositoryPermission.objects(repositoryPermissionId=gitId).all() 
        return List(permissions)  
    except Exception as e:
        raise UserPermissionDenied(f"Permission denied or error occurred: {str(e)}") from e
                



