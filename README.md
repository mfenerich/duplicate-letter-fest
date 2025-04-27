# Duplicate Letter Fest

![CI](https://github.com/mfenerich/duplicate-letter-fest/actions/workflows/ci.yml/badge.svg)
![Code Quality](https://github.com/mfenerich/duplicate-letter-fest/actions/workflows/code-quality.yml/badge.svg)

A playful CLI tool that detects repeated characters in strings and presents them with fun, flicker‑free ASCII balloon animations.

---

## Features

- **Interactive or Batch Mode**: Process a single input or multiple lines from a file.
- **Configurable Animation**: Adjust speed (`--fast`), height (`--height N`), or disable animation completely (`--no-animation`).
- **Verbose Debugging**: Enable `--verbose` to see per-character count logs.
- **Memory Profiling**: Use `--mem-profile` to display current and peak memory usage of the duplicate‑finding algorithm.
- **Non‑Overlapping Layout**: Balloons are evenly spaced to avoid overlap.
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

## Usage

### Interactive Mode

Run without arguments for a prompt:

```bash
python main.py
```

**Example:**
```
$ python main.py
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
python main.py --input-file inputs.txt
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
python main.py --fast --height 20 --mem-profile -v --input-file inputs.txt
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
   - Separate type stubs file (`main.pyi`) for enhanced IDE integration.
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

## Type Safety

This project implements robust type safety using Python's type annotation system:

- **Full Type Annotations**: All functions and methods are properly typed
- **Type Stubs File**: Separate `.pyi` file provides enhanced type information
- **Custom Type Aliases**: Specialized types like `CursesWindow` improve readability
- **Mypy Configuration**: Strict settings in `mypy.ini` enforce type safety
- **CI Integration**: Continuous type checking in GitHub Actions

To run type checking locally:

```bash
mypy main.py
```

If you encounter a "duplicate module" error with mypy, use one of these solutions:

1. **Quick fix**: Add `--exclude=stubs` to mypy arguments in your pre-commit configuration:
   ```yaml
   -   repo: https://github.com/pre-commit/mirrors-mypy
       rev: v1.15.0
       hooks:
       -   id: mypy
           additional_dependencies: [types-requests]
           args: [--explicit-package-bases, --exclude=stubs]
   ```

2. **Alternative approach**: Remove the `stubs/main.pyi` file and rely on the inline type annotations in `main.py`. Modern Python typing no longer requires separate `.pyi` stubs when code has thorough inline annotations.

Type annotations provide several benefits:
- Catch type errors before runtime
- Improved IDE integration with better autocompletion
- Self-documenting code with clear interfaces
- Enhanced maintainability for future contributors

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