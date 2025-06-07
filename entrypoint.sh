#!/bin/bash
set -e
flask db upgrade
exec gunicorn -w 4 -b 0.0.0.0:5000 run:app