from ..exceptions import BaseError


class JobManagerError(BaseError):
    """Base error raised in the QpiAi JobManager class"""


class AuthenticationError(JobManagerError):
    """Exception raised when authentication fails."""

    def __init__(
        self,
        message: str = "No API key found in the current user context. Please login using QpiAIQuantumAuth.login(...).",
    ):
        super().__init__(message)


class ExperimentError(JobManagerError):
    """Exception raised for experiment-related errors."""

    pass


class ExperimentNotFoundError(ExperimentError):
    """Exception raised when experiment is not found."""

    def __init__(self, experiment_name: str):
        super().__init__(
            f"Experiment '{experiment_name}' not found. Please create the experiment first."
        )


class InvalidExperimentResponseError(ExperimentError):
    """Exception raised when experiment API response is invalid."""

    def __init__(
        self,
        message: str = "Invalid response from experiments API: missing experiment_id",
    ):
        super().__init__(message)


class CircuitError(JobManagerError):
    """Exception raised for circuit-related errors in job manager."""

    pass


class CircuitNotFoundError(CircuitError):
    """Exception raised when circuit is not found."""

    def __init__(self, circuit_name: str):
        super().__init__(f"Could not find existing circuit '{circuit_name}' to update")


class CircuitUpdateError(CircuitError):
    """Exception raised when circuit update fails."""

    def __init__(self, error: Exception):
        super().__init__(f"Failed to update existing circuit: {error}")


class JobSubmissionError(JobManagerError):
    """Exception raised when job submission fails."""

    def __init__(
        self, message: str = "Job submission failed: no job ID found in response"
    ):
        super().__init__(message)


class JobStatusError(JobManagerError):
    """Exception raised when getting job status fails."""

    def __init__(self, job_id: str, error: Exception):
        super().__init__(f"Failed to get job status for {job_id}: {error}")


class InvalidResponseError(JobManagerError):
    """Exception raised when API response is invalid or missing required data."""

    pass
