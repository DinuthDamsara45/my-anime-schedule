# Quick Start Guide

This is a quick reference guide for your anime schedule calendar. For complete instructions, see the [full User Guide](USER_GUIDE.md).

## Updating Your Calendar

1. **Standard update** (for most calendar apps):
   ```bash
   ./update_calendar.sh
   ```

2. **Outlook-specific update**:
   ```bash
   ./update_for_outlook.sh
   ```

## Calendar Files

- `main.ics` - Standard calendar (Google Calendar, Apple Calendar)
- `main_outlook.ics` - Optimized for Microsoft Outlook
- `preview.html` - Visual preview with all images

## Security Reminder

This project uses The Movie Database (TMDB) API to fetch anime images. To maintain security:

1. **Never commit API keys or tokens** to the public repository
2. Store your credentials in a `.env` file (which is ignored by git)
3. See `.env.example` for the required format

## Need Help?

- For basic usage: [User Guide](USER_GUIDE.md)
- For maintenance: [Maintenance Guide](MAINTENANCE.md)
- For Outlook users: [Outlook Compatibility](docs/outlook_compatibility.md)
- For developers: [Scripts Documentation](scripts/README.md)
