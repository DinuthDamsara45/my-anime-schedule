#!/usr/bin/env python3
"""
Update Calendar Images

This script adds RFC 7986 compliant IMAGE properties to calendar events
using The Movie Database (TMDB) API to fetch anime artwork.

Usage:
  python update_calendar_images.py --access-token YOUR_ACCESS_TOKEN [--ics-file main.ics]
  or
  python update_calendar_images.py --api-key YOUR_API_KEY [--ics-file main.ics]
"""

import os
import sys
import re
import argparse
import icalendar
from datetime import datetime

# Use local import - make sure we're using the updated version
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tmdb_api import TMDBApi
from config import get_tmdb_credentials

def extract_series_info(summary):
    """Extract anime series name and episode number from event summary."""
    # Match patterns like "The Apothecary Diaries S2 - Episode 31"
    pattern = r"(.*?)(?:S(\d+)|Season (\d+))?\s*-\s*Episode\s*(\d+)"
    match = re.search(pattern, summary, re.IGNORECASE)
    
    if match:
        series = match.group(1).strip()
        season = match.group(2) or match.group(3) or "1"  # Default to season 1 if not specified
        episode = match.group(4)
        return series, int(season), int(episode)
    
    # Try simpler pattern without season specification
    pattern = r"(.*?)\s*-\s*Episode\s*(\d+)"
    match = re.search(pattern, summary, re.IGNORECASE)
    
    if match:
        series = match.group(1).strip()
        episode = match.group(2)
        return series, 1, int(episode)  # Assume season 1
    
    return None, None, None

def update_calendar_with_images(ics_file, tmdb_api):
    """Update calendar events with images from TMDB."""
    print(f"Processing calendar file: {ics_file}")
    
    # Read the iCalendar file
    with open(ics_file, 'r') as file:
        content = file.read()
    
    # Parse the iCalendar content
    cal = icalendar.Calendar.from_ical(content)
    
    # Process each event
    event_count = 0
    image_count = 0
    
    for component in cal.walk():
        if component.name == "VEVENT":
            event_count += 1
            summary = str(component.get('summary', ''))
            
            series, season, episode = extract_series_info(summary)
            if not series:
                print(f"Could not extract series info from: {summary}")
                continue
                
            print(f"Found event: {summary} (Series: {series}, Season: {season}, Episode: {episode})")
            
            # Get images for this anime series/episode
            try:
                # First try to get episode-specific image
                episode_image = tmdb_api.get_episode_image(series, season, episode)
                
                # Remove any existing IMAGE properties to avoid duplicates
                for existing_image in list(component.items()):
                    if existing_image[0] == 'IMAGE':
                        del component[existing_image[0]]
                
                if episode_image and episode_image.get('episode_still'):
                    # Add episode still as IMAGE property
                    image_url = episode_image.get('episode_still')
                    component.add('IMAGE', image_url, parameters={
                        'VALUE': 'URI',
                        'DISPLAY': 'THUMBNAIL',
                        'FMTTYPE': 'image/jpeg'
                    })
                    image_count += 1
                    print(f"  Added episode image: {image_url}")
                else:
                    # Fall back to series/season poster
                    images = tmdb_api.get_anime_images(series, season)
                    
                    if images.get('season_poster'):
                        image_url = images.get('season_poster')
                        component.add('IMAGE', image_url, parameters={
                            'VALUE': 'URI',
                            'DISPLAY': 'THUMBNAIL', 
                            'FMTTYPE': 'image/jpeg'
                        })
                        image_count += 1
                        print(f"  Added season poster: {image_url}")
                    elif images.get('poster'):
                        image_url = images.get('poster')
                        component.add('IMAGE', image_url, parameters={
                            'VALUE': 'URI',
                            'DISPLAY': 'THUMBNAIL',
                            'FMTTYPE': 'image/jpeg'
                        })
                        image_count += 1
                        print(f"  Added series poster: {image_url}")
            except Exception as e:
                print(f"  Error getting images for {series}: {e}")
    
    # Convert back to iCalendar format
    updated_content = cal.to_ical().decode('utf-8')
    
    # Write the updated calendar back to the file
    with open(ics_file, 'w') as file:
        file.write(updated_content)
    
    print(f"Calendar updated: {image_count}/{event_count} events have images")

def main():
    parser = argparse.ArgumentParser(description='Update calendar events with anime images.')
    parser.add_argument('--api-key', help='TMDB API key')
    parser.add_argument('--access-token', help='TMDB access token')
    parser.add_argument('--ics-file', default='main.ics', help='Path to the ICS calendar file')
    
    args = parser.parse_args()
    
    # Get credentials from .env file or environment variables
    env_access_token, env_api_key = get_tmdb_credentials()
    
    # Command line arguments take precedence over environment variables
    access_token = args.access_token or env_access_token
    api_key = args.api_key or env_api_key
    
    if not access_token and not api_key:
        print("Error: Either TMDB API key or access token is required.")
        print("Please create a .env file based on .env.example or provide credentials via command line.")
        return 1
    
    # Ensure the ICS file exists
    ics_file = args.ics_file
    if not os.path.isfile(ics_file):
        print(f"Error: Calendar file not found: {ics_file}")
        return 1
    
    try:
        tmdb_api = TMDBApi(access_token=access_token, api_key=api_key)
        update_calendar_with_images(ics_file, tmdb_api)
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
