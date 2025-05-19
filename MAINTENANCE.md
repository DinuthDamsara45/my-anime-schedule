# Anime Calendar Maintenance Guide

This document provides instructions for maintaining and updating the anime schedule calendar. This calendar follows the RFC 7986 standard for enhanced compatibility with modern calendar applications, particularly Microsoft Outlook.

## Adding New Anime Series

When adding a new anime series to the calendar:

1. **Research the series schedule**:
   - Confirm official release date and time
   - Determine episode count and broadcast schedule
   - Note any planned breaks in the schedule
   - Find the exact series name on TMDB for image integration

2. **Add entries to main.ics**:
   ```
   BEGIN:VEVENT
   UID:[TIMESTAMP]-[UNIQUE_ID]@dinuth.example.com
   DTSTAMP:[TIMESTAMP]
   DTSTART:[START_DATE_TIME]
   DTEND:[END_DATE_TIME]
   SUMMARY:[ANIME_TITLE] - Episode [NUMBER]
   DESCRIPTION:[DESCRIPTION_TEXT]
   LOCATION:[STREAMING_SERVICE]
   STATUS:TENTATIVE
   CREATED:[TIMESTAMP]
   LAST-MODIFIED:[TIMESTAMP]
   SEQUENCE:0
   TRANSP:OPAQUE
   PRIORITY:5
   CATEGORIES:Anime,Streaming,Entertainment
   URL:[OFFICIAL_ANIME_URL]
   ORGANIZER;CN=Dinuth:mailto:calendar@dinuth.example.com
   BEGIN:VALARM
   ACTION:DISPLAY
   DESCRIPTION:Reminder: [ANIME_TITLE] Episode [NUMBER] airs soon!
   TRIGGER:-PT15M
   END:VALARM
   END:VEVENT
   ```

3. **Update the README.md**:
   - Add the series to the "Current Anime Series" table
   - Update any other relevant sections

## Updating Existing Series

When a series schedule changes:

1. **Update the affected events** in main.ics
2. **Add a note** in the README about the schedule change
3. **Commit changes** with a descriptive message

## Seasonal Updates

At the end of each anime season:

1. **Remove completed series** or mark them as completed
2. **Add upcoming series** for the next season
3. **Update the "Current Anime Series" table** in README.md

## Adding Images to Calendar Events

This calendar supports images for events using the RFC 7986 IMAGE property, which is compatible with modern calendar applications including Microsoft Outlook.

### Adding Images to Events

1. **Using the Update Script**:
   ```bash
   # Method 1: Using environment variables (temporary)
   export TMDB_ACCESS_TOKEN="your_access_token_here"
   # OR
   export TMDB_API_KEY="your_api_key_here"
   
   # Run the update script
   python scripts/update_calendar_images.py
   
   # Method 2: Using .env file (recommended, more secure)
   # First create and populate your .env file based on .env.example
   # Then run:
   python scripts/update_calendar_images.py
   ```

2. **Manual Image Addition**:
   To manually add an image to an event, add the IMAGE property:
   ```
   BEGIN:VEVENT
   ...other event properties...
   IMAGE;VALUE=URI;DISPLAY=THUMBNAIL;FMTTYPE=image/jpeg:https://image.tmdb.org/t/p/w500/path_to_image.jpg
   END:VEVENT
   ```

3. **Image Types**:
   - `DISPLAY=THUMBNAIL` - Small image thumbnail 
   - `DISPLAY=BADGE` - Icon-sized image
   - `DISPLAY=GRAPHIC` - Full-sized image (caution: may be large)

### Outlook Compatibility Notes

- Outlook Web and newer Outlook desktop versions support the IMAGE property
- Images should use HTTPS URLs for security
- Smaller image sizes (w300, w500) are recommended for better performance

## ICS Format References

