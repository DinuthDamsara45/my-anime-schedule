# Anime Calendar Scripts

This directory contains scripts for working with the anime schedule calendar.

## Scripts Overview

- **refresh_calendar.py** - Main script for complete calendar refresh with validation and preview
- **update_calendar_images.py** - Adds anime images to calendar events using TMDB API
- **validate_calendar.py** - Validates the calendar file format
- **calendar_image_demo.py** - Creates a demo calendar with anime images
- **config.py** - Manages API credentials securely from .env file
- **tmdb_api.py** - Handles interactions with The Movie Database API

## Security Note

These scripts use TMDB API credentials which should be kept private. The scripts load credentials from:

1. Command line arguments (not recommended for public repositories)
2. Environment variables
3. A `.env` file in the project root (recommended)

**NEVER commit API keys or tokens to a public repository.**

## Usage Examples

### Using Shell Scripts (Recommended)

The easiest way to update the calendar is by using the provided shell scripts in the parent directory:

```bash
# Standard update with preview
../update_calendar.sh

# Outlook-optimized update
../update_for_outlook.sh
```

### Using Python Scripts Directly

For more control, you can use the Python scripts directly:

```bash
# Complete calendar refresh with preview
python refresh_calendar.py --preview

# Add images only
python update_calendar_images.py

# Validate the calendar
python validate_calendar.py --file ../main.ics
```

### Credential Management

```bash
# Recommended method (using .env file)
cp ../.env.example ../.env
# Edit the .env file with your TMDB API credentials

# Alternative (using environment variables)
export TMDB_ACCESS_TOKEN="your_token_here"
# OR
export TMDB_API_KEY="your_api_key_here"
```
