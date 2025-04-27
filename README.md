# Duplicate Letter Fest

![CI](https://github.com/mfenerich/duplicate-letter-fest/actions/workflows/ci.yml/badge.svg)

A playful CLI tool that detects repeated characters in strings and presents them with fun, flicker‑free ASCII balloon animations.

---

## Features

- **Interactive or Batch Mode**: Process a single input or multiple lines from a file.
- **Configurable Animation**: Adjust speed (`--fast`), height (`--height N`), or disable animation completely (`--no-animation`).
- **Verbose Debugging**: Enable `--verbose` to see per-character count logs.
- **Memory Profiling**: Use `--mem-profile` to display current and peak memory usage of the duplicate‑finding algorithm.
- **Non‑Overlapping Layout**: Balloons are evenly spaced to avoid overlap.
- **In‑Window Summary**: After animation, a summary of input, duplicates, time, and memory stats appears in the same terminal buffer.
- **Automated Testing & CI**: Parameterized Pytest suite and GitHub Actions CI integration.

---

## Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/duplicate-letter-fest.git
   cd duplicate-letter-fest
   ```
2. (Optional) Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies (if any):
   ```bash
   pip install -r requirements.txt
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
   - Built with Python’s `curses` library for flicker‑free rendering.
   - Evenly divides terminal width into slots to prevent balloon overlap.
   - Balloons rise over specified height and speed.
   - After animation, renders a summary in the same window.
5. **Testing & CI**:
   - Parameterized tests with `pytest.mark.parametrize` for coverage.
   - CI badge for GitHub Actions ensures tests run on every push.

---

## Running Tests

```bash
pytest
```

Make sure to activate your virtual environment before running tests.

---

## License

MIT