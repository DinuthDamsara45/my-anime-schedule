#!/bin/bash
# GitHub upload script for My Anime Schedule
# This script helps initialize and push the project to GitHub

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
echo -e "${BOLD}🚀 GitHub Upload - Anime Schedule Calendar 🚀${RESET}"
echo "=================================================="

# Check for Git installation
if ! command -v git &> /dev/null; then
  log_error "Git is not installed. Please install Git first."
  exit 1
fi

# Check if we're in the project root directory
if [ ! -f "main.ics" ] || [ ! -d "scripts" ]; then
  log_error "Please run this script from the project root directory."
  exit 1
fi

# Check for existing .git directory
if [ -d ".git" ]; then
  log_info "Git repository already initialized."
else
  log_info "Initializing Git repository..."
  git init
  log_success "Git repository initialized."
fi

# Check for .env file and warn if it exists
if [ -f ".env" ]; then
  log_warning "⚠️ .env file detected with potential API credentials."
  echo
  echo "Your .env file contains sensitive information that should NOT be uploaded to GitHub."
  echo "The .gitignore file should prevent this, but please double-check."
  echo
  read -p "Continue? (y/n): " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    log_info "Upload canceled. Please secure your credentials before continuing."
    exit 0
  fi
fi

# Add all files
log_info "Adding files to Git..."
git add .

# Initial commit if no commits exist
if ! git rev-parse --verify HEAD &> /dev/null; then
  log_info "Creating initial commit..."
  git commit -m "Initial commit: Anime Schedule Calendar with RFC 7986 image support"
  log_success "Initial commit created."
else
  # Ask for commit message
  echo
  echo "Enter a commit message for your changes:"
  read -r commit_msg
  
  if [ -z "$commit_msg" ]; then
    commit_msg="Update anime schedule calendar"
  fi
  
  git commit -m "$commit_msg"
  log_success "Changes committed."
fi

# Ask for GitHub repository URL
echo
echo "Enter your GitHub repository URL (format: https://github.com/username/repository):"
read -r github_url

if [ -z "$github_url" ]; then
  log_error "No GitHub URL provided. Cannot continue."
  exit 1
fi

# Extract username and repo from URL
if [[ $github_url =~ github\.com/([^/]+)/([^/]+) ]]; then
  username="${BASH_REMATCH[1]}"
  repo="${BASH_REMATCH[2]}"
  
  # Remove .git extension if present
  repo="${repo%.git}"
  
  # Set the remote
  git remote remove origin 2>/dev/null
  git remote add origin "https://github.com/$username/$repo.git"
  
  log_info "Pushing to GitHub repository: $username/$repo"
  echo "This will require your GitHub credentials."
  echo
  
  # Push to GitHub
  if git push -u origin main 2>/dev/null || git push -u origin master; then
    log_success "Successfully pushed to GitHub! 🎉"
    echo
    echo -e "${BOLD}Your calendar is now available at:${RESET}"
    echo "https://github.com/$username/$repo"
    echo
    echo -e "${BOLD}Raw calendar URL for subscription:${RESET}"
    echo "https://raw.githubusercontent.com/$username/$repo/main/main.ics"
    echo
    echo "Share this URL with anyone who wants to subscribe to your calendar."
  else
    log_error "Failed to push to GitHub. Please check your credentials and try again."
  fi
else
  log_error "Invalid GitHub URL format. Please use https://github.com/username/repository"
  exit 1
fi

exit 0
