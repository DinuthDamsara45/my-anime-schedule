# Outlook Calendar Compatibility Guide

This guide provides detailed instructions for ensuring optimal compatibility between your anime schedule calendar and Microsoft Outlook.

## Outlook Image Support

Microsoft Outlook supports the RFC 7986 IMAGE property, allowing the calendar to display anime images directly in your calendar events. However, Outlook has some specific requirements for optimal image display:

### Requirements for Image Display

1. **Image Format**: JPEG and PNG are best supported
2. **Image Properties**:
   - Must use `VALUE=URI` parameter
   - Should include `DISPLAY=THUMBNAIL` for proper sizing
   - Should specify `FMTTYPE` (e.g., `FMTTYPE=image/jpeg`)
3. **Image URLs**: Must use HTTPS URLs (not HTTP)
4. **Image Size**: Smaller images (300-500px width) work best

### Outlook-Specific Tips

- **Outlook Desktop**: May require restarting Outlook to see image changes
- **Outlook Web**: May require clearing browser cache for image updates
- **Outlook Mobile**: Has limited support for calendar images

## Using the Outlook-Optimized Calendar

For best results with Microsoft Outlook, use our Outlook-optimized version:

1. Run the Outlook-specific update script:
   ```bash
   ./update_for_outlook.sh
   ```

2. Use the generated `main_outlook.ics` file for importing into Outlook

## Import Instructions for Different Outlook Versions

### Outlook Desktop (Windows/Mac)

1. Open Outlook desktop application
2. Go to **File** > **Open & Export** > **Import/Export**
3. Select **Import an iCalendar (.ics) file**
4. Browse and select the `main_outlook.ics` file
5. Choose whether to import as a new calendar or add to existing

### Outlook Web

1. Go to [Outlook Web](https://outlook.office.com/)
2. Click on the Calendar icon
3. In the left sidebar, click **Add calendar**
4. Select **Upload from file**
5. Browse and select the `main_outlook.ics` file
6. Click **Import**

### Outlook Mobile

1. It's recommended to first import the calendar on desktop or web
2. The calendar will then sync automatically to your mobile app
3. Alternatively, email the `.ics` file to yourself and open in the Outlook mobile app

## Troubleshooting Outlook Image Display

If images don't appear in your Outlook calendar:

1. **Check Outlook Version**: Ensure you're using a modern version of Outlook that supports RFC 7986
2. **Reimport Calendar**: Remove the existing calendar and import the fresh version
3. **Clear Cache**: In Outlook Web, clear your browser cache
4. **Check Image URLs**: Verify the image URLs are accessible and use HTTPS
5. **Disable Security Features**: Some strict security settings may block external images
6. **Try Different Views**: Try day/week/month views as image support varies

## Regular Updates

After adding new anime episodes or updating images:

1. Run `./update_for_outlook.sh` to generate a fresh Outlook-optimized calendar
2. Remove the old calendar from Outlook
3. Import the new `main_outlook.ics` file

This complete reimport is often the most reliable way to ensure Outlook displays the updated images correctly.

## Resources

- [Microsoft Outlook iCalendar Implementation](https://learn.microsoft.com/en-us/outlook/troubleshoot/calendaring/supporting-calendar-clients)
- [RFC 7986 Specification](https://datatracker.ietf.org/doc/html/rfc7986)
