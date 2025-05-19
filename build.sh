#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files for production
python manage.py collectstatic --no-input --settings=settings.settings.prod

# Apply all migrations for production
python manage.py migrate accounts --no-input --settings=settings.settings.prod
python manage.py migrate --no-input --settings=settings.settings.prod
