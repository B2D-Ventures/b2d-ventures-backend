#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Load initial data if needed
python manage.py loaddata db_dump.json

# Create mock data if needed (optional)
# python manage.py create_mock_deals