"""
Core duplicate detection functionality for the Duplicate Letter Fest application.

This module provides interfaces and implementations for finding duplicate
characters in input strings.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List


class DuplicateFinder(ABC):
    """
    Abstract base class defining the interface for duplicate finding strategies.

    Implementations of this interface can use different algorithms to find
    duplicate characters in a string.
    """

    @abstractmethod
    def find_duplicates(self, text: str) -> List[str]:
        """
        Find non-space characters that appear more than once in the input string.

        Args:
            text: The input string to analyze for duplicate characters.

        Returns:
            A list of characters that appear more than once in the input string,
            excluding spaces.

        Raises:
            TypeError: If the input is not a string.
        """
        pass


class HistogramDuplicateFinder(DuplicateFinder):
    """
    Finds duplicates using a character frequency histogram approach.

    This implementation builds a histogram of character occurrences in a single
    pass and returns characters that appear multiple times.
    """

    def find_duplicates(self, text: str) -> List[str]:
        """
        Find non-space characters that appear more than once in the input string.

        This implementation creates a histogram of character occurrences and returns
        a list of characters that appear multiple times, excluding spaces.

        Args:
            text: The input string to analyze for duplicate characters.

        Returns:
            A list of characters that appear more than once in the input string,
            excluding spaces.

        Raises:
            TypeError: If the input is not a string.

        Example:
            >>> finder = HistogramDuplicateFinder()
            >>> finder.find_duplicates("banana")
            ['a', 'n']
            >>> finder.find_duplicates("hello world")
            ['l', 'o']
        """
        if not isinstance(text, str):
            raise TypeError(f"Expected text as str, got {type(text).__name__}")

        histogram: Dict[str, int] = {}
        for ch in text:
            if ch.isspace():
                continue
            histogram[ch] = histogram.get(ch, 0) + 1
            logging.debug(f"Count for '{ch}': {histogram[ch]}")

        return [ch for ch, cnt in histogram.items() if cnt > 1]
