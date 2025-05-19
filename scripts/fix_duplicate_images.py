#!/usr/bin/env python3
"""
Fix Duplicate Images

This simple utility removes duplicate IMAGE properties from the calendar file.
"""

import re
import sys
import os

def fix_duplicate_images(ics_file):
    """Remove duplicate IMAGE properties from calendar events."""
    print(f"Fixing duplicate images in {ics_file}...")
    
    # Read the calendar file
    with open(ics_file, 'r') as f:
        content = f.read()
    
    # Split by events
    parts = re.split(r'(BEGIN:VEVENT.*?END:VEVENT)', content, flags=re.DOTALL)
    
    fixed_parts = []
    event_count = 0
    fixed_count = 0
    
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
        
        fixed_parts.append(part)
    
    # Join the parts back together
    fixed_content = ''.join(fixed_parts)
    
    # Write back to the file
    with open(ics_file, 'w') as f:
        f.write(fixed_content)
    
    print(f"Fixed {fixed_count} events with duplicate images out of {event_count} total events.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_duplicate_images.py [calendar.ics]")
        sys.exit(1)
    
    ics_file = sys.argv[1]
    if not os.path.isfile(ics_file):
        print(f"Error: Calendar file not found: {ics_file}")
        sys.exit(1)
    
    if fix_duplicate_images(ics_file):
        print("Successfully fixed duplicate images.")
        sys.exit(0)
    else:
        print("Failed to fix duplicate images.")
        sys.exit(1)
