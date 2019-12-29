#!/bin/sh

chmod +x /venv/bin/activate
./venv/bin/activate

python manage.py collectstatic --verbosity 0
daphne -b 0.0.0.0 -p 8000 django_project.asgi:application