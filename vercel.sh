#!/bin/bash
echo -e "Installing dependencies"
python3.12 -m pip install -r requirements.txt


# Navigate to the project directory
cd django_practice


echo -e "Applying migrations..."
python3.12 ../manage.py migrate


# Initialize any custom commands if 'init' is defined
echo -e "Running custom initialization command..."
python3.12 ../manage.py init || echo "No custom initialization defined."

# Collect static files
echo -e "Collecting static files..."
python3.12 ../manage.py collectstatic --noinput

echo -e "Deployment script completed."