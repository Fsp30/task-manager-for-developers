from taskhub.interfaces.api.constants.status_codes import AppCode
from taskhub.interfaces.api.constants.status_codes import ErrorsAppStatus
from taskhub.middlewares.exceptions.base_exception_handler import CustomAppException

class ContentRepositoryAlreadyExists(CustomAppException):
        status_code = ErrorsAppStatus.CONFLICT
        default_detail = "Content Repository já existente"
        default_code = "content_repository_exists"
        app_code = AppCode.CONTENT_REPOSITORY_CREATED_FAILED  

class ContentRepositoryFailCreate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao criar content_repository"
    default_code = "create_content_repository_failed"
    app_code = AppCode.CONTENT_REPOSITORY_CREATED_FAILED

class ContentRepositoryFailList(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao buscar content_repository"
    default_code = "find_content_repository_failed"
    app_code = AppCode.CONTENT_REPOSITORY_LIST_FAILED

class ContentRepositoryFailUpdate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao atualizar content_repository"
    default_code = "update_content_repository_failed"
    app_code = AppCode.CONTENT_REPOSITORY_UPDATE_FAILED

class ContentRepositoryFailDelete(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao deletar content_repository"
    default_code = "delete_content_repository_failed"
    app_code = AppCode.CONTENT_REPOSITORY_DELETE_FAILED