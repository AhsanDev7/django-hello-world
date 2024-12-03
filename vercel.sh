#!/bin/bash
echo -e "Installing dependencies"
python3.12 -m pip install -r requirements.txt

# make migrations
echo -e "Making migrations"
python3.12 src/manage.py migrate
python3.12 src/manage.py init
python3.12 src/manage.py collectstatic --noinput