from .base_exception_mock import (
    BaseTestException,
    CustomAppException,
    InputExceededCharacterLimit,
    InvalidEmailFormat,
    ExternalAPIError
)

from .user_exceptions_mock import (
    UserAlreadyExists,
    UserNotFound,
    UserFailCreate,
    UserFailList,
    UserFailDetail,
    UserFailUpdate,
    UserFailDelete,
    UserPermissionDenied
)

__all__ = [
    # Base
    'BaseTestException', 'CustomAppException', 'InputExceededCharacterLimit',
    'InvalidEmailFormat', 'ExternalAPIError',
    
    # User
    'UserAlreadyExists', 'UserNotFound', 'UserFailCreate', 'UserFailList',
    'UserFailDetail', 'UserFailUpdate', 'UserFailDelete', 'UserPermissionDenied']