#!/bin/sh
sleep 10
python src/main.py create_db  # Initialize the database
python -m flask --app src.main run   