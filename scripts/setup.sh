#!/bin/bash

# Exit on error
set -e

# Check if python3 is installed
if ! command -v python3 &>/dev/null; then
    echo "Error: python3 is not installed."
    exit 1
fi

# Set the virtual environment directory (default: '.venv')
VENV_DIR=".venv"

# Create the virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    echo "Virtual environment created at '$VENV_DIR'"
fi

# Activate the virtual environment
if [ -d "$VENV_DIR/bin "]; then
  source "$VENV_DIR/bin/activate"
else if [ -d "$VENV_DIR/Scripts" ]; then
  source "$VENV_DIR/Scripts/activate"
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "Warning: requirements.txt not found. Skipping installation."
else
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "Dependencies installed from requirements.txt"
fi

echo "Virtual environment is ready!"

git config commit.template .gitmessage

echo "Set git commit template!"
