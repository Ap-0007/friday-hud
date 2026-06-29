import pytest
from friday.tools.utils import word_count

def test_word_count_empty_string():
    """Test word_count with an empty string."""
    result = word_count("")
    assert result == {"characters": 0, "words": 0, "lines": 0}

def test_word_count_simple_text():
    """Test word_count with simple normal text."""
    text = "Hello world.\nThis is a test."
    result = word_count(text)
    assert result == {"characters": 28, "words": 6, "lines": 2}

def test_word_count_whitespace_only():
    """Test word_count with only whitespaces, tabs, and newlines."""
    text = "   \n  \t  \n"
    result = word_count(text)
    assert result == {"characters": 10, "words": 0, "lines": 2}

def test_word_count_single_word():
    """Test word_count with a single word."""
    text = "Friday"
    result = word_count(text)
    assert result == {"characters": 6, "words": 1, "lines": 1}

def test_word_count_multiple_spaces_between_words():
    """Test word_count with multiple spaces between words."""
    text = "Hello    world \t test"
    result = word_count(text)
    assert result == {"characters": 21, "words": 3, "lines": 1}

def test_word_count_punctuation_only():
    """Test word_count with only punctuation characters."""
    text = "!.,?;:"
    result = word_count(text)
    assert result == {"characters": 6, "words": 1, "lines": 1}

def test_word_count_trailing_leading_newlines():
    """Test word_count with trailing and leading newlines."""
    text = "\n\nHello world\n\n"
    result = word_count(text)
    # len("\n\nHello world\n\n") is 15
    # splitlines() on "\n\nHello world\n\n" gives ['', '', 'Hello world', ''] -> 4 lines
    # split() gives ['Hello', 'world'] -> 2 words
    assert result == {"characters": 15, "words": 2, "lines": 4}
