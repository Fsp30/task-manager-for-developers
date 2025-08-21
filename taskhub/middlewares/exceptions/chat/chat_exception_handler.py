from taskhub.interfaces.api.constants.status_codes import AppCode
from taskhub.interfaces.api.constants.status_codes import ErrorsAppStatus
from taskhub.middlewares.exceptions.base_exception_handler import CustomAppException

class ChatAlreadyExists(CustomAppException):
    status_code = ErrorsAppStatus.CONFLICT
    default_detail = "Chat já existente"
    default_code = "chat_exists"
    app_code = AppCode.CHAT_ALREADY_EXISTS  

class ChatNotFound(CustomAppException):
    status_code = ErrorsAppStatus.NOT_FOUND
    default_detail = "Chat não encontrado"
    default_code = "chat_not_found"
    app_code = AppCode.CHAT_NOT_FOUND

class ChatFailCreate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao criar chat"
    default_code = "create_chat_failed"
    app_code = AppCode.CHAT_CREATE_FAILED 

class ChatFailList(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao listar chats"
    default_code = "list_chats_failed"
    app_code = AppCode.CHAT_LIST_FAILED

class ChatFailDetail(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao obter detalhes do chat"
    default_code = "detail_chat_failed"
    app_code = AppCode.CHAT_LIST_FAILED  

class ChatFailUpdate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao atualizar chat"
    default_code = "update_chat_failed"
    app_code = AppCode.CHAT_UPDATE_FAILED  

class ChatFailDelete(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao deletar chat"
    default_code = "delete_chat_failed"
    app_code = AppCode.CHAT_DELETE_FAILED

