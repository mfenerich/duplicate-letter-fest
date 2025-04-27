from src.core.result import DuplicateResult


def test_result_creation() -> None:
    """Test that DuplicateResult is created correctly with the expected attributes."""
    result = DuplicateResult(
        input_text="hello", duplicates=["l"], duration=0.0001, memory_stats=(1000, 2000)
    )

    assert result.input_text == "hello"
    assert result.duplicates == ["l"]
    assert result.duration == 0.0001
    assert result.memory_stats == (1000, 2000)


def test_summary_lines_without_memory() -> None:
    """Test that summary lines are generated correctly without memory stats."""
    result = DuplicateResult(
        input_text="banana",
        duplicates=["a", "n"],
        duration=0.0002,
    )

    lines = result.get_summary_lines()
    assert len(lines) == 4  # Should have 4 lines without memory stats
    assert "Input text" in lines[0]
    assert "banana" in lines[0]
    assert "Length" in lines[1]
    assert "6" in lines[1]
    assert "Duplicates" in lines[2]
    assert "a, n" in lines[2]
    assert "Algorithm time" in lines[3]
    assert "0.000200" in lines[3]


def test_summary_lines_with_memory() -> None:
    """Test that summary lines are generated correctly with memory stats."""
    result = DuplicateResult(
        input_text="hello", duplicates=["l"], duration=0.0001, memory_stats=(1024, 2048)
    )

    lines = result.get_summary_lines()
    assert len(lines) == 6  # Should have 6 lines with memory stats
    assert "Memory current usage" in lines[4]
    assert "1.00 KiB" in lines[4]
    assert "Memory peak usage" in lines[5]
    assert "2.00 KiB" in lines[5]
