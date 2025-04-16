#!/bin/bash
set -e
python3 -m pip install --upgrade pip
python3 -m pip install -e src
python3 -m alembic upgrade head
python3 -m gunicorn fastapi_app:app -c src/gunicorn.conf.py
