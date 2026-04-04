#!/usr/bin/env python3

import yaml
import logging
import os
import re
from datetime import datetime, timedelta, time

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
    while True:
        date_str = input("Enter the ride date (YYYY-MM-DD): ")
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


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
            if days_ahead == 0: days_ahead = 7
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

def main():
    # Check if 'DEBUG' environment variable exists    
    ride_attributes = load_ride_attributes("ride_attributes.yml")
    with open("ride_template.md", "r") as file:
        ride_template = file.read()

    # Get User Input for Date
    ride_date = get_date_input()

    # Get User Input for Discipline
    disciplines = ride_attributes["disciplines"]
    selected_discipline = select_from_list(disciplines, "discipline")

    # Get User Input for Start Time and Estimated Finish Time
    start_time = get_time_input("Enter the start time (14:30, 2 PM, 6p, 8am): ")
    finish_time = get_time_input("Enter the estimated finish time: ")

    # 4. Get User Input for Culture
    cultures = []
    for culture_collection in ride_attributes["ride_cultures"]:
        if culture_collection["discipline_id"] == selected_discipline["id"]:
            cultures = culture_collection["culture"]
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
    output_content = output_content.replace("RIDE_ATTRIBUTES_YML_CULTURES_NAME", selected_culture["name"])
    output_content = output_content.replace("RIDE_ATTRIBUTES_YML_CULTURES_URL", selected_culture["url"])
    #TODO if "approx_distance" is empty, then say "See routes" and don't append "km"
    if approx_distance.strip() == "":
        approx_distance = "See proposed route"
    else:
        approx_distance += " km"
    output_content = output_content.replace("DISTANCE", approx_distance)
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