#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Collect static files if needed (Flask doesn't have this by default, but if using Flask-Assets or similar)
# python manage.py collectstatic --no-input  # Uncomment if you add static file collection

# Apply any database migrations if using Flask-Migrate
# flask db upgrade  # Uncomment if using Flask-Migrate

echo "Build completed successfully"