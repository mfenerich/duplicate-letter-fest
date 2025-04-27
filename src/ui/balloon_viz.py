"""
Balloon visualization implementations for the Duplicate Letter Fest application.

This module provides concrete visualizer implementations that show duplicates
as animated balloons in the terminal or as a simple text summary.
"""

import curses
import random
import time
from typing import List, Tuple

from src.core.result import DuplicateResult
from src.ui.visualizer import Visualizer

# Type alias for the curses window
CursesWindow = curses.window

# Pre-defined ASCII balloon art
BALLOON_ART = [
    "   .---.   ",
    "  /     \\  ",
    "  |  {}  |  ",
    "  \\     /  ",
    "   `---'   ",
    "     |     ",
    "     |     ",
]


class BalloonVisualizer(Visualizer):
    """
    Visualizer that displays duplicate characters as animated balloons.

    This visualizer uses the curses library to create animated ASCII balloon
    visualizations in the terminal.
    """

    def __init__(self, float_time: float, height: int):
        """
        Initialize the balloon visualizer.

        Args:
            float_time: Time in seconds between animation frames.
            height: Number of vertical steps for the balloon animation.
        """
        self.float_time = float_time
        self.height = height

    def visualize(self, result: DuplicateResult) -> None:
        """
        Visualize the duplicates as animated balloons using curses.

        Args:
            result: The result object containing duplicates to visualize.
        """
        if not result.duplicates:
            # No duplicates to show - just print the summary
            print("\nSummary:")
            for line in result.get_summary_lines():
                print(f"  {line}")
            print("\n---\n")
            return

        # Use curses for the animation
        curses.wrapper(self._curses_balloons, result.duplicates, result.get_summary_lines())

    def _curses_balloons(
        self,
        stdscr: CursesWindow,
        duplicates: List[str],
        summary_lines: List[str],
    ) -> None:
        """
        Create animated balloons using the curses library.

        Args:
            stdscr: The curses standard screen window object.
            duplicates: List of characters to display in balloons.
            summary_lines: List of strings to display as summary after animation.
        """
        self._setup_curses(stdscr)
        positions = self._calculate_balloon_positions(stdscr, duplicates, summary_lines)
        self._animate_balloons(stdscr, positions)
        self._display_final_screen(stdscr, positions, summary_lines)
        self._wait_for_key(stdscr)

    def _setup_curses(self, stdscr: CursesWindow) -> None:
        """Set up the curses environment for animation."""
        curses.curs_set(0)
        stdscr.nodelay(True)
        curses.start_color()
        curses.use_default_colors()

        # Initialize color pairs
        for i, color in enumerate(
            (
                curses.COLOR_RED,
                curses.COLOR_YELLOW,
                curses.COLOR_GREEN,
                curses.COLOR_BLUE,
                curses.COLOR_MAGENTA,
            ),
            start=1,
        ):
            curses.init_pair(i, color, -1)

    def _calculate_balloon_positions(
        self, stdscr: CursesWindow, duplicates: List[str], summary_lines: List[str]
    ) -> List[Tuple[int, int, str, int]]:
        """Calculate the starting positions for each balloon."""
        max_y, max_x = stdscr.getmaxyx()
        num = len(duplicates)
        balloon_width = len(BALLOON_ART[0])
        slot_width = max_x // num if num else max_x

        positions = []
        y_start = max_y - len(BALLOON_ART) - len(summary_lines) - 2
        for idx, ch in enumerate(duplicates):
            min_x = idx * slot_width
            max_x_slot = min_x + slot_width - balloon_width
            x = random.randint(min_x, max_x_slot) if max_x_slot > min_x else min_x
            positions.append((y_start, x, ch, idx))

        return positions

    def _animate_balloons(
        self, stdscr: CursesWindow, positions: List[Tuple[int, int, str, int]]
    ) -> None:
        """Animate the balloons rising to their final positions."""
        max_y, max_x = stdscr.getmaxyx()
        for step in range(self.height):
            stdscr.erase()
            for y0, x0, ch, idx in positions:
                y = y0 - step
                color_pair = curses.color_pair((idx % 5) + 1)
                for dy, line in enumerate(BALLOON_ART):
                    if 0 <= y + dy < max_y and 0 <= x0 < max_x:
                        stdscr.addstr(y + dy, x0, line.format(ch), color_pair)
            stdscr.refresh()
            time.sleep(self.float_time)

    def _display_final_screen(
        self,
        stdscr: CursesWindow,
        positions: List[Tuple[int, int, str, int]],
        summary_lines: List[str],
    ) -> None:
        """Display the final screen with static balloons and summary."""
        max_y, max_x = stdscr.getmaxyx()
        stdscr.erase()

        # Draw balloons at final positions
        for y0, x0, ch, idx in positions:
            color_pair = curses.color_pair((idx % 5) + 1)
            for dy, line in enumerate(BALLOON_ART):
                if y0 + dy < max_y and x0 < max_x:
                    stdscr.addstr(y0 + dy, x0, line.format(ch), color_pair)

        # Draw summary below balloons
        y_start = max_y - len(BALLOON_ART) - len(summary_lines) - 2
        for i, line in enumerate(summary_lines):
            stdscr.addstr(y_start + len(BALLOON_ART) + i + 1, 0, line)
        stdscr.refresh()

    def _wait_for_key(self, stdscr: CursesWindow) -> None:
        """Wait for any key press before ending the animation."""
        stdscr.nodelay(False)
        stdscr.getkey()


class NoAnimationVisualizer(Visualizer):
    """
    Visualizer that simply prints a text summary without animation.

    This visualizer is used when animation is disabled or for inputs
    that are too long for effective balloon visualization.
    """

    def visualize(self, result: DuplicateResult) -> None:
        """
        Print a text summary of the duplicate analysis results.

        Args:
            result: The result object containing duplicates and other information.
        """
        print("\nSummary:")
        for line in result.get_summary_lines():
            print(f"  {line}")
        print("\n---\n")
