"""
Memory profiling functionality for the Duplicate Letter Fest application.

This module provides tools for tracking memory usage during the
duplicate finding process.
"""

import tracemalloc
from dataclasses import dataclass


@dataclass
class MemoryStats:
    """
    Data class for storing memory usage statistics.

    Attributes:
        current: Current memory usage in bytes.
        peak: Peak memory usage in bytes.
    """

    current: int
    peak: int


class MemoryProfiler:
    """
    Utility class for tracking memory usage.

    This class provides a simple interface for starting and stopping
    memory tracking using the tracemalloc module.
    """

    def start(self) -> None:
        """
        Start tracking memory allocations.
        """
        tracemalloc.start()

    def stop(self) -> MemoryStats:
        """
        Stop tracking memory allocations and return statistics.

        Returns:
            MemoryStats object containing current and peak memory usage.
        """
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return MemoryStats(current, peak)
