#!/usr/bin/env python3
"""
Refresh Calendar

A comprehensive tool to refresh the entire anime calendar:
- Updates the LAST-MODIFIED timestamp to force refresh in subscribed calendars
- Refreshes all anime images from TMDB
- Validates the calendar format
- Optionally generates a preview

Usage:
  python refresh_calendar.py [--preview]
"""

import os
import sys
import argparse
import datetime
import re
from pathlib import Path

# Use local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tmdb_api import TMDBApi
from config import get_tmdb_credentials
from update_calendar_images import update_calendar_with_images

def update_last_modified(ics_file):
    """Update the calendar's LAST-MODIFIED timestamp to current time."""
    print(f"Updating LAST-MODIFIED timestamp in {ics_file}...")
    
    # Read the calendar file
    with open(ics_file, 'r') as f:
        content = f.read()
    
    # Get current UTC time in iCalendar format
    now = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    
    # Replace the LAST-MODIFIED timestamp
    pattern = r'(LAST-MODIFIED:)(\d{8}T\d{6}Z)'
    updated_content = re.sub(pattern, f"\\1{now}", content)
    
    # Write back to file
    with open(ics_file, 'w') as f:
        f.write(updated_content)
    
    print(f"Calendar timestamp updated to {now}")
    return True

def validate_calendar(ics_file):
    """Validate the calendar format by calling the validation script."""
    print(f"Validating calendar: {ics_file}...")
    validator_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'validate_calendar.py')
    
    # Using os.system for simplicity here
    exit_code = os.system(f"python {validator_path} --file {ics_file}")
    if exit_code != 0:
        print("⚠️ Calendar validation failed!")
        return False
    
    print("✓ Calendar validation passed")
    return True

def generate_preview(ics_file, output_html="preview.html"):
    """Generate a simple HTML preview of the calendar.
    
    Returns:
        str: Path to the generated HTML file if successful, None otherwise.
    """
    print(f"Generating preview: {output_html}...")
    
    # Read the ics file content
    with open(ics_file, 'r') as f:
        ics_content = f.read()
    
    # Extract events and their images
    events = []
    for match in re.finditer(r'BEGIN:VEVENT(.*?)END:VEVENT', ics_content, re.DOTALL):
        event_data = match.group(1)
        
        # Extract summary
        summary_match = re.search(r'SUMMARY:(.*?)(?:\r?\n)', event_data)
        summary = summary_match.group(1) if summary_match else 'No Title'
        
        # Extract date
        date_match = re.search(r'DTSTART:(.*?)(?:\r?\n)', event_data)
        date_str = date_match.group(1) if date_match else ''
        
        # Try to format date
        if date_str:
            try:
                date = datetime.datetime.strptime(date_str, "%Y%m%dT%H%M%SZ")
                date_formatted = date.strftime("%Y-%m-%d %H:%M UTC")
            except:
                date_formatted = date_str
        else:
            date_formatted = 'No Date'
        
        # Extract image if it exists
        image_match = re.search(r'IMAGE;.*?VALUE=URI:(.*?)(?:\r?\n)', event_data)
        image_url = image_match.group(1) if image_match else None
        
        events.append({
            'summary': summary,
            'date': date_formatted,
            'image': image_url
        })
    
    # Create HTML
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Anime Calendar Preview</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #31a59f; }}
        .event {{ 
            margin-bottom: 20px; 
            padding: 15px; 
            border: 1px solid #ccc; 
            border-radius: 8px;
            display: flex;
            align-items: center;
        }}
        .event-details {{ margin-left: 20px; }}
        .event-image {{ 
            width: 150px; 
            height: 85px; 
            object-fit: cover;
            border-radius: 4px;
        }}
        .no-image {{ 
            width: 150px; 
            height: 85px; 
            background-color: #f0f0f0;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 4px;
        }}
        .timestamp {{ 
            color: #666; 
            font-size: 0.8em; 
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <h1>Anime Calendar Preview</h1>
    <p>This preview shows all events in your calendar with their images.</p>
    
    <h2>Events ({len(events)})</h2>
    
    {''.join([f'''
    <div class="event">
        {f'<img class="event-image" src="{event["image"]}" alt="{event["summary"]}" />' if event["image"] else '<div class="no-image">No Image</div>'}
        <div class="event-details">
            <h3>{event["summary"]}</h3>
            <p>{event["date"]}</p>
        </div>
    </div>
    ''' for event in events])}
    
    <p class="timestamp">Generated on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
</body>
</html>
    """
    
    # Write to file
    try:
        with open(output_html, 'w') as f:
            f.write(html_content)
        
        print(f"Preview generated: {output_html}")
        return output_html
    except Exception as e:
        print(f"Error generating preview: {e}")
        return None

def refresh_calendar(ics_file, generate_html_preview=False):
    """Complete calendar refresh process."""
    print(f"Starting complete refresh of {ics_file}...")
    
    # 1. Update the LAST-MODIFIED timestamp
    if not update_last_modified(ics_file):
        return False
    
    # 2. Update images
    try:
        # Get TMDB API credentials
        access_token, api_key = get_tmdb_credentials()
        if not access_token and not api_key:
            print("⚠️ No TMDB credentials found. Images will not be updated.")
            print("Please create a .env file with your TMDB_ACCESS_TOKEN or TMDB_API_KEY.")
        else:
            # Initialize TMDB API
            tmdb_api = TMDBApi(access_token=access_token, api_key=api_key)
            # Update calendar with images
            print("Updating images...")
            update_calendar_with_images(ics_file, tmdb_api)
    except Exception as e:
        print(f"⚠️ Error updating images: {e}")
    
    # 3. Validate the calendar
    validation_success = validate_calendar(ics_file)
    
    # 4. Generate preview if requested
    if generate_html_preview and validation_success:
        preview_file = generate_preview(ics_file)
        
        # Try to open preview in browser automatically
        if preview_file:
            try:
                import webbrowser
                print(f"Opening preview in web browser: {preview_file}")
                webbrowser.open(f"file://{os.path.abspath(preview_file)}")
            except Exception as e:
                print(f"Could not open preview in browser: {e}")
    
    print("Calendar refresh complete!")
    return validation_success

def main():
    parser = argparse.ArgumentParser(description='Refresh anime calendar with updated timestamps and images.')
    parser.add_argument('--ics-file', default='main.ics', help='Path to the ICS calendar file')
    parser.add_argument('--preview', action='store_true', help='Generate HTML preview of the calendar')
    
    args = parser.parse_args()
    
    # Ensure the ICS file exists
    ics_file = args.ics_file
    if not os.path.isfile(ics_file):
        print(f"Error: Calendar file not found: {ics_file}")
        return 1
    
    # Run the refresh process
    success = refresh_calendar(ics_file, args.preview)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
