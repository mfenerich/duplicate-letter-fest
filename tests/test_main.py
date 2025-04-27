import pytest

from src.main import highlight_repeats_in_name


@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("", []),
        ("banana", ["a", "n"]),
        ("a b a", ["a"]),
        ("AaAa", ["A", "a"]),
    ],
)  # type: ignore[misc]
def test_highlight_repeats_param(input_text: str, expected: list[str]) -> None:
    """
    Test the highlight_repeats_in_name function with various inputs.

    Args:
        input_text: Input string to test.
        expected: Expected list of duplicate characters.
    """
    assert highlight_repeats_in_name(input_text) == expected


def test_type_error() -> None:
    """
    Test that highlight_repeats_in_name raises TypeError for non-string inputs.
    """
    with pytest.raises(TypeError):
        highlight_repeats_in_name(123)
