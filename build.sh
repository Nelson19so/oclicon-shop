#!/usr/bin/env bash
set -o errexit
set -ex  # Print commands as they run and exit on failure

# Install dependencies
pip install -r requirements.txt

# Apply DB migrations (apply)
python manage.py migrate --no-input --settings=src.config.settings.prod

# Collect static files
python manage.py collectstatic --no-input --settings=src.config.settings.prod
