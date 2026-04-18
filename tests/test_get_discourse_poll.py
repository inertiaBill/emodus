"""Test get_discourse_poll function"""

import unittest
from emodus.gen import get_discourse_poll

class TestGetDiscoursePoll(unittest.TestCase):
    """Test get_discourse_poll function"""
    def setUp(self):
        self.ride_attributes = {
            "templates": {
                "default_poll": "Default Poll Content"
            },
            "ride_groups": [
                {
                    "discipline_id": "road",
                    "group_collections": [
                        {
                            "name": "A Group",
                            "discourse_poll": "A Group Poll"
                        },
                        {
                            "name": "B Group",
                            "discourse_poll": "B Group Poll"
                        }
                    ]
                },
                {
                    "discipline_id": "gravel",
                    "group_collections": [
                        {
                            "name": "Gravel Grinders",
                            "discourse_poll": "Gravel Group Poll"
                        }
                    ]
                }
            ]
        }

    def test_get_discourse_poll_found(self):
        """Test case where discourse_poll is found for discipline and collection"""
        result = get_discourse_poll(self.ride_attributes, "road", "A Group")
        self.assertEqual(result, "A Group Poll")

    def test_get_discourse_poll_found_case_insensitive(self):
        """Test case with case-insensitive collection name"""
        result = get_discourse_poll(self.ride_attributes, "road", "a group")
        self.assertEqual(result, "A Group Poll")

    def test_get_discourse_poll_not_found_collection(self):
        """Test case where collection name is not found"""
        result = get_discourse_poll(self.ride_attributes, "road", "Non Existent Group")
        self.assertEqual(result, self.ride_attributes["templates"]["default_poll"])

    def test_get_discourse_poll_not_found_discipline(self):
        """Test case where discipline_id is not found"""
        result = get_discourse_poll(self.ride_attributes, "mtb", "Any Group")
        self.assertEqual(result, self.ride_attributes["templates"]["default_poll"])

    def test_get_discourse_poll_no_group_collections(self):
        """Test case with a discipline that has no group_collections"""
        ride_attributes_no_collections = {
            "templates": {
                "default_poll": "Default Poll Content"
            },
            "ride_groups": [
                {
                    "discipline_id": "road",
                    "group_collections": []
                }
            ]
        }
        result = get_discourse_poll(ride_attributes_no_collections, "road", "A Group")
        self.assertEqual(result, self.ride_attributes["templates"]["default_poll"])

    def test_get_discourse_poll_no_ride_groups(self):
        """Test case with no ride_groups at all"""
        ride_attributes_empty = {"ride_groups": [],
                                 "templates": {
                                     "default_poll": "Default Poll Content"
                                 }
                                }
        result = get_discourse_poll(ride_attributes_empty, "road", "A Group")
        self.assertEqual(result, self.ride_attributes["templates"]["default_poll"])

    def test_get_discourse_poll_missing_discourse_poll_key(self):
        """Test case where discourse_poll key is missing for a matching collection"""
        ride_attributes_missing_key = {
            "ride_groups": [
                {
                    "discipline_id": "road",
                    "group_collections": [
                        {
                            "name": "C Group",
                        }
                    ]
                }
            ],
            "templates": {
                "default_poll": "Default Poll Content"
            }
        }
        result = get_discourse_poll(ride_attributes_missing_key, "road", "C Group")
        self.assertEqual(result, self.ride_attributes["templates"]["default_poll"])

    def test_get_discourse_poll_default_poll_returned_if_not_found(self):
        """
        Test case where no specific poll is found
         
        Default_poll should be returned
        """
        result = get_discourse_poll(self.ride_attributes, "road", "Non Existent Collection")
        self.assertEqual(result, self.ride_attributes["templates"]["default_poll"])

    def test_get_discourse_poll_default_poll_returned_if_discipline_not_found(self):
        """
        Test case where discipline is not found
         
        Default_poll should be returned
        """
        result = get_discourse_poll(self.ride_attributes, "non_existent_discipline", "Any Group")
        self.assertEqual(result, self.ride_attributes["templates"]["default_poll"])
