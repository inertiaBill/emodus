import pytest
from unittest.mock import patch
from emodus.gen import get_start_location

# Sample data for testing
MOCK_LOCATIONS = [
    {
        "name": "Central Park",
        "description": "The big green one",
        "map_url": "https://maps.google.com/cp",
        "applicable_disciplines": ["Running", "Cycling"]
    },
    {
        "name": "Local Pool",
        "description": "Indoor heated",
        "map_url": "",
        "applicable_disciplines": ["Swimming"]
    }
]

@patch("emodus.gen.select_from_list")
def test_get_start_location_with_url(mock_select):
    """Test a known location that has a map URL."""
    # Simulate selecting 'Central Park'
    mock_select.return_value = MOCK_LOCATIONS[0]
    
    full_string, name = get_start_location(MOCK_LOCATIONS, "Running")
    
    assert name == "Central Park"
    assert full_string == "[Central Park](https://maps.google.com/cp) - The big green one"
    # Ensure the filtering worked (only Running/Cycling passed to select)
    args, _ = mock_select.call_args
    assert len(args[0]) == 2  # Central Park + "Other"

@patch("emodus.gen.select_from_list")
def test_get_start_location_no_url(mock_select):
    """Test a known location that does NOT have a map URL."""
    # Simulate selecting 'Local Pool'
    mock_select.return_value = MOCK_LOCATIONS[1]
    
    full_string, name = get_start_location(MOCK_LOCATIONS, "Swimming")
    
    assert name == "Local Pool"
    assert full_string == "Local Pool - Indoor heated"

@patch("emodus.gen.collect_multiline_input")
@patch("emodus.gen.select_from_list")
def test_get_start_location_other_custom(mock_select, mock_collect):
    """Test selecting 'Other' and providing custom multiline input."""
    # Simulate selecting 'Other'
    mock_select.return_value = {"name": "Other", "description": "", "map_url": ""}
    # Simulate user typing a custom location
    mock_collect.return_value = ["My House", "123 Lane"]
    
    full_string, name = get_start_location(MOCK_LOCATIONS, "Running")
    
    expected_name = "My House\n123 Lane"
    assert name == expected_name
    assert full_string == expected_name

def test_filtering_logic_no_matches():
    """Verify that if no disciplines match, only 'Other' is available."""
    with patch("emodus.gen.select_from_list") as mock_select:
        mock_select.return_value = {"name": "Other", "description": "", "map_url": ""}
        with patch("emodus.gen.collect_multiline_input", return_value=["Anywhere"]):
            get_start_location(MOCK_LOCATIONS, "Yoga")
            
            # Check that available_start_locations only contained 'Other'
            passed_list = mock_select.call_args[0][0]
            assert len(passed_list) == 1
            assert passed_list[0]["name"] == "Other"
