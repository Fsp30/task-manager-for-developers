import uuid
from typing import Optional, List
from taskhub.core.models import Enterprise
from taskhub.core.models import User
from taskhub.core.models import Repository
from taskhub.core.services import UserService
from taskhub.middlewares.exceptions import (
        RepositoryFailList,
        RepositoryNotFound,
        EnterpriseFailCreate,
        EnterpriseAlreadyExists,
        EnterpriseFailDelete,
        EnterpriseFailUpdate,
        EnterpriseNotFound,
        UserFailList,
        EnterpriseFailDetail,
        EnterpriseFailAddedUser,
        UserNotFound,
        EnterpriseFailRemoveUser
)
class EnterpriseService:
    def get_enterprise(enterprise_id:str) -> Enterprise:
            try:
                    enterprise = Enterprise.objects(enterpriseId=enterprise_id).first()
                    if not enterprise:
                            raise EnterpriseNotFound(f"Enterprise with ID '{enterprise_id}' not found")
                    return enterprise
            except Exception as e:
                    raise EnterpriseFailDetail(f"Failed to get enterprise: {str(e)}") from e
            
    def create_enterprise(
            git_owner_id: str,
            name_enterprise: str,
            git_enterprise_id: Optional[str] = None,
            enterprise_id: Optional[str] = None
    ) -> Enterprise:
        if Enterprise.objects(nameEnterprise=name_enterprise).first():
            raise EnterpriseAlreadyExists(f"Enterprise with name '{name_enterprise}' already exists")
        
        enterprise_id = git_enterprise_id or str(uuid.uuid4())
        try:
            enterprise = Enterprise(
                owner_id=git_owner_id,
                enterpriseId=enterprise_id,
                nameEnterprise=name_enterprise,
                gitId_enterprise=git_enterprise_id
            )
            enterprise.save()
            return enterprise
        except Exception as e:
            raise EnterpriseFailCreate(f"Failed to create Enterprise: {str(e)}") from e


    def list_devs_enterprise(enterprise_id: str) -> List[User]:
        try:
            enterprise = EnterpriseService.get_enterprise(enterprise_id)
            return list(enterprise.devs_enterprise) if enterprise.devs_enterprise else []
        except EnterpriseNotFound:
            raise
        except Exception as e:
            raise UserFailList(f"Failed to list devs: {str(e)}") from e
                            
                    


    def list_repositories_enterprise(enterprise_id: str) -> List[Repository]:
        try:
            EnterpriseService.get_enterprise(enterprise_id) 
            repositories = Repository.objects(enterpriseId=enterprise_id).all()
            return list(repositories)
        except (EnterpriseNotFound, RepositoryNotFound):
            raise
        except Exception as e:
            raise RepositoryFailList(f"Failed to list repositories: {str(e)}") from e


    def add_dev_in_enterprise(enterprise_id: str, git_dev_id: str) -> List[User]:
        try:
            new_dev = UserService.get_user(git_dev_id)
            enterprise = EnterpriseService.get_enterprise(enterprise_id)
            
            if new_dev not in enterprise.devs_enterprise:
                enterprise.devs_enterprise.append(new_dev)
                enterprise.save()
            
            return list(enterprise.devs_enterprise)
        except (UserNotFound, EnterpriseNotFound):
            raise
        except Exception as e:
            raise EnterpriseFailAddedUser(f"Failed to add dev '{git_dev_id}' to enterprise '{enterprise_id}': {str(e)}") from e
        

    def delete_dev_to_enterprise(enterprise_id: str, git_dev_id: str) -> List[User]:
        try:
            enterprise = EnterpriseService.get_enterprise(enterprise_id)
            dev_to_remove = UserService.get_user(git_dev_id)
            
            if dev_to_remove in enterprise.devs_enterprise:
                enterprise.devs_enterprise.remove(dev_to_remove)
                enterprise.save()
            
            return list(enterprise.devs_enterprise)
        except (UserNotFound, EnterpriseNotFound):
            raise
        except Exception as e:
            raise EnterpriseFailRemoveUser(f"Failed to remove dev '{git_dev_id}': {str(e)}") from e



    def delete_enterprise(git_owner_id: str, enterprise_id: str) -> bool:
        try:
            UserService.get_user(git_owner_id)
            enterprise = EnterpriseService.get_enterprise(enterprise_id)
            
            if str(enterprise.owner_Id) != git_owner_id:
                raise EnterpriseFailDelete(f"User '{git_owner_id}' is not the owner of enterprise '{enterprise_id}'")
            
            enterprise.delete()
            return True
            
        except (UserNotFound, EnterpriseNotFound):
            raise
        except Exception as e:
            raise EnterpriseFailDelete(f"Failed to delete enterprise with ID '{enterprise_id}': {str(e)}") from e

    def update_enterprise(
        git_owner_id: str,
        enterprise_id: str,
        name_enterprise: Optional[str] = None,
    ) -> Enterprise:
        try:
            UserService.get_user(git_owner_id)
            enterprise = EnterpriseService.get_enterprise(enterprise_id)
            
            if str(enterprise.owner_Id) != git_owner_id:
                raise EnterpriseFailUpdate(f"User '{git_owner_id}' is not the owner of enterprise '{enterprise_id}'")
    
            if name_enterprise and name_enterprise != enterprise.nameEnterprise:
                if Enterprise.objects(nameEnterprise=name_enterprise).first():
                    raise EnterpriseAlreadyExists(f"Enterprise with name '{name_enterprise}' already exists")

            if name_enterprise is not None:
                enterprise.nameEnterprise = name_enterprise
            
            enterprise.save()
            return enterprise
            
        except (UserNotFound, EnterpriseNotFound, EnterpriseAlreadyExists):
            raise
        except Exception as e:
            raise EnterpriseFailUpdate(f"Failed to update enterprise with ID '{enterprise_id}': {str(e)}") from e
            


        