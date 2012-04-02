#!/bin/sh

python-coverage run test_all.py
python-coverage report --omit="/usr/share/*"  -m

