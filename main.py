"""
![CI](https://github.com/yourusername/duplicate-letter-fest/actions/workflows/ci.yml/badge.svg)
Duplicate Letter Fest: spot repeated letters with fun balloon animations
"""

import argparse
import logging
import time
import os
import random
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


def _print_balloons(duplicates: list[str], float_time: float = 0.1, height: int = 12) -> None:
    """
    Displays each duplicate character as a colorful ASCII balloon floating up,
    then shows all balloons side-by-side until the user exits.
    """
    colors = ['\033[31m', '\033[33m', '\033[32m', '\033[34m', '\033[35m']
    reset = '\033[0m'
    balloon_art = [
        "   .---.   ",
        "  /     \\  ",
        "  |  {}  |  ",
        "  \\     /  ",
        "   `---'   ",
        "     |     ",
        "     |     ",
    ]

    for idx, ch in enumerate(duplicates):
        color = colors[idx % len(colors)]
        art = [line.format(ch) for line in balloon_art]
        indent = ' ' * random.randint(0, 20)
        for step in range(height):
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n" * (height - step), end='')
            for line in art:
                print(f"{indent}{color}{line}{reset}")
            time.sleep(float_time)

    # After animations, show all balloons and pause briefly
    os.system('cls' if os.name == 'nt' else 'clear')
    max_art_height = len(balloon_art)
    all_arts = []
    for idx, ch in enumerate(duplicates):
        color = colors[idx % len(colors)]
        all_arts.append([f"{color}" + line.format(ch) + reset for line in balloon_art])

    for row in range(max_art_height):
        print("   ".join(art[row] for art in all_arts))
    print("\n🎈 All balloons are here! 🎈")
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')


def run_interactive(float_time: float, height: int, animate: bool) -> None:
    """
    CLI entry point: asks for input, optionally runs balloon animation, then displays summary.
    """
    print("🎈 Welcome to the Duplicate Letter Fest! 🎈")
    print("Type any word or name, and watch repeated letters pop up as balloons if enabled.")

    user_input = input("Enter text: ").strip()
    if not user_input:
        print("No input provided. Exiting.")
        return

    # measure processing time (excluding animation)
    start = time.perf_counter()
    duplicates = highlight_repeats_in_name(user_input)
    duration = time.perf_counter() - start

    if animate and duplicates:
        _print_balloons(duplicates, float_time, height)
    elif not duplicates:
        print("\nNo duplicate letters found! Nice and unique.")

    # always show summary
    print("\nSummary:")
    print(f"  Input text           : '{user_input}'")
    print(f"  Duplicates           : {', '.join(duplicates) if duplicates else 'None'}")
    print(f"  Algorithm time       : {duration:.6f} seconds")


def main():
    args = parse_args()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(message)s')

    float_time = 0.05 if args.fast else 0.1
    run_interactive(
        float_time=float_time,
        height=args.height,
        animate=not args.no_animation
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
