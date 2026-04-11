#!/usr/bin/env bash
# Exit on error
set -o errexit

cd verses1

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input
