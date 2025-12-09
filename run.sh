#!/bin/bash

# Quick start script for the Translation Service

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/.installed" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    touch venv/.installed
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Please create one from env.example"
    echo "Copying env.example to .env..."
    cp env.example .env
    echo "Please edit .env and add your OPENAI_API_KEY"
    exit 1
fi

# Run the service
echo "Starting Translation Service..."
python main.py

