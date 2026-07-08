from ..exceptions import BaseError


class CircuitError(BaseError):
    """Base error raised in the QpiAi Circuit class"""


class InvalidCircuitArgumentError(CircuitError):
    """Exception raised when invalid arguments are provided to Circuit initialization."""

    def __init__(self, message: str = "Invalid arguments for Circuit initialization."):
        super().__init__(message)


class DuplicateQubitError(CircuitError):
    """Exception raised when duplicate qubits are detected."""

    def __init__(self, message: str = "Duplicate qubits are not allowed in the input."):
        super().__init__(message)


class MeasurementError(CircuitError):
    """Exception raised for measurement-related errors."""

    def __init__(self, message: str = "Circuit contains measurement operations."):
        super().__init__(message)


class RegisterError(CircuitError):
    """Exception raised for register-related errors."""

    pass


class InvalidRegisterSizeError(RegisterError):
    """Exception raised when register size is invalid."""

    def __init__(self, message: str = "Size of a register must be a positive integer."):
        super().__init__(message)


class InvalidRegisterNameError(RegisterError):
    """Exception raised when register name is invalid."""

    def __init__(self, message: str = "Register name must be a non-empty string."):
        super().__init__(message)
