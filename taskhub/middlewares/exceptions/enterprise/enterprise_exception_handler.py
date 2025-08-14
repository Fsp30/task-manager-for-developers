from taskhub.interfaces.api.constants.status_codes import AppCode
from taskhub.interfaces.api.constants.status_codes import ErrorsAppStatus
from taskhub.middlewares.exceptions.base_exception_handler import CustomAppException

class EnterpriseAlreadyExists(CustomAppException):
    status_code = ErrorsAppStatus.CONFLICT
    default_detail = "Enterprise já existente"
    default_code = "enterprise_exists"
    app_code = AppCode.ENTERPRISE_ALREADY_EXISTS 

class EnterpriseNotFound(CustomAppException):
    status_code = ErrorsAppStatus.NOT_FOUND
    default_detail = "Enterprise não encontrada"
    default_code = "enterprise_not_found"
    app_code = AppCode.ENTERPRISE_NOT_FOUND

class EnterpriseFailCreate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao criar enterprise"
    default_code = "create_enterprise_failed"
    app_code = AppCode.ENTERPRISE_CREATE_FAILED  

class EnterpriseFailList(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao listar enterprises"
    default_code = "list_enterprises_failed"
    app_code = AppCode.ENTERPRISE_LIST_FAILED

class EnterpriseFailDetail(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao obter detalhes da enterprise"
    default_code = "detail_enterprise_failed"
    app_code = AppCode.ENTERPRISE_LIST_FAILED 

class EnterpriseFailUpdate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao atualizar enterprise"
    default_code = "update_enterprise_failed"
    app_code = AppCode.ENTERPRISE_UPDATE_FAILED

class EnterpriseFailDelete(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao deletar enterprise"
    default_code = "delete_enterprise_failed"
    app_code = AppCode.ENTERPRISE_DELETE_FAILED

class EnterprisePermissionDenied(CustomAppException):
    status_code = ErrorsAppStatus.FORBIDDEN
    default_detail = "Permissão negada para acessar a enterprise"
    default_code = "enterprise_permission_denied"
    app_code = AppCode.ENTERPRISE_LIST_FAILED 

class EnterpriseFailAddedUser(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao adiciona dev da enterprise"
    default_code = "enterprise_dev_add_failed"
    app_code = AppCode.USER_ADDED_ENTERPRISE_FAILED 

class EnterpriseFailRemoveUser(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao remover dev da enterprise"
    default_code = "enterprise_dev_add_failed"
    app_code = AppCode.ENTERPRISE_REMOVE_USER_FAILED 