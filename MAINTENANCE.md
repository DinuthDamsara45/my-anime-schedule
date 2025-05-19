# Anime Calendar Maintenance Guide

This document provides instructions for maintaining and updating the anime schedule calendar. This calendar follows the RFC 7986 standard for enhanced compatibility with modern calendar applications, particularly Microsoft Outlook.

## Adding New Anime Series

When adding a new anime series to the calendar:

1. **Research the series schedule**:
   - Confirm official release date and time
   - Determine episode count and broadcast schedule
   - Note any planned breaks in the schedule

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

## GitHub Workflow

1. **Make changes** to main.ics locally
2. **Test the calendar** by importing it to a calendar application
3. **Commit and push changes** to GitHub
4. **Verify the raw URL** works for subscription

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
