# Anime Schedule Calendar - User Guide

Welcome to your Anime Schedule Calendar! This guide will help you use and maintain your calendar effectively.

## Quick Start

For most users, these two simple commands are all you need:

```bash
# Standard update (for most calendar apps):
./update_calendar.sh

# Microsoft Outlook specific update:
./update_for_outlook.sh
```

## Available Calendar Files

After running the update scripts, you'll have:

- `main.ics` - The standard calendar file compatible with most calendar applications
- `main_outlook.ics` - A version optimized specifically for Microsoft Outlook
- `preview.html` - A visual preview of your calendar with all images

## How to Import Your Calendar

### Google Calendar

1. Go to Google Calendar
2. Click the "+" next to "Other calendars"
3. Select "Import"
4. Upload the `main.ics` file
5. Choose the destination calendar
6. Click "Import"

### Apple Calendar

1. Open Apple Calendar
2. Go to File > Import
3. Select the `main.ics` file
4. Click "Import"

### Microsoft Outlook

1. Use the `main_outlook.ics` file (not the regular main.ics)
2. Follow the detailed instructions in [Outlook Compatibility Guide](/docs/outlook_compatibility.md)

## Updating Your Calendar

When you need to update your calendar with new anime episodes or refresh images:

1. Make sure your TMDB credentials are in the `.env` file
2. Run `./update_calendar.sh` (or `./update_for_outlook.sh` for Outlook)
3. Import the updated .ics file into your calendar application

## Troubleshooting

### Images Not Showing

- Ensure you're using a calendar app that supports RFC 7986 image properties
- For Outlook, use the Outlook-specific file and follow the [dedicated guide](/docs/outlook_compatibility.md)
- Check that your TMDB API credentials are valid

### Calendar Not Updating

- Try removing the calendar completely and re-importing it
- For subscribed calendars, the refresh may take up to 24 hours

### API Issues

- If TMDB API is down or returns errors, your calendar will still work but may not have updated images

## Further Resources

- [Complete Maintenance Guide](/MAINTENANCE.md) - For advanced configuration
- [Scripts Documentation](/scripts/README.md) - Details on all available scripts
- [Outlook Compatibility](/docs/outlook_compatibility.md) - Special considerations for Outlook users

Enjoy your anime schedule calendar!
