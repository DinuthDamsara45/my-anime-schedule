# 📅 My Anime Schedule

![Calendar Banner](https://img.shields.io/badge/Calendar-Subscribable-brightgreen)
![Update Frequency](https://img.shields.io/badge/Updates-Weekly-blue)
![Format](https://img.shields.io/badge/Format-RFC7986-orange)
![Status](https://img.shields.io/badge/Status-Active-success)
![Compatibility](https://img.shields.io/badge/Compatibility-Outlook%20|%20Google%20|%20Apple-blue)

A professional anime viewing schedule in iCalendar (.ics) format that fully complies with the modern RFC 7986 standard. This calendar can be subscribed to and imported into your favorite calendar applications including Microsoft Outlook, Google Calendar, and Apple Calendar. Never miss an episode of your favorite anime series!

## 🚨 Important Notice

**This repository is maintained by @DinuthDamsara45**

While this repository is public for viewing, please **DO NOT modify any files** without explicit permission from the repository owner. The calendar entries are personal schedule items and should not be edited by others.

## About This Project

This calendar contains my personal anime viewing schedule with detailed information about:
- The Apothecary Diaries Season 2
- The Shiunji Family Children
- Other anime series (to be added)

## Subscribing to This Calendar

You can subscribe to this calendar to stay updated with the latest anime schedules:

### Google Calendar
1. Open [Google Calendar](https://calendar.google.com/)
2. Click the "+" next to "Other calendars"
3. Select "From URL"
4. Enter the raw URL of the ICS file: `https://raw.githubusercontent.com/DinuthDamsara45/my-anime-schedule/main/main.ics`
5. Click "Add calendar"

### Apple Calendar (macOS/iOS)
1. Open the Calendar app
2. Go to File > New Calendar Subscription (on macOS) or Settings > Accounts > Add Account > Other > Add Subscribed Calendar (on iOS)
3. Enter the raw URL: `https://raw.githubusercontent.com/DinuthDamsara45/my-anime-schedule/main/main.ics`
4. Configure refresh interval and alerts as desired
5. Click "Subscribe"

### Microsoft Outlook (Enhanced Compatibility)
For online subscription:
1. Go to Calendar view
2. Click "Add calendar" > "Subscribe from web"
3. Enter the raw URL: `https://raw.githubusercontent.com/DinuthDamsara45/my-anime-schedule/main/main.ics`
4. Name the calendar and choose color/display options
5. Click "Import"

For optimal image support in Outlook:
1. Clone or download this repository
2. Run the Outlook-specific update script: `./update_for_outlook.sh`
3. Import the generated `main_outlook.ics` file into Outlook

This calendar uses RFC 7986 compliant formatting with specific enhancements for Outlook, ensuring:
- **Episode thumbnails and anime posters** displayed directly in events
- Proper event categorization with anime-specific tags
- Accurate time display with UTC time zone support
- Full metadata support including episode links
- Optimized event display with priorities and transparency
- Support for Outlook-specific fields and notifications
- 15-minute reminder notifications before each episode
- Custom calendar icon when supported

> **Image Support:** Microsoft Outlook supports the RFC 7986 IMAGE property, allowing this calendar to display episode thumbnails and anime posters directly in your calendar events. Images are sourced from The Movie Database (TMDB).

### Other Calendar Apps
Most calendar applications support ICS subscription via URL. Look for options like:
- "Subscribe to calendar"
- "Add calendar from URL"
- "Import from URL"

Use the raw URL: `https://raw.githubusercontent.com/DinuthDamsara45/my-anime-schedule/main/main.ics`

### Manual Import (One-time)
If you prefer not to subscribe for updates:
1. Download the [main.ics](https://github.com/DinuthDamsara45/my-anime-schedule/raw/main/main.ics) file
2. Import it into your calendar application

Please create your own fork if you want to make a similar calendar for yourself.

## Features

- ✅ **RFC 7986 Compliant** - Uses modern iCalendar standard for maximum compatibility
- ✅ **Outlook Enhanced** - Special formatting for optimal Microsoft Outlook experience
- ✅ **Auto-updating calendar** - Subscribe once and receive all future updates
- ✅ **Multiple anime series** - Keep track of different shows in one place
- ✅ **Episode details** - View episode numbers and descriptions
- ✅ **Notification alerts** - Built-in 15-minute reminders before episodes air
- ✅ **Multi-platform** - Works with Google Calendar, Apple Calendar, Outlook, and more
- ✅ **Extended properties** - Rich metadata including categories, priorities, and transparency
- ✅ **Calendar branding** - Custom calendar icon when supported by applications
- ✅ **Anime artwork** - Episode thumbnails and series posters from TMDB
- ✅ **Visual events** - Image support in compatible clients like Outlook

## Current Anime Series

| Series Name | Season | Episodes | Airing Day | Time (UTC) |
|-------------|--------|----------|------------|------------|
| The Apothecary Diaries | 2 | 31-36 | Saturday | 13:00 |
| The Shiunji Family Children | 1 | 7-12 | Tuesday | 14:30 |

## Update Schedule

This calendar is updated:
- When new anime seasons are announced
- When broadcast schedules change
- At the end of each season to add the next season's lineup

## Getting Help

If you encounter any issues with the calendar subscription or have suggestions:

1. Check if your calendar app supports ICS subscriptions
2. Ensure you're using the raw URL to the ICS file
3. Try refreshing the calendar subscription in your app

## Contact

If you have any questions or suggestions regarding this calendar, please open an issue or contact the repository owner.

## Security Considerations

This project uses The Movie Database (TMDB) API to fetch anime images. To maintain security:

1. **Never commit API keys or tokens** to the public repository
2. For personal use or development:
   - Create a `.env` file based on `.env.example`
   - Add your TMDB credentials to this file (which is ignored by git)
   - Or use environment variables as described in MAINTENANCE.md

For more details on securely managing API credentials, see the [MAINTENANCE.md](MAINTENANCE.md) file.

## License

This calendar is provided for personal use only. The structure and code are freely available, but the schedule data is maintained by the repository owner.

---

<div align="center">
Created with ❤️ for anime fans
</div>