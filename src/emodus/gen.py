#!/usr/bin/env python3

# eModus - a tool to make event preparation easy
# Copyright (C) 2026 inertiaBill

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>

import logging
import os
import re
from datetime import datetime, timedelta, time
import yaml

# Define the logger that was missing
logger = logging.getLogger("modus")

if os.getenv('DEBUG'):
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
else:
    logging.basicConfig(level=logging.INFO)

def load_ride_attributes(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def get_date_input():
    day_map = {'m': 0, 'tu': 1, 'w': 2, 'th': 3, 'f': 4, 'sa': 5, 'su': 6}

    while True:
        user_input = input("\nEnter date (0-2, m-su, or YYYY-MM-DD): ").strip().lower()

        target_date = None

        if user_input in ['0', '1', '2']:
            target_date = datetime.now() + timedelta(days=int(user_input))

        elif user_input in day_map:
            today = datetime.now()
            days_ahead = (day_map[user_input] - today.weekday()) % 7
            if days_ahead == 0:
                days_ahead = 7
            target_date = today + timedelta(days=days_ahead)

        if target_date:
            target_date = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
            # LOGGING: This only shows if the level is set to DEBUG
            logger.debug(f"Shortcut interpreted: {user_input} -> {target_date.strftime('%Y-%m-%d (%A)')}")
            return target_date

        try:
            return datetime.strptime(user_input, "%Y-%m-%d")
        except ValueError:
            print("Invalid input.")

def get_time_input(prompt_message):
    """
    Prompts the user to enter a time in various formats:
    - 24-hour: "14", "14:30"
    - 12-hour: "2:00 PM", "02:00 PM", "2 PM", "2p", "6 p", "8 am"
    - Returns a datetime.time object if valid, otherwise prompts again.
    """
    while True:
        user_input = input(prompt_message).strip().lower()

        if not user_input:
            print("Input cannot be empty. Please try again.")
            continue

        try:
            parsed_time = parse_flexible_time(user_input)
            return parsed_time

        except ValueError as e:
            print(f"Invalid time: {e}. Please try again.")

def parse_flexible_time(time_str):
    """
    Parses a flexible time string into a time object.
    Handles 24-hour and 12-hour formats with various abbreviations.
    """
    # Remove extra spaces and normalize
    time_str = ' '.join(time_str.split())

    # Patterns to detect AM/PM indicators
    # TODO Patterns with word break. Do we need that at all
    # am_pattern = r'\b(a|am|am\.?)\b'
    # pm_pattern = r'\b(p|pm|pm\.?)\b'
    am_pattern = r'(a|am|am\.?)'
    pm_pattern = r'(p|pm|pm\.?)'

    # Check for AM/PM indicator
    is_pm = bool(re.search(pm_pattern, time_str, re.IGNORECASE))
    is_am = bool(re.search(am_pattern, time_str, re.IGNORECASE))

    # Remove AM/PM indicators for parsing
    #clean_str = re.sub(r'\s*(a|am|p|pm)\.?\s*', '', time_str, flags=re.IGNORECASE).strip()
    clean_str = re.sub(r'\s*(am|a|pm|p)\.?\s*', '', time_str, flags=re.IGNORECASE).strip()

    # Try to extract hours and minutes
    time_match = re.match(r'^(\d{1,2})(?::(\d{2}))?(?::(\d{2}))?$', clean_str)

    if not time_match:
        raise ValueError("Could not parse time format. Expected HH:MM or HH")

    hour = int(time_match.group(1))
    minute = int(time_match.group(2)) if time_match.group(2) else 0

    # Validate ranges
    if hour < 0 or hour > 23:
        raise ValueError("Hour must be between 0 and 23")
    if minute < 0 or minute > 59:
        raise ValueError("Minute must be between 0 and 59")
    #if second < 0 or second > 59:
    #    raise ValueError("Second must be between 0 and 59")

    # Convert 12-hour to 24-hour if needed
    if is_pm and hour != 12:
        hour += 12
    elif is_am and hour == 12:
        hour = 0

    # If no AM/PM indicator and hour > 12, assume 24-hour format
    # If no AM/PM indicator and hour <= 12, assume AM (midnight to noon)
    # This handles "8" = 08:00 AM, "14" = 14:00 (24-hour)

    return time(hour, minute)

def collect_multiline_input(prompt="Enter text (press Enter twice to finish):\n"):
    """
    Collects multiple lines of input from the user.
    Stops when two consecutive blank lines are entered.
    
    Args:
        prompt: Optional message to display before input collection starts
        
    Returns:
        A list of strings containing all entered lines (excluding the two blank lines)
    """
    print(prompt)

    lines = []
    consecutive_blank = 0

    while True:
        line = input()

        # Check if line is blank (empty or whitespace only)
        if line.strip() == "":
            consecutive_blank += 1
            if consecutive_blank >= 2:
                break
            # Add the blank line to preserve formatting
            lines.append(line)
        else:
            consecutive_blank = 0
            lines.append(line)

    return lines

def select_from_list(items, item_name):
    print(f"\nSelect a {item_name}:")
    for i, item in enumerate(items):
        print(f"{i + 1}. {item["name"]}")
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(items):
                return items[choice - 1]
            else:
                print("Invalid choice. Please enter a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def build_culture_string(ride_attributes, discipline, culture):
    """
    Build the list of hyperlinks for the cultures of this ride
    """

    culture_string = ""
    culture_list = get_specific_collection_list(ride_attributes, discipline, culture, "member_cultures")

    #for culture in culture_list:
    for culture_item in ride_attributes["ride_cultures"]:
        if culture_item["discipline_id"] == discipline:
            for item in culture_item["culture"]:
                if item.get("name") in culture_list:
                    logger.debug(f"Culture: {item.get("name")}")
                    logger.debug(f"URL:     {item.get("url")}")
                    if culture_string.strip() != "":
                        culture_string += ", "
                    culture_string = culture_string + "[" +\
                        item.get("name") + "](" +\
                        item.get("url") + ")"
        break
    return culture_string

def get_specific_member_groups(data, discipline_id, collection_name):
    """
    Returns a list from a ride group collection
    member_groups for a specific discipline and collection name.
    """
    # Access the ride_groups list
    ride_groups = data.get('ride_groups', [])

    for ride in ride_groups:
        # Check if discipline matches
        if ride.get('discipline_id') == discipline_id:

            # Access the group_collections within that discipline
            collections = ride.get('group_collections', [])

            for collection in collections:
                # Check if the collection name matches (case-insensitive)
                current_name = collection.get('name', '')
                if current_name.strip().lower() == collection_name.strip().lower():
                    return collection.get('member_groups', [])

    # Return None or an empty list if no match is found
    return None

def get_specific_collection_list(ride_attributes, discipline_id, collection_name, list_name):
    """
    Returns a list from a ride group collection
    """
    # Access the ride_groups list

    logger.debug(f"Available keys: {ride_attributes.keys()}")
    for ride in ride_attributes["ride_groups"]:
        # Check if discipline matches
        if ride['discipline_id'] == discipline_id:

            logger.debug(f"Available keys: {ride.keys()}")
            # Access the group_collections within that discipline
            for collection in ride["group_collections"]:

                # Check if the collection name matches (case-insensitive)
                current_name = collection["name"]
                if current_name.strip().lower() == collection_name.strip().lower():
                    return collection[list_name]

    # Return None or an empty list if no match is found
    return None

def main():
    # Check if 'DEBUG' environment variable exists
    ride_attributes = load_ride_attributes("ride_attributes.yml")
    with open("ride_template.md", "r") as file:
        ride_template = file.read()

    print("eModus, Copyright (c) 2026, inertiaBill. Licensed under AGPLv3")

    # Get User Input for Date
    ride_date = get_date_input()

    # Get User Input for Discipline
    disciplines = ride_attributes["disciplines"]
    selected_discipline = select_from_list(disciplines, "discipline")

    # Get User Input for Start Time and Estimated Finish Time
    start_time = get_time_input("Enter the start time (14:30, 2 PM, 6p, 9am): ")
    finish_time = get_time_input("Enter the estimated finish time: ")

    # Get User Input for Culture
    cultures = []
    for culture_collection in ride_attributes["ride_cultures"]:
        if culture_collection["discipline_id"] == selected_discipline["id"]:
            cultures.extend(culture_collection["culture"])
            break

    for group_collection_item in ride_attributes["ride_groups"]:
        if group_collection_item["discipline_id"] == selected_discipline["id"]:
            for group in group_collection_item["group_collections"]:
                cultures.append({"name": group["name"], "url": ""}) # Assuming no URL for group collections or a default empty string
            break

    selected_culture = select_from_list(cultures, "culture") if cultures else {"name": "N/A", "url": ""}

    # Get User Input for Approximate Distance
    approx_distance = input("\nEnter the approximate distance in km: ")

    # Get User Input for Routes
    route_description = collect_multiline_input("\nEnter the route URLs with any descriptors (press Enter twice to finish):\n")

    # Get User Input for Ride Description
    ride_description_text = input("\nEnter the ride description: ")

    # Get User Input for Optional Notes
    ride_notes = input("\nEnter any optional notes: ")

    # Populate template
    day_of_week = ride_date.strftime("%A")
    month = ride_date.strftime("%B")
    day_of_month = ride_date.strftime("%d")
    year = ride_date.strftime("%Y")

    output_content = ride_template.replace("DAY_OF_WEEK", day_of_week)
    output_content = output_content.replace("MONTH", month)
    output_content = output_content.replace("DAY_NUMBER", day_of_month)
    output_content = output_content.replace("YEAR", year)
    output_content = output_content.replace("HH:MM AM_OR_PM", start_time.strftime("%I:%M %p"), 1)
    output_content = output_content.replace("HH:MM AM_OR_PM", finish_time.strftime("%I:%M %p"), 1)
    output_content = output_content.replace("RIDE_ATTRIBUTES_YML_DISCIPLINES_NAME", selected_discipline["name"])
    output_content = output_content.replace("RIDE_ATTRIBUTES_YML_DISCIPLINES_URL", selected_discipline["url"])
    if selected_culture["url"] == "":
        culture_string = build_culture_string(ride_attributes, selected_discipline["id"], selected_culture["name"])
    else:
        # It's an individual culture with a URL
        culture_string = "[" + selected_culture["name"] +\
            "](" + selected_culture["url"] + ")"
    #TODO if "approx_distance" is empty, then say "See routes" and don't append "km"
    #def build_culture_string(ride_attributes, discipline, culture):
    logger.debug(f"culture_string: {culture_string}")
    output_content = output_content.replace("RIDE_ATTRIBUTES_YML_CULTURES_INFO", culture_string)
    if approx_distance.strip() == "":
        approx_distance = "See proposed route"
    else:
        approx_distance += " km"
    output_content = output_content.replace("DISTANCE", approx_distance)
    output_content = output_content.replace("ESTIMATED_MOVING_AVERAGE", "TODO")
    output_content = output_content.replace("PROMPT_FOR_ROUTE", "\n".join(route_description))
    output_content = output_content.replace("PROMPT_FOR_DESCRIPTION", ride_description_text)
    output_content = output_content.replace("PROMPT_FOR_NOTES", ride_notes)
    output_content = output_content.replace("RIDE_ATTRIBUTES_YML_RIDE_FOOTER", ride_attributes["ride_footer"])

    print("\nGenerated Ride Description:\n")
    print(output_content)

    with open("generated_ride_description.md", "w") as output_file:
        output_file.write(output_content)
    print("\nGenerated ride description saved to generated_ride_description.md")

if __name__ == "__main__":
    main()
