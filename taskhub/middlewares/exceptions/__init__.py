from taskhub.middlewares.exceptions.base_exception_handler import custom_exception_handler, InputExceededCharacterLimit, InvalidEmailFormat, InputEmptyOrNone

from taskhub.middlewares.exceptions.user.user_exception_handler import (
    UserAlreadyExists,
    UserFailCreate,
    UserFailDelete,
    UserFailList,
    UserFailUpdate,
    UserNotFound,
    UserPermissionDenied,
    UserFailDetail,
)
from taskhub.middlewares.exceptions.task.task_exception_handler import (
    TaskAlreadyExists,
    TaskFailCreate,
    TaskFailDelete,
    TaskFailList,
    TaskFailUpdate,
    TaskNotFound,
    TaskPermissionDenied,
    TaskFailDetail,
    TaskInvalidStatus,
    TaskInvalidPriority,
    TaskFailAddedUser,
    TaskFailRemoveUser
)
from taskhub.middlewares.exceptions.repository_permission.repository_permission_exception_handler import (
    RepositoryPermissionAlreadyExists,
    RepositoryPermissionFailCreate,
    RepositoryPermissionFailDelete,
    RepositoryPermissionFailUpdate,
    RepositoryPermissionNotFound,
    InvalidRepositoryAccess,
    RepositoryPermissionFailList,
    RepositoryPermissionFailDetail,
    RepositoryPermissionFailAddedUser,
    RepositoryPermissionFailRemoveUser
)
from taskhub.middlewares.exceptions.repository.repository_exception_handler import (
    RepositoryAlreadyExists,
    RepositoryFailCreate,
    RepositoryFailDelete,
    RepositoryFailList,
    RepositoryFailUpdate,
    RepositoryNotFound,

)
from taskhub.middlewares.exceptions.note.note_exception_handler import (
    NoteAlreadyExists,
    NoteFailCreate,
    NoteFailDelete,
    NoteFailList,
    NoteFailUpdate,
    NoteNotFound,
    NotePermissionDenied
)
from taskhub.middlewares.exceptions.content_repository.content_repository_exception_handler import (
    ContentRepositoryAlreadyExists,
    ContentRepositoryFailCreate,
    ContentRepositoryFailDelete,
    ContentRepositoryFailList,
    ContentRepositoryFailUpdate,
    ContentRepositoryNotFound,
    ContentRepositoryPermissionDenied,
    ContentRepositoryFailDetail
)
from taskhub.middlewares.exceptions.enterprise.enterprise_exception_handler import (
    EnterpriseAlreadyExists,
    EnterpriseFailCreate,
    EnterpriseFailDelete,
    EnterpriseFailList,
    EnterpriseFailUpdate,
    EnterpriseNotFound,
    EnterprisePermissionDenied,
    EnterpriseFailAddedUser,
    EnterpriseFailDetail,
    EnterpriseFailRemoveUser
)
from taskhub.middlewares.exceptions.chat.chat_exception_handler import (
    ChatAlreadyExists,
    ChatFailCreate,
    ChatFailDelete,
    ChatFailList,
    ChatFailUpdate,
    ChatNotFound,
)