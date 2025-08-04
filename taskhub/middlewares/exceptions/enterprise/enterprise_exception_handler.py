from taskhub.interfaces.api.constants.status_codes import AppCode
from taskhub.interfaces.api.constants.status_codes import ErrorsAppStatus
from taskhub.middlewares.exceptions.base_exception_handler import CustomAppException

class EnterpriseAlreadyExists(CustomAppException):
        status_code = ErrorsAppStatus.CONFLICT
        default_detail = "Enterprise já existente"
        default_code = "enterprise_exists"
        app_code = AppCode.ENTERPRISE_CREATED_FAILED  

class EnterpriseFailCreate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao criar enterprise"
    default_code = "create_enterprise_failed"
    app_code = AppCode.ENTERPRISE_CREATED_FAILED

class EnterpriseFailList(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao buscar enterprise"
    default_code = "find_enterprise_failed"
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