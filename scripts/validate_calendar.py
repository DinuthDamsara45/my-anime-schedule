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
    """Validate an ICS file for common issues and RFC 7986 compliance."""
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return False
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if file has proper structure
    if not content.startswith("BEGIN:VCALENDAR") or not content.endswith("END:VCALENDAR\n"):
        print("Error: File does not have proper VCALENDAR begin/end structure.")
        return False
    
    # Check for required properties (RFC 5545)
    required_props = ["VERSION", "PRODID", "CALSCALE", "METHOD"]
    for prop in required_props:
        if f"{prop}:" not in content:
            print(f"Warning: Missing recommended property '{prop}'.")
            
    # Check for RFC 7986 properties
    rfc7986_props = ["NAME", "DESCRIPTION", "LAST-MODIFIED", "URL", "REFRESH-INTERVAL", "SOURCE", "COLOR"]
    missing_modern_props = []
    for prop in rfc7986_props:
        if f"{prop}:" not in content and f"{prop};" not in content:
            missing_modern_props.append(prop)
    
    if missing_modern_props:
        print(f"Warning: Missing RFC 7986 properties: {', '.join(missing_modern_props)}")
        print("These properties improve compatibility with modern calendar clients like Outlook.")
    
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
        
        # Check for required event properties (RFC 5545)
        for prop in ["UID", "DTSTAMP", "DTSTART"]:
            if f"{prop}:" not in event:
                print(f"Error: Event {i+1} is missing required property '{prop}'.")
                errors += 1
        
        # Check for recommended properties (RFC 5545)
        for prop in ["SUMMARY", "DESCRIPTION"]:
            if f"{prop}:" not in event:
                print(f"Warning: Event {i+1} is missing recommended property '{prop}'.")
                warnings += 1
                
        # Check for RFC 7986/Outlook enhanced properties
        enhanced_props = ["CATEGORIES", "CREATED", "LAST-MODIFIED", "SEQUENCE", "TRANSP"]
        missing_enhanced = []
        for prop in enhanced_props:
            if f"{prop}:" not in event and f"{prop};" not in event:
                missing_enhanced.append(prop)
                
        if missing_enhanced:
            print(f"Warning: Event {i+1} missing enhanced properties: {', '.join(missing_enhanced)}")
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
    import os
    
    # Determine the path to main.ics relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_ics_path = os.path.join(os.path.dirname(script_dir), 'main.ics')
    
    parser = argparse.ArgumentParser(description='Validate an ICS calendar file.')
    parser.add_argument('--file', '-f', default=default_ics_path, 
                        help=f'Path to the ICS file (default: {default_ics_path})')
    
    args = parser.parse_args()
    
    print(f"Validating calendar file: {args.file}")
    success = validate_ics_file(args.file)
    sys.exit(0 if success else 1)
