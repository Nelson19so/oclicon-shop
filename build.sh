#!/usr/bin/env bash
set -o errexit
set -ex  # Print commands as they run and exit on failure

# Install dependencies using the required serverless bypass flag
python3 -m pip install -r requirements.txt --break-system-packages

# Create static directory explicitly
mkdir -p staticfiles

# Collect static files targeting your specific production configuration path
python3 manage.py collectstatic --no-input --settings=src.config.settings.prod
python manage.py migrate

echo "Build phase complete."
