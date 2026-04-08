import pytest
from datetime import datetime
from emodus.gen import format_group_paces  # Update with your actual filename

@pytest.fixture
def ride_attributes():
    return {
        'ride_groups': [
            {
                'discipline_id': 'gravel',
                'groups': [
                    {
                        'name': 'G1',
                        'estimated_moving_pace': {
                            'summer': '30km/h',
                            'winter': '25km/h'
                        }
                    },
                    {
                        'name': 'NoWinter',
                        'estimated_moving_pace': {
                            'summer': '20km/h'
                            # Missing winter pace
                        }
                    }
                ]
            }
        ]
    }

# Test the Date Logic
@pytest.mark.parametrize("ride_date, expected_pace", [
    (datetime(2026, 4, 1), "30km/h"),   # Start of Summer
    (datetime(2026, 7, 15), "30km/h"),  # Mid Summer
    (datetime(2026, 11, 15), "30km/h"), # End of Summer
    (datetime(2026, 11, 16), "25km/h"), # Start of Winter
    (datetime(2026, 1, 1), "25km/h"),   # Mid Winter
])
def test_seasonal_pace_selection(ride_attributes, ride_date, expected_pace):
    result = format_group_paces(ride_attributes, 'gravel', ['G1'], ride_date)
    assert f"G1: {expected_pace}" in result

# Test the Fallback Warning
def test_winter_fallback_warning(ride_attributes, capsys):
    winter_date = datetime(2026, 12, 25)
    # Testing 'NoWinter' group which has no winter pace defined
    result = format_group_paces(ride_attributes, 'gravel', ['NoWinter'], winter_date)

    # Check that it fell back to summer pace
    assert "NoWinter: 20km/h" in result

    # Check that the warning was printed to stdout
    captured = capsys.readouterr()
    assert "Warning: No winter pace found for NoWinter" in captured.out

# Test Multiple Groups
def test_multiple_groups_formatting(ride_attributes):
    ride_date = datetime(2026, 6, 1)
    result = format_group_paces(ride_attributes, 'gravel', ['G1', 'NoWinter'], ride_date)

    expected = "G1: 30km/h\nNoWinter: 20km/h"
    assert result == expected

# Test Missing Discipline
def test_invalid_discipline(ride_attributes):
    result = format_group_paces(ride_attributes, 'road', ['G1'], datetime(2026, 6, 1))
    assert "Error: Discipline 'road' not found" in result
