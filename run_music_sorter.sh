#!/bin/bash

# Apple Music Playlist Creator Runner Script
# This script sets up a Python virtual environment, installs dependencies,
# runs the music sorter, and manages the environment.
# Author: rekidderjr

# Exit immediately if a command exits with a non-zero status
set -e

# Define colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Define the virtual environment directory
VENV_DIR="venv"

# Print a formatted message
print_message() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

# Print a success message
print_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

# Print a warning message
print_warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

# Print an error message
print_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if Library.xml exists
if [ ! -f "data/Library.xml" ]; then
    print_error "Library.xml not found in data/ directory."
    print_message "Please export your iTunes/Apple Music library:"
    print_message "  macOS: Music app → File → Library → Export Library..."
    print_message "  Windows: iTunes → File → Library → Export Library..."
    print_message "Save as 'Library.xml' in the data/ directory."
    exit 1
fi

# Parse command line arguments
KEEP_VENV=true  # Default is to keep the venv
for arg in "$@"; do
    case $arg in
        --clean-venv)
            KEEP_VENV=false
            shift
            ;;
    esac
done

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    print_message "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    print_success "Virtual environment created."
else
    print_message "Using existing virtual environment."
fi

# Activate virtual environment
print_message "Activating virtual environment..."
source "$VENV_DIR/bin/activate"
print_success "Virtual environment activated."

# Install dependencies
print_message "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
print_success "Dependencies installed."

# Run the music sorter
print_message "Running Apple Music Playlist Creator..."
python3 music_sorter.py
print_success "Music sorter execution completed."

# Deactivate virtual environment
print_message "Deactivating virtual environment..."
deactivate
print_success "Virtual environment deactivated."

print_success "Script execution completed successfully."
print_message "Check the 'playlists/' directory for generated playlist files."
