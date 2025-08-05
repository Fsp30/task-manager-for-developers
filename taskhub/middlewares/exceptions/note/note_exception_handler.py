from taskhub.interfaces.api.constants.status_codes import AppCode
from taskhub.interfaces.api.constants.status_codes import ErrorsAppStatus
from taskhub.middlewares.exceptions.base_exception_handler import CustomAppException

class NoteAlreadyExists(CustomAppException):
    status_code = ErrorsAppStatus.CONFLICT
    default_detail = "Note já existente"
    default_code = "note_exists"
    app_code = AppCode.NOTE_ALREADY_EXISTS  

class NoteNotFound(CustomAppException):
    status_code = ErrorsAppStatus.NOT_FOUND
    default_detail = "Note não encontrada"
    default_code = "note_not_found"
    app_code = AppCode.NOTE_NOT_FOUND

class NoteFailCreate(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao criar note"
    default_code = "create_note_failed"
    app_code = AppCode.NOTE_CREATE_FAILED  

class NoteFailList(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao listar notes"
    default_code = "list_notes_failed"
    app_code = AppCode.NOTE_LIST_FAILED

class NoteFailDetail(CustomAppException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Falha ao obter detalhes da note"
    default_code = "detail_note_failed"
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

class NotePermissionDenied(CustomAppException):
    status_code = ErrorsAppStatus.FORBIDDEN
    default_detail = "Permissão negada para acessar a note"
    default_code = "note_permission_denied"
    app_code = AppCode.NOTE_LIST_FAILED 