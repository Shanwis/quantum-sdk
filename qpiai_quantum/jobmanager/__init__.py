"""
QPIAI Quantum SDK Job Manager

This module provides job lifecycle management functionality for quantum circuit execution,
including job submission, status monitoring, and results retrieval.

Classes:
    JobManager: Main class for managing quantum job operations
    Backend: Backend enumeration for quantum execution
    ExecutionEngine: Modern execution bridge
    JobResult: Result class for quantum job execution
    SSEResultHandler: SSE handler for job monitoring
"""

from .jobmanager import JobManager
from .backend import Backend, ResolvedBackend
from .execution_engine import ExecutionEngine
from .job_result import JobResult
from .sse_handler import SSEResultHandler

__all__ = [
    "JobManager",
    "Backend",
    "ResolvedBackend",
    "ExecutionEngine",
    "JobResult",
    "SSEResultHandler",
]
