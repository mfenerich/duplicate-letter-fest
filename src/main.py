"""
Duplicate Letter Fest: Spot repeated letters with fun balloon animations.

This module serves as the entry point for the application, orchestrating
the components that find duplicates and visualize them.
"""

import argparse
import logging
import time
from typing import List, Optional

from src.cli.parser import parse_args
from src.core.duplicate_finder import DuplicateFinder, HistogramDuplicateFinder
from src.core.result import DuplicateResult
from src.profiling.memory_profiler import MemoryProfiler
from src.ui.balloon_viz import BalloonVisualizer, NoAnimationVisualizer
from src.ui.visualizer import Visualizer


def get_inputs(args: argparse.Namespace) -> List[str]:
    """
    Get input strings from either file or interactive prompt.

    Args:
        args: Command line arguments

    Returns:
        A list of input strings to process
    """
    if args.input_file:
        try:
            with open(args.input_file, "r") as f:
                return [line.strip() for line in f if line.strip()]
        except Exception as e:
            logging.error(f"Error reading file: {e}")
            return []
    else:
        user_input = input("Enter text: ").strip()
        if not user_input:
            print("No input provided. Exiting.")
            return []
        return [user_input]


def process_input(
    input_text: str,
    finder: DuplicateFinder,
    visualizer: Visualizer,
    profiler: Optional[MemoryProfiler] = None,
) -> None:
    """
    Process a single input string to find duplicates and visualize results.

    Args:
        input_text: The string to analyze for duplicate characters
        finder: Component to find duplicates in the text
        visualizer: Component to visualize the results
        profiler: Optional component to profile memory usage
    """
    # Skip long text animation if needed
    should_skip_animation = len(input_text) > 30 and isinstance(visualizer, BalloonVisualizer)
    if should_skip_animation:
        print(f"Warning: input length {len(input_text)} > 30, skipping balloon animation.")

    # Start profiling if requested
    if profiler:
        profiler.start()

    # Find duplicates and measure time
    start = time.perf_counter()
    duplicates = finder.find_duplicates(input_text)
    duration = time.perf_counter() - start

    # Get memory stats if profiling
    memory_stats = None
    if profiler:
        stats = profiler.stop()
        memory_stats = (stats.current, stats.peak)

    # Create result object
    result = DuplicateResult(
        input_text=input_text, duplicates=duplicates, duration=duration, memory_stats=memory_stats
    )

    # Visualize the results with appropriate visualizer
    if should_skip_animation:
        NoAnimationVisualizer().visualize(result)
    else:
        visualizer.visualize(result)


def main() -> None:
    """
    Main entry point for the Duplicate Letter Fest application.

    This function orchestrates the application flow by:
    1. Parsing command line arguments
    2. Setting up logging
    3. Creating the appropriate components based on arguments
    4. Processing each input through the duplicate detection pipeline
    """
    # Parse arguments and set up logging
    args = parse_args()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format="%(message)s")

    # Create components based on arguments
    finder = HistogramDuplicateFinder()

    float_time = 0.05 if args.fast else 0.1

    # Explicitly type the visualizer variable to the interface type
    visualizer: Visualizer
    if args.no_animation:
        visualizer = NoAnimationVisualizer()
    else:
        visualizer = BalloonVisualizer(float_time, args.height)

    profiler = MemoryProfiler() if args.mem_profile else None

    # Get inputs and process each one
    inputs = get_inputs(args)
    for input_text in inputs:
        process_input(input_text, finder, visualizer, profiler)


if __name__ == "__main__":
    main()
