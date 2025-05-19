#!/usr/bin/env python3
"""
TMDB API Utility for Anime Schedule Calendar
Handles fetching anime artwork, posters, and banners from The Movie Database API.
"""

import os
import json
import requests
from urllib.parse import quote

class TMDBApi:
    """
    Handles interactions with The Movie Database API to fetch anime-related imagery.
    """
    
    BASE_URL = "https://api.themoviedb.org/3"
    IMAGE_BASE_URL = "https://image.tmdb.org/t/p/"
    
    def __init__(self, api_key=None, access_token=None):
        """Initialize with the TMDB API key or access token."""
        self.api_key = api_key or os.environ.get('TMDB_API_KEY')
        self.access_token = access_token or os.environ.get('TMDB_ACCESS_TOKEN')
        
        if not self.api_key and not self.access_token:
            raise ValueError("Either TMDB API key or access token is required.")
            
        # Set up headers for Bearer token authentication if using access token
        self.headers = None
        if self.access_token:
            self.headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json;charset=utf-8'
            }
    
    def search_anime(self, title):
        """Search for an anime by title."""
        endpoint = f"{self.BASE_URL}/search/tv"
        
        if self.headers:  # Using access token
            params = {
                'query': title,
                'language': 'en-US',
                # Filter for animation genre (16 is animation in TMDB)
                'with_genres': '16'
            }
            response = requests.get(endpoint, params=params, headers=self.headers)
        else:  # Using API key
            params = {
                'api_key': self.api_key,
                'query': title,
                'language': 'en-US',
                'with_genres': '16'
            }
            response = requests.get(endpoint, params=params)
            
        response.raise_for_status()
        return response.json()
    
    def get_tv_details(self, tv_id):
        """Get detailed information about a TV show."""
        endpoint = f"{self.BASE_URL}/tv/{tv_id}"
        
        if self.headers:  # Using access token
            params = {
                'language': 'en-US',
                'append_to_response': 'images'
            }
            response = requests.get(endpoint, params=params, headers=self.headers)
        else:  # Using API key
            params = {
                'api_key': self.api_key,
                'language': 'en-US',
                'append_to_response': 'images'
            }
            response = requests.get(endpoint, params=params)
            
        response.raise_for_status()
        return response.json()
    
    def get_season_details(self, tv_id, season_number):
        """Get detailed information about a specific season."""
        endpoint = f"{self.BASE_URL}/tv/{tv_id}/season/{season_number}"
        
        if self.headers:  # Using access token
            params = {
                'language': 'en-US',
                'append_to_response': 'images'
            }
            response = requests.get(endpoint, params=params, headers=self.headers)
        else:  # Using API key
            params = {
                'api_key': self.api_key,
                'language': 'en-US',
                'append_to_response': 'images'
            }
            response = requests.get(endpoint, params=params)
            
        response.raise_for_status()
        return response.json()
    
    def get_episode_details(self, tv_id, season_number, episode_number):
        """Get detailed information about a specific episode."""
        endpoint = f"{self.BASE_URL}/tv/{tv_id}/season/{season_number}/episode/{episode_number}"
        
        if self.headers:  # Using access token
            params = {
                'language': 'en-US',
                'append_to_response': 'images'
            }
            response = requests.get(endpoint, params=params, headers=self.headers)
        else:  # Using API key
            params = {
                'api_key': self.api_key,
                'language': 'en-US',
                'append_to_response': 'images'
            }
            response = requests.get(endpoint, params=params)
            
        response.raise_for_status()
        return response.json()
    
    def get_image_url(self, path, size='original'):
        """Convert image path to full URL with specified size."""
        if not path:
            return None
        return f"{self.IMAGE_BASE_URL}{size}/{path.lstrip('/')}"
    
    def get_anime_images(self, anime_title, season_number=None):
        """Get various images for an anime (poster, backdrop, season poster)."""
        results = self.search_anime(anime_title)
        
        if not results.get('results'):
            print(f"No results found for anime: {anime_title}")
            return {}
        
        # Get first match, assuming it's the most relevant
        show_id = results['results'][0]['id']
        show_details = self.get_tv_details(show_id)
        
        images = {
            'title': show_details.get('name'),
            'poster': self.get_image_url(show_details.get('poster_path')),
            'backdrop': self.get_image_url(show_details.get('backdrop_path')),
        }
        
        # If season number provided, get season-specific images
        if season_number is not None:
            try:
                season_details = self.get_season_details(show_id, season_number)
                images['season_poster'] = self.get_image_url(season_details.get('poster_path'))
                images['season_name'] = season_details.get('name')
            except Exception as e:
                print(f"Error fetching season {season_number} details: {e}")
        
        return images

    def get_episode_image(self, anime_title, season_number, episode_number):
        """Get episode-specific image if available."""
        try:
            results = self.search_anime(anime_title)
            if not results.get('results'):
                return None
                
            show_id = results['results'][0]['id']
            episode_details = self.get_episode_details(show_id, season_number, episode_number)
            
            return {
                'episode_still': self.get_image_url(episode_details.get('still_path')),
                'episode_name': episode_details.get('name')
            }
        except Exception as e:
            print(f"Error fetching episode image: {e}")
            return None


if __name__ == "__main__":
    # Simple command line test functionality
    import sys
    if len(sys.argv) < 2:
        print("Usage: python tmdb_api.py [anime_title] [season_number (optional)] [episode_number (optional)]")
        sys.exit(1)
    
    try:
        # Check for environment variables
        access_token = os.environ.get('TMDB_ACCESS_TOKEN')
        api_key = os.environ.get('TMDB_API_KEY')
        
        if access_token:
            tmdb = TMDBApi(access_token=access_token)
            print("Using access token for authentication")
        elif api_key:
            tmdb = TMDBApi(api_key=api_key)
            print("Using API key for authentication")
        else:
            print("No API credentials found. Set TMDB_ACCESS_TOKEN or TMDB_API_KEY environment variables.")
            sys.exit(1)
            
        anime_title = sys.argv[1]
        
        if len(sys.argv) >= 3:
            season_number = int(sys.argv[2])
            images = tmdb.get_anime_images(anime_title, season_number)
            
            if len(sys.argv) >= 4:
                episode_number = int(sys.argv[3])
                episode_image = tmdb.get_episode_image(anime_title, season_number, episode_number)
                if episode_image:
                    images.update(episode_image)
        else:
            images = tmdb.get_anime_images(anime_title)
        
        print(json.dumps(images, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
