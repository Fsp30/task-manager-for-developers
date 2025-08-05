from taskhub.interfaces.api.constants.status_codes import AppCode
from taskhub.interfaces.api.constants.status_codes import ErrorsAppStatus
from taskhub.middlewares.exceptions.base_exception_handler import CustomAppException

class ContentRepositoryAlreadyExists(CustomAppException):
    status_code = ErrorsAppStatus.CONFLICT
    default_detail = "Content Repository já existente"
    default_code = "content_repository_exists"
    app_code = AppCode.CONTENT_REPOSITORY_ALREADY_EXISTS

class ContentRepositoryNotFound(CustomAppException):
    status_code = ErrorsAppStatus.NOT_FOUND
    default_detail = "Content Repository não encontrado"
    default_code = "content_repository_not_found"
    app_code = AppCode.CONTENT_REPOSITORY_NOT_FOUND

class ContentRepositoryFailCreate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao criar Content Repository"
    default_code = "create_content_repository_failed"
    app_code = AppCode.CONTENT_REPOSITORY_CREATE_FAILED

class ContentRepositoryFailList(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao listar Content Repositories"
    default_code = "list_content_repositories_failed"
    app_code = AppCode.CONTENT_REPOSITORY_LIST_FAILED

class ContentRepositoryFailDetail(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao obter detalhes do Content Repository"
    default_code = "detail_content_repository_failed"
    app_code = AppCode.CONTENT_REPOSITORY_LIST_FAILED 

class ContentRepositoryFailUpdate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao atualizar Content Repository"
    default_code = "update_content_repository_failed"
    app_code = AppCode.CONTENT_REPOSITORY_UPDATE_FAILED

class ContentRepositoryFailDelete(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao deletar Content Repository"
    default_code = "delete_content_repository_failed"
    app_code = AppCode.CONTENT_REPOSITORY_DELETE_FAILED

class ContentRepositoryPermissionDenied(CustomAppException):
    status_code = ErrorsAppStatus.FORBIDDEN
    default_detail = "Permissão negada para acessar o Content Repository"
    default_code = "content_repository_permission_denied"
    app_code = AppCode.CONTENT_REPOSITORY_LIST_FAILED  