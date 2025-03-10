#!/bin/bash

echo "Updating Git Submodules..."
git submodule update --init --recursive  # Pull private documents

echo "Installing Dependencies..."
pip install -r requirements.txt

echo "Starting Application..."
gunicorn app:app
