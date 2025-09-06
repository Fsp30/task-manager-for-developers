from taskhub.interfaces.api.constants.status_codes import AppCode
from taskhub.interfaces.api.constants.status_codes import ErrorsAppStatus
from taskhub.middlewares.exceptions.base_exception_handler import CustomAppException

class RepositoryAlreadyExists(CustomAppException):
    status_code = ErrorsAppStatus.CONFLICT
    default_detail = "Repositório já existente"
    default_code = "repository_exists"
    app_code = AppCode.REPOSITORY_ALREADY_EXISTS  

class RepositoryNotFound(CustomAppException):
    status_code = ErrorsAppStatus.NOT_FOUND
    default_detail = "Repositório não encontrado"
    default_code = "repository_not_found"
    app_code = AppCode.REPOSITORY_NOT_FOUND

class RepositoryFailCreate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao criar repositório"
    default_code = "create_repository_failed"
    app_code = AppCode.REPOSITORY_CREATE_FAILED  

class RepositoryFailList(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao listar repositórios"
    default_code = "list_repositories_failed"
    app_code = AppCode.REPOSITORY_LIST_FAILED

class RepositoryFailDetail(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao obter detalhes do repositório"
    default_code = "detail_repository_failed"
    app_code = AppCode.REPOSITORY_DETAIL_FAILED

class RepositoryFailUpdate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao atualizar repositório"
    default_code = "update_repository_failed"
    app_code = AppCode.REPOSITORY_UPDATE_FAILED

class RepositoryFailDelete(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao deletar repositório"
    default_code = "delete_repository_failed"
    app_code = AppCode.REPOSITORY_DELETE_FAILED

