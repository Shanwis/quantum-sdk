from ..exceptions import BaseError


class AuthError(BaseError):
    """
    Base class for exceptions in the auth module.
    """


class UserNotFoundError(AuthError):
    """
    Exception raised when the API key is not found in the environment.
    """

    def __init__(self):
        super().__init__("API Key is not available. Please login using an API Key.")


class APIKeyInvalidError(AuthError):
    """
    Exception raised when the API key is invalid.
    """

    def __init__(self, message: str = "The provided API key is not valid."):
        super().__init__(message)


class APIKeyExpiredError(APIKeyInvalidError):
    """
    Exception raised when the API key is expired.
    """

    def __init__(self):
        super().__init__("API key is expired.")


class APIKeyRevokedError(APIKeyInvalidError):
    """
    Exception raised when the API key is revoked.
    """

    def __init__(self):
        super().__init__("API key is revoked.")


class APIKeyEmptyError(APIKeyInvalidError):
    """
    Exception raised when the API key is empty.
    """

    def __init__(self):
        super().__init__("API key cannot be empty.")
