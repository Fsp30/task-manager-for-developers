from taskhub.interfaces.api.constants.status_codes import AppCode
from taskhub.interfaces.api.constants.status_codes import ErrorsAppStatus
from taskhub.middlewares.exceptions.base_exception_handler import CustomAppException

class chatAlreadyExists(CustomAppException):
        status_code = ErrorsAppStatus.CONFLICT
        default_detail = "Chat já existente"
        default_code = "chat_exists"
        app_code = AppCode.CHAT_CREATED_FAILED  

class chatFailCreate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao criar chat"
    default_code = "create_chat_failed"
    app_code = AppCode.CHAT_CREATED_FAILED

class chatFailList(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao buscar chat"
    default_code = "find_chat_failed"
    app_code = AppCode.CHAT_LIST_FAILED

class chatFailUpdate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao atualizar chat"
    default_code = "update_chat_failed"
    app_code = AppCode.chat_UPDATE_FAILED

class chatFailDelete(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao deletar chat"
    default_code = "delete_chat_failed"
    app_code = AppCode.CHAT_DELETE_FAILED