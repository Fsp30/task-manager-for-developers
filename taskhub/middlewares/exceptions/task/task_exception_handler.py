from taskhub.interfaces.api.constants.status_codes import AppCode
from taskhub.interfaces.api.constants.status_codes import ErrorsAppStatus
from taskhub.middlewares.exceptions.base_exception_handler import CustomAppException

class TaskAlreadyExists(CustomAppException):
        status_code = ErrorsAppStatus.CONFLICT
        default_detail = "Taks já existente"
        default_code = "task_exists"
        app_code = AppCode.TASK_CREATED_FAILED  

class TaskFailCreate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao criar task"
    default_code = "create_task_failed"
    app_code = AppCode.TASK_CREATED_FAILED

class TaskFailList(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao buscar task"
    default_code = "find_task_failed"
    app_code = AppCode.TASK_LIST_FAILED

class TaskFailUpdate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao atualizar task"
    default_code = "update_task_failed"
    app_code = AppCode.TASK_UPDATE_FAILED

class TaskFailDelete(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao deletar task"
    default_code = "delete_task_failed"
    app_code = AppCode.TASK_DELETE_FAILED