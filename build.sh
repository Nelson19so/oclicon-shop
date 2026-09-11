#!/usr/bin/env bash
set -o errexit
set -ex  # Print commands as they run and exit on failure

# Install dependencies
python3 -m pip install -r requirements.txt

# Create staticfiles directory explicitly to ensure it exists
mkdir -p staticfiles

# Collect static files using your specific configuration path
python3 manage.py collectstatic --no-input --settings=src.confi.settings.prod

echo "Build phase complete."
