#!/bin/sh

chmod +x /venv/bin/activate
./venv/bin/activate

daphne -b 0.0.0.0 -p 8000 django_project.asgi:application