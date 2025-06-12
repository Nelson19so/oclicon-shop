#!/usr/bin/env bash
set -o errexit

# exit on error & print commands
set -ex

# Install dependencies
pip install -r requirements.txt

# Collect static files for production
python manage.py collectstatic --no-input --settings=settings.settings.prod

# create new migration files
python manage.py makemigrations

# Apply all migrations for production
python manage.py migrate --no-input --settings=settings.settings.prod

