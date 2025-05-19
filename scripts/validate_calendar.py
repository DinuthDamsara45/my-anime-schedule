#!/usr/bin/env python3
"""
Validates the ICS calendar file by checking for common issues.
Run this script before committing changes to ensure the calendar is valid.
"""

import re
import sys
import os.path
from datetime import datetime

def validate_ics_file(file_path):
    """Validate an ICS file for common issues."""
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return False
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if file has proper structure
    if not content.startswith("BEGIN:VCALENDAR") or not content.endswith("END:VCALENDAR\n"):
        print("Error: File does not have proper VCALENDAR begin/end structure.")
        return False
    
    # Check for required properties
    required_props = ["VERSION", "PRODID", "CALSCALE", "METHOD"]
    for prop in required_props:
        if f"{prop}:" not in content:
            print(f"Warning: Missing recommended property '{prop}'.")
    
    # Check for events
    event_pattern = r"BEGIN:VEVENT(.*?)END:VEVENT"
    events = re.findall(event_pattern, content, re.DOTALL)
    
    if not events:
        print("Warning: Calendar contains no events.")
        return False
    
    errors = 0
    warnings = 0
    
    # Validate each event
    for i, event in enumerate(events):
        print(f"Checking event {i+1}...")
        
        # Check for required event properties
        for prop in ["UID", "DTSTAMP", "DTSTART"]:
            if f"{prop}:" not in event:
                print(f"Error: Event {i+1} is missing required property '{prop}'.")
                errors += 1
        
        # Check for recommended properties
        for prop in ["SUMMARY", "DESCRIPTION"]:
            if f"{prop}:" not in event:
                print(f"Warning: Event {i+1} is missing recommended property '{prop}'.")
                warnings += 1
        
        # Check date format (simple check)
        date_pattern = r"DT\w+:(\d{8}T\d{6}Z)"
        dates = re.findall(date_pattern, event)
        for date_str in dates:
            try:
                datetime.strptime(date_str, "%Y%m%dT%H%M%SZ")
            except ValueError:
                print(f"Error: Event {i+1} has invalid date format '{date_str}'.")
                errors += 1
    
    if errors > 0:
        print(f"\nValidation failed with {errors} errors and {warnings} warnings.")
        return False
    elif warnings > 0:
        print(f"\nValidation passed with {warnings} warnings.")
        return True
    else:
        print("\nValidation passed successfully!")
        return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate an ICS calendar file.')
    parser.add_argument('--file', '-f', default='../main.ics', 
                        help='Path to the ICS file (default: ../main.ics)')
    
    args = parser.parse_args()
    
    success = validate_ics_file(args.file)
    sys.exit(0 if success else 1)
