#!/usr/bin/env python3
"""
Final Cleanup Script

This script performs a final cleanup of the calendar file:
1. Removes duplicate IMAGE properties
2. Corrects any malformed LAST-MODIFIED entries
3. Updates timestamps to current time
4. Validates the final calendar format

Usage:
  python final_cleanup.py [--ics-file main.ics]
"""

import os
import sys
import re
import argparse
import datetime
from pathlib import Path

def cleanup_calendar(ics_file):
    """Perform final cleanup of the calendar file."""
    print(f"Performing final cleanup of {ics_file}...")
    
    # Read the calendar file
    with open(ics_file, 'r') as f:
        content = f.read()
    
    # 1. Fix malformed LAST-MODIFIED entries (like P250519T164757Z)
    malformed_pattern = r'\nP\d+T\d+Z\n'
    content = re.sub(malformed_pattern, '\n', content)
    
    # 2. Fix duplicate IMAGE properties
    # Split by events
    parts = re.split(r'(BEGIN:VEVENT.*?END:VEVENT)', content, flags=re.DOTALL)
    
    fixed_parts = []
    event_count = 0
    fixed_count = 0
    
    # Current UTC time for updating LAST-MODIFIED
    now = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    
    for part in parts:
        if 'BEGIN:VEVENT' in part:
            event_count += 1
            
            # Check for duplicate IMAGE properties
            image_pattern = r'(IMAGE;.*?VALUE=URI:.*?)(\r?\n)'
            image_matches = list(re.finditer(image_pattern, part))
            
            if len(image_matches) > 1:
                # Keep only the first instance of each unique image URL
                seen_urls = set()
                indices_to_remove = []
                
                for i, match in enumerate(image_matches):
                    full_match = match.group(0)
                    url = re.search(r'VALUE=URI:(.*?)(\r?\n)', full_match)
                    if url:
                        url_value = url.group(1)
                        if url_value in seen_urls:
                            indices_to_remove.append(i)
                        else:
                            seen_urls.add(url_value)
                
                # Remove duplicates (process in reverse order to maintain indices)
                for i in sorted(indices_to_remove, reverse=True):
                    match = image_matches[i]
                    part = part[:match.start()] + part[match.end():]
                
                fixed_count += 1
            
            # Update LAST-MODIFIED timestamp
            part = re.sub(r'LAST-MODIFIED:.*?(\r?\n)', f'LAST-MODIFIED:{now}\\1', part)
        
        fixed_parts.append(part)
    
    # Update main calendar LAST-MODIFIED
    main_last_modified = re.sub(
        r'(LAST-MODIFIED:)(\d{8}T\d{6}Z)', 
        f'\\1{now}', 
        ''.join(fixed_parts)
    )
    
    # Join the parts back together
    fixed_content = main_last_modified
    
    # Write back to the file
    with open(ics_file, 'w') as f:
        f.write(fixed_content)
    
    print(f"Cleaned up {fixed_count} events with duplicate images out of {event_count} total events.")
    print(f"Updated all timestamps to {now}")
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Perform final cleanup of calendar file.')
    parser.add_argument('--ics-file', default='main.ics', help='Path to the ICS calendar file')
    
    args = parser.parse_args()
    
    # Ensure the ICS file exists
    ics_file = args.ics_file
    if not os.path.isfile(ics_file):
        print(f"Error: Calendar file not found: {ics_file}")
        return 1
    
    try:
        cleanup_calendar(ics_file)
        
        # Run validation as well
        print("Validating cleaned calendar...")
        validator_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'validate_calendar.py')
        exit_code = os.system(f"python {validator_path} --file {ics_file}")
        
        if exit_code == 0:
            print("✓ Calendar validation passed")
            return 0
        else:
            print("⚠️ Calendar validation failed!")
            return 1
            
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
