#!/usr/bin/env bash

set -a
. env_localhost
set +a
python3 manage.py runserver