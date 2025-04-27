"""
![CI](https://github.com/yourusername/duplicate-letter-fest/actions/workflows/ci.yml/badge.svg)
Duplicate Letter Fest: spot repeated letters with fun balloon animations (now using curses with non-overlapping layout and in-window summary)
Supports single input or batch processing from a file.
"""

import argparse
import logging
import time
import random
import tracemalloc
import curses
import pytest


def parse_args():
    parser = argparse.ArgumentParser(
        description="Duplicate Letter Fest: spot repeated letters with fun balloon animations"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable debug logging of character counts"
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Use faster balloon animation speed"
    )
    parser.add_argument(
        "--height",
        type=int,
        default=12,
        help="Height (number of steps) for balloon float"
    )
    parser.add_argument(
        "--no-animation",
        action="store_true",
        help="Skip balloon animation and only show summary"
    )
    parser.add_argument(
        "--mem-profile",
        action="store_true",
        help="Show memory usage statistics for duplicate-finding algorithm"
    )
    parser.add_argument(
        "--input-file",
        type=str,
        help="Path to a file containing one input per line"
    )
    return parser.parse_args()


def highlight_repeats_in_name(name: str) -> list[str]:
    """
    Given a string, returns a list of non-space characters that appear more than once.
    Raises TypeError if the input is not a string.
    """
    if not isinstance(name, str):
        raise TypeError(f"Expected name as str, got {type(name).__name__}")

    histogram: dict[str, int] = {}
    for ch in name:
        if ch.isspace():
            continue
        histogram[ch] = histogram.get(ch, 0) + 1
        logging.debug(f"Count for '{ch}': {histogram[ch]}")

    return [ch for ch, cnt in histogram.items() if cnt > 1]

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


def _curses_balloons(stdscr, duplicates: list[str], float_time: float, height: int, summary_lines: list[str]):
    """
    Internal: Use curses to animate balloons smoothly with non-overlapping positions and show summary in-window.
    """
    curses.curs_set(0)
    stdscr.nodelay(True)
    curses.start_color()
    curses.use_default_colors()
    # initialize color pairs
    for i, color in enumerate((curses.COLOR_RED, curses.COLOR_YELLOW, curses.COLOR_GREEN, curses.COLOR_BLUE, curses.COLOR_MAGENTA), start=1):
        curses.init_pair(i, color, -1)

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

    # rising animation
    for step in range(height):
        stdscr.erase()
        for (y0, x0, ch, idx) in positions:
            y = y0 - step
            color_pair = curses.color_pair((idx % 5) + 1)
            for dy, line in enumerate(BALLOON_ART):
                if 0 <= y + dy < max_y and 0 <= x0 < max_x:
                    stdscr.addstr(y + dy, x0, line.format(ch), color_pair)
        stdscr.refresh()
        time.sleep(float_time)

    # static display with summary
    stdscr.erase()
    # draw balloons at final positions
    for (y0, x0, ch, idx) in positions:
        color_pair = curses.color_pair((idx % 5) + 1)
        for dy, line in enumerate(BALLOON_ART):
            if y0 + dy < max_y and x0 < max_x:
                stdscr.addstr(y0 + dy, x0, line.format(ch), color_pair)
    # draw summary below balloons
    for i, line in enumerate(summary_lines):
        stdscr.addstr(y_start + len(BALLOON_ART) + i + 1, 0, line)
    stdscr.refresh()

    # wait for any key before ending
    stdscr.nodelay(False)
    stdscr.getkey()


def _print_balloons(duplicates: list[str], float_time: float, height: int, summary_lines: list[str]) -> None:
    """
    Wrapper to run the curses-based balloon animation with summary.
    """
    curses.wrapper(_curses_balloons, duplicates, float_time, height, summary_lines)


def process_input(input_text: str, float_time: float, height: int, animate: bool, mem_profile: bool) -> None:
    """
    Processes a single input: finds duplicates, optionally profiles memory,
    runs animation unless skipped (showing summary in-window), else prints summary.
    """
    if len(input_text) > 30 and animate:
        print(f"Warning: input length {len(input_text)} > 30, skipping balloon animation.")
        animate = False

    if mem_profile:
        tracemalloc.start()

    start = time.perf_counter()
    duplicates = highlight_repeats_in_name(input_text)
    duration = time.perf_counter() - start

    if mem_profile:
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    summary_lines = [
        f"Input text             : '{input_text}'",
        f"Length                 : {len(input_text)} characters",
        f"Duplicates             : {', '.join(duplicates) if duplicates else 'None'}",
        f"Algorithm time         : {duration:.6f} seconds"
    ]
    if mem_profile:
        summary_lines.append(f"Memory current usage   : {current/1024:.2f} KiB")
        summary_lines.append(f"Memory peak usage      : {peak/1024:.2f} KiB")

    if animate and duplicates:
        _print_balloons(duplicates, float_time, height, summary_lines)
    else:
        # no-animation or no duplicates: print summary to console
        print("\nSummary:")
        for line in summary_lines:
            print(f"  {line}")
        print("\n---\n")


def main():
    args = parse_args()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(message)s')

    float_time = 0.05 if args.fast else 0.1
    animate = not args.no_animation

    inputs = []
    if args.input_file:
        try:
            with open(args.input_file, 'r') as f:
                inputs = [line.strip() for line in f if line.strip()]
        except Exception as e:
            logging.error(f"Error reading file: {e}")
            return
    else:
        user_input = input("Enter text: ").strip()
        if not user_input:
            print("No input provided. Exiting.")
            return
        inputs = [user_input]

    for input_text in inputs:
        process_input(
            input_text, float_time, args.height, animate, args.mem_profile
        )


if __name__ == "__main__":
    main()


# ------------------- Tests -------------------
# To run tests: pytest

@pytest.mark.parametrize("input_text,expected", [
    ("", []),
    ("banana", ["a", "n"]),
    ("a b a", ["a"]),
    ("AaAa", ["A", "a"]),
])
def test_highlight_repeats_param(input_text, expected):
    assert highlight_repeats_in_name(input_text) == expected


def test_type_error():
    with pytest.raises(TypeError):
        highlight_repeats_in_name(123)  # type: ignore
