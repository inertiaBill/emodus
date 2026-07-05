from unittest.mock import patch
import pytest
# Adjust the import based on your package path
from emodus.gen import collect_multiline_input

@patch("builtins.input")
def test_collect_multiline_input_standard(mock_input):
    """Test entering a few regular lines followed by two blank lines."""
    # The iterator simulates the user typing line by line
    mock_input.side_effect = [
        "First line of text",
        "Second line of text",
        "",  # First blank
        ""   # Second blank (terminates input)
    ]

    result = collect_multiline_input()

    # The function appends the first blank line to preserve formatting,
    # but stops immediately when the second consecutive blank line is entered.
    assert result == ["First line of text", "Second line of text", ""]

@patch("builtins.input")
def test_collect_multiline_input_first_line_blank(mock_input):
    """Test entering a few regular lines followed by two blank lines."""
    # The iterator simulates the user typing line by line
    mock_input.side_effect = [
        "",  # Single blank line, don't terminate
        "Second line, but first of text",
        "",  # First blank
        ""   # Second blank (terminates input)
    ]

    result = collect_multiline_input()

    # The function appends the first blank line to preserve formatting,
    # but stops immediately when the second consecutive blank line is entered.
    assert result == ["", "Second line, but first of text", ""]


@patch("builtins.input")
def test_collect_multiline_input_preserves_internal_blanks(mock_input):
    """Test that isolated single blank lines are preserved within the text."""
    mock_input.side_effect = [
        "Header",
        "",  # Single blank line
        "Body paragraph",
        "",  # First blank line of double break
        ""   # Second blank line of double break
    ]

    result = collect_multiline_input()

    assert result == ["Header", "", "Body paragraph", ""]


@patch("builtins.input")
def test_collect_multiline_input_whitespace_lines(mock_input):
    """Test that lines containing only spaces are treated as blank lines."""
    mock_input.side_effect = [
        "Some text",
        "   ",  # Whitespace only
        "   ",  # Whitespace only (terminates the loop)
    ]

    result = collect_multiline_input()

    assert result == ["Some text", "   "]


@patch("builtins.input")
def test_collect_multiline_input_immediate_exit(mock_input):
    """Test that entering two blank lines immediately returns an empty list."""
    mock_input.side_effect = ["", ""]

    result = collect_multiline_input()

    # First blank is added, loop breaks on the second.
    assert result == [""]


@patch("builtins.print")
@patch("builtins.input")
def test_collect_multiline_input_custom_prompt(mock_input, mock_print):
    """Test that a custom prompt is printed when passed as an argument."""
    mock_input.side_effect = ["Text", "", ""]
    custom_prompt = "Custom message:\n"

    collect_multiline_input(prompt=custom_prompt)

    mock_print.assert_called_once_with(custom_prompt)
