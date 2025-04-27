import pytest

from src.core.duplicate_finder import HistogramDuplicateFinder


@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("", []),
        ("banana", ["a", "n"]),
        ("a b a", ["a"]),
        ("AaAa", ["A", "a"]),
    ],
)  # type: ignore[misc]
def test_histogram_duplicate_finder(input_text: str, expected: list[str]) -> None:
    """
    Test the HistogramDuplicateFinder with various inputs.

    Args:
        input_text: Input string to test.
        expected: Expected list of duplicate characters.
    """
    finder = HistogramDuplicateFinder()
    assert finder.find_duplicates(input_text) == expected


def test_type_error() -> None:
    """
    Test that HistogramDuplicateFinder raises TypeError for non-string inputs.
    """
    finder = HistogramDuplicateFinder()
    with pytest.raises(TypeError):
        # We're intentionally passing an invalid type to test error handling
        finder.find_duplicates(123)  # type: ignore[arg-type]
