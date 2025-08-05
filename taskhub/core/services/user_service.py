from taskhub.core.models.user import User
from taskhub.core.models.repository import Repository
from taskhub.middlewares.exceptions import (
        UserAlreadyExists,UserFailCreate,UserFailDelete,UserFailList,UserFailUpdate,UserNotFound,UserPermissionDenied, RepositoryFailList
)

def create_user(gitId:str, email:str, userName:str):
        if User.objects(gitId=gitId).first():
                raise UserAlreadyExists()

        if(userName==''):
                userName=gitId

        try:
                created_user = User(
                        gitId=gitId,
                        email=email,
                        userName=userName
                )
                created_user.save()
                return created_user
        except Exception as e:
                raise UserFailCreate() from e 

def get_user(gitId:str):
        try:
                user = User.objects(gitId=gitId).first()
                if not user:
                        raise UserNotFound()        
                return user
        except Exception as e:
                raise UserFailList(f"failed: {str(e)}") from e

def list_my_repository(gitId:str) -> list[Repository]:
        if not User.objects(gitId=gitId).first():
                raise UserNotFound(f"failed search repository's: {str(gitId)}") 
        
        try:                
                repository = Repository.objects(creator_Id=gitId).all()
                return repository

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
        




