import uuid
from typing import Optional, List
from taskhub.core.models import Enterprise
from taskhub.core.models import User
from taskhub.core.models import Repository
from taskhub.core.services.user_service import UserService
from taskhub.middlewares.exceptions import (
        RepositoryFailList,
        EnterpriseFailCreate,
        EnterpriseAlreadyExists,
        EnterpriseFailDelete,
        EnterpriseFailUpdate,
        EnterpriseNotFound,
        UserFailList,
        EnterpriseFailDetail,
        EnterpriseFailAddedUser,
        UserNotFound,
        EnterpriseFailRemoveUser,
        InputEmptyOrNone,
        InputExceededCharacterLimit
)
class EnterpriseService:
    def get_enterprise(enterprise_id:str) -> Enterprise:
        try:    
                if not enterprise_id or not enterprise_id.strip():
                    raise InputEmptyOrNone(f"Value input ID cannot be empty or None")
                enterprise = Enterprise.objects(enterpriseId=enterprise_id).first()
                if not enterprise:
                        raise EnterpriseNotFound(f"Enterprise with ID '{enterprise_id}' not found")
                return enterprise
        except (InputEmptyOrNone, EnterpriseNotFound):
            raise
        except Exception as e:
                raise EnterpriseFailDetail(f"Failed detail enterprise ID '{enterprise_id}': {str(e)}") from e

    def list_devs_enterprise(enterprise_id: str) -> List[User]:
        try:
            if not enterprise_id or not enterprise_id.strip():
                raise InputEmptyOrNone(f"Value input ID cannot be empty or None")
            
            enterprise = EnterpriseService.get_enterprise(enterprise_id)
            
            return list(enterprise.devs_enterprise) if enterprise.devs_enterprise else []
        
        except (InputEmptyOrNone,EnterpriseNotFound):
            raise
        except Exception as e:
            raise UserFailList(f"Failed to list enterprise ID: '{enterprise_id}' developers : {str(e)}") from e
                            
                

    def list_repositories_enterprise(enterprise_id: str) -> List[Repository]:
        try:
            if not enterprise_id or not enterprise_id.strip():
                raise InputEmptyOrNone(f"Value input ID cannot be empty or None")
            
            enterprise = EnterpriseService.get_enterprise(enterprise_id)

            return list(enterprise.repositorys_Id) if enterprise.repositorys_Id else []
        
        except (InputEmptyOrNone, EnterpriseNotFound):
            raise
        except Exception as e:
            raise RepositoryFailList(f"Failed to list enterprise ID '{enterprise_id}' repositories: {str(e)}") from e
            


    def create_enterprise(
            git_owner: 'User',
            name_enterprise: str,
            git_enterprise_id: Optional[str] = None
    ) -> Enterprise:
        try:
            if not isinstance(git_owner, User):
                raise InputEmptyOrNone("Enterprise creator must be a User instance")

            if not getattr(git_owner, "gitId", None) or not git_owner.gitId.strip():
                raise InputEmptyOrNone("Enterprise creator must have a valid gitId")

            if not name_enterprise or not name_enterprise.strip():
                raise InputEmptyOrNone(f"Value input name enterprise cannot be empty or None")


            if len(name_enterprise)>100:
                raise InputExceededCharacterLimit(f"Enterprise name must be 100 characters or less. Provided: {len(name_enterprise)} characters")
            
            if Enterprise.objects(nameEnterprise__iexact=name_enterprise).first():
                raise EnterpriseAlreadyExists(f"Enterprise with name '{name_enterprise}' already exists")
            
            enterprise_id = git_enterprise_id or str(uuid.uuid4())

            enterprise = Enterprise(
                owner_Id=git_owner,
                enterpriseId=enterprise_id,
                nameEnterprise=name_enterprise,
                gitId_enterprise=git_enterprise_id,
                devs_enterprise=[git_owner]
            )
            enterprise.save()
            return enterprise
        except (InputEmptyOrNone, InputExceededCharacterLimit, EnterpriseAlreadyExists):
            raise
        except Exception as e:
            raise EnterpriseFailCreate(f"Failed to create Enterprise: {str(e)}") from e



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
            


        