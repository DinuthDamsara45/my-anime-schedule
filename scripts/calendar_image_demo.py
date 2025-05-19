#!/usr/bin/env python3
"""
Calendar Image Demo

Creates a sample calendar with episode images to demonstrate
how anime images look in compatible calendar applications.

Usage:
  python calendar_image_demo.py --access-token YOUR_TMDB_ACCESS_TOKEN --output demo_calendar.ics
  or
  python calendar_image_demo.py --api-key YOUR_TMDB_API_KEY --output demo_calendar.ics
"""

import os
import sys
import argparse
from datetime import datetime, timedelta
import icalendar

# Use local import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tmdb_api import TMDBApi
from config import get_tmdb_credentials

# Sample anime series to demonstrate the image feature
SAMPLE_ANIME = [
    {
        "title": "The Apothecary Diaries",
        "season": 1,
        "episodes": [1, 2],
        "start_date": datetime.now() + timedelta(days=1)
    },
    {
        "title": "Demon Slayer",
        "season": 3,
        "episodes": [1, 2],
        "start_date": datetime.now() + timedelta(days=3)
    },
    {
        "title": "My Hero Academia",
        "season": 6,
        "episodes": [1, 2],
        "start_date": datetime.now() + timedelta(days=5)
    }
]

def create_demo_calendar(tmdb_api, output_file="demo_calendar.ics"):
    """Create a demo calendar with images for various anime series."""
    print(f"Creating demo calendar: {output_file}")
    
    # Create a new calendar
    cal = icalendar.Calendar()
    cal.add('prodid', '-//Demo Anime Calendar//EN')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    cal.add('NAME', 'Anime Calendar Image Demo')
    cal.add('DESCRIPTION', 'Demonstration of anime images in calendar events')
    cal.add('X-WR-CALNAME', 'Anime Demo Calendar')
    cal.add('X-WR-CALDESC', 'Demonstration of anime images in calendar events')
    cal.add('REFRESH-INTERVAL', timedelta(hours=12), parameters={'VALUE': 'DURATION'})
    cal.add('COLOR', '#6a1b9a')
    cal.add('CATEGORIES', ['Demo', 'Anime', 'Calendar'])
    
    event_count = 0
    image_count = 0
    
    # Create events for each anime
    for anime in SAMPLE_ANIME:
        # Try to get anime images first
        try:
            anime_images = tmdb_api.get_anime_images(anime["title"], anime["season"])
            
            # If we found the anime, create events for each episode
            print(f"Creating events for: {anime['title']} (Season {anime['season']})")
            
            start_date = anime["start_date"]
            
            for episode_num in anime["episodes"]:
                event = icalendar.Event()
                
                # Create a unique ID
                now = datetime.now()
                uid = f"{now.strftime('%Y%m%dT%H%M%SZ')}-{anime['title'].replace(' ', '-')}-S{anime['season']}E{episode_num}"
                event.add('uid', uid)
                
                # Add basic event properties
                event_start = start_date + timedelta(days=(episode_num-1) * 7)  # Weekly episodes
                event_end = event_start + timedelta(minutes=30)  # 30-minute episodes
                
                event.add('dtstamp', datetime.now())
                event.add('dtstart', event_start)
                event.add('dtend', event_end)
                event.add('summary', f"{anime['title']} S{anime['season']} - Episode {episode_num}")
                event.add('description', f"Watch {anime['title']} Season {anime['season']} Episode {episode_num}")
                event.add('location', 'Crunchyroll/Streaming Services')
                event.add('status', 'TENTATIVE')
                event.add('TRANSP', 'OPAQUE')
                event.add('SEQUENCE', 0)
                
                # Add image - first try episode image
                episode_image = None
                try:
                    episode_image = tmdb_api.get_episode_image(anime["title"], anime["season"], episode_num)
                except Exception as e:
                    print(f"  Could not get episode image: {e}")
                
                if episode_image and episode_image.get('episode_still'):
                    # Add episode still as IMAGE property
                    image_url = episode_image.get('episode_still')
                    event.add('IMAGE', image_url, parameters={
                        'VALUE': 'URI',
                        'DISPLAY': 'THUMBNAIL',
                        'FMTTYPE': 'image/jpeg'
                    })
                    print(f"  Added episode thumbnail: {image_url}")
                    image_count += 1
                elif anime_images:
                    # Fall back to season poster or series poster
                    if anime_images.get('season_poster'):
                        image_url = anime_images.get('season_poster')
                    elif anime_images.get('poster'):
                        image_url = anime_images.get('poster')
                    else:
                        image_url = None
                        
                    if image_url:
                        event.add('IMAGE', image_url, parameters={
                            'VALUE': 'URI',
                            'DISPLAY': 'THUMBNAIL',
                            'FMTTYPE': 'image/jpeg'
                        })
                        print(f"  Added series poster: {image_url}")
                        image_count += 1
                
                # Add reminder
                alarm = icalendar.Alarm()
                alarm.add('ACTION', 'DISPLAY')
                alarm.add('DESCRIPTION', f"Reminder: {anime['title']} S{anime['season']} E{episode_num} is about to start!")
                alarm.add('TRIGGER', timedelta(minutes=-15))
                event.add_component(alarm)
                
                # Add the event to the calendar
                cal.add_component(event)
                event_count += 1
                
        except Exception as e:
            print(f"Error processing {anime['title']}: {e}")
    
    # Write the calendar to file
    with open(output_file, 'wb') as f:
        f.write(cal.to_ical())
    
    print(f"Demo calendar created with {event_count} events ({image_count} with images)")
    print(f"File saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Create a demo calendar with anime images.')
    parser.add_argument('--api-key', help='TMDB API key')
    parser.add_argument('--access-token', help='TMDB access token')
    parser.add_argument('--output', default='demo_calendar.ics', help='Output ICS file')
    
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
    
    try:
        tmdb_api = TMDBApi(access_token=access_token, api_key=api_key)
        create_demo_calendar(tmdb_api, args.output)
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
