
from .base_exception_mock import BaseTestException

class UserAlreadyExists(BaseTestException):
    status_code = 409  
    default_detail = "Usuário já existe"
    default_code = "user_already_exists"
    app_code = "USER_ALREADY_EXISTS"

class UserNotFound(BaseTestException):
    status_code = 404  
    default_detail = "Usuário não encontrado"
    default_code = "user_not_found"
    app_code = "USER_NOT_FOUND"

class UserFailCreate(BaseTestException):
    status_code = 400 
    default_detail = "Falha ao criar usuário"
    default_code = "user_creation_failed"
    app_code = "USER_CREATE_FAILED"

class UserFailList(BaseTestException):
    status_code = 400  
    default_detail = "Falha ao listar usuários"
    default_code = "user_list_failed"
    app_code = "USER_LIST_FAILED"

class UserFailDetail(BaseTestException):
    status_code = 400 
    default_detail = "Falha ao obter detalhes do usuário"
    default_code = "user_detail_failed"
    app_code = "USER_DETAIL_FAILED"

class UserFailUpdate(BaseTestException):
    status_code = 400  
    default_detail = "Falha ao atualizar usuário"
    default_code = "user_update_failed"
    app_code = "USER_UPDATE_FAILED"

class UserFailDelete(BaseTestException):
    status_code = 400  
    default_detail = "Falha ao deletar usuário"
    default_code = "user_deletion_failed"
    app_code = "USER_DELETE_FAILED"

class UserPermissionDenied(BaseTestException):
    status_code = 403  
    default_detail = "Permissão negada para acessar o usuário"
    default_code = "user_permission_denied"
    app_code = "USER_PERMISSION_DENIED"