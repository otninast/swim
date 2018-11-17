#!/usr/bin/bash

gunicorn -c gunicorn_conf.py swim.wsgi:application --log-file -
