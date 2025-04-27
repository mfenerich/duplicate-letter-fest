"""Type stubs for the main module.

This file provides enhanced type annotations without duplicating full docstrings.
"""

import argparse
from typing import List, TypeVar
import _curses  # For the window type

# Type variable for generic functions
T = TypeVar('T')

# Type aliases for clarity
BalloonPosition = tuple[int, int, str, int]  # (y, x, character, color_index)
SummaryLines = List[str]
CursesWindow = _curses.window  # The proper type for curses window objects

def parse_args() -> argparse.Namespace: ...

def highlight_repeats_in_name(name: str) -> List[str]: ...

def _curses_balloons(
    stdscr: CursesWindow,
    duplicates: List[str],
    float_time: float,
    height: int,
    summary_lines: List[str]
) -> None: ...

def _print_balloons(
    duplicates: List[str],
    float_time: float,
    height: int,
    summary_lines: List[str]
) -> None: ...

def process_input(
    input_text: str,
    float_time: float,
    height: int,
    animate: bool,
    mem_profile: bool
) -> None: ...

def main() -> None: ...

# Constants
BALLOON_ART: List[str]  # Pre-defined ASCII balloon art template
