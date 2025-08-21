from taskhub.interfaces.api.constants.status_codes import AppCode
from taskhub.interfaces.api.constants.status_codes import ErrorsAppStatus
from taskhub.middlewares.exceptions.base_exception_handler import CustomAppException

class TaskAlreadyExists(CustomAppException):
    status_code = ErrorsAppStatus.CONFLICT
    default_detail = "Task já existente"
    default_code = "task_already_exists"
    app_code = AppCode.TASK_ALREADY_EXISTS  

class TaskNotFound(CustomAppException):
    status_code = ErrorsAppStatus.NOT_FOUND
    default_detail = "Task não encontrada"
    default_code = "task_not_found"
    app_code = AppCode.TASK_NOT_FOUND

class TaskFailCreate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao criar task"
    default_code = "task_creation_failed"
    app_code = AppCode.TASK_CREATE_FAILED 

class TaskFailList(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao listar tasks"
    default_code = "task_list_failed"
    app_code = AppCode.TASK_LIST_FAILED

class TaskFailDetail(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao obter detalhes da task"
    default_code = "task_detail_failed"
    app_code = AppCode.TASK_DETAIL_FAILED  

class TaskFailUpdate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao atualizar task"
    default_code = "task_update_failed"
    app_code = AppCode.TASK_UPDATE_FAILED

class TaskFailDelete(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao deletar task"
    default_code = "task_deletion_failed"
    app_code = AppCode.TASK_DELETE_FAILED

class TaskInvalidStatus(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Status de task invalido"
    default_code = "task_status_invalid"
    app_code = AppCode.TASK_INVALID_STATUS

class TaskInvalidPriority(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Prioridade de task invalido"
    default_code = "task_priority_invalid"
    app_code = AppCode.TASK_INVALID_PRIORITY

class TaskPermissionDenied(CustomAppException):
    status_code = ErrorsAppStatus.FORBIDDEN
    default_detail = "Permissão negada para acessar a task"
    default_code = "task_permission_denied"
    app_code = AppCode.TASK_INVALID_CREDENTIALS 

class TaskFailAddedUser(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao adicionar user da task"
    default_code = "add_user_to_task_failed"
    app_code = AppCode.USER_ADDED_TASK_FAILED

class TaskFailRemoveUser(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao remover user da task"
    default_code = "remove_user_to_task_failed"
    app_code = AppCode.USER_REMOVE_TASK_FAILED
