from taskhub.interfaces.api.constants.status_codes import AppCode
from taskhub.interfaces.api.constants.status_codes import ErrorsAppStatus
from taskhub.middlewares.exceptions.base_exception_handler import CustomAppException

class RepositoryPermissionAlreadyExists(CustomAppException):
    status_code = ErrorsAppStatus.CONFLICT
    default_detail = "Permissão de repositório já existente"
    default_code = "repository_permission_exists"
    app_code = AppCode.REPOSITORY_PERMISSION_ALREADY_EXISTS 

class RepositoryPermissionNotFound(CustomAppException):
    status_code = ErrorsAppStatus.NOT_FOUND
    default_detail = "Permissão de repositório não encontrada"
    default_code = "repository_permission_not_found"
    app_code = AppCode.REPOSITORY_PERMISSION_NOT_FOUND

class RepositoryPermissionFailCreate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao criar permissão de repositório"
    default_code = "create_repository_permission_failed"
    app_code = AppCode.REPOSITORY_PERMISSION_CREATE_FAILED  

class RepositoryPermissionFailList(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao listar permissões de repositório"
    default_code = "list_repository_permissions_failed"
    app_code = AppCode.REPOSITORY_PERMISSION_LIST_FAILED

class RepositoryPermissionFailDetail(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao obter detalhes da permissão de repositório"
    default_code = "detail_repository_permission_failed"
    app_code = AppCode.REPOSITORY_PERMISSION_DETAIL

class RepositoryPermissionFailUpdate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao atualizar permissão de repositório"
    default_code = "update_repository_permission_failed"
    app_code = AppCode.REPOSITORY_PERMISSION_UPDATE_FAILED

class RepositoryPermissionFailDelete(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao deletar permissão de repositório"
    default_code = "delete_repository_permission_failed"
    app_code = AppCode.REPOSITORY_PERMISSION_DELETE_FAILED

class InvalidRepositoryAccess(CustomAppException):
    status_code = ErrorsAppStatus.FORBIDDEN
    default_detail = "Acesso negado ao repositório"
    default_code = "repository_access_denied"
    app_code = AppCode.REPOSITORY_PERMISSION_DETAIL