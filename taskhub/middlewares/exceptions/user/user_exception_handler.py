from taskhub.interfaces.api.constants.status_codes import AppCode
from taskhub.interfaces.api.constants.status_codes import ErrorsAppStatus
from taskhub.middlewares.exceptions.base_exception_handler import CustomAppException

class UserAlreadyExists(CustomAppException):
    status_code = ErrorsAppStatus.CONFLICT
    default_detail = "Usuário já existe"
    default_code = "user_already_exists"
    app_code = AppCode.USER_ALREADY_EXISTS 

class UserNotFound(CustomAppException):
    status_code = ErrorsAppStatus.NOT_FOUND
    default_detail = "Usuário não encontrado"
    default_code = "user_not_found"
    app_code = AppCode.USER_NOT_FOUND

class UserFailCreate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao criar usuário"
    default_code = "user_creation_failed"
    app_code = AppCode.USER_CREATE_FAILED  

class UserFailList(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao listar usuários"
    default_code = "user_list_failed"
    app_code = AppCode.USER_LIST_FAILED

class UserFailDetail(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao obter detalhes do usuário"
    default_code = "user_detail_failed"
    app_code = AppCode.USER_LIST_FAILED  

class UserFailUpdate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao atualizar usuário"
    default_code = "user_update_failed"
    app_code = AppCode.USER_UPDATE_FAILED

class UserFailDelete(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao deletar usuário"
    default_code = "user_deletion_failed"
    app_code = AppCode.USER_DELETE_FAILED

class UserPermissionDenied(CustomAppException):
    status_code = ErrorsAppStatus.FORBIDDEN
    default_detail = "Permissão negada para acessar o usuário"
    default_code = "user_permission_denied"
    app_code = AppCode.USER_LIST_FAILED  