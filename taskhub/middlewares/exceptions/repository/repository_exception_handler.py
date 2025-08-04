from taskhub.interfaces.api.constants.status_codes import AppCode
from taskhub.interfaces.api.constants.status_codes import ErrorsAppStatus
from taskhub.middlewares.exceptions.base_exception_handler import CustomAppException

class RepositoryAlreadyExists(CustomAppException):
        status_code = ErrorsAppStatus.CONFLICT
        default_detail = "Repository já existente"
        default_code = "repository_exists"
        app_code = AppCode.REPOSITORY_CREATED_FAILED  

class RepositoryFailCreate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao criar enterprise"
    default_code = "create_repository_failed"
    app_code = AppCode.REPOSITORY_CREATED_FAILED

class RepositoryFailList(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao buscar repository"
    default_code = "find_repository_failed"
    app_code = AppCode.REPOSITORY_LIST_FAILED

class RepositoryFailUpdate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao atualizar repository"
    default_code = "update_repository_failed"
    app_code = AppCode.REPOSITORY_UPDATE_FAILED

class RepositoryFailDelete(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao deletar repository"
    default_code = "delete_repository_failed"
    app_code = AppCode.REPOSITORY_DELETE_FAILED