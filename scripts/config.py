#!/usr/bin/env python3
"""
Configuration module for anime calendar scripts.
Loads environment variables from .env file if present.
"""

import os
import sys
from pathlib import Path

def load_dotenv():
    """
    Load environment variables from .env file if it exists.
    Simple implementation without requiring the python-dotenv package.
    """
    # Find the .env file (looking in parent directories if needed)
    script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    root_dir = script_dir.parent
    env_path = root_dir / '.env'
    
    if not env_path.exists():
        print("Note: No .env file found at", env_path)
        return False
    
    # Read and set environment variables from .env file
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
                
            # Handle export prefix (if present)
            if line.startswith('export '):
                line = line[7:]
                
            # Split key-value by first equals sign
            if '=' in line:
                key, value = line.split('=', 1)
                
                # Strip quotes if present
                key = key.strip()
                value = value.strip()
                for quote in ["'", '"']:
                    if value.startswith(quote) and value.endswith(quote):
                        value = value[1:-1]
                        
                # Set environment variable if not already set
                if key and key not in os.environ:
                    os.environ[key] = value
    
    return True

def get_tmdb_credentials():
    """
    Get TMDB API credentials from environment.
    Returns tuple of (access_token, api_key).
    """
    # Try loading from .env file first
    load_dotenv()
    
    # Get credentials from environment
    access_token = os.environ.get('TMDB_ACCESS_TOKEN')
    api_key = os.environ.get('TMDB_API_KEY')
    
    return access_token, api_key

if __name__ == "__main__":
    # Test the config module
    load_dotenv()
    access_token, api_key = get_tmdb_credentials()
    print("TMDB Access Token:", "✓ Set" if access_token else "✗ Not set")
    print("TMDB API Key:", "✓ Set" if api_key else "✗ Not set")
