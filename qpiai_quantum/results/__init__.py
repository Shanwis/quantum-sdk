"""
Results Module

Provides base classes and interfaces for quantum execution results.

This module defines a common interface for all result types in the SDK,
ensuring consistent API across different execution pathways.
"""

from .base_result import BaseQuantumResult

__all__ = ["BaseQuantumResult"]
