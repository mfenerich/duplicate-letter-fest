"""
Command-line argument parsing for the Duplicate Letter Fest application.

This module handles the parsing of command-line arguments for
configuring the application behavior.
"""

import argparse


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments for the application.

    The function sets up argument parsing for various configuration options
    including verbosity level, animation speed, and input sources.

    Returns:
        argparse.Namespace: An object containing all the command line arguments.

    Example:
        >>> args = parse_args()
        >>> print(args.verbose)
        False
    """
    parser = argparse.ArgumentParser(
        description="Duplicate Letter Fest: spot repeated letters with fun balloon animations"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable debug logging of character counts"
    )
    parser.add_argument("--fast", action="store_true", help="Use faster balloon animation speed")
    parser.add_argument(
        "--height", type=int, default=12, help="Height (number of steps) for balloon float"
    )
    parser.add_argument(
        "--no-animation", action="store_true", help="Skip balloon animation and only show summary"
    )
    parser.add_argument(
        "--mem-profile",
        action="store_true",
        help="Show memory usage statistics for duplicate-finding algorithm",
    )
    parser.add_argument(
        "--input-file", type=str, help="Path to a file containing one input per line"
    )
    return parser.parse_args()
