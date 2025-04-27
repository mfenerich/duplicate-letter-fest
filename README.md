# Duplicate Letter Fest

A playful CLI tool that detects repeated characters in strings and presents them with fun, flicker‑free ASCII balloon animations.

---

## Features

- **Interactive or Batch Mode**: Process a single input or multiple lines from a file.
- **Configurable Animation**: Adjust speed (`--fast`), height (`--height N`), or disable animation completely (`--no-animation`).
- **Verbose Debugging**: Enable `--verbose` to see per-character count logs.
- **Memory Profiling**: Use `--mem-profile` to display current and peak memory usage of the duplicate‑finding algorithm.
- **In‑Window Summary**: After animation, a summary of input, duplicates, time, and memory stats appears in the same terminal buffer.
- **Static Type Checking**: Comprehensive type annotations with mypy validation.
- **Code Quality Tools**: Integrated Black, isort, flake8, and pre-commit hooks.
- **Automated Testing & CI**: Parameterized Pytest suite and GitHub Actions CI integration.

---

## Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/mfenerich/duplicate-letter-fest.git
   cd duplicate-letter-fest
   ```
2. (Optional) Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. (Optional) Install pre-commit hooks:
   ```bash
   pip install pre-commit
   pre-commit install
   ```

---

## Docker

You can run Duplicate Letter Fest in a Docker container without installing Python or any dependencies locally.

### Building the Docker Image

```bash
docker build -t duplicate-letter-fest .
```

### Running with Docker

#### Interactive Mode

```bash
docker run -it duplicate-letter-fest
```

#### Batch Mode (File Input)

```bash
docker run -it -v "$(pwd)/inputs.txt:/app/inputs.txt:ro" duplicate-letter-fest --input-file inputs.txt
```

#### Using Flags with Docker

All command-line flags work with Docker:

```bash
docker run -it duplicate-letter-fest --fast --height 20 --mem-profile --no-animation
```

#### Notes on Terminal Support in Docker

- The `-it` flags are essential for interactive mode and animations
- If you experience issues with animations in Docker, try the `--no-animation` flag
- For best results, ensure your terminal window is sufficiently large

---

## Usage

### Interactive Mode

Run without arguments for a prompt:

```bash
python -m src.main
```

**Example:**
```
$ python -m src.main
🎈 Welcome to the Duplicate Letter Fest! 🎈
Type any word or name, and watch repeated letters pop up as balloons if enabled.
Enter text: balloon
```
_(Balloons rise in your terminal, then summary appears.)_


### Batch Mode (File Input)

Prepare a text file (`inputs.txt`) with one input per line:
```
hello
banana
supercalifragilisticexpialidocious
```

Run:
```bash
python -m src.main --input-file inputs.txt
```

Outputs each result (animation or summary) in sequence.


### Flags

- `-v`, `--verbose`  : Show debug logs of histogram counts
- `--fast`           : Decrease animation delay for faster floats
- `--height N`       : Set number of animation steps (default: 12)
- `--no-animation`   : Skip animations and print summary only
- `--mem-profile`    : Report memory usage of the duplicate‑finding step
- `--input-file FILE`: Process multiple inputs from `FILE`

**Combining Flags Example:**
```bash
python -m src.main --fast --height 20 --mem-profile -v --input-file inputs.txt
```

---

## Approach & Architecture

1. **Parsing & Configuration**: Uses `argparse` for flexible CLI options.
2. **Duplicate Detection**: Single-pass histogram with O(n) time and O(k) space (k = distinct chars). Skips whitespace.
3. **Performance Measurement**:
   - **Time**: `time.perf_counter()` around the core algorithm.
   - **Memory**: `tracemalloc` to capture current and peak usage if requested.
4. **Terminal Animation**:
   - Built with Python's `curses` library for flicker‑free rendering.
   - Evenly divides terminal width into slots to prevent balloon overlap.
   - Balloons rise over specified height and speed.
   - After animation, renders a summary in the same window.
5. **Type Safety**:
   - Comprehensive type annotations throughout the codebase.
   - Strict mypy configuration enforcing type checking.
6. **Code Quality**:
   - Black for consistent code formatting.
   - isort for organized imports.
   - flake8 for code linting and style checking.
   - pre-commit hooks to automate quality checks.
7. **Testing & CI**:
   - Parameterized tests with `pytest.mark.parametrize` for coverage.
   - CI pipeline includes test execution, type checking, and code quality verification.

---

## SOLID Architecture

The project implements SOLID principles for better maintainability, testability, and extensibility:

### Single Responsibility Principle (SRP)

Each class and module has a single, well-defined responsibility:

- **DuplicateFinder**: Focuses solely on finding duplicate characters
- **Visualizer**: Handles only the visualization of results
- **MemoryProfiler**: Manages memory tracking functionality
- **CLI Parser**: Handles command-line argument parsing
- **Result Class**: Encapsulates analysis results

### Open/Closed Principle (OCP)

Components are open for extension but closed for modification:

- New visualization methods can be added by implementing the `Visualizer` interface
- Different duplicate detection algorithms can extend the `DuplicateFinder` class
- Core functionality doesn't need to change to accommodate new features

### Liskov Substitution Principle (LSP)

All implementations can be substituted for their abstract base classes:

- `BalloonVisualizer` and `NoAnimationVisualizer` can be used interchangeably
- The high-level code doesn't need to know which specific implementation is being used

### Interface Segregation Principle (ISP)

Interfaces are focused and minimal:

- `Visualizer` interface has only what visualizers need
- `DuplicateFinder` interface focuses only on duplicate finding functionality
- No client is forced to depend on methods it doesn't use

### Dependency Inversion Principle (DIP)

High-level modules depend on abstractions, not concrete implementations:

- `process_input()` accepts interfaces rather than concrete classes
- Dependencies are injected rather than created internally
- Components are loosely coupled through interfaces

### Project Structure

The refactored code is organized into logical modules:

```
src/
├── __init__.py
├── main.py                  # Entry point
├── cli/                     # Command-line interface
│   ├── __init__.py
│   └── parser.py            # Command-line argument parsing
├── core/                    # Core functionality
│   ├── __init__.py
│   ├── duplicate_finder.py  # Duplicate detection logic
│   └── result.py            # Result data structures
├── profiling/               # Performance measurement
│   ├── __init__.py
│   └── memory_profiler.py   # Memory profiling functionality
└── ui/                      # User interface
    ├── __init__.py
    ├── summary.py           # Visualization interfaces for the Duplicate Letter Fest application.
    ├── visualizer.py        # Visualization interface
    └── balloon_viz.py       # Balloon visualization implementations
