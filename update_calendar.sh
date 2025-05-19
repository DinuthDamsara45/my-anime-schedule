#!/bin/bash
# Comprehensive update script for anime calendar
# Usage: ./update_calendar.sh [--no-preview]

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
echo -e "${BOLD}✨ Anime Calendar Update Tool ✨${RESET}"
echo "=================================================="

# Navigate to the project directory (adjust if needed)
cd "$(dirname "$0")"

# Check if .env file exists
if [ ! -f .env ]; then
  log_warning "No .env file found! Images won't be updated properly."
  log_info "Please create a .env file with your TMDB credentials."
  
  # If .env.example exists, show it as a guide
  if [ -f .env.example ]; then
    echo -e "\nExample .env file structure:"
    cat .env.example
  fi
  
  # Ask to continue
  read -p "Continue anyway? (y/n): " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    log_info "Update canceled."
    exit 0
  fi
fi

# Check python availability
if ! command -v python &> /dev/null; then
  log_error "Python not found! Please install Python to run this script."
  exit 1
fi

# Parse arguments
PREVIEW="--preview"
if [ "$1" == "--no-preview" ]; then
  PREVIEW=""
  log_info "HTML preview generation disabled"
fi

# Run the update with progress indicator
log_info "Updating anime calendar..."

# First run the cleanup script to fix any existing issues
log_info "Running cleanup to fix any existing issues..."
python scripts/final_cleanup.py

# Run the calendar refresh script
if python scripts/refresh_calendar.py $PREVIEW; then
  log_success "Calendar updated successfully!"
  
  # Show next steps
  echo -e "\n${BOLD}Next Steps:${RESET}"
  echo "1. If you've made changes to the calendar, commit them to Git"
  echo "2. If this calendar is shared, distribute the updated .ics file"
  
  # Show Outlook-specific tips
  echo -e "\n${BOLD}Outlook Tips:${RESET}"
  echo "• You may need to remove and re-add the calendar in Outlook for image changes to appear"
  echo "• In Outlook web, try clearing the browser cache if images don't update"
  echo "• Images may not appear in all calendar views (day/week/month)"
  
  exit 0
else
  log_error "Calendar update failed!"
  log_info "Check the error messages above for details."
  exit 1
fi

# Show success message if the script succeeded
if [ $? -eq 0 ]; then
  echo "✅ Calendar updated successfully!"
  echo "📅 Your calendar now has the latest images and timestamps."
  echo "📝 A preview.html file has been generated for you to view."
  echo ""
  echo "Your subscribed calendar clients (like Outlook) will refresh within their refresh interval."
else
  echo "❌ Calendar update failed. Please check the error messages above."
fi
