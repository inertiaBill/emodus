import pytest
from unittest.mock import patch
from emodus.gen import get_group_name_as_list # Ensure this matches your filename

@pytest.fixture
def sample_data():
    """Provides a mock version of your YAML data."""
    return {
        'ride_groups': [
            {
                'discipline_id': 'gravel',
                'groups': [
                    {'name': 'G1'},
                    {'name': 'G2'},
                    {'name': 'G3'}
                ]
            }
        ]
    }

def test_valid_selection(sample_data):
    """Test that entering '1' returns the first group name in a list."""
    with patch('builtins.input', return_value='1'):
        result = get_group_name_as_list(sample_data, 'gravel')
        assert result == ['G1']

def test_valid_selection_middle(sample_data):
    """Test that entering '2' returns the correct middle group."""
    with patch('builtins.input', return_value='2'):
        result = get_group_name_as_list(sample_data, 'gravel')
        assert result == ['G2']

def test_invalid_discipline(sample_data):
    """Test that a non-existent discipline returns an empty list."""
    result = get_group_name_as_list(sample_data, 'road')
    assert result == []

def test_invalid_input_retry(sample_data):
    """
    Test that the function handles an invalid input (99) 
    followed by a valid one (3).
    """
    # side_effect feeds the inputs sequentially until the loop finishes
    with patch('builtins.input', side_effect=['99', '3']):
        result = get_group_name_as_list(sample_data, 'gravel')
        assert result == ['G3']

def test_non_integer_input_retry(sample_data):
    """Test that the function handles 'abc' followed by '1'."""
    with patch('builtins.input', side_effect=['abc', '1']):
        result = get_group_name_as_list(sample_data, 'gravel')
        assert result == ['G1']
