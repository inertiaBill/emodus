import pytest
import re
from datetime import time
from unittest.mock import patch
# Replace 'your_script' with the actual filename where your code lives
from emodus.gen import parse_flexible_time, get_time_input

@pytest.mark.parametrize("input_str, expected", [
    ("14", time(14, 0)),            # 24-hour hour only
    ("14:30", time(14, 30)),        # 24-hour full
    ("2:00 PM", time(14, 0)),       # 12-hour space AM/PM
    ("2p", time(14, 0)),            # Abbreviated PM
    ("8 am", time(8, 0)),           # 12-hour lowercase
    ("12:30 AM", time(0, 30)),      # Midnight case
    ("12:00 PM", time(12, 0)),      # Noon case
    ("6 p", time(18, 0)),           # Space and single letter
])
def test_parse_flexible_time_valid(input_str, expected):
    assert parse_flexible_time(input_str) == expected

@pytest.mark.parametrize("invalid_input", [
    "25:00",      # Hour out of range
    "12:60",      # Minute out of range
    "abc",        # Not a time
    "12:34:56:78" # Too many segments
])
def test_parse_flexible_time_errors(invalid_input):
    with pytest.raises(ValueError):
        parse_flexible_time(invalid_input)

def test_get_time_input_success(monkeypatch):
    # Simulate user typing "14:30"
    monkeypatch.setattr('builtins.input', lambda _: "14:30")
    result = get_time_input("Enter time: ")
    assert result == time(14, 30)

def test_get_time_input_retry_on_invalid(monkeypatch, capsys):
    # Simulate: 1. Empty input, 2. Invalid string, 3. Valid time
    inputs = iter(["", "not-a-time", "2 PM"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    result = get_time_input("Enter time: ")
    
    # Check that it eventually returned the correct time
    assert result == time(14, 0)
    
    # Check that the error messages were printed to the console
    captured = capsys.readouterr()
    assert "Input cannot be empty" in captured.out
    assert "Invalid time" in captured.out