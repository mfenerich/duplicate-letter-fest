"""
Visualization interfaces for the Duplicate Letter Fest application.

This module defines the core visualization interfaces that allow
different visualization strategies to be implemented.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Protocol, Tuple

from src.core.result import DuplicateResult


class Visualizer(ABC):
    """
    Abstract base class defining the interface for result visualization.

    Implementations of this interface can use different visualization strategies
    to display the results of duplicate character analysis.
    """

    @abstractmethod
    def visualize(self, result: DuplicateResult) -> None:
        """
        Visualize the results of duplicate character analysis.

        Args:
            result: The result object containing input text, duplicates found,
                   processing time, and optional memory stats.
        """
        pass