- [iCalendar Specification (RFC 5545)](https://datatracker.ietf.org/doc/html/rfc5545)
- [iCalendar Extensions (RFC 7986)](https://datatracker.ietf.org/doc/html/rfc7986) - Modern standard used in this calendar
- [Microsoft Outlook iCalendar Implementation](https://learn.microsoft.com/en-us/outlook/troubleshoot/calendaring/supporting-calendar-clients)
- [Common iCalendar Properties](https://www.kanzaki.com/docs/ical/)
- [Event Publishing Extensions](https://datatracker.ietf.org/doc/html/rfc7986#section-5.1)

## Validation Tools

Before publishing updates, validate your ICS file with:

- [iCalendar Validator](https://icalendar.org/validator.html)
- [iCal4j Validator](https://github.com/ical4j/ical4j-validator)

## API Credentials Security

When using the TMDB API for fetching anime images:

1. **Never commit API keys or tokens to the repository**
2. **Use environment variables** to store sensitive credentials:
   - Create a `.env` file based on `.env.example`
   - Add your TMDB API key and/or access token to this file
   - The `.env` file is ignored by git (listed in `.gitignore`)

Example of using environment variables:
```bash
# Set environment variables directly (temporary)
export TMDB_ACCESS_TOKEN="your_token_here"
export TMDB_API_KEY="your_key_here"

# Or use the .env file (recommended)
cp .env.example .env
# Edit the .env file with your actual credentials
```

## GitHub Workflow

1. **Make changes** to main.ics locally
2. **Test the calendar** by importing it to a calendar application
3. **Commit and push changes** to GitHub
4. **Verify the raw URL** works for subscription

## Automated Calendar Update Process

For a streamlined maintenance workflow, this repository includes automated update scripts:

### Standard Update Script

The `update_calendar.sh` script automates the entire update process:

```bash
# Run the standard update script
./update_calendar.sh
```

This script:
1. Updates the `LAST-MODIFIED` timestamp to force refresh in subscribed calendars
2. Fetches updated anime images from TMDB API
3. Validates the calendar format
4. Generates an HTML preview of the calendar
5. Opens the preview in your default web browser

Options:
- `--no-preview`: Skip preview generation and browser opening
  ```bash
  ./update_calendar.sh --no-preview
  ```

### Outlook-Specific Update Script

For optimal Outlook compatibility, use the `update_for_outlook.sh` script:

```bash
# Run the Outlook-optimized update script
./update_for_outlook.sh
```

This script:
1. Updates the calendar with all standard updates
2. Creates an Outlook-optimized version of the calendar (`main_outlook.ics`)
3. Properly formats all images for optimal Outlook compatibility
4. Generates a preview of the Outlook-optimized calendar
5. Provides specific instructions for importing into Outlook

### Manual Script Execution

If you prefer more control over the update process, you can run individual scripts:

```bash
# Update calendar timestamps
python scripts/refresh_calendar.py

# Update images only
python scripts/update_calendar_images.py

# Validate the calendar
python scripts/validate_calendar.py

# Generate preview
python scripts/refresh_calendar.py --preview
```

---

**Note**: This calendar uses the following RFC 7986 compliant properties:

**Calendar Properties**:
- `REFRESH-INTERVAL;VALUE=DURATION:P1D` - Calendar apps should refresh once per day
- `NAME` - Standard name property (RFC 7986)
- `DESCRIPTION` - Standard description property (RFC 7986)
- `SOURCE;VALUE=URI` - Original source location (RFC 7986)
- `COLOR` - Color property for calendar apps (RFC 7986)
- `CATEGORIES` - Calendar categorization (RFC 7986)
- `IMAGE` - Calendar image for supported clients (RFC 7986)

**Legacy Properties** (for maximum compatibility):
- `X-PUBLISHED-TTL:P1D` - Legacy time-to-live property
- `X-WR-CALNAME` - Legacy name property
- `X-WR-CALDESC` - Legacy description property

**Event Properties**:
- `TRANSP` - Time transparency (RFC 5545)
- `PRIORITY` - Event priority (RFC 5545)
- `SEQUENCE` - Revision sequence number (RFC 5545)
- `CATEGORIES` - Event categorization (RFC 5545/7986)
- `ORGANIZER` - Event organizer with CN parameter (RFC 5545)
