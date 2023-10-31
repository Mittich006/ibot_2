#!/bin/bash

# Add the project directory to the PYTHONPATH environment variable by appending it to the .bashrc file.
project_path=$(pwd)
if ! grep -q 'export PYTHONPATH="${PYTHONPATH}' ~/.bashrc; then
  echo 'export PYTHONPATH="${PYTHONPATH}:'"$project_path"'"' >> ~/.bashrc
fi

until pg_isready -h ${POSTGRES_HOST} &>/dev/null; do sleep 1; done

python3 init_db.py
uvicorn src.main:app --host 0.0.0.0 --proxy-headers --reload