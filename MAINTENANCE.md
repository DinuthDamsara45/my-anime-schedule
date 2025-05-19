# Anime Calendar Maintenance Guide

This document provides instructions for maintaining and updating the anime schedule calendar.

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
- [Common iCalendar Properties](https://www.kanzaki.com/docs/ical/)

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

**Note**: This calendar uses the following properties:
- `REFRESH-INTERVAL;VALUE=DURATION:P1D` - Calendar apps should refresh once per day
- `X-PUBLISHED-TTL:P1D` - Published time-to-live is 1 day
- `X-WR-RELCALID:anime-schedule-001` - Calendar identifier
