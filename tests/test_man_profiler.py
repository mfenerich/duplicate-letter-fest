import pytest

from src.profiling.memory_profiler import MemoryProfiler, MemoryStats


def test_memory_profiler() -> None:
    """Test that MemoryProfiler correctly tracks memory usage."""
    profiler = MemoryProfiler()
    
    # Start profiling
    profiler.start()
    
    # Allocate some memory to track
    big_list = [0] * 1000000  # Allocate a large list
    
    # Stop profiling and get stats
    stats = profiler.stop()
    
    # Verify stats
    assert isinstance(stats, MemoryStats)
    assert stats.current > 0
    assert stats.peak > 0
    assert stats.peak >= stats.current
    
    # Force garbage collection to clean up
    del big_list
