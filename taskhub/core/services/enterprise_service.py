import uuid
import logging
from typing import Optional, List, Union
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
        EnterpriseFailRemoveUser,
        InputEmptyOrNone,
        InputExceededCharacterLimit,
        DomainNoChange,
        EnterprisePermissionDenied
)

logger = logging.getLogger('taskhub.enterprise_service')

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



    def add_devs_in_enterprise(
        enterprise: Enterprise, 
        git_dev_enterprise: User, 
        new_devs: Union[User, List[User]]
        ) -> List[User]:

        try:
            if not isinstance(enterprise, Enterprise):
                raise InputEmptyOrNone("Enterprise must be a valid instance")
            
            if not enterprise.enterpriseId or not enterprise.enterpriseId.strip():
                raise InputEmptyOrNone("Enterprise must have a valid ID")
            
            if not isinstance(git_dev_enterprise, User):
                raise InputEmptyOrNone("Performing user must be a User instance")
            
            if not git_dev_enterprise.gitId or not git_dev_enterprise.gitId.strip():
                raise InputEmptyOrNone("Performing user must have a valid gitId")

            devs_to_add = new_devs if isinstance(new_devs, list) else [new_devs]
            
            if not devs_to_add:
                return list(enterprise.devs_enterprise)  

            for i, new_dev in enumerate(devs_to_add):
                if not isinstance(new_dev, User):
                    raise InputEmptyOrNone(f"New user at index {i} must be a User instance")
                if not new_dev.gitId or not new_dev.gitId.strip():
                    raise InputEmptyOrNone(f"New user at index {i} must have a valid gitId")

            existing_dev_ids = {dev.gitId for dev in enterprise.devs_enterprise}
            if git_dev_enterprise.gitId not in existing_dev_ids:
                raise EnterprisePermissionDenied(
                    f"User {git_dev_enterprise.gitId} does not belong to the enterprise"
                )

            new_devs_to_add = [
                new_dev for new_dev in devs_to_add 
                if new_dev.gitId not in existing_dev_ids
            ]

            if new_devs_to_add:
                enterprise.devs_enterprise.extend(new_devs_to_add)
                enterprise.save()
                
                added_ids = [dev.gitId for dev in new_devs_to_add]
                logger.info(
                    f"Users {added_ids} added to enterprise {enterprise.enterpriseId} "
                    f"by {git_dev_enterprise.gitId}. Total devs: {len(enterprise.devs_enterprise)}"
                )

            return list(enterprise.devs_enterprise)
            
        except (InputEmptyOrNone, EnterprisePermissionDenied):
            raise
        except Exception as e:
            logger.error(
                f"Failed to add users to enterprise {getattr(enterprise, 'enterpriseId', 'unknown')}: {str(e)}"
            )
            raise EnterpriseFailAddedUser(f"Failed to add users to enterprise ID: '{enterprise.enterpriseId}';  {str(e)}") from e

    def remove_dev_to_enterprise(
            enterprise: Enterprise,
            creator_enterprise: User,
            devs_remove: Union[User, List[User]]
        ) -> List[User]:
        try:
            if not isinstance(enterprise, Enterprise):
                raise InputEmptyOrNone("Enterprise must be a valid instance")
            
            if not enterprise.enterpriseId or not enterprise.enterpriseId.strip():
                raise InputEmptyOrNone("Enterprise must have a valid ID")
            
            if not isinstance(creator_enterprise, User):
                raise InputEmptyOrNone("Performing user must be a User instance")
            
            if not creator_enterprise.gitId or not creator_enterprise.gitId.strip():
                raise InputEmptyOrNone("Performing user must have a valid gitId")

            if creator_enterprise != enterprise.owner_Id:
                raise EnterprisePermissionDenied(f"User {creator_enterprise.gitId} does not creator to the enterprise")
        
            if devs_remove is None:
                return list(enterprise.devs_enterprise)

            devs_to_remove = devs_remove if isinstance(devs_remove, list) else [devs_remove]

            if not devs_to_remove:
                return list(enterprise.devs_enterprise)
            
            for i, dev_remove in enumerate(devs_to_remove):
                if not isinstance(dev_remove, User):
                    raise InputEmptyOrNone(f"Delete user at index {i} must be a User instance") 
                if not dev_remove.gitId or not dev_remove.gitId.strip():
                    raise InputEmptyOrNone(f"Delete user at index {i} must have a valid gitId")
            
            existing_dev_ids = {dev.gitId for dev in enterprise.devs_enterprise}

            list_devs_remove = [
                dev_remove for dev_remove in devs_to_remove
                if dev_remove.gitId in existing_dev_ids
            ]
            if creator_enterprise in list_devs_remove:
                raise EnterpriseFailRemoveUser("You can't delete the creator")

            if list_devs_remove:
                for dev in list_devs_remove:
                    logger.info(
                        f"Creator: {creator_enterprise.gitId} removed Developer"
                        f"{dev.gitId} from enterprise {enterprise.enterpriseId}"
                    )
                    enterprise.devs_enterprise.remove(dev)
                enterprise.save()
            
            return list(enterprise.devs_enterprise)
        
        except (InputEmptyOrNone, EnterprisePermissionDenied, EnterpriseFailRemoveUser):
            raise
        except Exception as e:
            logger.error(
                f"Error removing dev(s) from enterprise {getattr(enterprise, 'enterpriseId', None)} "
                f"by user {getattr(creator_enterprise, 'gitId', None)}: {e}"
            )
            raise EnterpriseFailRemoveUser(f"Failed remove dev(s) from enterprise '{enterprise.enterpriseId}'; {str(e)}" ) from e


    def delete_enterprise(enterprise: Enterprise, creator_enterprise: User) -> bool:
        try:
            if not isinstance(enterprise, Enterprise):
                raise InputEmptyOrNone("Enterprise must be a valid instance")
            
            if not enterprise.enterpriseId or not enterprise.enterpriseId.strip():
                raise InputEmptyOrNone("Enterprise must have a valid ID")
            
            if not isinstance(creator_enterprise, User):
                raise InputEmptyOrNone("Performing user must be a User instance")
            
            if not creator_enterprise.gitId or not creator_enterprise.gitId.strip():
                raise InputEmptyOrNone("Performing user must have a valid gitId")

            if creator_enterprise != enterprise.owner_Id:
                raise EnterprisePermissionDenied(f"User {creator_enterprise.gitId} does not creator to the enterprise")
            try:
                Enterprise.objects.get(enterpriseId=enterprise.enterpriseId)
            except Enterprise.DoesNotExist:
                raise EnterpriseNotFound(f"Enterprise with ID '{enterprise.enterpriseId}' does not exist")
                
            logger.info(
                f"Creator: {creator_enterprise.gitId} deleted "
                f"Enterprise: {enterprise.enterpriseId}"
            )
            enterprise.delete()
            return True
            
        except (InputEmptyOrNone, EnterprisePermissionDenied, EnterpriseNotFound):
            raise
        except Exception as e:
            enterprise_id = getattr(enterprise, 'enterpriseId', 'invalid_enterprise_object')
            creator = getattr(creator_enterprise, 'gitId', 'invalid_creator_object')
            logger.error(
                f"Failed delete enterprise {enterprise_id}"
                f"by your creator {creator}"
            )
            raise EnterpriseFailDelete(f"Failed to delete enterprise with ID: '{enterprise.enterpriseId}': {str(e)}") from e

    def update_enterprise(
        git_owner: User,
        enterprise: Enterprise,
        name_enterprise: str,
    ) -> Enterprise:
        try:

            if not name_enterprise or not name_enterprise.strip():
                raise InputEmptyOrNone("Name Enterprise must be filled in")
            
            if len(name_enterprise) > 100:
                raise InputExceededCharacterLimit(f"Enterprise name must be 100 characters or less. Provided: {len(name_enterprise)} characters")
            
            if not isinstance(enterprise, Enterprise):
                raise InputEmptyOrNone("Enterprise must be a valid instance")
            
            if not enterprise.enterpriseId or not enterprise.enterpriseId.strip():
                raise InputEmptyOrNone("Enterprise must have a valid ID")
            
            if not isinstance(git_owner, User):
                raise InputEmptyOrNone("Performing user must be a User instance")
            
            if not git_owner.gitId or not git_owner.gitId.strip():
                raise InputEmptyOrNone("Performing user must have a valid gitId")


            if git_owner != enterprise.owner_Id:
                raise EnterprisePermissionDenied(f"User {git_owner.gitId} does not creator to the enterprise")

            if name_enterprise == enterprise.nameEnterprise:
                raise DomainNoChange("A change is necessary")
            
            if Enterprise.objects(nameEnterprise=name_enterprise, id__ne=enterprise.id).first():
                raise EnterpriseAlreadyExists(f"Enterprise with name '{name_enterprise}' already exists")

            logger.info(
                f"Update enterprise: {enterprise.enterpriseId} by Creator: {git_owner.gitId}"
            )         

            enterprise.nameEnterprise = name_enterprise   
            enterprise.save()
            return enterprise.reload() 
            
        except (InputExceededCharacterLimit ,InputEmptyOrNone, EnterprisePermissionDenied, DomainNoChange,EnterpriseAlreadyExists):
            raise
        except Exception as e:
            logger.error(
                f"Error update enterprise {getattr(enterprise, 'enterpriseId', None)} "
                f"by user {getattr(git_owner, 'gitId', None)}: {e}"
            )
            raise EnterpriseFailUpdate(f"Failed to update enterprise with ID '{enterprise.enterpriseId}': {str(e)}") from e
            


        