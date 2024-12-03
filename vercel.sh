#!/bin/bash
echo -e "Installing dependencies"
python3.12 -m pip install -r requirements.txt

echo -e "Applying migrations..."
python3.12 manage.py migrate


echo -e "Running custom initialization command..."
python3.12 manage.py init

echo -e "Collecting static files..."
python3.12 manage.py collectstatic --noinput

echo -e "Deployment script completed."