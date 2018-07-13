#!/bin/bash
echo "changing environment"
export ENVIRONMENT="production"
echo "running migrations"
python manage.py db upgrade
echo "done running migrations"