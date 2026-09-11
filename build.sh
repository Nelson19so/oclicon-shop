#!/usr/bin/env bash
set -o errexit
set -ex

# Install project dependencies
python3 -m pip install -r requirements.txt

# Create the folder explicitly so Vercel doesn't think it's missing
mkdir -p staticfiles

# Collect files using your exact nested settings route
python3 manage.py collectstatic --no-input --settings=src.confi.settings.prod

echo "Build phase complete."
