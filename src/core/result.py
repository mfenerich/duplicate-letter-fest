"""
Result data structures for the Duplicate Letter Fest application.

This module defines the data structures used to represent the results
of duplicate character analysis.
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class DuplicateResult:
    """
    Data class representing the result of duplicate character analysis.

    Attributes:
        input_text: The original input string that was analyzed.
        duplicates: List of characters that appear multiple times in the input.
        duration: Time in seconds that the algorithm took to run.
        memory_stats: Optional tuple of (current, peak) memory usage in bytes.
    """

    input_text: str
    duplicates: List[str]
    duration: float
    memory_stats: Optional[Tuple[int, int]] = None

    def get_summary_lines(self) -> List[str]:
        """
        Generate a list of formatted summary lines for this result.

        Returns:
            A list of strings containing formatted result information.
        """
        lines = [
            f"Input text             : '{self.input_text}'",
            f"Length                 : {len(self.input_text)} characters",
            f"Duplicates             : {', '.join(self.duplicates) if self.duplicates else 'None'}",
            f"Algorithm time         : {self.duration:.6f} seconds",
        ]
        if self.memory_stats:
            current, peak = self.memory_stats
            lines.append(f"Memory current usage   : {current/1024:.2f} KiB")
            lines.append(f"Memory peak usage      : {peak/1024:.2f} KiB")
        return lines
