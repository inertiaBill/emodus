import pytest
from datetime import datetime
from unittest.mock import patch
from emodus.gen import get_date_input

# We mock 'now' to be a Friday (index 4) to test weekday wrap-around
MOCK_NOW = datetime(2026, 4, 3) # April 3, 2026 is a Friday

@pytest.fixture
def mock_datetime_now(monkeypatch):
    class MockDateTime(datetime):
        @classmethod
        def now(cls):
            return MOCK_NOW
    # Patch the datetime class in the module where get_date_input lives
    monkeypatch.setattr("emodus.gen.datetime", MockDateTime)

def test_numeric_shortcuts(mock_datetime_now):
    """Test 0, 1, and 2 shortcuts."""
    with patch('builtins.input', side_effect=['0', '1', '2']):
        assert get_date_input() == datetime(2026, 4, 3) # Today
        assert get_date_input() == datetime(2026, 4, 4) # Tomorrow
        assert get_date_input() == datetime(2026, 4, 5) # Day After

def test_weekday_shortcuts(mock_datetime_now):
    """Test day of week shortcuts, specifically handling the 'future-only' logic."""
    # MOCK_NOW is Friday (4).
    # 'sa' should be tomorrow (+1)
    # 'th' should be next Thursday (+6)
    # 'f' (today) should be next Friday (+7)
    with patch('builtins.input', side_effect=['sa', 'th', 'f']):
        assert get_date_input() == datetime(2026, 4, 4)
        assert get_date_input() == datetime(2026, 4, 9)
        assert get_date_input() == datetime(2026, 4, 10)

def test_explicit_date(mock_datetime_now):
    """Test standard YYYY-MM-DD format."""
    with patch('builtins.input', return_value='2026-12-25'):
        assert get_date_input() == datetime(2026, 12, 25)

def test_invalid_then_valid(mock_datetime_now):
    """Test boundary: User enters garbage first, then a valid shortcut."""
    # This tests that the 'while True' loop actually loops
    with patch('builtins.input', side_effect=['garbage', '3', '0']):
        assert get_date_input() == datetime(2026, 4, 3)