import argparse
import sys
from unittest.mock import patch

import pytest

from src.cli.parser import parse_args


def test_default_args() -> None:
    """Test that default arguments are set correctly."""
    with patch.object(sys, 'argv', ['main.py']):
        args = parse_args()
    
    assert not args.verbose
    assert not args.fast
    assert args.height == 12
    assert not args.no_animation
    assert not args.mem_profile
    assert args.input_file is None


def test_verbose_flag() -> None:
    """Test that verbose flag is set correctly."""
    with patch.object(sys, 'argv', ['main.py', '--verbose']):
        args = parse_args()
    
    assert args.verbose
    
    # Test short form
    with patch.object(sys, 'argv', ['main.py', '-v']):
        args = parse_args()
    
    assert args.verbose


def test_animation_flags() -> None:
    """Test that animation-related flags are set correctly."""
    with patch.object(sys, 'argv', ['main.py', '--fast', '--height', '20']):
        args = parse_args()
    
    assert args.fast
    assert args.height == 20
    
    with patch.object(sys, 'argv', ['main.py', '--no-animation']):
        args = parse_args()
    
    assert args.no_animation


def test_memory_profiling_flag() -> None:
    """Test that memory profiling flag is set correctly."""
    with patch.object(sys, 'argv', ['main.py', '--mem-profile']):
        args = parse_args()
    
    assert args.mem_profile


def test_input_file_arg() -> None:
    """Test that input file argument is set correctly."""
    with patch.object(sys, 'argv', ['main.py', '--input-file', 'inputs.txt']):
        args = parse_args()
    
    assert args.input_file == 'inputs.txt'
