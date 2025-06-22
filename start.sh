#!/bin/bash
# You must chmod +x start.sh if running locally
# Render will run this to launch your web app

gunicorn app:app --bind 0.0.0.0:$PORT
