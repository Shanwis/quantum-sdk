class BaseError(Exception):
    """
    Base exception for all QpiAI Quantum SDK errors.

    This is the root exception class that all other exceptions in the SDK inherit from.
    It provides a standard interface for error handling across all modules.

    Args:
        *message: Variable length message strings that will be concatenated to form the error message.

    Example:
        >>> raise BaseError("An error occurred: ", "Invalid input")
        BaseError: An error occurred: Invalid input
    """

    def __init__(self, *message):
        """
        Initialize the BaseError with a concatenated message.

        Args:
            *message: Variable length message strings to concatenate.
        """
        super().__init__("".join(message))
        self.message = "".join(message)

    def __str__(self):
        """Return the error message as a string."""
        return self.message
