from taskhub.interfaces.api.constants.status_codes import AppCode
from taskhub.interfaces.api.constants.status_codes import ErrorsAppStatus
from taskhub.middlewares.exceptions.base_exception_handler import CustomAppException

class NoteAlreadyExists(CustomAppException):
        status_code = ErrorsAppStatus.CONFLICT
        default_detail = "Note já existente"
        default_code = "note_exists"
        app_code = AppCode.NOTE_CREATED_FAILED  

class NoteFailCreate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao criar note"
    default_code = "create_note_failed"
    app_code = AppCode.NOTE_CREATED_FAILED

class NoteFailList(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao buscar note"
    default_code = "find_note_failed"
    app_code = AppCode.NOTE_LIST_FAILED

class NoteFailUpdate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao atualizar note"
    default_code = "update_note_failed"
    app_code = AppCode.NOTE_UPDATE_FAILED

class NoteFailDelete(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao deletar note"
    default_code = "delete_note_failed"
    app_code = AppCode.NOTE_DELETE_FAILED