from taskhub.interfaces.api.constants.status_codes import AppCode
from taskhub.interfaces.api.constants.status_codes import ErrorsAppStatus
from taskhub.middlewares.exceptions.base_exception_handler import CustomAppException


class UserAlreadyExists(CustomAppException):
    status_code = ErrorsAppStatus.CONFLICT
    default_detail = "Usuário já existe."
    default_code = "user_exists"
    app_code = AppCode.AUTH_USER_ALREADY_EXISTS

class UserFailCreate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao criar usuário"
    default_code = "create_user_fail"
    app_code = AppCode.USER_CREATED_FAILED

class UserFailList(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao buscar usuário"
    default_code = "find_user_fail"
    app_code = AppCode.USER_LIST_FAILED

class UserFailUpdate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao atualizar usuário"
    default_code = "update_user_fail"
    app_code = AppCode.USER_UPDATE_FAILED

class UserFailDelete(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao deletar usuário"
    default_code = "delete_user_fail"
    app_code = AppCode.USER_DELETE_FAILED
