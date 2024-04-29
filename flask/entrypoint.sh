#!/bin/bash

export FLASK_APP=run.py
flask create_db
flask run --host=0.0.0.0 --port=3000