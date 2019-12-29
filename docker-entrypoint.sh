#!/bin/sh

chmod +x /venv/bin/activate
./venv/bin/activate

python manage.py collectstatic --verbosity 0
uwsgi --ini uwsgi.ini