#!/usr/bin/env python3
"""
Optimize Calendar for Outlook

This script optimizes the calendar file specifically for Microsoft Outlook:
1. Removes duplicate IMAGE properties
2. Ensures IMAGE properties use parameters compatible with Outlook
3. Increments the SEQUENCE counter to force update in subscribed calendars

Usage:
  python optimize_for_outlook.py [--ics-file main.ics] [--output main_outlook.ics]
"""

import os
import sys
import re
import argparse
from pathlib import Path

def optimize_calendar_for_outlook(input_file, output_file):
    """Optimize the calendar file for Microsoft Outlook."""
    print(f"Optimizing calendar for Outlook: {input_file} -> {output_file}")
    
    # Read the input calendar file
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Remove duplicate IMAGE properties
    event_count = 0
    image_count = 0
    
    # Split the file by events
    events = re.split(r'(BEGIN:VEVENT.*?END:VEVENT)', content, flags=re.DOTALL)
    updated_events = []
    
    for i, event in enumerate(events):
        if 'BEGIN:VEVENT' in event:
            event_count += 1
            
            # Keep only one IMAGE property per event
            image_pattern = r'(IMAGE;.*?VALUE=URI:.*?)(\r?\n)'
            image_matches = re.findall(image_pattern, event, re.DOTALL)
            
            if image_matches:
                # Keep only the first image
                first_image = image_matches[0][0]
                
                # Replace all image properties with the optimized version
                event = re.sub(image_pattern, '', event, flags=re.DOTALL)
                
                # Add the optimized image property
                # Ensure the IMAGE property uses parameters compatible with Outlook
                optimized_image = first_image.replace('DISPLAY=THUMBNAIL', 'DISPLAY=BADGE')
                
                # Insert optimized image before LAST-MODIFIED
                event = re.sub(
                    r'(LAST-MODIFIED:.*?)(\r?\n)',
                    f'\\1\\2{optimized_image}\\2',
                    event
                )
                
                image_count += 1
            
            # Increment the SEQUENCE counter to force update
            sequence_match = re.search(r'SEQUENCE:(\d+)', event)
            if sequence_match:
                current_sequence = int(sequence_match.group(1))
                event = re.sub(
                    r'SEQUENCE:\d+',
                    f'SEQUENCE:{current_sequence + 1}',
                    event
                )
        
        updated_events.append(event)
    
    # Join the events back together
    updated_content = ''.join(updated_events)
    
    # Write the updated content to the output file
    with open(output_file, 'w') as f:
        f.write(updated_content)
    
    print(f"Calendar optimized: {image_count}/{event_count} events have optimized images")
    return True

def main():
    parser = argparse.ArgumentParser(description='Optimize calendar for Microsoft Outlook.')
    parser.add_argument('--ics-file', default='main.ics', help='Path to the input ICS calendar file')
    parser.add_argument('--output', default='main_outlook.ics', help='Path to the output optimized calendar file')
    
    args = parser.parse_args()
    
    # Ensure the ICS file exists
    input_file = args.ics_file
    output_file = args.output
    
    if not os.path.isfile(input_file):
        print(f"Error: Calendar file not found: {input_file}")
        return 1
    
    try:
        optimize_calendar_for_outlook(input_file, output_file)
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
