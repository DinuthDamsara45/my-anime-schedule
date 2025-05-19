#!/bin/bash
# Outlook-optimized update script for anime calendar
# Usage: ./update_for_outlook.sh

# Terminal colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
RESET='\033[0m'
BOLD='\033[1m'

# Log functions
log_info() {
  echo -e "${BLUE}[INFO]${RESET} $1"
}

log_success() {
  echo -e "${GREEN}[SUCCESS]${RESET} $1"
}

log_warning() {
  echo -e "${YELLOW}[WARNING]${RESET} $1"
}

log_error() {
  echo -e "${RED}[ERROR]${RESET} $1"
}

# Show banner
echo -e "${BOLD}🔄 Anime Calendar Outlook Optimization Tool 🔄${RESET}"
echo "=================================================="

# Navigate to the project directory
cd "$(dirname "$0")"

# Check python availability
if ! command -v python &> /dev/null; then
  log_error "Python not found! Please install Python to run this script."
  exit 1
fi

# 1. Clean up and update the calendar
log_info "Running cleanup to fix any existing issues..."
python scripts/final_cleanup.py

log_info "Updating calendar with images..."
python scripts/refresh_calendar.py --preview

# 2. Create an Outlook-optimized copy of the calendar
log_info "Creating Outlook-optimized version..."

# File paths
ORIGINAL="main.ics"
OPTIMIZED="main_outlook.ics"

# Run the python script to optimize for Outlook
python scripts/optimize_for_outlook.py --ics-file "$ORIGINAL" --output "$OPTIMIZED"

# Update the calendar name to indicate it's optimized for Outlook
sed -i 's/X-WR-CALNAME:My Anime Schedule/X-WR-CALNAME:My Anime Schedule (Outlook)/g' "$OPTIMIZED"

# Remove duplicate IMAGE properties and fix LAST-MODIFIED date
log_info "Removing duplicate images and fixing timestamps..."

# Final validation
if python scripts/validate_calendar.py --file "$OPTIMIZED"; then
  log_success "Created Outlook-optimized calendar: $OPTIMIZED"
  
  # Generate a preview
  python scripts/refresh_calendar.py --preview --ics-file "$OPTIMIZED"
  
  # Final instructions
  echo -e "\n${BOLD}Instructions for Outlook:${RESET}"
  echo "1. Use the '$OPTIMIZED' file for importing into Outlook"
  echo "2. In Outlook desktop, go to File > Open & Export > Import/Export > Import from file"
  echo "3. Choose 'Import an iCalendar (.ics) file' and select $OPTIMIZED"
  echo "4. For Outlook web, go to Calendar > Import calendar > select $OPTIMIZED"
  echo
  echo -e "${YELLOW}Note: If you've previously imported this calendar, you may need to remove it first${RESET}"
  echo -e "${YELLOW}      before importing the updated version for images to refresh correctly.${RESET}"
else
  log_error "Outlook optimization failed. Please check the errors above."
fi

exit 0