```

### Benefits of This Architecture

1. **Improved testability**: Each component can be tested in isolation
2. **Better maintainability**: Smaller, focused classes are easier to understand and modify
3. **Enhanced extensibility**: New features can be added with minimal changes to existing code
4. **Reduced coupling**: Components interact through abstractions, not direct dependencies
5. **Clear separation of concerns**: Each part of the system has a well-defined responsibility

---

## Type Safety

This project implements robust type safety using Python's type annotation system:

- **Full Type Annotations**: All functions and methods are properly typed
- **Custom Type Aliases**: Specialized types like `CursesWindow` improve readability
- **Mypy Configuration**: Strict settings in `mypy.ini` enforce type safety
- **CI Integration**: Continuous type checking in GitHub Actions

To run type checking locally:

```bash
mypy src
```
---

## Code Quality Tools

The project uses the following tools to ensure code quality:

### Black

The uncompromising code formatter that enforces consistent style.

```bash
# Format code
black .

# Check formatting without modifying
black --check .
```

### isort

Sorts imports alphabetically and automatically separated into sections.

```bash
# Sort imports
isort .

# Check import sorting
isort --check .
```

### flake8

Enforces style guide compliance and catches common errors.

```bash
# Lint code
flake8 .
```

### pre-commit

Runs quality checks before each commit to maintain high standards.

```bash
# Run on staged files
pre-commit run

# Run on all files
pre-commit run --all-files
```

---

## Running Tests

```bash
pytest
```

Make sure to activate your virtual environment before running tests.

---

## Requirements

- Python 3.9+
- Dependencies (see `requirements.txt`):
  - pytest
  - mypy
  - black
  - isort
  - flake8
  - pre-commit

---

## License

MIT
