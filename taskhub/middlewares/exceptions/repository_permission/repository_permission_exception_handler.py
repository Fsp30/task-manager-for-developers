from taskhub.interfaces.api.constants.status_codes import AppCode
from taskhub.interfaces.api.constants.status_codes import ErrorsAppStatus
from taskhub.middlewares.exceptions.base_exception_handler import CustomAppException

class RepositoryPermissionAlreadyExists(CustomAppException):
        status_code = ErrorsAppStatus.CONFLICT
        default_detail =  "Repository permissionjá existente"
        default_code = "_repository_exists"
        app_code = AppCode.REPOSITORY_PERMISSION_CREATED_FAILED  

class RepositoryPermissionFailCreate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao criar repository permission"
    default_code = "create_repository_permission_failed"
    app_code = AppCode.REPOSITORY_PERMISSION_CREATED_FAILED

class RepositoryPermissionFailUpdate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao atualizar repository permission"
    default_code = "update_repository_permission_failed"
    app_code = AppCode.REPOSITORY_PERMISSION_UPDATE_FAILED

class RepositoryPermissionFailDelete(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao deletar repository permission"
    default_code = "delete_repository_permission_failed"
    app_code = AppCode.REPOSITORY_PERMISSION_DELETE_FAILED

class InvalidRepositoryAccess(CustomAppException):
    status_code = ErrorsAppStatus.FORBIDDEN
    default_detail = "Acesso negado ao repositório."
    default_code = "repository_forbidden"
    app_code = AppCode.REPOSITORY_PERMISSION_DETAIL
